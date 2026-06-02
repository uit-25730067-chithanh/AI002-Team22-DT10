# API Handoff Team 2 Real Data Model — 13/05/2026

> [!IMPORTANT]
> **Trạng thái tích hợp Frontend:** Mã nguồn chính thức của Web UI hiện vẫn đang nằm ở máy local của Phúc (Team 1) và đang chuẩn bị để push lên GitHub. Dưới đây là các hướng dẫn và checklist để Phúc thực hiện tích hợp và kiểm thử khi push code.

## Hướng dẫn & Checklist tích hợp cho Team 1 (Phúc)
Phúc cần đảm bảo các bước sau khi tích hợp mã nguồn frontend local vào repo:
1. [ ] **Thêm tài nguyên UI:** Commit đầy đủ các file UI gồm `frontend/index.html`, các file CSS và JS liên quan vào thư mục `frontend/` của repository.
2. [ ] **Cấu hình API Endpoint:** Đảm bảo mã nguồn JavaScript gọi đúng endpoint API của backend. Khi chạy local dùng `http://localhost:8000`. Khi deploy self-host hoặc dùng shared API, cấu hình base URL tương ứng.
3. [ ] **Cấu hình Bảo mật (API Key):** Các API protected như `/predict` và `/model/info` yêu cầu gửi kèm header `X-API-Key`. Hãy thiết lập cơ chế gửi header này đúng cách. Không hardcode API key thật lên Git.
4. [ ] **Kiểm thử các Endpoint:**
   - [ ] Kiểm thử `GET /health` (trả về trạng thái OK và model load state).
   - [ ] Kiểm thử `GET /model/info` (trả về thông tin metadata của model).
   - [ ] Kiểm thử `POST /predict` (gửi request mẫu bên dưới, nhận response thành công 200).

---

## Scope

Note này dành cho Phúc/Thịnh khi chuẩn bị nối frontend với backend tuần 18/5-24/5.

## Giới hạn dữ liệu thời tiết và năm demo

Phần demo hiện nên giới hạn ở năm 2025 vì dataset đã xử lý có dữ liệu giá, thời tiết và đất đến hết năm 2025. Backend hiện không có model riêng để dự báo thời tiết tương lai.

Các field thời tiết như `avg_temperature_c`, `total_rainfall_mm`, `avg_humidity_percent`, `avg_soil_moisture_0_7cm` phải đến từ dữ liệu đã chuẩn bị sẵn hoặc do frontend/user nhập. API chỉ dùng các giá trị này làm input để dự báo giá và tạo gợi ý canh tác rule-based; API không tự sinh dự báo thời tiết.

Khi viết báo cáo hoặc UI copy, nên nói: "gợi ý canh tác dựa trên dữ liệu thời tiết/đất đầu vào và rule mùa vụ". Không nên nói hệ thống đã có model dự báo thời tiết hoặc model AI riêng để lập kế hoạch canh tác.

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
| `avg_temperature_c`            | Có       | Lấy từ dữ liệu thời tiết đã chuẩn bị hoặc user nhập; backend không dự báo field này     |
| `total_rainfall_mm`            | Có       | Lấy từ dữ liệu thời tiết đã chuẩn bị hoặc user nhập; backend không dự báo field này     |
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
| Gợi ý chăm sóc mùa vụ    | `farming_recommendation.action`, `farming_recommendation.season_type`, `farming_recommendation.confidence`, `farming_recommendation.reasoning` | Render thành card gợi ý mùa vụ; `reasoning` là text tiếng Việt có thể hiển thị thẳng |
| Cảnh báo điều kiện       | `farming_recommendation.warnings`                                          | Map sang nhãn tiếng Việt; nếu rỗng thì không cần hiện badge cảnh báo                |
| Bước tiếp theo           | `farming_recommendation.next_action_month`, `farming_recommendation.next_action` | Hiển thị text phụ kiểu `Tháng tiếp theo: Thu hoạch`                                 |
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
