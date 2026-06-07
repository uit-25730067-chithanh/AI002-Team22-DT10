from __future__ import annotations

from pathlib import Path

from crawler import independent_data_contract as contract


def test_independent_date_range_is_frozen() -> None:
    assert contract.START_DATE == "2020-01-01"
    assert contract.END_DATE == "2026-04-30"


def test_independent_paths_use_separate_namespace() -> None:
    paths = [
        contract.RAW_DIR,
        contract.SOURCE_OUTPUT_DIR,
        contract.ERROR_OUTPUT_DIR,
        contract.RAW_PRICE_FILE,
        contract.RAW_WEATHER_FILE,
        contract.MONTHLY_OUTPUT_FILE,
        contract.WEEKLY_OUTPUT_FILE,
    ]

    for path in paths:
        assert isinstance(path, Path)
        assert "independent" in path.as_posix()
        assert "coffee_environment_all_areas_monthly_2022_2025.csv" not in path.as_posix()
        assert "coffee_environment_all_areas_weekly_2022_2025.csv" not in path.as_posix()


def test_processed_schema_keeps_model_required_columns() -> None:
    required = set(contract.REQUIRED_PROCESSED_COLUMNS)
    assert {
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
    }.issubset(required)


def test_source_evidence_columns_are_declared() -> None:
    assert set(contract.SOURCE_EVIDENCE_COLUMNS) == {
        "source_url_count",
        "source_names",
    }
