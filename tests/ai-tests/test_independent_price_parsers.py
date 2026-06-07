from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from crawler.price_crawler_common import parse_article


FIXTURE_DIR = Path("tests/ai-tests/fixtures/price-articles")
MANIFEST_PATH = Path("crawler/source_manifest_independent.json")


def read_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def manifest_source_names() -> list[str]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return [source["source_name"] for source in manifest["sources"]]


def test_parse_table_fixture_with_change() -> None:
    rows, error = parse_article(
        "https://example.test/gia-ca-phe-hom-nay-12-12-2024.html",
        read_fixture("table-row.html"),
        date(2020, 1, 1),
        date(2026, 4, 30),
        "Fixture Source",
    )

    assert error is None
    assert len(rows) == 1
    assert rows[0]["date"] == "2024-12-12"
    assert rows[0]["province"] == "Lam Dong"
    assert rows[0]["area"] == "Di Linh"
    assert rows[0]["price_vnd_per_kg"] == 120500
    assert rows[0]["change_vnd_per_kg"] == 500
    assert rows[0]["source_name"] == "Fixture Source"


@pytest.mark.parametrize("source_name", manifest_source_names())
def test_each_manifest_source_has_parser_fixture_coverage(source_name: str) -> None:
    rows, error = parse_article(
        "https://example.test/gia-ca-phe-hom-nay-12-12-2024.html",
        read_fixture("table-row.html"),
        date(2020, 1, 1),
        date(2026, 4, 30),
        source_name,
    )

    assert error is None
    assert rows[0]["source_name"] == source_name
    assert rows[0]["area"] == "Di Linh"


def test_parse_grouped_area_text_fixture() -> None:
    rows, error = parse_article(
        "https://example.test/gia-ca-phe-hom-nay-15-3-2025.html",
        read_fixture("grouped-area-text.html"),
        date(2020, 1, 1),
        date(2026, 4, 30),
        "Fixture Source",
    )

    assert error is None
    area_prices = {row["area"]: row["price_vnd_per_kg"] for row in rows}
    assert area_prices["Di Linh"] == 101000
    assert area_prices["Lam Ha"] == 101000
    assert area_prices["Bao Loc"] == 101000
    assert area_prices["Ea H'leo"] == 102500
    assert area_prices["Buon Ho"] == 102500


def test_parse_article_outside_independent_range() -> None:
    rows, error = parse_article(
        "https://example.test/gia-ca-phe-hom-nay-12-12-2019.html",
        read_fixture("table-row.html"),
        date(2020, 1, 1),
        date(2026, 4, 30),
        "Fixture Source",
    )

    assert rows == []
    assert error == "outside_range"


def test_parse_malformed_fixture_returns_no_price_rows() -> None:
    rows, error = parse_article(
        "https://example.test/gia-ca-phe-hom-nay-16-3-2025.html",
        read_fixture("malformed-price.html"),
        date(2020, 1, 1),
        date(2026, 4, 30),
        "Fixture Source",
    )

    assert rows == []
    assert error == "no_price_rows"
