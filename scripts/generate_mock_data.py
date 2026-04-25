"""
Sinh dữ liệu giả (mock data) cho AI002 - Dự báo Giá Cà phê.
Mô phỏng thời tiết + giá lịch sử cho vùng Tây Nguyên, Việt Nam.

Các lựa chọn thiết kế:
- Mùa vụ: giá cao hơn vào mùa thu hoạch (tháng 11-3).
- NaN ~5% để test khả năng xử lý missing data (Robustness).
- Outliers ~2% để test độ chịu đựng của pipeline.
- Ghi chú Bias: data chỉ mô phỏng Đắk Lắk / Lâm Đồng.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Để tái lập kết quả (cố định seed)
RNG = np.random.default_rng(seed=42)

# Cấu hình
N_ROWS = 1200
START_DATE = "2022-01-01"
REGION_BIAS_NOTE = (
    "Dữ liệu huấn luyện từ vùng Tây Nguyên (Đắk Lắk, Lâm Đồng). "
    "Dự đoán có thể sai lệch khi áp dụng cho vùng khác."
)


def generate_weather_features(dates: pd.DatetimeIndex) -> pd.DataFrame:
    """Sinh đặc trưng thời tiết theo quy luật mùa vụ."""
    month = dates.month.astype(float)
    day_of_year = dates.dayofyear.astype(float)

    # Nhiệt độ: cao hơn vào hè (tháng 4-9), thấp hơn vào đông
    temp_base = 24.0 + 3.0 * np.sin((day_of_year - 100) * 2 * np.pi / 365)
    avg_temp_c = temp_base + RNG.normal(0, 1.5, size=len(dates))
    avg_temp_c = np.clip(avg_temp_c, 18.0, 32.0)

    # Lượng mưa: mùa mưa tháng 5-10
    rain_base = 150.0 + 120.0 * np.sin((day_of_year - 150) * 2 * np.pi / 365)
    rainfall_mm = rain_base + RNG.exponential(40, size=len(dates))
    rainfall_mm = np.clip(rainfall_mm, 0.0, 450.0)

    # Độ ẩm: cao hơn vào mùa mưa
    humidity_base = 75.0 + 10.0 * np.sin((day_of_year - 150) * 2 * np.pi / 365)
    humidity_pct = humidity_base + RNG.normal(0, 5, size=len(dates))
    humidity_pct = np.clip(humidity_pct, 55.0, 98.0)

    # Giờ nắng: xấp xỉ nghịch với lượng mưa
    sun_base = 7.0 - 2.5 * np.sin((day_of_year - 150) * 2 * np.pi / 365)
    sunshine_hours = sun_base + RNG.normal(0, 1.2, size=len(dates))
    sunshine_hours = np.clip(sunshine_hours, 2.0, 11.0)

    return pd.DataFrame({
        "date": dates,
        "avg_temp_c": np.round(avg_temp_c, 2),
        "rainfall_mm": np.round(rainfall_mm, 2),
        "humidity_pct": np.round(humidity_pct, 2),
        "sunshine_hours": np.round(sunshine_hours, 2),
        "month": month.astype(int),
    })


def generate_historical_price(dates: pd.DatetimeIndex, weather_df: pd.DataFrame) -> pd.Series:
    """Sinh giá cà phê với hiệu ứng mùa vụ thu hoạch và ảnh hưởng thời tiết."""
    month = dates.month
    day_of_year = dates.dayofyear.astype(float)

    # Xu hướng cơ bản: tăng nhẹ qua 3 năm (lạm phát / cầu toàn cầu)
    days_since_start = (dates - dates[0]).days.astype(float)
    base_price = 52000.0 + 8.0 * days_since_start

    # Thưởng mùa vụ: tháng 11-3 (các tháng 11,12,1,2,3)
    is_harvest = np.isin(month, [11, 12, 1, 2, 3]).astype(float)
    harvest_premium = is_harvest * 8000.0

    # Ảnh hưởng thời tiết: hạn hán (mưa ít) làm giá tăng; mưa quá nhiều làm giảm nhẹ
    rainfall = weather_df["rainfall_mm"].values
    rain_effect = -15.0 * (rainfall - 150.0)  # độ lệch so với trung bình
    rain_effect = np.clip(rain_effect, -8000.0, 8000.0)

    # Stress nhiệt độ: nhiệt độ rất cao làm giảm chất lượng năng suất
    temp = weather_df["avg_temp_c"].values
    temp_stress = np.where(temp > 29.0, -2000.0, 0.0)

    noise = RNG.normal(0, 2500, size=len(dates))

    price = base_price + harvest_premium + rain_effect + temp_stress + noise
    price = np.clip(price, 38000.0, 92000.0)

    return pd.Series(np.round(price, 2), index=dates, name="historical_price_vnd")


def inject_missing_values(df: pd.DataFrame, missing_rate: float = 0.05) -> pd.DataFrame:
    """Chèn ngẫu nhiên NaN vào cột đặc trưng để test độ bền (Robustness)."""
    df_out = df.copy()
    feature_cols = ["avg_temp_c", "rainfall_mm", "humidity_pct", "sunshine_hours"]

    for col in feature_cols:
        n_missing = int(missing_rate * len(df_out))
        missing_idx = RNG.choice(df_out.index, size=n_missing, replace=False)
        df_out.loc[missing_idx, col] = np.nan

    return df_out


def inject_outliers(df: pd.DataFrame, outlier_rate: float = 0.02) -> pd.DataFrame:
    """Chèn outliers cực đoan để test độ chịu đựng của pipeline."""
    df_out = df.copy()
    feature_cols = ["avg_temp_c", "rainfall_mm", "humidity_pct", "sunshine_hours"]

    for col in feature_cols:
        n_outliers = int(outlier_rate * len(df_out))
        outlier_idx = RNG.choice(df_out.index, size=n_outliers, replace=False)
        # Chèn giá trị vô lý / cực đoan để test độ chịu đựng của pipeline
        extreme_values = {
            "avg_temp_c": [-20.0, 65.0],
            "rainfall_mm": [-10.0, 600.0],
            "humidity_pct": [-5.0, 120.0],
            "sunshine_hours": [-5.0, 18.0],
        }
        df_out.loc[outlier_idx, col] = RNG.choice(
            extreme_values[col], size=n_outliers
        )

    return df_out


def main() -> None:
    dates = pd.date_range(start=START_DATE, periods=N_ROWS, freq="D")

    weather_df = generate_weather_features(dates)
    price_series = generate_historical_price(dates, weather_df)

    df = weather_df.copy()
    df["historical_price_vnd"] = price_series.values

    # Chèn dữ liệu test độ bền (NaN + outliers)
    df = inject_missing_values(df, missing_rate=0.05)
    df = inject_outliers(df, outlier_rate=0.02)

    # Đảm bảo thư mục đầu ra tồn tại
    output_path = Path(__file__).resolve().parents[1] / "data" / "raw" / "mock_coffee_data.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"Đã ghi mock dataset vào: {output_path}")
    print(f"Kích thước: {df.shape}")
    print(f"Số NaN mỗi cột:\n{df.isna().sum()}")
    print(f"\nGhi chú Bias / Hạn chế:\n{REGION_BIAS_NOTE}")

    # Kiểm tra nhanh (sanity check)
    assert len(df) >= 1000, "Dataset phải có ít nhất 1000 dòng"
    assert df.isna().sum().sum() > 0, "Dataset phải chứa NaN để test độ bền"
    print("\nKiểm tra nhanh thành công.")


if __name__ == "__main__":
    main()
