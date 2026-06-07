"""Constants for the Team 2 independent coffee dataset rebuild."""

from __future__ import annotations

from pathlib import Path


DATASET_ID = "team2_independent_coffee_2020_2026"
START_DATE = "2020-01-01"
END_DATE = "2026-04-30"
YEAR_RANGE_LABEL = "2020_2026"

RAW_DIR = Path("data/raw/independent")
SOURCE_OUTPUT_DIR = RAW_DIR / "sources"
ERROR_OUTPUT_DIR = RAW_DIR / "errors"

RAW_PRICE_FILE = RAW_DIR / f"coffee_price_all_areas_daily_{YEAR_RANGE_LABEL}.csv"
RAW_WEATHER_FILE = RAW_DIR / f"weather_all_areas_daily_{YEAR_RANGE_LABEL}.csv"

PROCESSED_MONTHLY_DIR = Path("data/processed/monthly")
PROCESSED_WEEKLY_DIR = Path("data/processed/weekly")
MONTHLY_OUTPUT_FILE = (
    PROCESSED_MONTHLY_DIR
    / f"coffee_environment_independent_all_areas_monthly_{YEAR_RANGE_LABEL}.csv"
)
WEEKLY_OUTPUT_FILE = (
    PROCESSED_WEEKLY_DIR
    / f"coffee_environment_independent_all_areas_weekly_{YEAR_RANGE_LABEL}.csv"
)

REQUIRED_RAW_PRICE_COLUMNS = [
    "date",
    "province",
    "area",
    "coffee_type",
    "price_vnd_per_kg",
    "change_vnd_per_kg",
    "source_name",
    "source_url",
]

REQUIRED_PROCESSED_COLUMNS = [
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

SOURCE_EVIDENCE_COLUMNS = [
    "source_url_count",
    "source_names",
]

OPTIONAL_PROCESSED_COLUMNS = SOURCE_EVIDENCE_COLUMNS

