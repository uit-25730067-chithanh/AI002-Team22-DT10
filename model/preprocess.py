from typing import Tuple
import numpy as np
import pandas as pd
import warnings
"""
Module tiền xử lý dữ liệu cho pipeline dự báo giá cà phê.
Các hàm xử lý missing data, outliers, và engineer features.
"""


def preprocess_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline đầy đủ: fill missing -> remove outliers -> engineer features.
    """
    df = normalize_real_schema(df)
    df = fill_missing(df)
    df = cap_outliers(df)
    df = feature_engineer(df)
    df = fill_missing(df)
    df = encode_features(df)
    return df


"""
Module chuẩn hóa schema cho pipeline dự báo giá cà phê.
"""

REAL_SCHEMA_RENAME_MAP = {
    "period_start": "date",
    "avg_price_vnd_per_kg": "historical_price_vnd",
    "avg_temperature_c": "avg_temp_c",
    "total_rainfall_mm": "rainfall_mm",
    "avg_humidity_percent": "humidity_pct",
}

CATEGORICAL_FEATURES = [
    "province",
    "area",
    "coffee_type",
    "price_fill_method",
    "dominant_soil_type",
    "soil_data_confidence",
]


def normalize_real_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa schema real processed data về schema nội bộ để tái dùng pipeline Team 2.
    """
    df = df.copy()
    df = df.rename(
        columns={
            k: v for k,
            v in REAL_SCHEMA_RENAME_MAP.items() if k in df.columns})

    required_cols = [
        "date",
        "historical_price_vnd",
        "avg_temp_c",
        "rainfall_mm",
        "humidity_pct"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Thiếu cột bắt buộc sau normalize schema: {missing_cols}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["historical_price_vnd"] = pd.to_numeric(
        df["historical_price_vnd"], errors="coerce")
    row_count_before_drop = len(df)
    df = df.dropna(subset=["date", "historical_price_vnd"])
    dropped_count = row_count_before_drop - len(df)
    if dropped_count > 0:
        warnings.warn(
            f"Đã drop {dropped_count} dòng vì date hoặc historical_price_vnd không parse được",
            stacklevel=2,
        )
    if df.empty:
        raise ValueError(
            "Không còn dòng hợp lệ sau khi chuẩn hóa date và historical_price_vnd")

    numeric_cols = [
        "avg_temp_c",
        "rainfall_mm",
        "humidity_pct",
        "avg_soil_moisture_0_7cm",
        "soil_score",
        "price_observations",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "month" not in df.columns:
        df["month"] = df["date"].dt.month
    if "year" not in df.columns:
        df["year"] = df["date"].dt.year
    if "quarter" not in df.columns:
        df["quarter"] = df["date"].dt.quarter

    return df


"""
Module feature engineering, xử lý missing data và outliers.
"""


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Điền giá trị NaN bằng median cho cột số liệu.
    Trụ cột Robustness: xử lý missing data mà không làm biến dạng phân bố.
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col == "historical_price_vnd":
            continue
        if df[col].isna().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in categorical_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna("unknown")
    return df


def cap_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Winsorize/cap outliers thay vì drop mạnh, phù hợp giá cà phê 2024-2025 tăng thật.
    """
    df = df.copy()
    numeric_cols = [
        "avg_temp_c",
        "rainfall_mm",
        "humidity_pct",
        "avg_soil_moisture_0_7cm",
        "soil_score"]

    for col in numeric_cols:
        if col not in df.columns:
            continue

        lower = df[col].quantile(0.01)
        upper = df[col].quantile(0.99)
        df[col] = df[col].clip(lower=lower, upper=upper)

    return df.reset_index(drop=True)


def remove_outliers(df: pd.DataFrame, method: str = "iqr") -> pd.DataFrame:
    """
    Backward-compatible wrapper: real-data pipeline dùng cap_outliers thay vì drop rows.
    """
    return cap_outliers(df)


def feature_engineer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo thêm đặc trưng (feature engineering) cho time-series dự báo.

    Các features mới:
    - month_sin, month_cos: mã hóa chu kỳ tháng (cyclic encoding).
    - rolling_avg_7d: trung bình trượt 7 kỳ dữ liệu giá cà phê.
    - lag_1d, lag_7d: giá trị trễ (lag) 1 và 7 kỳ dữ liệu.
    """
    df = df.copy()
    sort_cols = ["area", "date"] if "area" in df.columns else ["date"]
    df = df.sort_values(sort_cols).reset_index(drop=True)

    # Mã hóa chu kỳ tháng (cyclic encoding) — giữ quan hệ mùa vụ liên tục
    month = df["month"]
    df["month_sin"] = np.sin(2 * np.pi * month / 12)
    df["month_cos"] = np.cos(2 * np.pi * month / 12)

    if "area" in df.columns:
        grouped_price = df.groupby("area", sort=False)["historical_price_vnd"]
        df["lag_1d"] = grouped_price.shift(1)
        df["lag_7d"] = grouped_price.shift(7)
        df["rolling_avg_7d"] = df.groupby(
            "area", sort=False)["lag_1d"].transform(
            lambda s: s.rolling(
                window=7, min_periods=1).mean())
    else:
        df["lag_1d"] = df["historical_price_vnd"].shift(1)
        df["lag_7d"] = df["historical_price_vnd"].shift(7)
        df["rolling_avg_7d"] = df["lag_1d"].rolling(
            window=7, min_periods=1).mean()

    if "area" in df.columns:
        df["lag_1d"] = df.groupby(
            "area", sort=False)["lag_1d"].transform(
            lambda s: s.ffill())
        df["lag_7d"] = df.groupby(
            "area", sort=False)["lag_7d"].transform(
            lambda s: s.ffill())
        df["rolling_avg_7d"] = df.groupby(
            "area", sort=False)["rolling_avg_7d"].transform(
            lambda s: s.ffill())
    else:
        df["lag_1d"] = df["lag_1d"].ffill()
        df["lag_7d"] = df["lag_7d"].ffill()
        df["rolling_avg_7d"] = df["rolling_avg_7d"].ffill()

    df["lag_7d"] = df["lag_7d"].fillna(df["lag_1d"])
    df = df.dropna(subset=["lag_1d", "rolling_avg_7d"])

    return df


"""
Module encoding và split dữ liệu.
"""


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    existing_cats = [col for col in CATEGORICAL_FEATURES if col in df.columns]
    df = pd.get_dummies(df, columns=existing_cats, dummy_na=False)

    drop_cols = [
        col for col in [
            "period_end",
            "observed_price_vnd_per_kg"] if col in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    bool_cols = df.select_dtypes(include=["bool"]).columns
    if len(bool_cols) > 0:
        df[bool_cols] = df[bool_cols].astype(int)

    return df


def split_temporal(
    df: pd.DataFrame,
    train_end: str = "2024-12-31",
    test_start: str = "2025-01-01",
    train_ratio: float = 0.8,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Chia train/test theo thời gian (không random shuffle — tránh data leakage trong time-series).

    Args:
        df: DataFrame đã qua feature engineering, có cột 'date'.
        train_end: Ngày kết thúc tập train (mặc định 2024-12-31).
        test_start: Ngày bắt đầu tập test (mặc định 2025-01-01).
        train_ratio: Tỷ lệ train nếu split theo ratio (mặc định 0.8). Chỉ dùng khi test set rỗng theo ngày.

    Returns:
        X_train, X_test, y_train, y_test
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Các cột đặc trưng (loại bỏ date và target)
    feature_cols = [
        c for c in df.columns if c not in [
            "date", "historical_price_vnd"]]
    feature_cols = [
        c for c in feature_cols if pd.api.types.is_numeric_dtype(
            df[c])]
    target_col = "historical_price_vnd"  # cột mục tiêu: giá cà phê

    # Chia theo thời gian — KHÔNG dùng random shuffle để tránh data leakage
    # trong time-series
    train_mask = df["date"] <= train_end
    test_mask = df["date"] >= test_start

    train_df = df[train_mask]
    test_df = df[test_mask]

    # Fallback: nếu test rỗng, split theo ratio (giữ thứ tự thời gian)
    if len(test_df) == 0:
        split_idx = int(len(df) * train_ratio)
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]

    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]

    return X_train, X_test, y_train, y_test
