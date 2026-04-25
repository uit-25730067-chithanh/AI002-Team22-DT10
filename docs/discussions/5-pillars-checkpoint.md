# Kiểm điểm 5 Trụ cột AI (Foundation Week)

**Ngày:** 2026-04-26  
**Phạm vi:** Phase 1-3 (mock data -> model baseline -> API skeleton)

## Bảng chứng minh (Evidence Matrix)

| Trụ cột                             | Bằng chứng trong code                                                                              | File liên quan                                                                      |
| ----------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Reliability (Tính tin cậy)**      | Chia train/test theo thời gian; metrics MAE/RMSE/R² trong kết quả train baseline                   | `model/train_rf.py`                                                                 |
| **Bias (Không thiên vị)**           | Ghi chú hạn chế vùng Tây Nguyên; cảnh báo trong data spec                                          | `scripts/generate_mock_data.py`, `docs/discussions/data-format-spec.md`             |
| **Robustness (Kháng nhiễu)**        | Validate input bằng Pydantic ranges; xử lý NaN/outlier trong tiền xử lý; kịch bản stress test      | `backend/schemas/prediction.py`, `model/preprocess.py`, `model/stress_test.py`      |
| **Social Impact (Tác động xã hội)** | API hỗ trợ nông dân nhỏ lẻ dự báo tham khảo; yêu cầu disclaimer rủi ro trong UI                    | `plans/team2-foundation-week/phase-03-api-skeleton-5-pillars-check.md`, `README.md` |
| **Transparency (Minh bạch)**        | Random Forest feature importance; endpoint `/predict` trả về lý giải top features + khoảng tin cậy | `model/train_rf.py`, `backend/services/predictor.py`, `backend/api/routes.py`       |

## Hạn chế & Giải pháp "Hành chính" (không code)

| Hạn chế                                    | Tại sao chưa giải quyết bằng code                | Giải pháp hiện tại                                                          |
| ------------------------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------- |
| Thao túng thị trường cực đoan / Black Swan | Model baseline đơn giản, data là mock            | Ghi nhận độ lệch MAE trong stress test; thêm cảnh báo rủi ro trong UI/slide |
| Thiên vị vùng miền (data chỉ Tây Nguyên)   | Crawler thật chưa mở rộng                        | Giữ disclaimer rõ ràng trong docs và UI                                     |
| Hiệu chỉnh độ tin cậy (calibration)        | Chưa có bước hiệu chỉnh xác suất trong phase này | Trả về khoảng tin cậy ước lượng từ variance cây RF                          |

## Ghi chú tích hợp cho Team 1 (UI)

- Hiển thị cảnh báo bên cạnh kết quả dự báo: "Dự báo AI chỉ mang tính tham khảo; nông dân cân nhắc thêm bối cảnh thị trường địa phương trước khi giao dịch lớn."
- Hiển thị ghi chú hạn chế vùng miền khi áp dụng cho khu vực ngoài Tây Nguyên.

## Bước tiếp theo (Sau kỳ nghỉ lễ)

- Thay mock data bằng data thật từ crawler và train lại model.
- Kiểm tra lại MAE/RMSE và chất lượng giải thích sau khi có data thật.
- Bổ sung số liệu đánh giá thực tế và các trường hợp thất bại vào tài liệu này.
