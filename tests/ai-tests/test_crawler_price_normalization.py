from __future__ import annotations
import crawler.coffee_areas as coffee_areas
import crawler.area_dataset_builder as area_dataset_builder
import crawler.price_crawler_common as price_crawler_common
import model.experiment_tracker as experiment_tracker

import pytest

from crawler import price_crawler_common as price_normalization


def test_normalize_name() -> None:
    assert coffee_areas.normalize_name("Đắk Lắk") == "dak lak"
    assert coffee_areas.normalize_name("Chư Prông") == "chu prong"
    assert coffee_areas.normalize_name("Hồ Chí Minh") == "ho chi minh"


def test_parse_price() -> None:
    assert price_crawler_common.parse_price("120.500") == 120500
    assert price_crawler_common.parse_price("120,500") == 120500
    assert price_crawler_common.parse_price("120500") == 120500
    assert price_crawler_common.parse_price("Giá: 120.500 vnđ") == 120500
    assert price_crawler_common.parse_price("invalid") is None


def test_parse_change() -> None:
    assert price_crawler_common.parse_change("+ 500") == 500
    assert price_crawler_common.parse_change("- 500") == -500
    assert price_crawler_common.parse_change("-500") == -500
    assert price_crawler_common.parse_change("—") is None
    assert price_crawler_common.parse_change("-") is None


def test_area_from_text() -> None:
    area = price_crawler_common.area_from_text("Di Linh")
    assert area is not None
    assert area["province"] == "Lam Dong"

    area2 = price_crawler_common.area_from_text("Chư Prông")
    assert area2 is not None
    assert area2["province"] == "Gia Lai"

    area3 = price_crawler_common.area_from_text("Dak R'lap")
    assert area3 is not None
    assert area3["province"] == "Dak Nong"

    assert price_crawler_common.area_from_text("Unknown Area") is None