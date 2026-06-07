# Kết quả model baseline từ dataset độc lập

Ngày chạy: 2026-06-07

## Quyết định baseline

- Dataset nguồn: `data/processed/monthly/coffee_environment_independent_all_areas_monthly_2020_2026.csv`.
- Dataset train đã lọc: `data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv`.
- Dải dùng cho baseline chính: 2022-01 đến 2026-04.
- Lý do chọn dải này: 2022-2026/04 có 624 dòng monthly, 12 area, 587 dòng giá quan sát thật, tỷ lệ quan sát thật 94.07%.
- Không dùng dải 2020-2026/04 làm baseline chính vì 2020-2021 yếu hơn và có nhiều dòng phải nội suy.

## Split

- Train: các dòng đến 2024-12-31.
- Test: 2025-01-01 đến 2025-12-31.
- Holdout freshness: 2026-01 đến 2026-04, không đưa vào test mặc định.
- Mục tiêu: tránh rò rỉ thời gian khi crawl thêm data 2026.

## Lệnh chạy

```bash
python3 model/train_rf.py \
  --data data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv \
  --tag rf_independent_monthly
```

## Artifact

- Experiment: `model/experiments/20260607_235428__rf_independent_monthly`.
- Model: `model/experiments/20260607_235428__rf_independent_monthly/rf_baseline.pkl`.
- Best model API/demo: `model/best_model/model.pkl`.
- Best metadata: `model/best_model/metadata.json`.

## Metrics

| Metric | Value |
| --- | ---: |
| Train rows | 420 |
| Test rows | 144 |
| Feature count | 42 |
| MAE | 10,906.89 VND/kg |
| RMSE | 13,963.24 VND/kg |
| R2 | -0.3574 |

So với `rf_real_monthly` cũ tốt nhất trong registry:

| Experiment | MAE | RMSE | R2 |
| --- | ---: | ---: | ---: |
| `20260513_155759__rf_real_monthly` | 13,551.71 | 16,754.40 | -0.9044 |
| `20260607_235428__rf_independent_monthly` | 10,906.89 | 13,963.24 | -0.3574 |

Kết luận: model độc lập tốt hơn baseline real cũ theo MAE/RMSE/R2, nhưng R2 vẫn âm. Báo cáo phải nói rõ đây là baseline có thể demo, chưa phải model dự báo mạnh.

## Top feature importance

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

Nhận xét: model đang phụ thuộc rất mạnh vào lag/rolling price. Weather/soil hiện đóng góp rất thấp. Khi bảo vệ, nên trình bày model là baseline minh bạch theo chuỗi thời gian, không phóng đại tác động thời tiết.

## Quyết định promote

Đã promote `rf_independent_monthly` vào `model/best_model/` có chủ đích để API/demo dùng model không phụ thuộc data Phúc/Thịnh.

Sửa kèm theo: `model/train_rf.py` chọn best model theo scope `rf_independent` khi tag bắt đầu bằng `rf_independent`, không bị `rf_real` cũ lấn át.

## Rủi ro còn lại

- Giá nguồn độc lập vẫn lệch mạnh về một nguồn báo.
- 2025 là năm giá biến động mạnh nên test khó, R2 âm.
- 2026/01-04 mới chỉ giữ freshness holdout, chưa train model phụ.

## Câu hỏi chưa giải quyết

- Có cần thêm model phụ train đến 2026/04 để demo riêng không?
- Có cần đổi API area enum nếu Phase 6 phát hiện area nào nên thay bằng area tốt hơn không?
