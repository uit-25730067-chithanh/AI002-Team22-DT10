"""Async coffee price crawler for nongnghiepmoitruong.vn."""

from __future__ import annotations

from price_crawler_common import SiteConfig, run_site


CONFIG = SiteConfig(
    source_name="Nong Nghiep Moi Truong",
    base_url="https://nongnghiepmoitruong.vn/",
    sitemap_candidates=("sitemap.xml", "sitemap_index.xml"),
    url_keywords=("gia-ca-phe-hom-nay",),
    seed_urls=(
        "https://nongnghiepmoitruong.vn/gia-ca-phe-hom-nay-12-12-2022-tuan-qua-giam-300--500-d-kg-d339610.html",
        "https://nongnghiepmoitruong.vn/gia-ca-phe-hom-nay-7-3-2023-giam-nhe-mat-moc-48000-d-kg-d345345.html",
        "https://nongnghiepmoitruong.vn/gia-ca-phe-hom-nay-25-7-2025-thi-truong-tiep-tuc-tang-d764611.html",
    ),
    search_domain="nongnghiepmoitruong.vn",
)


if __name__ == "__main__":
    run_site(CONFIG)
