"""Shared helpers for async coffee price crawlers."""

from __future__ import annotations

import asyncio
import argparse
import csv
import re
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote_plus, unquote, urljoin, urlparse, parse_qs

import aiohttp
import pandas as pd
import requests
from bs4 import BeautifulSoup

from coffee_areas import AREAS, COFFEE_TYPE, slugify
from crawl_coffee_prices import parse_article, url_date_in_range


HEADERS = {
    "User-Agent": "AI002 coffee dataset crawler/1.0 (+educational project)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
FIELDNAMES = [
    "date",
    "province",
    "area",
    "coffee_type",
    "price_vnd_per_kg",
    "change_vnd_per_kg",
    "source_name",
    "source_url",
]


@dataclass(frozen=True)
class SiteConfig:
    source_name: str
    base_url: str
    sitemap_candidates: tuple[str, ...]
    url_keywords: tuple[str, ...]
    seed_urls: tuple[str, ...] = ()
    search_domain: str = ""


def source_slug(source_name: str) -> str:
    return slugify(source_name).replace("_", "")


def date_from_url(url: str) -> date | None:
    patterns = [
        r"gia-ca-phe-hom-nay-(\d{1,2})-(\d{1,2})-(20\d{2})",
        r"gia-ca-phe-hom-nay-(\d{1,2})(\d{2})(20\d{2})",
        r"gia-ca-phe-hom-nay-(\d{1,2})-(\d{1,2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url, flags=re.IGNORECASE)
        if not match:
            continue
        groups = match.groups()
        if len(groups) == 3:
            day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
            try:
                return date(year, month, day)
            except ValueError:
                continue
    return None


def url_likely_in_range(url: str, start: date, end: date) -> bool:
    parsed = date_from_url(url)
    if parsed is None:
        return True
    return start <= parsed <= end


def discover_sitemap_urls(config: SiteConfig, start: date, end: date, max_sitemaps: int = 250) -> list[str]:
    seen_sitemaps: set[str] = set()
    seen_urls: set[str] = set(config.seed_urls)
    queue = [urljoin(config.base_url, item) for item in config.sitemap_candidates]

    while queue and len(seen_sitemaps) < max_sitemaps:
        sitemap_url = queue.pop(0)
        if sitemap_url in seen_sitemaps:
            continue
        seen_sitemaps.add(sitemap_url)
        try:
            response = requests.get(sitemap_url, headers=HEADERS, timeout=20)
            if response.status_code >= 400:
                continue
            xml = response.text
        except requests.RequestException:
            continue

        soup = BeautifulSoup(xml, "html.parser")
        for loc in [node.get_text(strip=True) for node in soup.find_all("loc")]:
            if not loc:
                continue
            lower = loc.lower()
            if lower.endswith(".xml") and loc not in seen_sitemaps:
                queue.append(loc)
                continue
            if any(keyword in lower for keyword in config.url_keywords) and url_likely_in_range(loc, start, end):
                seen_urls.add(loc)
    return sorted(seen_urls)


def clean_search_href(href: str) -> str:
    if href.startswith("/url?"):
        parsed = urlparse(href)
        values = parse_qs(parsed.query).get("q")
        if values:
            return unquote(values[0])
    return href


def discover_search_urls(config: SiteConfig, start: date, end: date, pages_per_query: int = 4) -> list[str]:
    domain = config.search_domain or urlparse(config.base_url).netloc
    found: set[str] = set()
    years = range(start.year, end.year + 1)
    queries = []
    for year in years:
        queries.extend(
            [
                f'site:{domain} "gia ca phe hom nay" "{year}"',
                f'site:{domain} "giá cà phê hôm nay" "{year}"',
                f'site:{domain} "Cư M\'gar" "{year}" "giá cà phê"',
            ]
        )
    for query in queries:
        encoded = quote_plus(query)
        for page in range(pages_per_query):
            first = page * 10 + 1
            url = f"https://www.bing.com/search?q={encoded}&first={first}"
            try:
                response = requests.get(url, headers=HEADERS, timeout=20)
                if response.status_code >= 400:
                    continue
            except requests.RequestException:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                href = clean_search_href(link["href"])
                lower = href.lower()
                if domain in lower and any(keyword in lower for keyword in config.url_keywords):
                    if url_likely_in_range(href, start, end):
                        found.add(href.split("#")[0])
    return sorted(found)


def read_existing_rows(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=FIELDNAMES)
    return pd.read_csv(path)


def append_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def finalize_source_output(path: Path) -> pd.DataFrame:
    frame = read_existing_rows(path)
    if frame.empty:
        return frame
    frame = (
        frame.drop_duplicates(["date", "province", "area", "source_url"])
        .sort_values(["date", "province", "area", "source_name"])
        .reset_index(drop=True)
    )
    frame.to_csv(path, index=False, encoding="utf-8-sig")
    return frame


def merge_source_into_raw(source_path: Path, raw_dir: Path) -> None:
    source_frame = finalize_source_output(source_path)
    if source_frame.empty:
        return

    combined_path = raw_dir / "coffee_price_all_areas_daily_2022_2025.csv"
    existing = read_existing_rows(combined_path)
    combined = pd.concat([existing, source_frame], ignore_index=True)
    combined = (
        combined.drop_duplicates(["date", "province", "area", "source_name", "source_url"])
        .sort_values(["date", "province", "area", "source_name"])
        .reset_index(drop=True)
    )
    combined.to_csv(combined_path, index=False, encoding="utf-8-sig")

    for area, area_frame in combined.groupby("area"):
        output = raw_dir / f"coffee_price_{slugify(area)}_daily_2022_2025.csv"
        area_frame.sort_values(["date", "province", "area", "source_name"]).to_csv(
            output,
            index=False,
            encoding="utf-8-sig",
        )


async def fetch(session: aiohttp.ClientSession, url: str, retries: int = 2) -> tuple[str, str | None]:
    for attempt in range(retries + 1):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=25)) as response:
                if response.status >= 400:
                    return "", f"http_{response.status}"
                body = await response.read()
                charset = response.charset or "utf-8"
                try:
                    return body.decode(charset, errors="replace"), None
                except LookupError:
                    return body.decode("utf-8", errors="replace"), None
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            if attempt >= retries:
                return await fetch_with_requests(url)
            await asyncio.sleep(0.5 * (attempt + 1))
    return "", "unknown_error"


async def fetch_with_requests(url: str) -> tuple[str, str | None]:
    def _get() -> tuple[str, str | None]:
        try:
            response = requests.get(url, headers=HEADERS, timeout=25)
            if response.status_code >= 400:
                return "", f"http_{response.status_code}"
            return response.text, None
        except requests.RequestException as exc:
            return "", exc.__class__.__name__

    return await asyncio.to_thread(_get)


def retag_rows(rows: list[dict[str, object]], source_name: str) -> list[dict[str, object]]:
    for row in rows:
        row["source_name"] = source_name
    return rows


async def crawl_site_async(
    config: SiteConfig,
    start: date,
    end: date,
    output_dir: Path,
    raw_dir: Path,
    max_urls: int | None,
    concurrency: int,
    flush_every: int,
    stop_after_seconds: int,
) -> Path:
    discovered = sorted(set(discover_sitemap_urls(config, start, end)) | set(discover_search_urls(config, start, end)))
    urls = discovered[:max_urls] if max_urls else discovered
    output_path = output_dir / f"coffee_price_{source_slug(config.source_name)}_daily_2022_2025.csv"
    error_path = output_dir / f"coffee_price_{source_slug(config.source_name)}_errors.csv"
    print(f"{config.source_name}: discovered {len(discovered)} URLs, crawling {len(urls)}", flush=True)

    started = time.monotonic()
    semaphore = asyncio.Semaphore(concurrency)
    rows_buffer: list[dict[str, object]] = []
    errors_buffer: list[dict[str, object]] = []
    processed = 0

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(headers=HEADERS, connector=connector, trust_env=True) as session:
        async def handle_url(url: str) -> None:
            nonlocal processed
            if time.monotonic() - started > stop_after_seconds:
                return
            async with semaphore:
                html, error = await fetch(session, url)
            if error:
                errors_buffer.append({"url": url, "error": error})
            else:
                parsed_rows, parse_error = parse_article(url, html, start, end)
                if parsed_rows:
                    rows_buffer.extend(retag_rows(parsed_rows, config.source_name))
                elif parse_error and parse_error != "outside_range":
                    errors_buffer.append({"url": url, "error": parse_error})
            processed += 1
            if processed % flush_every == 0:
                append_rows(output_path, rows_buffer)
                rows_buffer.clear()
                if errors_buffer:
                    pd.DataFrame(errors_buffer).to_csv(error_path, index=False, encoding="utf-8-sig")
                    errors_buffer.clear()
                print(f"{config.source_name}: processed {processed}/{len(urls)}", flush=True)

        await asyncio.gather(*(handle_url(url) for url in urls))

    append_rows(output_path, rows_buffer)
    if errors_buffer:
        existing_errors = pd.read_csv(error_path) if error_path.exists() else pd.DataFrame()
        pd.concat([existing_errors, pd.DataFrame(errors_buffer)], ignore_index=True).to_csv(
            error_path,
            index=False,
            encoding="utf-8-sig",
        )
    frame = finalize_source_output(output_path)
    merge_source_into_raw(output_path, raw_dir)
    print(f"{config.source_name}: wrote {output_path} ({len(frame)} rows)", flush=True)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2022-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--output-dir", default="data/raw/sources")
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--max-urls", type=int, default=None)
    parser.add_argument("--concurrency", type=int, default=12)
    parser.add_argument("--flush-every", type=int, default=25)
    parser.add_argument("--stop-after-seconds", type=int, default=1140)
    return parser.parse_args()


def run_site(config: SiteConfig) -> None:
    args = parse_args()
    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end = datetime.strptime(args.end, "%Y-%m-%d").date()
    asyncio.run(
        crawl_site_async(
            config=config,
            start=start,
            end=end,
            output_dir=Path(args.output_dir),
            raw_dir=Path(args.raw_dir),
            max_urls=args.max_urls,
            concurrency=args.concurrency,
            flush_every=args.flush_every,
            stop_after_seconds=args.stop_after_seconds,
        )
    )
