from __future__ import annotations

import pandas as pd
import pytest

from crawler import data_quality as quality


def test_validate_required_columns_reports_missing_columns() -> None:
    frame = pd.DataFrame({"date": ["2025-01-01"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        quality.validate_required_columns(frame, ["date", "source_url"])


def test_find_duplicate_observations_detects_same_source_row() -> None:
    frame = pd.DataFrame(
        [
            {
                "date": "2025-01-01",
                "province": "Lam Dong",
                "area": "Di Linh",
                "source_name": "Fixture",
                "source_url": "https://example.test/a",
            },
            {
                "date": "2025-01-01",
                "province": "Lam Dong",
                "area": "Di Linh",
                "source_name": "Fixture",
                "source_url": "https://example.test/a",
            },
        ]
    )

    duplicates = quality.find_duplicate_observations(frame)
    assert len(duplicates) == 2


def test_validate_date_range_rejects_out_of_range_rows() -> None:
    frame = pd.DataFrame({"date": ["2019-12-31", "2025-01-01"]})

    with pytest.raises(ValueError, match="outside allowed date range"):
        quality.validate_date_range(frame, "2020-01-01", "2026-04-30")


def test_validate_observed_rows_have_source_url() -> None:
    frame = pd.DataFrame(
        {
            "price_vnd_per_kg": [101000],
            "source_url": [""],
        }
    )

    with pytest.raises(ValueError, match="missing source_url"):
        quality.validate_observed_source_urls(frame)


def test_validate_price_range_rejects_implausible_values() -> None:
    frame = pd.DataFrame({"price_vnd_per_kg": [9000, 101000, 250000]})

    with pytest.raises(ValueError, match="outside expected range"):
        quality.validate_price_range(frame)


def test_summarize_observed_data_completeness() -> None:
    frame = pd.DataFrame(
        {
            "province": ["Lam Dong", "Lam Dong", "Dak Lak"],
            "price_fill_method": ["observed", "province_proxy", "observed"],
        }
    )

    summary = quality.summarize_observed_data_completeness(frame, ["province"])
    lam_dong = summary[summary["province"] == "Lam Dong"].iloc[0]
    assert lam_dong["total_rows"] == 2
    assert lam_dong["observed_rows"] == 1
    assert lam_dong["observed_rate"] == 0.5
