"""Run all site-specific coffee price crawlers with a per-site time budget."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PRICE_CRAWLERS = [
    "crawler/crawl_price_vinanet.py",
    "crawler/crawl_price_congthuong.py",
    "crawler/crawl_price_nongnghiep.py",
    "crawler/crawl_price_kinhtedothi.py",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2022-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--per-site-timeout", type=int, default=1200)
    parser.add_argument("--stop-after-seconds", type=int, default=1140)
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--flush-every", type=int, default=25)
    parser.add_argument("--max-urls", type=int, default=None)
    args = parser.parse_args()

    for crawler in PRICE_CRAWLERS:
        command = [
            sys.executable,
            crawler,
            "--start",
            args.start,
            "--end",
            args.end,
            "--concurrency",
            str(args.concurrency),
            "--flush-every",
            str(args.flush_every),
            "--stop-after-seconds",
            str(args.stop_after_seconds),
        ]
        if args.max_urls:
            command.extend(["--max-urls", str(args.max_urls)])
        print(f"Running {' '.join(command)}", flush=True)
        try:
            subprocess.run(command, cwd=Path.cwd(), check=False, timeout=args.per_site_timeout)
        except subprocess.TimeoutExpired:
            print(f"Timed out: {crawler}. Data flushed so far is kept.", flush=True)

    for freq in ["weekly", "monthly"]:
        command = [sys.executable, "crawler/build_area_datasets.py", "--freq", freq]
        print(f"Running {' '.join(command)}", flush=True)
        subprocess.run(command, cwd=Path.cwd(), check=False)


if __name__ == "__main__":
    main()
