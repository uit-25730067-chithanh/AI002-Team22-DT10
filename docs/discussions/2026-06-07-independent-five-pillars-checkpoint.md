# Checkpoint 5 trụ cột với dataset độc lập

Ngày cập nhật: 2026-06-07

## Phạm vi

- Không dùng dataset Phúc/Thịnh làm source-of-truth hiện tại.
- Dataset mới được Team 2 tự crawl, tự audit, tự build lại.
- Dải crawl: 2020-01 đến 2026-04 nếu nguồn có dữ liệu.
- Baseline model chính: dùng monthly 2022-01 đến 2026-04 vì độ phủ giá quan sát thật cao nhất và đủ dài để train/test.

## Dataset hiện tại

| Nhóm | File | Ghi chú |
| --- | --- | --- |
| Raw giá độc lập | `data/raw/independent/coffee_price_all_areas_daily_2020_2026.csv` | Gitignored, 6,306 dòng |
| Raw thời tiết độc lập | `data/raw/independent/weather_all_areas_daily_2020_2026.csv` | Gitignored, 27,744 dòng |
| Monthly full | `data/processed/monthly/coffee_environment_independent_all_areas_monthly_2020_2026.csv` | 912 dòng |
| Monthly baseline | `data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv` | 624 dòng |
| Weekly tham khảo | `data/processed/weekly/coffee_environment_independent_all_areas_weekly_2020_2026.csv` | 3,972 dòng |
| Ranking area | `data/processed/independent_area_real_price_data_ranking.csv` | Dùng audit area |

## Reliability

- Model: `RandomForestRegressor`.
- Experiment: `model/experiments/20260607_235428__rf_independent_monthly`.
- Split:
  - Train: đến 2024-12-31.
  - Test: 2025-01-01 đến 2025-12-31.
  - 2026-01 đến 2026-04 giữ làm freshness holdout, không trộn vào test mặc định.

| Metric | Value |
| --- | ---: |
| Train rows | 420 |
| Test rows | 144 |
| Feature count | 42 |
| MAE | 10,906.89 VND/kg |
| RMSE | 13,963.24 VND/kg |
| R2 | -0.3574 |

Kết luận Reliability: model độc lập tốt hơn baseline real-data cũ trong registry, nhưng R2 vẫn âm nên chỉ nên trình bày là baseline minh bạch/demo-safe, không nói là dự báo chính xác cao.

## Bias

Độ phủ giá quan sát thật theo tỉnh trong monthly baseline 2022-2026/04:

| Tỉnh | Dòng | Area | Dòng quan sát thật | Tỷ lệ |
| --- | ---: | ---: | ---: | ---: |
| Đắk Lắk | 156 | 3 | 146 | 93.59% |
| Đắk Nông | 104 | 2 | 90 | 86.54% |
| Gia Lai | 156 | 3 | 146 | 93.59% |
| Kon Tum | 52 | 1 | 52 | 100.00% |
| Lâm Đồng | 156 | 3 | 153 | 98.08% |

Area yếu nhất:

| Area | Tỉnh | Tỷ lệ quan sát thật | Dòng proxy/nội suy |
| --- | --- | ---: | ---: |
| Chư Prông | Gia Lai | 84.62% | 8 |
| Cư M'gar | Đắk Lắk | 84.62% | 8 |
| Gia Nghĩa | Đắk Nông | 84.62% | 8 |
| Đắk R'lấp | Đắk Nông | 88.46% | 6 |

Thiên lệch nguồn: raw giá có 6,293 dòng từ Nông Nghiệp Môi Trường và 13 dòng từ Công Thương. Đây là bias nguồn đáng kể, cần nói rõ dữ liệu là giá tham khảo public, không phải giao dịch chính thức.

## Robustness

Stress test chạy trên model độc lập:

- Báo cáo: `docs/discussions/robustness-stress-test.md`.
- JSON: `model/experiments/20260607_235428__rf_independent_monthly/stress/stress_results.json`.

| Scenario | MAE | RMSE | Nhận xét |
| --- | ---: | ---: | --- |
| Normal 2025 | 10,906.89 | 13,963.24 | Baseline |
| `price_crash` | 22,105.73 | 30,314.72 | MAE tăng 102.68% |
| `heat_wave` | 10,905.30 | 13,961.36 | Gần như không đổi |
| `both` | 22,108.76 | 30,319.94 | MAE tăng 102.70% |

Kết luận Robustness: model nhạy với shock giá vì phụ thuộc mạnh vào lag/rolling price; ít nhạy với nhiệt độ vì weather feature importance thấp. API/UI cần disclaimer khi thị trường biến động ngoài lịch sử train.

API smoke test ngày 2026-06-07:

| Endpoint / Case | Kết quả |
| --- | --- |
| `GET /health` | 200, `model_loaded=true` |
| `GET /model/info` | 200, model version `20260607_235428__rf_independent_monthly` |
| `POST /predict` Kon Tum | 200, dự báo 113,864.54 VND/kg |
| `POST /predict` Gia Nghĩa | 200, dự báo 113,945.57 VND/kg |
| `POST /predict` Di Linh | 200, dự báo 113,846.92 VND/kg |

## Social Impact

- Hệ thống chỉ hỗ trợ tham khảo, không thay thế tư vấn nông nghiệp hoặc quyết định bán hàng.
- Người dùng cần biết giá là public reference, có bias theo nguồn tin và khu vực.
- Khi demo, nên ưu tiên các area có dữ liệu tốt: Kon Tum, Buôn Hồ, Ea H'leo, Di Linh, Lâm Hà, Pleiku, Ia Grai, Bảo Lộc.
- Với area yếu hơn như Gia Nghĩa, Chư Prông, Cư M'gar, phải nói rõ dữ liệu có nhiều proxy/nội suy hơn.

## Transparency

Top feature importance của model độc lập:

| Feature | Importance |
| --- | ---: |
| `rolling_avg_7d` | 0.5046 |
| `lag_1d` | 0.4610 |
| `month_sin` | 0.0091 |
| `lag_7d` | 0.0090 |
| `month` | 0.0081 |
| `source_url_count` | 0.0020 |
| `price_observations` | 0.0017 |
| `month_cos` | 0.0014 |
| `quarter` | 0.0014 |
| `year` | 0.0009 |

Kết luận Transparency: dự báo chủ yếu dựa vào lịch sử giá gần nhất. Weather/soil có trong schema để giải thích bối cảnh, nhưng không phải driver chính của baseline hiện tại.

## Câu hỏi chưa giải quyết

- Có cần train thêm model phụ dùng cả 2026/01-04 để demo freshness không?
- Có cần gắn warning runtime theo area yếu ngay trong `/predict` không?
