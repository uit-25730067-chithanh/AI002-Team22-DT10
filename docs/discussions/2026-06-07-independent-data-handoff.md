# Bàn giao dataset và model độc lập

Ngày bàn giao: 2026-06-08 theo artifact validation.

## Kết luận ngắn

Team 2 đã tự crawl, audit, tạo dataset và train lại model độc lập. Không dùng dataset Phúc/Thịnh làm source-of-truth hiện tại.

## File chính

| Nhóm | File |
| --- | --- |
| Monthly baseline | `data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv` |
| Monthly full | `data/processed/monthly/coffee_environment_independent_all_areas_monthly_2020_2026.csv` |
| Weekly reference | `data/processed/weekly/coffee_environment_independent_all_areas_weekly_2020_2026.csv` |
| Area ranking | `data/processed/independent_area_real_price_data_ranking.csv` |
| Model experiment | `model/experiments/20260607_235428__rf_independent_monthly` |
| Best model | `model/best_model/model.pkl` |
| 5 Pillars checkpoint | `docs/discussions/2026-06-07-independent-five-pillars-checkpoint.md` |

## Lệnh rerun tối thiểu

```bash
python3 -m pytest tests/ai-tests -q
python3 model/train_rf.py --data data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv --tag rf_independent_monthly
python3 model/stress_test.py --data data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv --model model/best_model/model.pkl --exp-dir model/experiments/20260607_235428__rf_independent_monthly --also-docs
```

Nếu chỉ muốn train kiểm tra mà không đổi best model:

```bash
python3 model/train_rf.py --data data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv --tag rf_independent_monthly_validation --no-promote
```

## Số liệu cần nói khi báo cáo

- Dataset baseline: 624 dòng, 12 area, 2022-01 đến 2026-04.
- Tỷ lệ giá quan sát thật: 94.07%.
- Split: train đến 2024-12-31, test năm 2025, giữ 2026-01 đến 2026-04 làm freshness holdout.
- Model: Random Forest, MAE 10,906.89 VND/kg, RMSE 13,963.24 VND/kg, R2 -0.3574.
- Top features: `rolling_avg_7d` 0.5046, `lag_1d` 0.4610.
- Stress test: shock giá làm MAE tăng khoảng 102.7%; heat wave gần như không đổi.

## Area nên demo

- Nên ưu tiên: Kon Tum, Di Linh, Ea H'leo, Buôn Hồ, Bảo Lộc, Lâm Hà, Pleiku, Ia Grai.
- Cần cảnh báo kỹ hơn: Gia Nghĩa, Chư Prông, Cư M'gar, Đắk R'lấp.

## Không nên claim

- Không nói model dự báo chính xác cao; R2 vẫn âm.
- Không nói weather/soil là driver chính; feature importance hiện rất thấp.
- Không nói dữ liệu là giao dịch chính thức; đây là public reference dataset.
- Không nói đang dùng dataset Phúc/Thịnh làm nguồn chính.

## Câu hỏi chưa giải quyết

- Có cần thêm warning runtime theo area yếu trong API không?
- Có cần train model phụ cập nhật đến 2026-04 để demo freshness không?
