"""Run manifest-based independent coffee price crawlers for Team 2."""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from . import independent_data_contract as contract
    from .price_crawler_common import SiteConfig, crawl_site_async
except ImportError:
    import independent_data_contract as contract
    from price_crawler_common import SiteConfig, crawl_site_async


MANIFEST_PATH = Path("crawler/source_manifest_independent.json")


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_date_range(manifest: dict[str, Any]) -> tuple[str, str]:
    date_range = manifest["date_range"]
    return str(date_range["start"]), str(date_range["end"])


def site_configs_from_manifest(manifest: dict[str, Any]) -> list[SiteConfig]:
    configs: list[SiteConfig] = []
    for source in manifest["sources"]:
        configs.append(
            SiteConfig(
                source_name=source["source_name"],
                base_url=source["base_url"],
                sitemap_candidates=tuple(source["sitemap_candidates"]),
                url_keywords=tuple(source["url_keywords"]),
                seed_urls=tuple(source["seed_urls"]),
                search_domain=source["search_domain"],
            )
        )
    return configs


def ensure_independent_output_dir(path: Path) -> None:
    normalized = path.as_posix().rstrip("/")
    if normalized == "data/raw" or "independent" not in normalized:
        raise ValueError(f"Refusing to write independent crawl to {path}")


def write_timeout_error(error_dir: Path, source_name: str, timeout_seconds: int) -> None:
    error_dir.mkdir(parents=True, exist_ok=True)
    source_id = source_name.lower().replace(" ", "_")
    error_path = error_dir / f"coffee_price_{source_id}_errors.csv"
    write_header = not error_path.exists() or error_path.stat().st_size == 0
    with error_path.open("a", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["url", "error"])
        if write_header:
            writer.writeheader()
        writer.writerow(
            {
                "url": "*",
                "error": f"source_timeout_{timeout_seconds}s",
            }
        )


async def run_all_sites(args: argparse.Namespace) -> None:
    manifest = load_manifest(Path(args.manifest))
    start_text, end_text = manifest_date_range(manifest)
    start = datetime.strptime(args.start or start_text, "%Y-%m-%d").date()
    end = datetime.strptime(args.end or end_text, "%Y-%m-%d").date()

    output_dir = Path(args.output_dir or contract.SOURCE_OUTPUT_DIR)
    raw_dir = Path(args.raw_dir or contract.RAW_DIR)
    error_dir = Path(args.error_dir or contract.ERROR_OUTPUT_DIR)
    ensure_independent_output_dir(output_dir)
    ensure_independent_output_dir(raw_dir)
    ensure_independent_output_dir(error_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    error_dir.mkdir(parents=True, exist_ok=True)

    for config in site_configs_from_manifest(manifest):
        try:
            await asyncio.wait_for(
                crawl_site_async(
                    config=config,
                    start=start,
                    end=end,
                    output_dir=output_dir,
                    raw_dir=raw_dir,
                    max_urls=args.max_urls,
                    concurrency=args.concurrency,
                    flush_every=args.flush_every,
                    stop_after_seconds=args.stop_after_seconds,
                    year_range_label=contract.YEAR_RANGE_LABEL,
                    combined_filename=contract.RAW_PRICE_FILE.name,
                    error_dir=error_dir,
                    seed_only=args.seed_only,
                ),
                timeout=args.per_site_timeout,
            )
        except asyncio.TimeoutError:
            write_timeout_error(error_dir, config.source_name, args.per_site_timeout)
            print(
                f"{config.source_name}: timed out after {args.per_site_timeout}s",
                flush=True,
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(MANIFEST_PATH))
    parser.add_argument("--start", default=None)
    parser.add_argument("--end", default=None)
    parser.add_argument("--output-dir", default=str(contract.SOURCE_OUTPUT_DIR))
    parser.add_argument("--raw-dir", default=str(contract.RAW_DIR))
    parser.add_argument("--error-dir", default=str(contract.ERROR_OUTPUT_DIR))
    parser.add_argument("--max-urls", type=int, default=None)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--flush-every", type=int, default=25)
    parser.add_argument("--stop-after-seconds", type=int, default=900)
    parser.add_argument("--per-site-timeout", type=int, default=1200)
    parser.add_argument(
        "--seed-only",
        action="store_true",
        help="Use manifest seed URLs only. Intended for smoke tests.",
    )
    return parser.parse_args()


def main() -> None:
    asyncio.run(run_all_sites(parse_args()))


if __name__ == "__main__":
    main()
