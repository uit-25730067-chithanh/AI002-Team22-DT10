# Data Contract - Team 2 Independent Coffee Dataset

**Ngày:** 2026-06-07  
**Trạng thái:** Phase 1 contract  
**Owner:** Thanh + Sơn  

## Quyết định

Team 2 sẽ tự crawl và audit lại dataset cà phê. Không dùng lại dataset do Phúc/Thịnh chuẩn bị. Có thể crawl cùng nguồn public, nhưng output phải được tạo lại độc lập.

Dataset mới là **public reference dataset**, không phải dữ liệu giao dịch chính thức.

## Phạm vi ngày

| Mục | Giá trị |
| --- | --- |
| Raw crawl start | `2020-01-01` |
| Raw crawl end | `2026-04-30` |
| Baseline range | Chọn sau audit |
| Fallback an toàn | Nếu 2020-2021 yếu, dùng 2022-2026/04 |

## Namespace dữ liệu

Raw data độc lập đặt trong:

```text
data/raw/independent/
```

Processed data độc lập phải có `independent` trong filename:

```text
data/processed/monthly/coffee_environment_independent_all_areas_monthly_2020_2026.csv
data/processed/weekly/coffee_environment_independent_all_areas_weekly_2020_2026.csv
```

Không overwrite dataset cũ:

```text
data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv
data/processed/weekly/coffee_environment_all_areas_weekly_2022_2025.csv
```

Dataset cũ chỉ dùng để so sánh độ phủ dữ liệu, phải label là `old_dataset`.

## Schema processed tối thiểu

Các cột bắt buộc giữ tương thích model hiện tại:

| Nhóm | Cột |
| --- | --- |
| Time | `period_start`, `period_end` |
| Location | `province`, `area` |
| Coffee | `coffee_type`, `avg_price_vnd_per_kg`, `observed_price_vnd_per_kg`, `price_observations`, `price_fill_method` |
| Weather | `avg_temperature_c`, `avg_humidity_percent`, `total_rainfall_mm`, `avg_soil_moisture_0_7cm` |
| Soil | `dominant_soil_type`, `soil_score`, `soil_data_confidence` |

Cột evidence nên có nếu builder làm được gọn:

- `source_url_count`
- `source_names`

## Source policy

Nguồn giá ưu tiên:

- Công Thương
- Nông Nghiệp Môi Trường
- Kinh Tế Đô Thị
- Vinanet

Weather source:

- Open-Meteo Historical Weather API.

World Bank Pink Sheet chỉ dùng làm benchmark xu hướng global robusta, không dùng làm target nội địa.

## Area policy

Ban đầu dùng area list hiện tại trong `crawler/coffee_areas.py`.

Sau audit, được thay area yếu bằng area khác nếu dữ liệu tốt hơn. Mọi thay đổi area phải ghi rõ:

- Area cũ.
- Area mới.
- Tỉnh.
- Lý do thay.
- Tác động API/frontend.

## Liên hệ 5 trụ cột

| Trụ cột | Data requirement |
| --- | --- |
| Reliability | Có metrics, split thời gian, audit data completeness |
| Bias | Có so sánh tỉnh/area, ghi rõ vùng yếu |
| Robustness | Có missing/fill method, parser errors, validation |
| Social Impact | Có disclaimer public reference, không khuyên quyết định tài chính tuyệt đối |
| Transparency | Có source provenance và feature importance |

## Next

Phase 2 viết parser fixtures và data quality tests trước khi live crawl.
