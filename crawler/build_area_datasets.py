"""Merge area coffee prices, weather, and soil profile into analysis datasets."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .area_dataset_builder import build_dataset
except ImportError:
    from area_dataset_builder import build_dataset


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freq", choices=["weekly", "monthly"], required=True)
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--output-root", default="data/processed")
    args = parser.parse_args()
    build_dataset(Path(args.raw_dir), Path(args.output_root), args.freq)


if __name__ == "__main__":
    main()
