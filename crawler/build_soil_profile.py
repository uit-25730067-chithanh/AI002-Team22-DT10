"""Create a static soil profile table for coffee price areas."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .coffee_areas import AREAS


def build_soil_profile(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "area": item["area"],
            "province": item["province"],
            "dominant_soil_type": item["dominant_soil_type"],
            "soil_note": item["soil_note"],
            "soil_score": item["soil_score"],
            "soil_data_confidence": item["soil_data_confidence"],
            "source_url": item["source_url"],
        }
        for item in AREAS
    ]
    pd.DataFrame(rows).to_csv(output, index=False, encoding="utf-8-sig")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/soil_profile_by_area.csv")
    args = parser.parse_args()
    print(f"Wrote {build_soil_profile(Path(args.output))}")


if __name__ == "__main__":
    main()
