# Coffee Area Dataset Crawler

This folder builds an educational coffee-price dataset by local market area.
Each area keeps its own price series, weather series, and static soil feature.

## Setup

Install dependencies from the repository root:

```bash
pip install -r requirements.txt
```

## Run Order

```bash
python crawler/crawl_coffee_prices.py --start 2022-01-01 --end 2025-12-31
python crawler/crawl_weather_by_area.py --start 2022-01-01 --end 2025-12-31
python crawler/build_soil_profile.py
python crawler/build_area_datasets.py --freq weekly
python crawler/build_area_datasets.py --freq monthly
```

To run all site-specific price crawlers with a 20-minute budget per site:

```bash
python crawler/run_price_crawlers.py --per-site-timeout 1200 --stop-after-seconds 1140
```

Each site writes incremental source files under `data/raw/sources/`, then merges
into `data/raw/coffee_price_all_areas_daily_2022_2025.csv`.

Current site-specific crawlers:

- `crawler/crawl_price_vinanet.py`
- `crawler/crawl_price_congthuong.py`
- `crawler/crawl_price_nongnghiep.py`
- `crawler/crawl_price_kinhtedothi.py`

## Outputs

- `data/raw/coffee_price_<area>_daily_2022_2025.csv`
- `data/raw/weather_<area>_daily_2022_2025.csv`
- `data/raw/soil_profile_by_area.csv`
- `data/processed/weekly/coffee_environment_<area>_weekly_2022_2025.csv`
- `data/processed/monthly/coffee_environment_<area>_monthly_2022_2025.csv`

Processed price columns:

- `avg_price_vnd_per_kg`: model-ready price. Missing periods are filled.
- `observed_price_vnd_per_kg`: crawled price only. Blank means no direct price observation for that period.
- `price_observations`: number of crawled price rows used in that period.
- `price_fill_method`: `observed`, `province_proxy`, `interpolated_area`, `global_period_proxy`, `area_median`, or `global_median`.

If sitemap discovery misses articles, create a text file with one source URL per
line and pass it to the price crawler:

```bash
python crawler/crawl_coffee_prices.py --url-file data/raw/coffee_article_urls.txt
```
