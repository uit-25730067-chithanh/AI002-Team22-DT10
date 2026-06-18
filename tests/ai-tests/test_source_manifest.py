from __future__ import annotations

import json
from pathlib import Path

from crawler import coffee_data_contract as contract


MANIFEST_PATH = Path("crawler/source_manifest.json")
REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "source_name",
    "base_url",
    "search_domain",
    "sitemap_candidates",
    "url_keywords",
    "seed_urls",
    "allowed_date_range",
}


def load_manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_manifest_exists_and_uses_contract_range() -> None:
    assert MANIFEST_PATH.exists()
    manifest = load_manifest()

    assert manifest["dataset_id"] == contract.DATASET_ID
    assert manifest["date_range"] == {
        "start": contract.START_DATE,
        "end": contract.END_DATE,
    }


def test_manifest_sources_have_required_fields() -> None:
    manifest = load_manifest()
    sources = manifest["sources"]
    assert isinstance(sources, list)
    assert len(sources) >= 4

    for source in sources:
        assert REQUIRED_SOURCE_FIELDS.issubset(source)
        assert source["allowed_date_range"] == {
            "start": contract.START_DATE,
            "end": contract.END_DATE,
        }
        assert source["source_id"]
        assert source["source_name"]
        assert source["base_url"].startswith("https://")
        assert isinstance(source["sitemap_candidates"], list)
        assert isinstance(source["url_keywords"], list)
        assert isinstance(source["seed_urls"], list)


def test_manifest_source_ids_are_unique() -> None:
    sources = load_manifest()["sources"]
    source_ids = [source["source_id"] for source in sources]
    assert len(source_ids) == len(set(source_ids))


def test_manifest_outputs_do_not_point_to_old_data() -> None:
    manifest = load_manifest()
    output_values = json.dumps(manifest.get("outputs", {}), ensure_ascii=False)

    assert "coffee_environment_all_areas_monthly_2020_2026.csv" in output_values
    assert "coffee_environment_all_areas_weekly_2020_2026.csv" in output_values
