# Real Data Audit - Team 2 Sơn

> **Archive note 2026-06-07:** Tài liệu này là audit lịch sử cho dataset cũ trước khi nhóm tách. Source-of-truth hiện tại là `docs/discussions/2026-06-07-independent-data-audit.md`.

**Ngày:** 2026-05-13
**Người:** Sơn
**Plan:** Local-only `plans/team2-real-data-model-week/` (gitignored)
**Phạm vi:** Phase 1 - Real Data Audit, hỗ trợ Phase 4 - Five Pillars Evidence
**PR #9 status:** Merged 2026-05-14 local time, merge commit `e50e8a691c8aac89edce058fbf41a3cd70af913a`

## Kết luận nhanh

Team 2 nên dùng `data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv` làm dataset baseline chính.

Lý do:

- Monthly ổn định hơn weekly cho bài AI cơ bản.
- Monthly có tỷ lệ giá observed cao hơn: **86.5%** so với weekly **72.7%**.
- Train/test split theo năm đã khớp với yêu cầu môn: train 2022-2024, test 2025.
- Weekly vẫn hữu ích để phân tích phụ, nhưng nhiễu và proxy nhiều hơn.

## Dataset được audit

| Dataset           |  Rows | Columns | Period             | Observed price rows | Observed rate | Kết luận                |
| ----------------- | ----: | ------: | ------------------ | ------------------: | ------------: | ----------------------- |
| Monthly all areas |   576 |      16 | 2022-01 -> 2025-12 |                 498 |         86.5% | Chọn làm baseline chính |
| Weekly all areas  | 2,520 |      16 | 2022-01 -> 2025-12 |               1,831 |         72.7% | Optional analysis       |

## Schema chính

Target chính cho baseline là `avg_price_vnd_per_kg`.

`observed_price_vnd_per_kg` không nên dùng làm target chính vì có nhiều dòng thiếu. Cột này dùng để đánh giá độ tin cậy dữ liệu giá.

Các nhóm feature phù hợp:

| Nhóm             | Columns                                                                                               |
| ---------------- | ----------------------------------------------------------------------------------------------------- |
| Price confidence | `price_observations`, `price_fill_method`                                                             |
| Weather          | `avg_temperature_c`, `avg_humidity_percent`, `total_rainfall_mm`                                      |
| Soil             | `avg_soil_moisture_0_7cm`, `dominant_soil_type`, `soil_score`, `soil_data_confidence`                 |
| Location         | `province`, `area`                                                                                    |
| Time             | `period_start`, `period_end`, feature engineered `year`, `month`, `quarter`, `month_sin`, `month_cos` |

## Missing values

| Dataset | Missing column chính        | Missing rows | Ghi chú                                                    |
| ------- | --------------------------- | -----------: | ---------------------------------------------------------- |
| Monthly | `observed_price_vnd_per_kg` |           78 | Không thiếu target train vì `avg_price_vnd_per_kg` đã fill |
| Weekly  | `observed_price_vnd_per_kg` |          689 | Weekly phụ thuộc proxy/interpolation nhiều hơn monthly     |

Các cột môi trường, đất, location và `avg_price_vnd_per_kg` không thiếu trong bản processed đã audit.

## Price fill method

### Monthly

| Fill method         | Rows |  Rate |
| ------------------- | ---: | ----: |
| `observed`          |  498 | 86.5% |
| `province_proxy`    |   58 | 10.1% |
| `interpolated_area` |   20 |  3.5% |

### Weekly

| Fill method         |  Rows |  Rate |
| ------------------- | ----: | ----: |
| `observed`          | 1,831 | 72.7% |
| `interpolated_area` |   371 | 14.7% |
| `province_proxy`    |   318 | 12.6% |

## Độ phủ area-row theo tỉnh

Lưu ý: bảng dưới tính theo số dòng area-period có giá observed, nên khác với `data/processed/AREA_REAL_PRICE_DATA_RANKING.md` nơi độ phủ tỉnh được tính là một tỉnh có observed nếu ít nhất một area trong tỉnh có giá thật trong kỳ.

### Độ phủ observed hàng tháng

| Province | Observed | Total rows | Coverage | Ghi chú                |
| -------- | -------: | ---------: | -------: | ---------------------- |
| Lam Dong |      144 |        144 |   100.0% | Mạnh                   |
| Kon Tum  |       48 |         48 |   100.0% | Mạnh nhưng ít area hơn |
| Dak Lak  |      134 |        144 |    93.1% | Tốt                    |
| Gia Lai  |      134 |        144 |    93.1% | Tốt                    |
| Dak Nong |       38 |         96 |    39.6% | Yếu, cần cảnh báo bias |

### Độ phủ observed hàng tuần

| Province | Observed | Total rows | Coverage | Ghi chú                   |
| -------- | -------: | ---------: | -------: | ------------------------- |
| Lam Dong |      592 |        630 |    94.0% | Mạnh                      |
| Kon Tum  |      194 |        210 |    92.4% | Mạnh nhưng ít area hơn    |
| Dak Lak  |      482 |        630 |    76.5% | Đạt mức dùng được         |
| Gia Lai  |      475 |        630 |    75.4% | Đạt mức dùng được         |
| Dak Nong |       88 |        420 |    21.0% | Yếu, không nên demo chính |

## Khu vực nên ưu tiên và cần cảnh báo

Ưu tiên demo/report:

- **Di Linh, Lam Dong:** độ phủ mạnh nhất theo xếp hạng data thật.
- **Ea H'leo, Dak Lak:** phù hợp để train/demo.
- **Buon Ho, Dak Lak:** phù hợp để train/demo.
- **Bao Loc/Lam Ha, Lam Dong:** phù hợp để phân tích phụ.
- **Pleiku, Gia Lai:** dùng được nhưng thấp hơn nhóm đầu.

Cần cảnh báo:

- **Dak Nong:** độ phủ thấp hơn các tỉnh còn lại.
- **Dak R'lap:** không có observed price riêng, dữ liệu hiện là fill/proxy.
- Không áp dụng kết luận bừa cho vùng ngoài Tây Nguyên.

## Liên hệ với PR #9 của Thanh

PR #9 đã merge phần Thanh:

- Phase 2: preprocess schema migration.
- Phase 3: Random Forest baseline.
- Phase 5: API handoff.

Sau PR #14, `model/best_model/metadata.json` đã được đồng bộ lại về experiment real-data có MAE thấp nhất trong nhóm `rf_real_*`. Việc còn lại của Team 2 là chạy API smoke test, xác nhận response mẫu, và chạy stress test trước tuần integration.

Số liệu model chính từ PR #9:

| Metric        |                              Value |
| ------------- | ---------------------------------: |
| Experiment    | `20260513_155830__rf_real_monthly` |
| Train size    |                                432 |
| Test size     |                                144 |
| MAE           |                      13,552 VND/kg |
| RMSE          |                      16,754 VND/kg |
| R²            |                            -0.9044 |
| Feature count |                                 41 |

R² âm là tín hiệu cần ghi thẳng trong báo cáo: phân phối giá 2025 lệch mạnh so với giai đoạn train 2022-2024, nên baseline hiện dùng để minh họa pipeline đáng tin cậy, chưa phải model final để ra quyết định tài chính.

## Risk notes cho 5 trụ cột

| Trụ cột       | Evidence / Risk                                                                  |
| ------------- | -------------------------------------------------------------------------------- |
| Reliability   | Có split temporal và metrics thật; R² âm nên phải report limitation              |
| Bias          | Độ phủ không đều, Dak Nong yếu nhất                                              |
| Robustness    | Processed data không thiếu feature chính; cần giữ validation API và NaN handling |
| Social Impact | Dự báo chỉ tham khảo cho nông dân, không thay thế quyết định bán/mua             |
| Transparency  | Feature importance cho thấy model phụ thuộc lớn vào lag/rolling price context    |

## Definition of Done Phase 1

- [x] Có kết luận dataset chính: monthly all-areas.
- [x] Có thống kê rows/columns/missing/fill-method.
- [x] Có ghi chú bias theo province/area.
- [x] Có số liệu đầu vào cho Phase 4 five pillars evidence.
