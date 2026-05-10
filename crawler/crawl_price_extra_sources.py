"""Async coffee price crawler for additional Vietnamese news sources."""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime
from pathlib import Path

from price_crawler_common import SiteConfig, crawl_site_async


EXTRA_SOURCES = [
    SiteConfig(
        source_name="Bao Nghe An",
        base_url="https://baonghean.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe-hom-nay",),
        seed_urls=(
            "https://baonghean.vn/gia-ca-phe-hom-nay-17-9-2024-tang-khong-diem-dung-lien-tuc-pha-dinh-10280505.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-20-9-2024-arabica-va-robusta-cung-giam-nhe-10280744.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-26-9-2024-tang-giam-trai-chieu-tu-100-dong-kg-10281168.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-25-10-2024-tang-nhe-200-dong-kg-10283155.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-4-11-2024-giam-manh-gan-3-500-dong-kg-so-voi-tuan-truoc-10283944.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-17-11-2024-cuoi-tuan-giam-nhe-200-dong-10284942.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-2-12-2025-giam-manh-cong-hai-ca-phe-tang-10313398.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-6-12-2025-tang-nhe-tro-lai-10313990.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-7-12-2025-chot-tuan-khong-doi-10314105.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-12-12-2025-giu-vung-da-tang-nhe-10314881.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-17-12-2025-tiep-tuc-giam-sau-nong-dan-chiu-lo-10315432.html",
            "https://baonghean.vn/gia-ca-phe-hom-nay-25-12-2025-tang-manh-do-nong-dan-han-che-ban-ra-10316824.html",
        ),
        search_domain="baonghean.vn",
    ),
    SiteConfig(
        source_name="Bao Da Nang",
        base_url="https://baodanang.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe-hom-nay",),
        seed_urls=(
            "https://baodanang.vn/gia-ca-phe-hom-nay-3-12-2025-the-gioi-giam-sau-do-ap-luc-thu-hoach-3312412.html",
            "https://baodanang.vn/gia-ca-phe-hom-nay-15-12-2025-giam-sau-thi-truong-chiu-ap-luc-nguon-cung-3314939.html",
        ),
        search_domain="baodanang.vn",
    ),
    SiteConfig(
        source_name="VnBusiness",
        base_url="https://vnbusiness.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe", "ca-phe"),
        seed_urls=(
            "https://vnbusiness.vn/ca-phe-giu-muc-gia-72200-dongkg.html",
            "https://vnbusiness.vn/thi-truong/gia-ca-phe-trong-nuoc-thu-mua-cao-nhat-79-200-dong-kg-1098167.html",
            "https://vnbusiness.vn/thi-truong/tang-den-4-000-dong-kg-ca-phe-lay-lai-moc-100-000-dong-kg-1099703.html",
            "https://vnbusiness.vn/ca-phe-giu-muc-122700-dongkg-ton-kho-can-kiet.html",
            "https://vnbusiness.vn/di-ngang-o-vung-130000-130700-dongkg-du-bao-gia-ca-phe-tiep-tuc-tang.html",
            "https://vnbusiness.vn/cho-doi-tin-hieu-thi-truong-ca-phe-giu-muc-125200-dongkg.html",
            "https://vnbusiness.vn/tang-nhe-500-dongkg-gia-ca-phe-cham-moc-112500-dongkg.html",
            "https://vnbusiness.vn/thi-truong/ca-phe-neo-gia-cao-sat-nam-moi-thi-truong-nin-tho-cho-nhip-but-pha-2026-1111831.html",
        ),
        search_domain="vnbusiness.vn",
    ),
    SiteConfig(
        source_name="VietBao",
        base_url="https://vietbao.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe", "nong-san"),
        seed_urls=("https://vietbao.vn/ban-tin-nong-san-hom-nay-12-6-gia-ca-phe-ho-tieu-tiep-tuc-giam-546749.html",),
        search_domain="vietbao.vn",
    ),
    SiteConfig(
        source_name="HomeUp",
        base_url="https://homeup.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe-hom-nay",),
        seed_urls=(
            "https://homeup.vn/tin-tuc/gia-ca-phe-hom-nay-2911-ca-phe-tiep-tuc-tang-thiet-lap-dinh-lich-su-moi-p4931",
            "https://homeup.vn/tin-tuc/gia-ca-phe-hom-nay-13102025-dao-dong-113000-114000-dongkg-huong-tang-kho-but-pha-p3954",
        ),
        search_domain="homeup.vn",
    ),
    SiteConfig(
        source_name="Banker",
        base_url="https://www.banker.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe-hom-nay",),
        seed_urls=("https://www.banker.vn/gia-ca-phe-hom-nay-14-12-2025-lui-sat-ve-moc-100-000-dong-kg",),
        search_domain="banker.vn",
    ),
    SiteConfig(
        source_name="Bao Moi",
        base_url="https://baomoi.com/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe-hom-nay",),
        seed_urls=(
            "https://baomoi.com/gia-ca-phe-hom-nay-17-12-2025-tiep-tuc-giam-sau-nong-dan-chiu-lo-c54027733.epi",
            "https://baomoi.com/gia-ca-phe-hom-nay-12-12-2025-dao-dong-quanh-moc-100-000-dong-kg-c53990815.epi",
        ),
        search_domain="baomoi.com",
    ),
    SiteConfig(
        source_name="Kamereo",
        base_url="https://kamereo.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe-hom-nay",),
        seed_urls=("https://kamereo.vn/blog/vi/gia-ca-phe-hom-nay/",),
        search_domain="kamereo.vn",
    ),
    SiteConfig(
        source_name="Kinh Te Moi Truong",
        base_url="https://kinhtemoitruong.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe-hom-nay",),
        seed_urls=("https://kinhtemoitruong.vn/gia-ca-phe-hom-nay-2912-tien-sat-moc-100000-dongkg-104966.html",),
        search_domain="kinhtemoitruong.vn",
    ),
    SiteConfig(
        source_name="Thuong Hieu Cong Luan",
        base_url="https://thuonghieucongluan.com.vn/",
        sitemap_candidates=("sitemap.xml",),
        url_keywords=("gia-ca-phe",),
        seed_urls=("https://thuonghieucongluan.com.vn/2pdf/gia-ca-phe-ngay-16-7-tang-giam-khong-dong-nhat-tai-thi-truong-the-gioi/228419",),
        search_domain="thuonghieucongluan.com.vn",
    ),
]


async def main_async() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2022-01-01")
    parser.add_argument("--end", default="2025-12-31")
    parser.add_argument("--output-dir", default="data/raw/sources")
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--max-urls-per-site", type=int, default=250)
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--flush-every", type=int, default=20)
    parser.add_argument("--stop-after-seconds", type=int, default=1140)
    args = parser.parse_args()

    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    end = datetime.strptime(args.end, "%Y-%m-%d").date()
    for config in EXTRA_SOURCES:
        await crawl_site_async(
            config=config,
            start=start,
            end=end,
            output_dir=Path(args.output_dir),
            raw_dir=Path(args.raw_dir),
            max_urls=args.max_urls_per_site,
            concurrency=args.concurrency,
            flush_every=args.flush_every,
            stop_after_seconds=args.stop_after_seconds,
        )


if __name__ == "__main__":
    asyncio.run(main_async())
