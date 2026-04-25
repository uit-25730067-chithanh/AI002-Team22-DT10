"""
Module tiền xử lý dữ liệu cho pipeline dự báo giá cà phê.
Các hàm xử lý missing data, outliers, và engineer features.
"""

import numpy as np
import pandas as pd
from typing import Tuple


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Điền giá trị NaN bằng median cho cột số liệu.
    Trụ cột Robustness: xử lý missing data mà không làm biến dạng phân bố.
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isna().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
    return df


def remove_outliers(df: pd.DataFrame, method: str = "iqr") -> pd.DataFrame:
    """
    Loại bỏ outliers bằng IQR hoặc Z-score.
    Mặc định: IQR (ít nhạy cảm với extreme values hơn Z-score).
    """
    df = df.copy()
    numeric_cols = ["avg_temp_c", "rainfall_mm", "humidity_pct", "sunshine_hours", "historical_price_vnd"]

    for col in numeric_cols:
        if col not in df.columns:
            continue

        if method == "iqr":
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
        elif method == "zscore":
            mean = df[col].mean()
            std = df[col].std()
            lower = mean - 3 * std
            upper = mean + 3 * std
        else:
            raise ValueError(f"method phải là 'iqr' hoặc 'zscore', nhận: {method}")

        mask = (df[col] >= lower) & (df[col] <= upper)
        df = df[mask]

    return df.reset_index(drop=True)


def feature_engineer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo thêm đặc trưng (feature engineering) cho time-series dự báo.

    Các features mới:
    - month_sin, month_cos: mã hóa chu kỳ tháng (cyclic encoding).
    - rolling_avg_7d: trung bình trượt 7 ngày giá cà phê.
    - lag_1d, lag_7d: giá trị trễ (lag) 1 và 7 ngày.
    """
    df = df.copy()
    df = df.sort_values("date").reset_index(drop=True)

    # Mã hóa chu kỳ tháng (cyclic encoding) — giữ quan hệ mùa vụ liên tục
    month = df["month"]
    df["month_sin"] = np.sin(2 * np.pi * month / 12)
    df["month_cos"] = np.cos(2 * np.pi * month / 12)

    # Trung bình trượt 7 ngày giá cà phê — nắm bắt xu hướng ngắn hạn
    df["rolling_avg_7d"] = df["historical_price_vnd"].rolling(window=7, min_periods=1).mean()

    # Giá trị trễ (lag): giá ngày hôm trước và 7 ngày trước
    df["lag_1d"] = df["historical_price_vnd"].shift(1)
    df["lag_7d"] = df["historical_price_vnd"].shift(7)

    # Điền NaN từ lag bằng forward-fill rồi backfill để không mất dòng đầu
    df["lag_1d"] = df["lag_1d"].ffill().bfill()
    df["lag_7d"] = df["lag_7d"].ffill().bfill()

    return df


def split_temporal(df: pd.DataFrame, train_end: str = "2024-12-31", test_start: str = "2025-01-01") -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Chia train/test theo thời gian (không random shuffle — tránh data leakage trong time-series).

    Args:
        df: DataFrame đã qua feature engineering, có cột 'date'.
        train_end: Ngày kết thúc tập train (mặc định 2024-12-31).
        test_start: Ngày bắt đầu tập test (mặc định 2025-01-01).

    Returns:
        X_train, X_test, y_train, y_test
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Các cột đặc trưng (loại bỏ date và target)
    feature_cols = [c for c in df.columns if c not in ["date", "historical_price_vnd"]]
    target_col = "historical_price_vnd"  # cột mục tiêu: giá cà phê

    # Chia theo thời gian — KHÔNG dùng random shuffle để tránh data leakage trong time-series
    train_mask = df["date"] <= train_end
    test_mask = df["date"] >= test_start

    train_df = df[train_mask]
    test_df = df[test_mask]

    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]

    return X_train, X_test, y_train, y_test


def preprocess_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline đầy đủ: fill missing -> remove outliers -> engineer features.
    """
    df = fill_missing(df)
    df = remove_outliers(df)
    df = feature_engineer(df)
    return df
