# Stress Test Report — Robustness Pillar

**Date:** 2026-04-26
**Model:** Random Forest Baseline
**Dataset:** mock_coffee_data.csv

## Baseline (Normal Test Set)

- MAE:  2,538 VND/kg
- RMSE: 3,170 VND/kg

## Black Swan Scenarios

### price_crash

- MAE:  4,778 VND/kg (+88.3%)
- RMSE: 7,895 VND/kg (+149.1%)

### heat_wave

- MAE:  2,535 VND/kg (+-0.1%)
- RMSE: 3,166 VND/kg (+-0.1%)

### both

- MAE:  4,743 VND/kg (+86.9%)
- RMSE: 7,766 VND/kg (+145.0%)

## Ghi nhận

> Khi thị trường biến động cực đoan (giá sụp 50%, nhiệt độ 45°C),
> model dự báo lệch đáng kể so với baseline. Điều này là bình thường
> vì model được huấn luyện trên phân bố lịch sử, không phải sự kiện hiếm.

## Khuyến nghị cho Slide Tuần 6

- Trình bày MAE lift % như bằng chứng Robustness.
- Giải thích: 'Model hoạt động tốt trong phân bố lịch sử,
  nhưng cần cảnh báo người dùng khi input nằm ngoài phân bố đã thấy.'