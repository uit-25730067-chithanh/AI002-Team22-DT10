# Stress Test Report — Robustness Pillar

**Date:** 2026-06-07 23:58:02
**Model:** model/best_model/model.pkl
**Dataset:** data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv
**Experiment:** 20260607_235428__rf_independent_monthly

## Baseline (Normal Test Set - 2025)

- MAE:  10,907 VND/kg
- RMSE: 13,963 VND/kg

## Black Swan Scenarios (Gây nhiễu tập Test 2025)

### price_crash

- MAE:  22,106 VND/kg (+102.7%)
- RMSE: 30,315 VND/kg (+117.1%)

### heat_wave

- MAE:  10,905 VND/kg (+0.0%)
- RMSE: 13,961 VND/kg (+0.0%)

### both

- MAE:  22,109 VND/kg (+102.7%)
- RMSE: 30,320 VND/kg (+117.1%)

## Nhận xét và Ghi nhận

> Kịch bản shock giá làm MAE tăng tối đa +102.7%, cho thấy baseline
> Random Forest phụ thuộc đáng kể vào lịch sử giá gần nhất và không ngoại suy tốt khi
> thị trường sụp đổ đột ngột. Kịch bản heat_wave gần như không đổi sai số vì feature
> nhiệt độ có trọng số rất thấp trong mô hình hiện tại.

## Khuyến nghị cho Slide Báo cáo

- Trình bày MAE lift % làm bằng chứng định lượng cho trụ cột Robustness.
- Nhấn mạnh baseline chịu rủi ro cao hơn với shock giá so với shock nhiệt độ.
- Tích hợp cảnh báo người dùng trên UI khi các chỉ số thực tế vượt ngưỡng lịch sử đã train.