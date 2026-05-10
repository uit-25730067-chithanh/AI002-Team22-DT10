"""Async coffee price crawler for vinanet.vn."""

from __future__ import annotations

from price_crawler_common import SiteConfig, run_site


CONFIG = SiteConfig(
    source_name="Vinanet",
    base_url="https://vinanet.vn/",
    sitemap_candidates=("sitemap.xml",),
    url_keywords=("bang-gia-ca-phe-trong-nuoc-va-the-gioi", "gia-ca-phe"),
    seed_urls=(
        "https://vinanet.vn/nong-san/bang-gia-ca-phe-trong-nuoc-va-the-gioi-ngay-7102024-790417.html",
        "https://vinanet.vn/nong-san/bang-gia-ca-phe-trong-nuoc-va-the-gioi-ngay-29102024-791362.html",
        "https://vinanet.vn/nong-san/bang-gia-ca-phe-trong-nuoc-va-the-gioi-ngay-12122024-792883.html",
        "https://vinanet.vn/nong-san/bang-gia-ca-phe-trong-nuoc-va-the-gioi-ngay-122025-795533.html",
        "https://vinanet.vn/nong-san/bang-gia-ca-phe-trong-nuoc-va-the-gioi-ngay-1522025-796134.html",
        "https://vinanet.vn/nong-san/bang-gia-ca-phe-trong-nuoc-va-the-gioi-ngay-2532025-797209.html",
    ),
    search_domain="vinanet.vn",
)


if __name__ == "__main__":
    run_site(CONFIG)
