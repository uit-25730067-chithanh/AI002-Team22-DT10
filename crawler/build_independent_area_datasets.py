"""Build processed datasets from Team 2 independent raw data."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from . import independent_data_contract as contract
    from .area_dataset_builder import build_dataset
except ImportError:
    import independent_data_contract as contract
    from area_dataset_builder import build_dataset


def build_independent_dataset(
    raw_dir: Path,
    output_root: Path,
    freq: str,
):
    combined_name = (
        contract.MONTHLY_OUTPUT_FILE.name
        if freq == "monthly"
        else contract.WEEKLY_OUTPUT_FILE.name
    )
    return build_dataset(
        raw_dir,
        output_root,
        freq,
        price_file=contract.RAW_PRICE_FILE.name,
        weather_file=contract.RAW_WEATHER_FILE.name,
        combined_output_name=combined_name,
        area_output_year_label=contract.YEAR_RANGE_LABEL,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freq", choices=["weekly", "monthly"], required=True)
    parser.add_argument("--raw-dir", default=str(contract.RAW_DIR))
    parser.add_argument("--output-root", default="data/processed")
    args = parser.parse_args()
    build_independent_dataset(Path(args.raw_dir), Path(args.output_root), args.freq)


if __name__ == "__main__":
    main()
