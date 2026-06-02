# Stress Test Report — Robustness Pillar

**Date:** 2026-06-02 18:20:19
**Model:** model/best_model/model.pkl
**Dataset:** data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv
**Experiment:** 20260514_013051__rf_real_monthly

## Baseline (Normal Test Set - 2025)

- MAE:  13,552 VND/kg
- RMSE: 16,754 VND/kg

## Black Swan Scenarios (Gây nhiễu tập Test 2025)

### price_crash

- MAE:  22,566 VND/kg (+66.5%)
- RMSE: 29,398 VND/kg (+75.5%)

### heat_wave

- MAE:  13,549 VND/kg (+-0.0%)
- RMSE: 16,752 VND/kg (+-0.0%)

### both

- MAE:  22,569 VND/kg (+66.5%)
- RMSE: 29,403 VND/kg (+75.5%)

## Nhận xét và Ghi nhận

> Kịch bản price_crash và both làm MAE tăng mạnh (+66.5%), cho thấy baseline
> Random Forest phụ thuộc đáng kể vào lịch sử giá gần nhất và không ngoại suy tốt khi
> thị trường sụp đổ đột ngột. Kịch bản heat_wave gần như không đổi sai số vì feature
> nhiệt độ có trọng số rất thấp trong mô hình hiện tại.

## Khuyến nghị cho Slide Báo cáo

- Trình bày MAE lift % làm bằng chứng định lượng cho trụ cột Robustness.
- Nhấn mạnh baseline chịu rủi ro cao hơn với shock giá so với shock nhiệt độ.
- Tích hợp cảnh báo người dùng trên UI khi các chỉ số thực tế vượt ngưỡng lịch sử đã train.
