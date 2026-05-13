# API Handoff Team 2 Real Data Model — 13/05/2026

## Scope

Note này dành cho Phúc/Thịnh khi chuẩn bị nối frontend với backend tuần 18/5-24/5.

## Endpoint dự kiến

- `POST /predict`
- `GET /health`
- `GET /model/info`

## Request mẫu

```json
{
  "province": "Dak Lak",
  "area": "Buon Ho",
  "avg_temperature_c": 26.0,
  "total_rainfall_mm": 20.0,
  "avg_humidity_percent": 80.0,
  "avg_soil_moisture_0_7cm": 0.24,
  "soil_score": 5.0,
  "soil_data_confidence": "medium",
  "coffee_type": "Robusta / ca phe nhan xo noi dia",
  "price_fill_method": "observed",
  "dominant_soil_type": "Dat do bazan",
  "month": 11,
  "year": 2025,
  "latest_price_vnd_per_kg": 90000,
  "rolling_avg_price_vnd_per_kg": 88000
}
```

## Field tối thiểu frontend nên cho user chọn

| Field                          | Bắt buộc | Ghi chú                                                                                |
| ------------------------------ | -------- | -------------------------------------------------------------------------------------- |
| `province`                     | Có       | Tỉnh trồng cà phê                                                                      |
| `area`                         | Có       | Khu vực/huyện, ví dụ `Buon Ho`                                                         |
| `month`                        | Có       | Tháng cần dự báo, 1-12                                                                 |
| `avg_temperature_c`            | Có       | Có thể lấy default/latest từ data nếu UI chưa nhập                                     |
| `total_rainfall_mm`            | Có       | Có thể lấy default/latest từ data nếu UI chưa nhập                                     |
| `avg_humidity_percent`         | Không    | Backend default 75 nếu thiếu                                                           |
| `avg_soil_moisture_0_7cm`      | Không    | Backend default 0.24 nếu thiếu                                                         |
| `soil_score`                   | Không    | Backend default 5 nếu thiếu                                                            |
| `soil_data_confidence`         | Không    | Chỉ nhận `low`, `medium`, `high`; nếu thiếu thì không set one-hot                      |
| `coffee_type`                  | Không    | Backend default `Robusta / ca phe nhan xo noi dia`                                     |
| `price_fill_method`            | Không    | Backend default `observed`; chỉ nhận `observed`, `interpolated_area`, `province_proxy` |
| `dominant_soil_type`           | Không    | Backend default `Dat do bazan`                                                         |
| `latest_price_vnd_per_kg`      | Không    | Backend default 90000 nếu thiếu                                                        |
| `rolling_avg_price_vnd_per_kg` | Không    | Backend dùng latest price nếu thiếu                                                    |

`province`, `area`, và các categorical field phải nằm trong nhóm feature đã train. Nếu frontend gửi giá trị ngoài tập train, API trả `422` thay vì âm thầm tạo vector one-hot toàn 0.

## Response mẫu

```json
{
  "predicted_price_vnd": 88450.0,
  "confidence_interval": [82000.0, 94900.0],
  "top_features": [
    {
      "feature": "rolling_avg_7d",
      "importance": 0.728,
      "input_value": 88000.0,
      "explanation": "rolling_avg_7d có mức quan trọng cao với giá trị hiện tại."
    }
  ],
  "model_version": "20260513_161417__rf_real_monthly",
  "disclaimer": "Dự báo chỉ mang tính tham khảo, không thay thế tư vấn tài chính hoặc quyết định bán hàng thực tế."
}
```

## Ghi chú model hiện tại

| Metric     |                            Giá trị |
| ---------- | ---------------------------------: |
| Experiment | `20260513_161417__rf_real_monthly` |
| Train size |                                420 |
| Test size  |                                144 |
| MAE        |                      13,874 VND/kg |
| RMSE       |                      17,261 VND/kg |
| R²         |                            -1.0213 |

R² âm cho thấy distribution 2025 lệch mạnh so với 2022-2024; báo cáo cần nói rõ đây là baseline thật, chưa phải model cuối.

## Disclaimer UI bắt buộc

Frontend nên hiển thị câu: `Dự báo chỉ mang tính tham khảo, không thay thế tư vấn tài chính hoặc quyết định bán hàng thực tế.`
