"""Async coffee price crawler for congthuong.vn."""

from __future__ import annotations

from price_crawler_common import SiteConfig, run_site


CONFIG = SiteConfig(
    source_name="Cong Thuong",
    base_url="https://congthuong.vn/",
    sitemap_candidates=("sitemap.xml", "sitemap_index.xml"),
    url_keywords=("gia-ca-phe-hom-nay",),
    seed_urls=(
        "https://congthuong.vn/gia-ca-phe-hom-nay-173-gia-ca-phe-trong-nuoc-giam-200-dongkg-246664.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-252-gia-ca-phe-trong-nuoc-giam-500-dongkg-243835.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-262-gia-ca-phe-trong-nuoc-giam-200-dongkg-243939.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-2862023-gia-ca-phe-trong-nuoc-tang-den-700-dongkg-259845.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-ngay-1272023-gia-ca-phe-trong-nuoc-giam-toi-700-dongkg-261831.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-ngay-1372023-gia-ca-phe-trong-nuoc-giam-nhe-261957.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-ngay-2172023-gia-ca-phe-trong-nuoc-tang-1300-dongkg-263121.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-3072023-ca-phe-trong-nuoc-giam-1500-dongkg-264416.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-ngay-2792023-gia-ca-phe-trong-nuoc-giam-400-dongkg-274787.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-ngay-23122023-gia-ca-phe-trong-nuoc-quay-dau-tang-manh-293623.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-ngay-28122023-gia-ca-phe-trong-nuoc-tang-nhe-294476.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-ngay-29122023-gia-ca-phe-trong-nuoc-duy-tri-muc-tang-cao-294758.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-2762024-gia-ca-phe-giam-manh-o-ca-trong-nuoc-va-the-gioi-328398.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-2672024-gia-ca-phe-trong-nuoc-noi-tiep-da-giam-manh-334853.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-1282024-giao-dich-duoi-moc-120000-dongkg-338392.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-29102024-trong-nuoc-giam-nhe-the-gioi-tang-tro-lai-355334.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-2112024-tiep-tuc-lao-doc-trong-nuoc-giam-1500-dongkg-356248.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-5122024-gia-ca-phe-trong-nuoc-tiep-da-giam-362520.html",
        "https://congthuong.vn/gia-ca-phe-hom-nay-12122024-gia-ca-phe-trong-nuoc-tang-nhe-363788.html",
    ),
    search_domain="congthuong.vn",
)


if __name__ == "__main__":
    run_site(CONFIG)
