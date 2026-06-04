from __future__ import annotations
from bs4 import BeautifulSoup
from datetime import date
from pathlib import Path
from urllib.parse import quote_plus, unquote, urljoin, urlparse, parse_qs
import csv
import pandas as pd
import re
import requests

from .coffee_areas import AREA_BY_NORMALIZED, normalize_name
"""Shared helpers for async coffee price crawlers."""


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

from .coffee_areas import AREAS, COFFEE_TYPE, slugify


HEADERS = {
    "User-Agent": "AI002 coffee dataset crawler/1.0 (+educational project)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}



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
    discovered = sorted(set(discover_sitemap_urls(config, start, end, HEADERS)) | set(discover_search_urls(config, start, end, HEADERS)))
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

# --- MERGED HELPERS ---

# --- from price_normalization.py ---



def parse_price(value: str) -> int | None:
    value = value.replace("\xa0", " ").strip()
    match = re.search(r"(\d{1,3}(?:[.,]\d{3})+|\d{3,6})", value)
    if not match:
        return None
    return int(match.group(1).replace(".", "").replace(",", ""))

def parse_change(value: str) -> int | None:
    value = value.replace("\xa0", " ").strip()
    if value in {"", "-", "—"}:
        return None
    sign = -1 if value.startswith("-") else 1
    price = parse_price(value)
    return sign * price if price is not None else None

def area_from_text(value: str) -> dict[str, object] | None:
    normalized = normalize_name(value)
    aliases = {
        "la grai": "ia grai",
        "chuprong": "chu prong",
        "dak rl ap": "dak r lap",
        "dak rlap": "dak r lap",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized in AREA_BY_NORMALIZED:
        return AREA_BY_NORMALIZED[normalized]
    for area_name, area in AREA_BY_NORMALIZED.items():
        if area_name and area_name in normalized:
            return area
    return None

def source_name_for_url(url: str, default_source_name: str) -> str:
    if "vicofa.org.vn" in url:
        return "VICOFA"
    if "chogia.vn" in url:
        return "Cho Gia"
    return default_source_name

# --- from price_csv_io.py ---




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

# --- from price_date_parsing.py ---




def parse_date_from_url_or_text(url: str, text: str) -> date | None:
    patterns = [
        r"gia-ca-phe-hom-nay-(\d{1,2})-(\d{1,2})-(20\d{2})",
        r"gia-ca-phe-hom-nay-(\d{1,2})(\d{2})(20\d{2})",
        r"gia-ca-phe-hom-nay-ngay-(\d{1,2})(\d{2})(20\d{2})",
        r"bang-gia-ca-phe-trong-nuoc-va-the-gioi-ngay-(\d{1,2})(\d{2})(20\d{2})",
        r"ngay-(\d{1,2})(\d{2})(20\d{2})",
        r"ngay-(\d{1,2})/(\d{1,2})/(20\d{2})",
        r"(\d{1,2})[/-](\d{1,2})[/-](20\d{2})",
    ]
    source = f"{url}\n{text[:2000]}"
    for pattern in patterns:
        match = re.search(pattern, source, flags=re.IGNORECASE)
        if match:
            day, month, year = map(int, match.groups())
            try:
                return date(year, month, day)
            except ValueError:
                continue
    return None


def parse_date_from_meta(soup: BeautifulSoup) -> date | None:
    selectors = [
        ("meta", {"property": "article:published_time"}),
        ("meta", {"name": "pubdate"}),
        ("meta", {"name": "publishdate"}),
        ("meta", {"name": "date"}),
        ("meta", {"itemprop": "datePublished"}),
    ]
    values: list[str] = []
    for name, attrs in selectors:
        node = soup.find(name, attrs=attrs)
        if node and node.get("content"):
            values.append(str(node["content"]))
    for node in soup.find_all("time"):
        if node.get("datetime"):
            values.append(str(node["datetime"]))
        values.append(node.get_text(" ", strip=True))
    for value in values:
        match = re.search(r"(20\d{2})-(\d{1,2})-(\d{1,2})", value)
        if match:
            year, month, day = map(int, match.groups())
            try:
                return date(year, month, day)
            except ValueError:
                continue
        match = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](20\d{2})", value)
        if match:
            day, month, year = map(int, match.groups())
            try:
                return date(year, month, day)
            except ValueError:
                continue
    return None

# --- from price_html_parsers.py ---




def parse_table_rows(soup: BeautifulSoup, article_date, source_url: str, default_source_name: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    current_province = ""
    for table in soup.find_all("table"):
        for tr in table.find_all("tr"):
            cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["td", "th"])]
            if len(cells) < 2:
                continue
            normalized_cells = [normalize_name(cell) for cell in cells]
            if any("tinh thanh" in cell or "dia phuong" in cell for cell in normalized_cells):
                continue

            area_cell = ""
            price_cell = ""
            change_cell = ""
            if len(cells) >= 4:
                current_province = cells[0] or current_province
                area_cell, price_cell, change_cell = cells[1], cells[2], cells[3]
                if not area_cell.strip() and normalize_name(current_province) == "kon tum":
                    area_cell = "Kon Tum"
            elif len(cells) == 3:
                area_cell, price_cell, change_cell = cells[0], cells[1], cells[2]
            elif len(cells) == 2:
                area_cell, price_cell = cells[0], cells[1]

            area = area_from_text(area_cell)
            price = parse_price(price_cell)
            if not area or price is None:
                continue
            province = str(area["province"])
            if current_province and normalize_name(current_province) in {"dak lak", "dak nong", "gia lai", "lam dong", "kon tum"}:
                province = str(area["province"])
            rows.append(
                {
                    "date": article_date.isoformat(),
                    "province": province,
                    "area": area["area"],
                    "coffee_type": COFFEE_TYPE,
                    "price_vnd_per_kg": price,
                    "change_vnd_per_kg": parse_change(change_cell),
                    "source_name": source_name_for_url(source_url, default_source_name),
                    "source_url": source_url,
                }
            )
    return rows

def parse_text_rows(soup: BeautifulSoup, article_date, source_url: str, default_source_name: str) -> list[dict[str, object]]:
    text = soup.get_text("\n", strip=True)
    rows: list[dict[str, object]] = []
    for area in AREAS:
        variants = {area["area"], area["area"].replace("Dak", "Đắk"), area["area"].replace("Chu", "Chư")}
        for variant in variants:
            pattern = rf"{re.escape(variant)}[^\n]{{0,120}}?(\d{{1,3}}[.,]\d{{3}}|\d{{5,6}})\s*(?:d|đ|dong|đồng)?/?kg"
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if not match:
                continue
            rows.append(
                {
                    "date": article_date.isoformat(),
                    "province": area["province"],
                    "area": area["area"],
                    "coffee_type": COFFEE_TYPE,
                    "price_vnd_per_kg": parse_price(match.group(1)),
                    "change_vnd_per_kg": None,
                    "source_name": source_name_for_url(source_url, default_source_name),
                    "source_url": source_url,
                }
            )
            break
    return rows

def parse_text_rows_enhanced(soup: BeautifulSoup, article_date, source_url: str, default_source_name: str) -> list[dict[str, object]]:
    text = soup.get_text("\n", strip=True)
    compact_text = re.sub(r"\s+", " ", text)
    rows = parse_text_rows(soup, article_date, source_url, default_source_name)
    for area in AREAS:
        variants = {
            area["area"],
            area["area"].replace("Dak", "Đắk"),
            area["area"].replace("Chu", "Chư"),
            area["area"].replace("Ia", "La"),
        }
        for variant in variants:
            pattern = rf"{re.escape(variant)}[^.;]{{0,220}}?(?:mức|giá|khoảng|là)\s*(\d{{1,3}}[.,]\d{{3}}|\d{{5,6}})"
            match = re.search(pattern, compact_text, flags=re.IGNORECASE)
            if not match:
                continue
            rows.append(
                {
                    "date": article_date.isoformat(),
                    "province": area["province"],
                    "area": area["area"],
                    "coffee_type": COFFEE_TYPE,
                    "price_vnd_per_kg": parse_price(match.group(1)),
                    "change_vnd_per_kg": None,
                    "source_name": source_name_for_url(source_url, default_source_name),
                    "source_url": source_url,
                }
            )
            break
    rows.extend(parse_grouped_area_text(compact_text, article_date, source_url, default_source_name))
    unique: dict[tuple[str, str, str], dict[str, object]] = {}
    for row in rows:
        unique[(str(row["date"]), str(row["province"]), str(row["area"]))] = row
    return list(unique.values())

def parse_grouped_area_text(text: str, article_date, source_url: str, default_source_name: str) -> list[dict[str, object]]:
    groups = [
        (["Di Linh", "Lâm Hà", "Bảo Lộc", "Lam Ha", "Bao Loc"], ["Di Linh", "Lam Ha", "Bao Loc"]),
        (["Ea H'leo", "Buôn Hồ", "Buon Ho"], ["Ea H'leo", "Buon Ho"]),
        (["Pleiku", "La Grai", "Ia Grai"], ["Pleiku", "Ia Grai"]),
    ]
    rows: list[dict[str, object]] = []
    lower_text = text.lower()
    for markers, canonical_areas in groups:
        if not any(marker.lower() in lower_text for marker in markers):
            continue
        marker_pattern = "|".join(re.escape(marker) for marker in markers)
        match = re.search(
            rf"(?:{marker_pattern})[^.;]{{0,260}}?(?:mức|giá|cùng giá|cùng mức|là)\s*(\d{{1,3}}[.,]\d{{3}}|\d{{5,6}})",
            text,
            flags=re.IGNORECASE,
        )
        if not match:
            continue
        price = parse_price(match.group(1))
        if price is None:
            continue
        for area_name in canonical_areas:
            area = area_from_text(area_name)
            if not area:
                continue
            rows.append(
                {
                    "date": article_date.isoformat(),
                    "province": area["province"],
                    "area": area["area"],
                    "coffee_type": COFFEE_TYPE,
                    "price_vnd_per_kg": price,
                    "change_vnd_per_kg": None,
                    "source_name": source_name_for_url(source_url, default_source_name),
                    "source_url": source_url,
                }
            )
    return rows

def parse_article(url: str, html: str, start, end, default_source_name: str = "Bao Nong nghiep va Moi truong") -> tuple[list[dict[str, object]], str | None]:
    soup = BeautifulSoup(html, "html.parser")
    article_date = parse_date_from_url_or_text(url, soup.get_text(" ", strip=True)) or parse_date_from_meta(soup)
    if article_date is None:
        return [], "missing_date"
    if article_date < start or article_date > end:
        return [], "outside_range"
    rows = parse_table_rows(soup, article_date, url, default_source_name)
    if not rows:
        rows = parse_text_rows_enhanced(soup, article_date, url, default_source_name)
    return rows, None if rows else "no_price_rows"

# --- from price_crawler_discovery.py ---




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


def discover_sitemap_urls(config, start: date, end: date, headers: dict[str, str], max_sitemaps: int = 250) -> list[str]:
    seen_sitemaps: set[str] = set()
    seen_urls: set[str] = set(config.seed_urls)
    queue = [urljoin(config.base_url, item) for item in config.sitemap_candidates]

    while queue and len(seen_sitemaps) < max_sitemaps:
        sitemap_url = queue.pop(0)
        if sitemap_url in seen_sitemaps:
            continue
        seen_sitemaps.add(sitemap_url)
        try:
            response = requests.get(sitemap_url, headers=headers, timeout=20)
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


def discover_search_urls(config, start: date, end: date, headers: dict[str, str], pages_per_query: int = 4) -> list[str]:
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
                response = requests.get(url, headers=headers, timeout=20)
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
