# Independent Crawl Summary - Team 2

**Ngày:** 2026-06-07  
**Phase:** Independent Coffee Data Rebuild - Phase 3  
**Trạng thái:** Raw crawl độc lập đã có dữ liệu giá và thời tiết để chuyển sang build processed dataset.

## Quyết định thực thi

- Không dùng lại dataset Phúc/Thịnh.
- Dữ liệu giá được crawl lại vào `data/raw/independent/`.
- Dữ liệu weather được lấy lại từ Open-Meteo cho `2020-01-01` đến `2026-04-30`.
- Old dataset chỉ dùng để so sánh ở Phase 4.

## Output chính

| File | Rows | Ghi chú |
| --- | ---: | --- |
| `data/raw/independent/coffee_price_all_areas_daily_2020_2026.csv` | 6,306 | Raw observed price rows |
| `data/raw/independent/weather_all_areas_daily_2020_2026.csv` | 27,744 | 12 areas x 2,312 days |
| `tmp/independent-price-crawl-smoke.log` | - | Smoke crawl log |
| `tmp/independent-price-crawl-full.log` | - | Full seed-set crawl log |
| `tmp/independent-weather-crawl.log` | - | Open-Meteo crawl log |

## Price crawl result

| Source | Rows | Status |
| --- | ---: | --- |
| Cong Thuong | 13 | Parsed |
| Nong Nghiep Moi Truong | 6,293 | Parsed, dominant source |
| Kinh Te Do Thi | 0 | Timeout, error recorded |
| Vinanet | 0 | No parser rows from selected seeds, errors recorded |

Raw price validation:

- Required columns: pass.
- Date range: pass, `2020-06-10` to `2026-04-13`.
- Duplicate observed rows: `0`.
- Source URL for observed rows: pass.
- Price range sanity: pass.

## Weather crawl result

Open-Meteo result:

- 12/12 areas completed.
- Date range: `2020-01-01` to `2026-04-30`.
- Each area has `2,312` daily rows.
- Combined rows: `27,744`.

During first run, Open-Meteo returned HTTP 429 after 10 areas. The crawler was updated with retry/backoff and `--reuse-existing`, then rerun completed all areas.

## Known limitations

- Full discovery through sitemap/search can hang on some sources. Phase 3 therefore used full manifest seed-set crawl as safe fallback.
- Kinh Te Do Thi timed out; keep error evidence and revisit parser/network later if Phase 4 shows data gaps.
- Vinanet seeds returned no parsed rows; keep as benchmark/source candidate, not main source.
- Current raw price is heavily dominated by Nong Nghiep Moi Truong. Phase 4 must audit province/area distribution before selecting baseline range.

## Commands used

```bash
python3 crawler/run_independent_price_crawlers.py --seed-only --max-urls 5 --per-site-timeout 45 --stop-after-seconds 45 --concurrency 2 --flush-every 5 > tmp/independent-price-crawl-smoke.log 2>&1
python3 crawler/run_independent_price_crawlers.py --seed-only --per-site-timeout 90 --stop-after-seconds 80 --concurrency 4 --flush-every 25 > tmp/independent-price-crawl-full.log 2>&1
python3 crawler/crawl_weather_by_area.py --independent --reuse-existing --sleep 1 --retries 4 --retry-sleep 10 > tmp/independent-weather-crawl.log 2>&1
```

## Next

Phase 4 build processed weekly/monthly datasets từ raw independent, sau đó audit độ phủ dữ liệu theo province/area.

## Unresolved Questions

- Có cần đầu tư sửa Kinh Te Do Thi/Vinanet ngay không, hay đợi Phase 4 audit quyết định dựa trên lỗ hổng thực tế?
