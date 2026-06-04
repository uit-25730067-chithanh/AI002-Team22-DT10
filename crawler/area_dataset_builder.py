from __future__ import annotations

from pathlib import Path
import pandas as pd

from .coffee_areas import slugify



from .build_soil_profile import build_soil_profile

PRICE_FILE = "coffee_price_all_areas_daily_2022_2025.csv"
WEATHER_FILE = "weather_all_areas_daily_2022_2025.csv"
SOIL_FILE = "soil_profile_by_area.csv"


def load_inputs(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    price_path = raw_dir / PRICE_FILE
    weather_path = raw_dir / WEATHER_FILE
    soil_path = raw_dir / SOIL_FILE

    if not price_path.exists():
        raise FileNotFoundError(f"Missing {price_path}. Run crawl_coffee_prices.py first.")
    if not weather_path.exists():
        raise FileNotFoundError(f"Missing {weather_path}. Run crawl_weather_by_area.py first.")
    if not soil_path.exists():
        build_soil_profile(soil_path)

    prices = pd.read_csv(price_path)
    weather = pd.read_csv(weather_path)
    soil = pd.read_csv(soil_path)
    prices["date"] = pd.to_datetime(prices["date"])
    weather["date"] = pd.to_datetime(weather["date"])
    return prices, weather, soil


def add_period_columns(
    frame: pd.DataFrame,
    freq: str,
    start_date: pd.Timestamp | None = None,
    end_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    frame = frame.copy()
    if freq == "weekly":
        period_start = frame["date"] - pd.to_timedelta(frame["date"].dt.weekday, unit="D")
        period_end = period_start + pd.Timedelta(days=6)
        if start_date is not None:
            period_start = period_start.mask(period_start < start_date, start_date)
        if end_date is not None:
            period_end = period_end.mask(period_end > end_date, end_date)
        frame["period_start"] = period_start.dt.date
        frame["period_end"] = period_end.dt.date
    elif freq == "monthly":
        frame["period_start"] = frame["date"].dt.to_period("M").dt.start_time.dt.date
        frame["period_end"] = frame["date"].dt.to_period("M").dt.end_time.dt.date
    else:
        raise ValueError("freq must be weekly or monthly")
    return frame


def aggregate_prices(
    prices: pd.DataFrame,
    freq: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> pd.DataFrame:
    prices = add_period_columns(prices, freq, start_date, end_date)
    return (
        prices.groupby(
            ["period_start", "period_end", "province", "area", "coffee_type"],
            dropna=False,
            as_index=False,
        )
        .agg(
            avg_price_vnd_per_kg=("price_vnd_per_kg", "mean"),
            price_observations=("price_vnd_per_kg", "count"),
        )
    )


def aggregate_weather(
    weather: pd.DataFrame,
    freq: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> pd.DataFrame:
    weather = add_period_columns(weather, freq, start_date, end_date)
    return (
        weather.groupby(
            ["period_start", "period_end", "province", "area"],
            dropna=False,
            as_index=False,
        )
        .agg(
            avg_temperature_c=("temperature_c", "mean"),
            avg_humidity_percent=("humidity_percent", "mean"),
            total_rainfall_mm=("rainfall_mm", "sum"),
            avg_soil_moisture_0_7cm=("soil_moisture_0_7cm", "mean"),
        )
    )


def fill_missing_prices(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame["observed_price_vnd_per_kg"] = frame["avg_price_vnd_per_kg"]
    frame["price_fill_method"] = "observed"
    frame.loc[frame["avg_price_vnd_per_kg"].isna(), "price_fill_method"] = "missing"

    observed_period_province = (
        frame[frame["avg_price_vnd_per_kg"].notna()]
        .groupby(["period_start", "province"], as_index=False)["avg_price_vnd_per_kg"]
        .mean()
        .rename(columns={"avg_price_vnd_per_kg": "province_period_price"})
    )
    frame = frame.merge(observed_period_province, on=["period_start", "province"], how="left")
    mask = frame["avg_price_vnd_per_kg"].isna() & frame["province_period_price"].notna()
    frame.loc[mask, "avg_price_vnd_per_kg"] = frame.loc[mask, "province_period_price"]
    frame.loc[mask, "price_fill_method"] = "province_proxy"

    frame = frame.sort_values(["area", "period_start"])
    for area, area_index in frame.groupby("area").groups.items():
        series = frame.loc[area_index, "avg_price_vnd_per_kg"].astype(float)
        interpolated = series.interpolate(method="linear", limit_direction="both")
        mask = frame.loc[area_index, "avg_price_vnd_per_kg"].isna() & interpolated.notna()
        frame.loc[area_index[mask.to_numpy()], "avg_price_vnd_per_kg"] = interpolated[mask].to_numpy()
        frame.loc[area_index[mask.to_numpy()], "price_fill_method"] = "interpolated_area"

    observed_period_global = (
        frame[frame["observed_price_vnd_per_kg"].notna()]
        .groupby("period_start")["observed_price_vnd_per_kg"]
        .mean()
    )
    mask = frame["avg_price_vnd_per_kg"].isna()
    frame.loc[mask, "avg_price_vnd_per_kg"] = frame.loc[mask, "period_start"].map(observed_period_global)
    frame.loc[mask & frame["avg_price_vnd_per_kg"].notna(), "price_fill_method"] = "global_period_proxy"

    area_medians = frame.groupby("area")["avg_price_vnd_per_kg"].transform("median")
    mask = frame["avg_price_vnd_per_kg"].isna()
    frame.loc[mask, "avg_price_vnd_per_kg"] = area_medians[mask]
    frame.loc[mask & frame["avg_price_vnd_per_kg"].notna(), "price_fill_method"] = "area_median"

    global_median = frame["avg_price_vnd_per_kg"].median()
    mask = frame["avg_price_vnd_per_kg"].isna()
    frame.loc[mask, "avg_price_vnd_per_kg"] = global_median
    frame.loc[mask, "price_fill_method"] = "global_median"

    frame = frame.drop(columns=["province_period_price"])
    output_columns = [
        "period_start",
        "period_end",
        "province",
        "area",
        "coffee_type",
        "avg_price_vnd_per_kg",
        "observed_price_vnd_per_kg",
        "price_observations",
        "price_fill_method",
        "avg_temperature_c",
        "avg_humidity_percent",
        "total_rainfall_mm",
        "avg_soil_moisture_0_7cm",
        "dominant_soil_type",
        "soil_score",
        "soil_data_confidence",
    ]
    return frame[output_columns].sort_values(["period_start", "province", "area"])

def build_dataset(raw_dir: Path, output_root: Path, freq: str) -> pd.DataFrame:
    prices, weather, soil = load_inputs(raw_dir)
    start_date = weather["date"].min()
    end_date = weather["date"].max()
    price_periods = aggregate_prices(prices, freq, start_date, end_date)
    weather_periods = aggregate_weather(weather, freq, start_date, end_date)
    merged = weather_periods.merge(
        price_periods,
        on=["period_start", "period_end", "province", "area"],
        how="left",
        validate="one_to_one",
    )
    merged["coffee_type"] = merged["coffee_type"].fillna("Robusta / ca phe nhan xo noi dia")
    grouped = merged.merge(
        soil[
            [
                "area",
                "province",
                "dominant_soil_type",
                "soil_score",
                "soil_data_confidence",
            ]
        ],
        on=["area", "province"],
        how="left",
        validate="many_to_one",
    )
    grouped = grouped[
        [
            "period_start",
            "period_end",
            "province",
            "area",
            "coffee_type",
            "avg_price_vnd_per_kg",
            "price_observations",
            "avg_temperature_c",
            "avg_humidity_percent",
            "total_rainfall_mm",
            "avg_soil_moisture_0_7cm",
            "dominant_soil_type",
            "soil_score",
            "soil_data_confidence",
        ]
    ].sort_values(["period_start", "province", "area"])
    grouped["price_observations"] = grouped["price_observations"].fillna(0).astype("Int64")
    grouped = fill_missing_prices(grouped)
    grouped["avg_price_vnd_per_kg"] = grouped["avg_price_vnd_per_kg"].round(0).astype("Int64")
    for column in [
        "avg_temperature_c",
        "avg_humidity_percent",
        "total_rainfall_mm",
        "avg_soil_moisture_0_7cm",
    ]:
        grouped[column] = grouped[column].round(3)

    output_dir = output_root / freq
    output_dir.mkdir(parents=True, exist_ok=True)
    combined_output = output_dir / f"coffee_environment_all_areas_{freq}_2022_2025.csv"
    grouped.to_csv(combined_output, index=False, encoding="utf-8-sig")
    print(f"Wrote {combined_output} ({len(grouped)} rows)")

    for area, area_frame in grouped.groupby("area"):
        output = output_dir / f"coffee_environment_{slugify(area)}_{freq}_2022_2025.csv"
        area_frame.to_csv(output, index=False, encoding="utf-8-sig")
        print(f"Wrote {output} ({len(area_frame)} rows)")
    return grouped


__all__ = [
    "add_period_columns",
    "aggregate_prices",
    "aggregate_weather",
    "build_dataset",
    "fill_missing_prices",
    "load_inputs",
]