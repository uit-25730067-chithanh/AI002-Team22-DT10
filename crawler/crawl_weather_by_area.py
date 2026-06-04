"""Download daily weather data from Open-Meteo for each coffee price area."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from .coffee_areas import AREAS, slugify


OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_weather(area: dict[str, Any], start: str, end: str) -> pd.DataFrame:
    params = {
        "latitude": area["latitude"],
        "longitude": area["longitude"],
        "start_date": start,
        "end_date": end,
        "daily": ",".join(
            [
                "temperature_2m_mean",
                "relative_humidity_2m_mean",
                "precipitation_sum",
                "soil_moisture_0_to_7cm_mean",
            ]
        ),
        "timezone": "Asia/Bangkok",
    }
    response = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    daily = payload.get("daily", {})
    frame = pd.DataFrame(
        {
            "date": daily.get("time", []),
            "province": area["province"],
            "area": area["area"],
            "latitude": area["latitude"],
            "longitude": area["longitude"],
            "temperature_c": daily.get("temperature_2m_mean", []),
            "humidity_percent": daily.get("relative_humidity_2m_mean", []),
            "rainfall_mm": daily.get("precipitation_sum", []),
            "soil_moisture_0_7cm": daily.get("soil_moisture_0_to_7cm_mean", []),
        }
    )
    frame["date"] = pd.to_datetime(frame["date"]).dt.date
    return frame


def write_area_weather(frame: pd.DataFrame, output_dir: Path, area_name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"weather_{slugify(area_name)}_daily_2022_2025.csv"
    frame.to_csv(output, index=False, encoding="utf-8-sig")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2022-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--output-dir", default="data/raw")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    all_frames: list[pd.DataFrame] = []
    for area in AREAS:
        frame = fetch_weather(area, args.start, args.end)
        output = write_area_weather(frame, output_dir, area["area"])
        all_frames.append(frame)
        print(f"Wrote {output} ({len(frame)} rows)")

    combined = pd.concat(all_frames, ignore_index=True)
    combined_output = output_dir / "weather_all_areas_daily_2022_2025.csv"
    combined.to_csv(combined_output, index=False, encoding="utf-8-sig")
    print(f"Wrote {combined_output} ({len(combined)} rows)")


if __name__ == "__main__":
    main()
