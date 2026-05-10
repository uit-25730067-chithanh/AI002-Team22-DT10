"""Async coffee price crawler for kinhtedothi.vn."""

from __future__ import annotations

from price_crawler_common import SiteConfig, run_site


CONFIG = SiteConfig(
    source_name="Kinh Te Do Thi",
    base_url="https://kinhtedothi.vn/",
    sitemap_candidates=("sitemap.xml", "sitemap_index.xml"),
    url_keywords=("gia-ca-phe-hom-nay",),
    seed_urls=(
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-2-1-ca-phe-trong-nuoc-tang-cham-nong-dan-giu-hang-cho-thoi-co",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-1-2-du-bao-2022-vuot-dinh-nam-cu",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-1-10-xuat-khau-lao-doc-mat-1-600-1-800-dong-kg-trong-thang-9-2022.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-31-12-dong-usd-suy-yeu-khong-cuu-duoc-gia-ca-phe.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-1-1-ca-phe-duoc-hay-mat-trong-nam-2022",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-23-3-fed-tang-lai-suat-vang-tang-ca-phe-giam",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-8-5-nang-nong-ca-phe-co-the-dat-dinh-cuoi-2023",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-14-10-arabica-tang-manh-trong-nuoc-gan-64-000-dong-kg",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-11-12-nguyen-nhan-trong-nuoc-tang-nguoc-so-voi-the-gioi.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-14-12-nguyen-nhan-ca-phe-hom-nay-tiep-tuc-tang-manh.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-17-12-1-tuan-tang-soc-ca-phe-them-toi-6-000-dong-kg.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-1-2-tang-hon-11-000-dong-kg-trong-thang-dau-nam-2024.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-1-4-thang-3-2024-tang-15-000-dong-kg-co-noi-vuot-100-000-dong-kg",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-19-4-giai-ma-cu-quay-dau-giam-manh-cua-ca-phe",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-4-11-chuyen-gia-nhan-dinh-dien-bien-ca-phe-tuan-nay",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-29-12-robusta-giam-lien-2-tuan-cuoi-nam-2024",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-24-2-2025-nhan-dinh-tuan-nay-robusta-tang-hoac-arabica-giam.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-2-5-2025-nguyen-nhan-ca-phe-quay-xe-manh-ngay-dau-thang-5-2025.692315.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-15-5-2025-3-nguyen-nhan-khien-thi-truong-ca-phe-quay-xe-cuc-gat.704067.html",
        "https://kinhtedothi.vn/gia-ca-phe-hom-nay-26-5-2025-yeu-to-quan-trong-anh-huong-den-gia-ca-phe-tuan-nay.715145.html",
    ),
    search_domain="kinhtedothi.vn",
)


if __name__ == "__main__":
    run_site(CONFIG)
