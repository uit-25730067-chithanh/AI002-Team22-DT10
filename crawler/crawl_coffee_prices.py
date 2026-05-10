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

from coffee_areas import AREA_BY_NORMALIZED, AREAS, COFFEE_TYPE, normalize_name, slugify


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


def parse_price(value: str) -> int | None:
    value = value.replace("\xa0", " ").strip()
    match = re.search(r"(\d{1,3}(?:[.,]\d{3})+|\d{4,6})", value)
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


def source_name_for_url(url: str) -> str:
    if "vicofa.org.vn" in url:
        return "VICOFA"
    if "chogia.vn" in url:
        return "Cho Gia"
    return SOURCE_NAME


def parse_table_rows(soup: BeautifulSoup, article_date: date, source_url: str) -> list[dict[str, object]]:
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
                    "source_name": source_name_for_url(source_url),
                    "source_url": source_url,
                }
            )
    return rows


def parse_text_rows(soup: BeautifulSoup, article_date: date, source_url: str) -> list[dict[str, object]]:
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
                    "source_name": source_name_for_url(source_url),
                    "source_url": source_url,
                }
            )
            break
    return rows


def parse_text_rows_enhanced(soup: BeautifulSoup, article_date: date, source_url: str) -> list[dict[str, object]]:
    text = soup.get_text("\n", strip=True)
    compact_text = re.sub(r"\s+", " ", text)
    rows = parse_text_rows(soup, article_date, source_url)
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
                    "source_name": source_name_for_url(source_url),
                    "source_url": source_url,
                }
            )
            break
    rows.extend(parse_grouped_area_text(compact_text, article_date, source_url))
    unique: dict[tuple[str, str, str], dict[str, object]] = {}
    for row in rows:
        unique[(str(row["date"]), str(row["province"]), str(row["area"]))] = row
    return list(unique.values())


def parse_grouped_area_text(text: str, article_date: date, source_url: str) -> list[dict[str, object]]:
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
                    "source_name": source_name_for_url(source_url),
                    "source_url": source_url,
                }
            )
    return rows


def fetch_url(url: str, sleep_seconds: float) -> str:
    time.sleep(sleep_seconds)
    response = requests.get(url, headers=HEADERS, timeout=25)
    response.raise_for_status()
    return response.text


def parse_article(url: str, html: str, start: date, end: date) -> tuple[list[dict[str, object]], str | None]:
    soup = BeautifulSoup(html, "html.parser")
    article_date = parse_date_from_url_or_text(url, soup.get_text(" ", strip=True)) or parse_date_from_meta(soup)
    if article_date is None:
        return [], "missing_date"
    if article_date < start or article_date > end:
        return [], "outside_range"
    rows = parse_table_rows(soup, article_date, url)
    if not rows:
        rows = parse_text_rows_enhanced(soup, article_date, url)
    return rows, None if rows else "no_price_rows"


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
            parsed_rows, error = parse_article(url, html, start, end)
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
