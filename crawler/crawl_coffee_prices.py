"""Crawl and parse coffee prices by local area.

The crawler keeps each market area separate. It first tries to discover article
URLs from sitemap files, then appends known seed URLs and any user-provided URL
file. Parsed rows are exported per area and as a combined CSV.
"""

from __future__ import annotations

import argparse
import re
import time
from datetime import date, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .coffee_areas import slugify
from .price_crawler_common import parse_article


SOURCE_NAME = "Bao Nong nghiep va Moi truong"
BASE_URL = "https://nongnghiepmoitruong.vn/"
KNOWN_SEED_URLS = [
    "https://nongnghiepmoitruong.vn/gia-ca-phe-hom-nay-12-12-2022-tuan-qua-giam-300--500-d-kg-d339610.html",
    "https://nongnghiepmoitruong.vn/gia-ca-phe-hom-nay-7-3-2023-giam-nhe-mat-moc-48000-d-kg-d345345.html",
    "https://nongnghiepmoitruong.vn/gia-ca-phe-hom-nay-25-7-2025-thi-truong-tiep-tuc-tang-d764611.html",
    "https://vicofa.org.vn/gia-ca-phe-trong-nuoc-sang-ngay-29/4/2022-bid974.html",
]
HEADERS = {
    "User-Agent": "AI002 coffee dataset crawler/1.0 (+educational project)",
}




def fetch_url(url: str, sleep_seconds: float) -> str:
    time.sleep(sleep_seconds)
    response = requests.get(url, headers=HEADERS, timeout=25)
    response.raise_for_status()
    return response.text



def url_date_in_range(url: str, start: date, end: date) -> bool:
    match = re.search(r"gia-ca-phe-hom-nay-(\d{1,2})-(\d{1,2})-(20\d{2})", url, flags=re.IGNORECASE)
    if not match:
        return True
    day, month, year = map(int, match.groups())
    try:
        value = date(year, month, day)
    except ValueError:
        return False
    return start <= value <= end


def sitemap_urls(start: date, end: date) -> Iterable[str]:
    candidates = [urljoin(BASE_URL, "sitemap.xml"), urljoin(BASE_URL, "sitemap_index.xml")]
    seen: set[str] = set()
    queue = list(candidates)
    while queue:
        sitemap_url = queue.pop(0)
        if sitemap_url in seen:
            continue
        seen.add(sitemap_url)
        try:
            xml = requests.get(sitemap_url, headers=HEADERS, timeout=20).text
        except requests.RequestException:
            continue
        soup = BeautifulSoup(xml, "html.parser")
        locs = [loc.get_text(strip=True) for loc in soup.find_all("loc")]
        for loc in locs:
            if loc.endswith(".xml") and loc not in seen:
                queue.append(loc)
            elif "gia-ca-phe-hom-nay" in loc and url_date_in_range(loc, start, end):
                yield loc


def load_url_file(path: Path | None) -> list[str]:
    if not path or not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def collect_urls(
    url_file: Path | None,
    start: date,
    end: date,
    include_sitemap: bool = True,
    max_urls: int | None = None,
) -> list[str]:
    urls = list(sitemap_urls(start, end)) if include_sitemap else []
    urls.extend(KNOWN_SEED_URLS)
    urls.extend(load_url_file(url_file))
    urls = [url for url in sorted(set(urls)) if url_date_in_range(url, start, end)]
    return urls[:max_urls] if max_urls else urls


def write_outputs(rows: list[dict[str, object]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    if frame.empty:
        print("No rows parsed; no price files written.")
        return
    frame = frame.drop_duplicates(["date", "province", "area", "source_url"]).sort_values(["date", "province", "area"])
    combined = output_dir / "coffee_price_all_areas_daily_2022_2025.csv"
    frame.to_csv(combined, index=False, encoding="utf-8-sig")
    print(f"Wrote {combined} ({len(frame)} rows)")
    for area, area_frame in frame.groupby("area"):
        output = output_dir / f"coffee_price_{slugify(area)}_daily_2022_2025.csv"
        area_frame.sort_values(["date", "province", "area"]).to_csv(output, index=False, encoding="utf-8-sig")
        print(f"Wrote {output} ({len(area_frame)} rows)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2022-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--output-dir", default="data/raw")
    parser.add_argument("--url-file", default=None, help="Optional newline-separated article URL file.")
    parser.add_argument("--no-sitemap", action="store_true", help="Only use seed URLs and --url-file.")
    parser.add_argument("--max-urls", type=int, default=None, help="Optional cap for faster test crawls.")
    parser.add_argument("--sleep", type=float, default=0.8)
    args = parser.parse_args()

    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end = datetime.strptime(args.end, "%Y-%m-%d").date()
    urls = collect_urls(
        Path(args.url_file) if args.url_file else None,
        start,
        end,
        include_sitemap=not args.no_sitemap,
        max_urls=args.max_urls,
    )
    print(f"Discovered {len(urls)} candidate URLs", flush=True)

    rows: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []
    for index, url in enumerate(urls, start=1):
        try:
            html = fetch_url(url, args.sleep)
            parsed_rows, error = parse_article(url, html, start, end, SOURCE_NAME)
            rows.extend(parsed_rows)
            if error and error != "outside_range":
                errors.append({"url": url, "error": error})
        except requests.RequestException as exc:
            errors.append({"url": url, "error": str(exc)})
        if index % 25 == 0:
            print(f"Processed {index}/{len(urls)} URLs, parsed {len(rows)} rows", flush=True)

    output_dir = Path(args.output_dir)
    write_outputs(rows, output_dir)
    if errors:
        error_output = output_dir / "coffee_price_crawl_errors.csv"
        pd.DataFrame(errors).to_csv(error_output, index=False, encoding="utf-8-sig")
        print(f"Wrote {error_output} ({len(errors)} rows)")


if __name__ == "__main__":
    main()
