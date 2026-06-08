# Stress Test Report — Robustness Pillar

**Date:** 2026-06-08 00:46:11
**Model:** model/best_model/model.pkl
**Dataset:** data/processed/monthly/coffee_environment_all_areas_monthly_2020_2026.csv
**Experiment:** 20260608_004601__rf_monthly_baseline

## Baseline (Normal Test Set - 2025)

- MAE:  14,474 VND/kg
- RMSE: 17,874 VND/kg

## Black Swan Scenarios (Gây nhiễu tập Test 2025)

### price_crash

- MAE:  24,538 VND/kg (+69.5%)
- RMSE: 31,514 VND/kg (+76.3%)

### heat_wave

- MAE:  14,472 VND/kg (+0.0%)
- RMSE: 17,871 VND/kg (+0.0%)

### both

- MAE:  24,541 VND/kg (+69.6%)
- RMSE: 31,519 VND/kg (+76.3%)

## Nhận xét và Ghi nhận

> Kịch bản shock giá làm MAE tăng tối đa +69.6%, cho thấy baseline
> Random Forest phụ thuộc đáng kể vào lịch sử giá gần nhất và không ngoại suy tốt khi
> thị trường sụp đổ đột ngột. Kịch bản heat_wave gần như không đổi sai số vì feature
> nhiệt độ có trọng số rất thấp trong mô hình hiện tại.

## Khuyến nghị cho Slide Báo cáo

- Trình bày MAE lift % làm bằng chứng định lượng cho trụ cột Robustness.
- Nhấn mạnh baseline chịu rủi ro cao hơn với shock giá so với shock nhiệt độ.
- Tích hợp cảnh báo người dùng trên UI khi các chỉ số thực tế vượt ngưỡng lịch sử đã train.