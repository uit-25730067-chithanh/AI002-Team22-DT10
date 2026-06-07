from __future__ import annotations

from pathlib import Path

import pandas as pd

from crawler import independent_data_contract as contract
from crawler import area_dataset_builder
from crawler import build_independent_area_datasets
from crawler import independent_data_audit


def write_raw_inputs(raw_dir: Path) -> None:
    raw_dir.mkdir(parents=True)
    pd.DataFrame(
        [
            {
                "date": "2025-01-05",
                "province": "Lam Dong",
                "area": "Di Linh",
                "coffee_type": "Robusta",
                "price_vnd_per_kg": 100000,
                "change_vnd_per_kg": 0,
                "source_name": "A Source",
                "source_url": "https://example.test/a",
            },
            {
                "date": "2025-01-06",
                "province": "Lam Dong",
                "area": "Di Linh",
                "coffee_type": "Robusta",
                "price_vnd_per_kg": 102000,
                "change_vnd_per_kg": 500,
                "source_name": "B Source",
                "source_url": "https://example.test/b",
            },
        ]
    ).to_csv(raw_dir / contract.RAW_PRICE_FILE.name, index=False)
    pd.DataFrame(
        [
            {
                "date": "2025-01-05",
                "province": "Lam Dong",
                "area": "Di Linh",
                "latitude": 11.58,
                "longitude": 108.07,
                "temperature_c": 20.0,
                "humidity_percent": 80.0,
                "rainfall_mm": 1.0,
                "soil_moisture_0_7cm": 0.25,
            },
            {
                "date": "2025-01-06",
                "province": "Lam Dong",
                "area": "Di Linh",
                "latitude": 11.58,
                "longitude": 108.07,
                "temperature_c": 22.0,
                "humidity_percent": 82.0,
                "rainfall_mm": 2.0,
                "soil_moisture_0_7cm": 0.27,
            },
        ]
    ).to_csv(raw_dir / contract.RAW_WEATHER_FILE.name, index=False)
    pd.DataFrame(
        [
            {
                "area": "Di Linh",
                "province": "Lam Dong",
                "dominant_soil_type": "Dat do vang tren bazan",
                "soil_score": 4,
                "soil_data_confidence": "medium",
            }
        ]
    ).to_csv(raw_dir / "soil_profile_by_area.csv", index=False)


def test_aggregate_prices_keeps_source_evidence() -> None:
    prices = pd.DataFrame(
        {
            "date": pd.to_datetime(["2025-01-05", "2025-01-06"]),
            "province": ["Lam Dong", "Lam Dong"],
            "area": ["Di Linh", "Di Linh"],
            "coffee_type": ["Robusta", "Robusta"],
            "price_vnd_per_kg": [100000, 102000],
            "source_name": ["B Source", "A Source"],
            "source_url": ["https://example.test/b", "https://example.test/a"],
        }
    )

    aggregated = area_dataset_builder.aggregate_prices(
        prices,
        "monthly",
        pd.Timestamp("2025-01-01"),
        pd.Timestamp("2025-01-31"),
    )

    row = aggregated.iloc[0]
    assert row["avg_price_vnd_per_kg"] == 101000
    assert row["price_observations"] == 2
    assert row["source_url_count"] == 2
    assert row["source_names"] == "A Source; B Source"


def test_build_independent_dataset_writes_independent_filename(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw" / "independent"
    output_root = tmp_path / "processed"
    write_raw_inputs(raw_dir)

    result = build_independent_area_datasets.build_independent_dataset(
        raw_dir,
        output_root,
        "monthly",
    )

    output = output_root / "monthly" / contract.MONTHLY_OUTPUT_FILE.name
    old_output = output_root / "monthly" / "coffee_environment_all_areas_monthly_2022_2025.csv"
    assert output.exists()
    assert not old_output.exists()
    assert len(result) == 1
    assert result.iloc[0]["source_url_count"] == 2
    assert result.iloc[0]["price_fill_method"] == "observed"


def test_audit_helper_summarizes_old_and_new_by_province() -> None:
    old = pd.DataFrame(
        {
            "province": ["Lam Dong", "Lam Dong"],
            "price_fill_method": ["observed", "province_proxy"],
        }
    )
    new = pd.DataFrame(
        {
            "province": ["Lam Dong", "Lam Dong", "Lam Dong"],
            "price_fill_method": ["observed", "observed", "province_proxy"],
        }
    )

    summary = independent_data_audit.compare_observed_data_completeness(
        old,
        new,
        ["province"],
    )

    row = summary.iloc[0]
    assert row["old_observed_rate"] == 0.5
    assert row["new_observed_rate"] == 0.6667
    assert row["delta_observed_rate"] == 0.1667
