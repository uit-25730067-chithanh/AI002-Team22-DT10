"""Validation helpers for the independent coffee dataset pipeline."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


DEFAULT_OBSERVATION_KEYS = [
    "date",
    "province",
    "area",
    "source_name",
    "source_url",
]


def validate_required_columns(
    frame: pd.DataFrame,
    required_columns: Sequence[str],
) -> None:
    missing = [column for column in required_columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def find_duplicate_observations(
    frame: pd.DataFrame,
    keys: Sequence[str] = DEFAULT_OBSERVATION_KEYS,
) -> pd.DataFrame:
    validate_required_columns(frame, keys)
    mask = frame.duplicated(list(keys), keep=False)
    return frame.loc[mask].copy()


def validate_date_range(
    frame: pd.DataFrame,
    start: str,
    end: str,
    date_column: str = "date",
) -> None:
    validate_required_columns(frame, [date_column])
    dates = pd.to_datetime(frame[date_column], errors="coerce")
    invalid_mask = dates.isna() | (dates < pd.Timestamp(start)) | (dates > pd.Timestamp(end))
    if invalid_mask.any():
        count = int(invalid_mask.sum())
        raise ValueError(f"{count} rows outside allowed date range {start} -> {end}")


def validate_observed_source_urls(
    frame: pd.DataFrame,
    price_column: str = "price_vnd_per_kg",
    source_column: str = "source_url",
) -> None:
    validate_required_columns(frame, [price_column, source_column])
    observed_mask = pd.to_numeric(frame[price_column], errors="coerce").notna()
    source_values = frame[source_column].fillna("").astype(str).str.strip()
    invalid_mask = observed_mask & source_values.eq("")
    if invalid_mask.any():
        count = int(invalid_mask.sum())
        raise ValueError(f"{count} observed rows missing source_url")


def validate_price_range(
    frame: pd.DataFrame,
    price_column: str = "price_vnd_per_kg",
    minimum: int = 10_000,
    maximum: int = 200_000,
) -> None:
    validate_required_columns(frame, [price_column])
    prices = pd.to_numeric(frame[price_column], errors="coerce")
    invalid_mask = prices.isna() | (prices < minimum) | (prices > maximum)
    if invalid_mask.any():
        count = int(invalid_mask.sum())
        raise ValueError(f"{count} prices outside expected range {minimum} -> {maximum}")


def summarize_observed_data_completeness(
    frame: pd.DataFrame,
    group_cols: Sequence[str],
    fill_method_column: str = "price_fill_method",
) -> pd.DataFrame:
    validate_required_columns(frame, [*group_cols, fill_method_column])
    work = frame.copy()
    work["_is_observed"] = work[fill_method_column].eq("observed")
    summary = (
        work.groupby(list(group_cols), dropna=False)
        .agg(
            total_rows=("_is_observed", "size"),
            observed_rows=("_is_observed", "sum"),
        )
        .reset_index()
    )
    summary["observed_rate"] = (
        summary["observed_rows"] / summary["total_rows"]
    ).round(4)
    return summary
