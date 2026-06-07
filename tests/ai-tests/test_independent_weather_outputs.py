from __future__ import annotations

from pathlib import Path

import pandas as pd

from crawler import independent_data_contract as contract
from crawler.crawl_weather_by_area import (
    combined_weather_output_path,
    write_area_weather,
)


def test_independent_combined_weather_output_path() -> None:
    path = combined_weather_output_path(Path("data/raw/independent"), "2020_2026")

    assert path == contract.RAW_WEATHER_FILE
    assert "2022_2025" not in path.as_posix()


def test_write_area_weather_uses_requested_year_range(tmp_path: Path) -> None:
    frame = pd.DataFrame(
        {
            "date": ["2025-01-01"],
            "province": ["Lam Dong"],
            "area": ["Di Linh"],
            "latitude": [11.5814],
            "longitude": [108.0727],
            "temperature_c": [20.0],
            "humidity_percent": [80.0],
            "rainfall_mm": [0.0],
            "soil_moisture_0_7cm": [0.25],
        }
    )

    output = write_area_weather(frame, tmp_path, "Di Linh", "2020_2026")

    assert output == tmp_path / "weather_di_linh_daily_2020_2026.csv"
    assert output.exists()
