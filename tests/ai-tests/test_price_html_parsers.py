from __future__ import annotations

import crawler.price_crawler_common as price_crawler_common

from datetime import date

from bs4 import BeautifulSoup

from crawler.price_crawler_common import parse_date_from_meta, parse_date_from_url_or_text


def test_parse_date_from_url_or_text() -> None:
    url = "https://example.com/gia-ca-phe-hom-nay-12-12-2022-demo.html"
    assert parse_date_from_url_or_text(url, "") == date(2022, 12, 12)

    fallback_url = "https://example.com/article.html"
    fallback_text = "Bài viết đăng ngày 13/12/2022 về giá cà phê"
    assert parse_date_from_url_or_text(fallback_url, fallback_text) == date(2022, 12, 13)


def test_parse_date_from_meta() -> None:
    soup = BeautifulSoup(
        """
        <html>
          <head><meta property="article:published_time" content="2022-12-14T08:00:00+07:00"></head>
          <body></body>
        </html>
        """,
        "html.parser",
    )
    assert parse_date_from_meta(soup) == date(2022, 12, 14)


def test_parse_article_table_row() -> None:
    html = """
    <html>
      <head><meta property="article:published_time" content="2022-12-12T08:00:00+07:00"></head>
      <body>
        <table>
          <tr><td>Di Linh</td><td>40.500</td><td>+ 500</td></tr>
        </table>
      </body>
    </html>
    """
    rows, error = price_crawler_common.parse_article(
        "https://example.com/gia-ca-phe-hom-nay-12-12-2022-demo.html",
        html,
        date(2022, 1, 1),
        date(2022, 12, 31),
    )
    assert error is None
    assert len(rows) == 1
    row = rows[0]
    assert row["date"] == "2022-12-12"
    assert row["area"] == "Di Linh"
    assert row["price_vnd_per_kg"] == 40500
