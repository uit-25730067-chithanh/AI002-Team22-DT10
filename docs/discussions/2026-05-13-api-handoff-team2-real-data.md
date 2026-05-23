# API Handoff Team 2 Real Data Model — 13/05/2026

## Scope

Note này dành cho Phúc/Thịnh khi chuẩn bị nối frontend với backend tuần 18/5-24/5.

## UI mode đã chốt

Frontend dùng hướng **form nhập thông số + advisory card**, không làm chatbot hay Q&A tự do.
User nhập/chọn các thông số có cấu trúc, gọi `POST /predict`, rồi UI render 2 nhóm kết quả:

- Card dự báo giá.
- Card gợi ý chăm sóc mùa vụ từ `farming_recommendation`.

Các câu hỏi kỹ thuật chi tiết như "vặt chồi bao lâu" không thuộc API contract hiện tại. Nếu cần hiển thị, nên đặt ở phần FAQ tĩnh hoặc note hướng dẫn riêng, không gọi đây là agent chat nông nghiệp.

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
  "rolling_avg_price_vnd_per_kg": 88000,
  "price_observations": 1
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
| `price_observations`           | Không    | Backend default 1 nếu `price_fill_method=observed`, ngược lại 0                        |

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
  "model_version": "20260513_155830__rf_real_monthly",
  "farming_recommendation": {
    "action": "harvest",
    "season_type": "main_season",
    "confidence": 0.85,
    "reasoning": "Tháng 11 là giai đoạn thu hoạch chính ở Tây Nguyên. Điều kiện đất và thời tiết hiện tại không có cảnh báo lớn. Đây là gợi ý rule-based để tham khảo.",
    "warnings": [],
    "next_action_month": 12,
    "next_action": "harvest",
    "advisory_type": "rule_based"
  },
  "disclaimer": "Dự báo giá và gợi ý canh tác chỉ mang tính tham khảo, không thay thế tư vấn tài chính hoặc tư vấn nông nghiệp tại địa phương."
}
```

## Field mới: `farming_recommendation`

Request payload không đổi. Backend chỉ thêm field mới trong response để frontend hiển thị **advisory card** về gợi ý chăm sóc mùa vụ dựa trên rule.

| Field               | Ý nghĩa                                                                                                               | Gợi ý render                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `action`            | Mã hành động chính: `post_harvest_care`, `flowering_care`, `growth_care`, `harvest`, `off_season`                     | Map sang tiêu đề tiếng Việt          |
| `season_type`       | Nhóm mùa: `dry_season`, `rainy_season`, `main_season`, `off_season`                                                   | Badge mùa vụ                         |
| `confidence`        | Độ tin cậy rule, từ 0 đến 1                                                                                           | Hiển thị phần trăm                   |
| `reasoning`         | Diễn giải tiếng Việt                                                                                                  | Hiển thị trực tiếp cho user          |
| `warnings`          | Mã cảnh báo: `low_soil_moisture`, `heavy_rainfall`, `heat_stress`, `low_soil_suitability`, `low_soil_data_confidence`, `advisory_config_unavailable` | Map badge/icon nếu kịp               |
| `next_action_month` | Tháng tiếp theo backend xét rule                                                                                      | Text phụ                             |
| `next_action`       | Hành động rule của tháng tiếp theo                                                                                    | Text phụ                             |
| `advisory_type`     | Hiện là `rule_based`                                                                                                  | Có thể ẩn hoặc show nhỏ để minh bạch |

Lưu ý wording cho UI/report: dùng "gợi ý canh tác dựa trên rule", không viết "model AI canh tác đã được huấn luyện". Phần này hỗ trợ minh bạch và social impact, nhưng chưa phải mô hình học máy cho canh tác.

Nếu nhận `warnings=["advisory_config_unavailable"]`, frontend nên vẫn hiển thị kết quả dự báo giá, nhưng card canh tác cần báo nhẹ rằng cấu hình gợi ý mùa vụ chưa sẵn sàng và người dùng nên kiểm tra lại với nguồn địa phương.

Lưu ý scope UI: không hiển thị như chatbot, không promise trả lời câu hỏi tự do. UI nên dùng heading như "Gợi ý chăm sóc mùa vụ" hoặc "Gợi ý canh tác theo mùa vụ".

## Ghi chú model hiện tại

| Metric     |                            Giá trị |
| ---------- | ---------------------------------: |
| Experiment | `20260513_155830__rf_real_monthly` |
| Train size |                                432 |
| Test size  |                                144 |
| MAE        |                      13,552 VND/kg |
| RMSE       |                      16,754 VND/kg |
| R²         |                            -0.9044 |

R² âm cho thấy distribution 2025 lệch mạnh so với 2022-2024; báo cáo cần nói rõ đây là baseline thật, chưa phải model cuối.

## Disclaimer UI bắt buộc

Frontend nên hiển thị câu: `Dự báo giá và gợi ý canh tác chỉ mang tính tham khảo, không thay thế tư vấn tài chính hoặc tư vấn nông nghiệp tại địa phương.`
