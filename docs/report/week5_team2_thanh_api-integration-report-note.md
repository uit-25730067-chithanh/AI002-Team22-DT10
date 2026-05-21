# Note báo cáo phần việc của Thanh — Week 5 API và Integration

**Ngày note:** 2026-05-18  
**Người báo cáo:** Thanh  
**Báo cho:** em Phúc / Team 1 / Team 2  
**Roadmap:** Tuần 5 — API và Integration  
**Phạm vi:** Phần Thanh phụ trách API real-data contract, validation, handoff frontend và docs sync. QA checklist của Sơn chỉ nhắc là tài liệu phối hợp.

## 1. Tóm tắt ngắn để báo miệng

Tuần 5, anh cập nhật backend để dùng model real-data: `/predict` nhận payload theo schema thật, validate numeric ranges/enum/category đã train, trả prediction kèm confidence interval, top features, model version và disclaimer. Anh cũng viết handoff note cho Phúc/Thịnh nối frontend và mở PR #11 để sync README, roadmap, codebase summary, data-flow docs. Lưu ý khi checkout sạch: `model/best_model/model.pkl` bị gitignore, nên cần train/generate model local hoặc cung cấp artifact trước khi frontend gọi `/predict` thật. Frontend integration và demo end-to-end vẫn chưa có bằng chứng hoàn tất trong repo.

## 2. Mapping theo roadmap

| Roadmap item                                                            | Trạng thái   | Phần Thanh báo cáo                                       | Bằng chứng                                                        |
| ----------------------------------------------------------------------- | ------------ | -------------------------------------------------------- | ----------------------------------------------------------------- |
| Hoàn thiện `/predict`, `/health`, `/model/info` theo real-data contract | Xong         | Cập nhật API nhận payload real-data                      | `backend/api/routes.py`, `backend/schemas/prediction.py`          |
| API validate numeric ranges, enum và category đã train                  | Xong         | Reject input ngoài tập train thay vì predict sai âm thầm | `backend/schemas/prediction.py`, `backend/services/predictor.py`  |
| Sơn bổ sung integration QA checklist                                    | Xong bởi Sơn | Thanh tham chiếu khi handoff frontend                    | `docs/discussions/2026-05-13-son-api-integration-qa-checklist.md` |
| Team 1 nối frontend với API                                             | Chưa xong    | Thanh chuẩn bị handoff và hỗ trợ                         | `docs/discussions/2026-05-13-api-handoff-team2-real-data.md`      |
| Demo end-to-end                                                         | Chưa xong    | Chờ frontend integration                                 | Chưa có bằng chứng hoàn tất                                       |

## 3. API contract hiện tại

| Endpoint          | Vai trò                              | Ghi chú frontend                    |
| ----------------- | ------------------------------------ | ----------------------------------- |
| `GET /health`     | Kiểm tra backend và model load state | UI có thể dùng kiểm tra server sống |
| `GET /model/info` | Lấy metadata model/version/features  | Có thể hiển thị thông tin model     |
| `POST /predict`   | Dự báo giá cà phê                    | Form cần map đúng field real-data   |

Điều kiện trước khi frontend test `/predict`: backend phải load được `model/best_model/model.pkl`. Nếu checkout sạch chưa có artifact này, `/health` sẽ báo model chưa load và `/predict` chưa sẵn sàng để demo.

## 4. Request/response cần nhắc Team 1

### Field frontend nên quan tâm

| Field                          | Vai trò                | Ghi chú                                                 |
| ------------------------------ | ---------------------- | ------------------------------------------------------- |
| `province`                     | Tỉnh                   | Phải nằm trong feature đã train                         |
| `area`                         | Huyện/khu vực          | Phải nằm trong feature đã train                         |
| `month`                        | Tháng dự báo           | Bắt buộc, 1-12                                          |
| `year`                         | Năm dự báo             | Có default `2025`, range 2022-2030                      |
| `avg_temperature_c`            | Nhiệt độ               | Có validate range                                       |
| `total_rainfall_mm`            | Lượng mưa              | Có validate range                                       |
| `avg_humidity_percent`         | Độ ẩm                  | Optional, backend có default                            |
| `soil_data_confidence`         | Độ tin cậy dữ liệu đất | Optional enum: `low`, `medium`, `high`                  |
| `latest_price_vnd_per_kg`      | Giá gần nhất           | Có default nếu UI chưa nhập                             |
| `rolling_avg_price_vnd_per_kg` | Rolling average        | Có default từ latest price nếu thiếu                    |
| `price_fill_method`            | Chất lượng/nguồn giá   | Enum: `observed`, `interpolated_area`, `province_proxy` |

### Response chính

| Field                 | Ý nghĩa                                                 |
| --------------------- | ------------------------------------------------------- |
| `predicted_price_vnd` | Giá dự báo                                              |
| `confidence_interval` | Khoảng tin cậy; FastAPI serialize tuple thành mảng JSON |
| `top_features`        | Top feature giải thích dự báo                           |
| `model_version`       | Experiment/model đang dùng                              |
| `disclaimer`          | Cảnh báo dự báo chỉ mang tính tham khảo                 |

## 5. Validation và Robustness

- **Numeric range:** API kiểm tra các field numeric để tránh input vô lý.
- **Enum:** API chỉ nhận enum hợp lệ cho các field categorical có danh sách rõ.
- **Trained category:** Nếu frontend gửi province/area/category ngoài feature đã train, API trả lỗi thay vì tạo vector one-hot toàn 0.
- **Disclaimer:** Response có disclaimer để tránh hiểu dự báo là lời khuyên tài chính/bán hàng.

## 6. Handoff note cho frontend

| File                                                         | Mục đích                                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| `docs/discussions/2026-05-13-api-handoff-team2-real-data.md` | Request mẫu, response mẫu, field bắt buộc/default, metric model và disclaimer UI      |
| `docs/project-roadmap.md`                                    | Theo dõi milestone, trách nhiệm và luồng crawler → processed → model → API → frontend |

## 7. PR/docs sync

| PR     | Trạng thái trong lần kiểm tra gần nhất | Nội dung                                                                        |
| ------ | -------------------------------------- | ------------------------------------------------------------------------------- |
| PR #11 | Open, merge clean                      | Sync README, roadmap, codebase summary, field descriptions và data-flow wording |
| PR #12 | Merged, của Sơn                        | Evaluation pack, real-data audit, API QA checklist, 5 Pillars checkpoint        |
| PR #13 | Merged                                 | Reorganize report notes vào `docs/report/`                                      |
| PR #14 | Merged                                 | Promote best real-data model theo metric trong `rf_real_*`                      |

Cách nói trong họp: PR #12 là phần Sơn. PR #13/#14 đã được sync lại vào PR #11 để docs/report và số liệu model không lệch `origin/main`.

## 8. Follow-up kỹ thuật cần chốt

Các việc cần đảm bảo trước khi chốt tuần 5/6:

- **Feature leakage:** historical features phải dùng dữ liệu quá khứ, không dùng current target.
- **Response JSON:** frontend sẽ nhận `confidence_interval` dạng mảng JSON dù backend dùng tuple.
- **Regression tests:** đã có test predictor response và unknown category; còn thiếu test invalid-range/schema validation nếu muốn chốt robustness đầy đủ.
- **Verification:** chạy pytest, compileall và `git diff --check` trước khi merge/chốt báo cáo.

## 9. Việc chưa đánh dấu hoàn tất

| Việc                                            | Lý do                                                   |
| ----------------------------------------------- | ------------------------------------------------------- |
| Team 1 nối frontend với API                     | Chưa thấy bằng chứng frontend gọi `/predict` trong repo |
| Demo end-to-end                                 | Chưa có log/screenshot/test xác nhận                    |
| Stress test real-data/API integration follow-up | Roadmap ghi sau khi frontend/backend ổn định            |
| Slide/report cuối kỳ                            | Thuộc tuần 6, chưa nên report là đã xong                |

## 10. Tin nhắn ngắn có thể gửi team

```text
Tuần 5 phần của anh đã cập nhật API theo real-data contract: `/predict` nhận payload thật, validate numeric/enum/category đã train, trả predicted price, confidence interval, top features, model version và disclaimer. Anh cũng đã viết handoff note cho Phúc/Thịnh nối frontend và có PR #11 sync README/roadmap/codebase summary. Phần frontend gọi API và demo end-to-end chưa có bằng chứng hoàn tất, nên tuần tới anh sẽ hỗ trợ test request/response và xử lý lỗi `422` khi UI gửi input ngoài tập train.
```
