"""Download daily weather data from Open-Meteo for each coffee price area."""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

try:
    from .coffee_areas import AREAS, slugify
    from . import independent_data_contract as independent_contract
except ImportError:
    from coffee_areas import AREAS, slugify
    import independent_data_contract as independent_contract


OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_weather(
    area: dict[str, Any],
    start: str,
    end: str,
    retries: int = 3,
    retry_sleep_seconds: float = 8.0,
) -> pd.DataFrame:
    params = {
        "latitude": area["latitude"],
        "longitude": area["longitude"],
        "start_date": start,
        "end_date": end,
        "daily": ",".join(
            [
                "temperature_2m_mean",
                "relative_humidity_2m_mean",
                "precipitation_sum",
                "soil_moisture_0_to_7cm_mean",
            ]
        ),
        "timezone": "Asia/Bangkok",
    }
    response = None
    for attempt in range(retries + 1):
        response = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=30)
        if response.status_code != 429:
            break
        if attempt < retries:
            time.sleep(retry_sleep_seconds * (attempt + 1))
    assert response is not None
    response.raise_for_status()
    payload = response.json()
    daily = payload.get("daily", {})
    frame = pd.DataFrame(
        {
            "date": daily.get("time", []),
            "province": area["province"],
            "area": area["area"],
            "latitude": area["latitude"],
            "longitude": area["longitude"],
            "temperature_c": daily.get("temperature_2m_mean", []),
            "humidity_percent": daily.get("relative_humidity_2m_mean", []),
            "rainfall_mm": daily.get("precipitation_sum", []),
            "soil_moisture_0_7cm": daily.get("soil_moisture_0_to_7cm_mean", []),
        }
    )
    frame["date"] = pd.to_datetime(frame["date"]).dt.date
    return frame


def write_area_weather(
    frame: pd.DataFrame,
    output_dir: Path,
    area_name: str,
    year_range_label: str = "2022_2025",
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"weather_{slugify(area_name)}_daily_{year_range_label}.csv"
    frame.to_csv(output, index=False, encoding="utf-8-sig")
    return output


def combined_weather_output_path(
    output_dir: Path,
    year_range_label: str = "2022_2025",
) -> Path:
    return output_dir / f"weather_all_areas_daily_{year_range_label}.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2022-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--output-dir", default="data/raw")
    parser.add_argument("--year-range-label", default="2022_2025")
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-sleep", type=float, default=8.0)
    parser.add_argument(
        "--reuse-existing",
        action="store_true",
        help="Reuse existing per-area weather files in output dir instead of refetching.",
    )
    parser.add_argument(
        "--independent",
        action="store_true",
        help="Use the Team 2 independent data contract paths and date range.",
    )
    args = parser.parse_args()

    if args.independent:
        args.start = independent_contract.START_DATE
        args.end = independent_contract.END_DATE
        args.output_dir = str(independent_contract.RAW_DIR)
        args.year_range_label = independent_contract.YEAR_RANGE_LABEL

    output_dir = Path(args.output_dir)
    all_frames: list[pd.DataFrame] = []
    for area in AREAS:
        output = output_dir / f"weather_{slugify(area['area'])}_daily_{args.year_range_label}.csv"
        if args.reuse_existing and output.exists():
            frame = pd.read_csv(output)
            print(f"Reused {output} ({len(frame)} rows)")
        else:
            frame = fetch_weather(
                area,
                args.start,
                args.end,
                retries=args.retries,
                retry_sleep_seconds=args.retry_sleep,
            )
            output = write_area_weather(
                frame,
                output_dir,
                area["area"],
                args.year_range_label,
            )
            time.sleep(args.sleep)
        all_frames.append(frame)
        print(f"Wrote {output} ({len(frame)} rows)")

    combined = pd.concat(all_frames, ignore_index=True)
    combined_output = combined_weather_output_path(output_dir, args.year_range_label)
    combined.to_csv(combined_output, index=False, encoding="utf-8-sig")
    print(f"Wrote {combined_output} ({len(combined)} rows)")


if __name__ == "__main__":
    main()
