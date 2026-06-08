from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from crawler import coffee_data_contract as contract
from crawler import price_crawler_common
from crawler import run_price_crawlers as runner


def test_load_manifest_configs_use_contract_date_range() -> None:
    manifest = runner.load_manifest()
    configs = runner.site_configs_from_manifest(manifest)

    assert len(configs) >= 4
    assert runner.manifest_date_range(manifest) == (
        contract.START_DATE,
        contract.END_DATE,
    )
    assert {config.source_name for config in configs} >= {
        "Cong Thuong",
        "Nong Nghiep Moi Truong",
        "Kinh Te Do Thi",
        "Vinanet",
    }


def test_runner_refuses_legacy_raw_output_dir() -> None:
    with pytest.raises(ValueError, match="Refusing to write crawl output"):
        runner.ensure_canonical_output_dir(Path("data"))


def test_runner_accepts_raw_output_dir() -> None:
    runner.ensure_canonical_output_dir(contract.RAW_DIR)


def test_merge_source_into_raw_uses_canonical_combined_filename(tmp_path: Path) -> None:
    source_path = tmp_path / "sources" / "coffee_price_fixture_daily_2020_2026.csv"
    source_path.parent.mkdir()
    rows = pd.DataFrame(
        [
            {
                "date": "2025-01-01",
                "province": "Lam Dong",
                "area": "Di Linh",
                "coffee_type": "Robusta",
                "price_vnd_per_kg": 101000,
                "change_vnd_per_kg": 0,
                "source_name": "Fixture",
                "source_url": "https://example.test/a",
            },
            {
                "date": "2025-01-01",
                "province": "Lam Dong",
                "area": "Di Linh",
                "coffee_type": "Robusta",
                "price_vnd_per_kg": 101000,
                "change_vnd_per_kg": 0,
                "source_name": "Fixture",
                "source_url": "https://example.test/a",
            },
        ]
    )
    rows.to_csv(source_path, index=False)

    price_crawler_common.merge_source_into_raw(
        source_path,
        tmp_path,
        combined_filename=contract.RAW_PRICE_FILE.name,
        year_range_label=contract.YEAR_RANGE_LABEL,
    )

    combined_path = tmp_path / contract.RAW_PRICE_FILE.name
    old_path = tmp_path / "coffee_price_all_areas_daily_2022_2025.csv"
    area_path = tmp_path / "coffee_price_di_linh_daily_2020_2026.csv"
    combined = pd.read_csv(combined_path)

    assert combined_path.exists()
    assert not old_path.exists()
    assert area_path.exists()
    assert len(combined) == 1
