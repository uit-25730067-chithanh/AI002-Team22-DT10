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

Request payload không đổi. Backend chỉ thêm field mới trong response để frontend có thể hiển thị gợi ý chăm sóc mùa vụ bên cạnh kết quả dự báo giá.

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

## Luồng frontend gọi API

1. Gọi `GET /health` khi mở màn hình hoặc trước lúc demo để kiểm tra backend và model đã sẵn sàng.
2. User nhập/chọn field trong form, frontend build payload theo `Request mẫu`.
3. Gửi `POST /predict`.
4. Nếu response `200`, frontend render kết quả giá và `farming_recommendation`.
5. Nếu response lỗi, frontend hiển thị lỗi ngắn gọn theo bảng `Xử lý lỗi frontend`.

Có thể test nhanh contract bằng Swagger UI tại `http://localhost:8000/docs` khi backend đang chạy.

## Frontend render response như thế nào

| Nhóm UI                  | Field backend trả về                                                       | Cách hiển thị gợi ý                                                                 |
| ------------------------ | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Kết quả dự báo giá       | `predicted_price_vnd`                                                      | Format VND/kg, làm số chính của card dự báo                                         |
| Khoảng dao động          | `confidence_interval`                                                      | Hiển thị dạng `82.000 - 94.900 VND/kg`                                              |
| Giải thích dự báo        | `top_features`                                                             | Render 1-3 dòng lý do ảnh hưởng chính, dùng `explanation` nếu muốn nhanh            |
| Phiên bản model          | `model_version`                                                            | Có thể để nhỏ ở footer/debug info để trace khi báo lỗi                              |
| Gợi ý chăm sóc mùa vụ    | `farming_recommendation.action`, `season_type`, `confidence`, `reasoning`  | Render thành card gợi ý mùa vụ; `reasoning` là text tiếng Việt có thể hiển thị thẳng |
| Cảnh báo điều kiện       | `farming_recommendation.warnings`                                          | Map sang nhãn tiếng Việt; nếu rỗng thì không cần hiện badge cảnh báo                |
| Bước tiếp theo           | `next_action_month`, `next_action`                                         | Hiển thị text phụ kiểu `Tháng tiếp theo: Thu hoạch`                                 |
| Disclaimer               | `disclaimer`                                                               | Luôn hiển thị gần cuối kết quả                                                      |

## Mapping UI cho `farming_recommendation`

| `action`            | Nhãn tiếng Việt gợi ý     |
| ------------------- | ------------------------- |
| `post_harvest_care` | Chăm sóc sau thu hoạch    |
| `flowering_care`    | Chăm sóc giai đoạn ra hoa |
| `growth_care`       | Chăm sóc giai đoạn sinh trưởng |
| `harvest`           | Thu hoạch                 |
| `off_season`        | Theo dõi ngoài mùa chính  |

| `season_type`  | Nhãn tiếng Việt gợi ý |
| -------------- | --------------------- |
| `dry_season`   | Mùa khô               |
| `rainy_season` | Mùa mưa               |
| `main_season`  | Mùa chính             |
| `off_season`   | Ngoài mùa chính       |

| Warning code                    | Nhãn tiếng Việt gợi ý                                           |
| ------------------------------- | --------------------------------------------------------------- |
| `low_soil_moisture`             | Độ ẩm đất thấp, cần theo dõi tưới nước                          |
| `heavy_rainfall`                | Lượng mưa cao, cần chú ý thoát nước                             |
| `heat_stress`                   | Nhiệt độ cao, cây có thể chịu stress nhiệt                      |
| `low_soil_suitability`          | Điểm phù hợp đất thấp, nên kiểm tra điều kiện đất               |
| `low_soil_data_confidence`      | Độ tin cậy dữ liệu đất thấp                                     |
| `advisory_config_unavailable`   | Chưa tải được cấu hình gợi ý mùa vụ, chỉ nên xem dự báo giá trước |

`confidence` là số từ 0 đến 1. Frontend có thể hiển thị `Math.round(confidence * 100) + "%"`.

## Xử lý lỗi frontend

| Trường hợp                        | Backend trả về                      | Frontend nên xử lý                                                                 |
| --------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------------- |
| Input sai range hoặc thiếu field  | `422` từ Pydantic                   | Báo user kiểm tra lại field nhập; ưu tiên highlight field tương ứng nếu UI có form |
| Category ngoài tập train          | `422` với message từ backend        | Báo giá trị tỉnh/khu vực/loại đất chưa nằm trong dữ liệu train hiện tại            |
| Model chưa load hoặc thiếu `.pkl` | `503`                               | Báo backend/model chưa sẵn sàng; không gọi lại liên tục                            |
| Lỗi không mong muốn               | `500`                               | Báo lỗi hệ thống ngắn gọn và nhờ thử lại sau                                       |
| `advisory_config_unavailable`     | `200` + warning trong recommendation | Vẫn hiển thị card giá; card gợi ý mùa vụ báo cấu hình gợi ý chưa sẵn sàng          |

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
