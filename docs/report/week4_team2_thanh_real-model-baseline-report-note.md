# Note báo cáo phần việc của Thanh — Week 4 Model thật

**Ngày note:** 2026-05-18  
**Người báo cáo:** Thanh  
**Báo cho:** em Phúc / Team 1 / Team 2  
**Roadmap:** Tuần 4 — Model thật  
**Phạm vi:** Phần Thanh xử lý real-data baseline: preprocess schema, feature engineering, train model, metadata và feature importance. Evaluation/5 Pillars của Sơn chỉ nhắc ở mức phối hợp.

## 1. Tóm tắt ngắn để báo miệng

Tuần 4, anh đã đưa pipeline model sang dữ liệu thật: normalize schema monthly CSV, tạo feature theo khu vực/thời gian, split train/test theo thời gian, train Random Forest baseline và lưu best model/metadata/feature importance. Model hiện là baseline thật, chưa phải model cuối; R² còn âm nên cần báo cáo trung thực, nhưng pipeline đã chạy end-to-end và có bằng chứng Reliability/Transparency rõ ràng.

## 2. Mapping theo roadmap

| Roadmap item                                        | Trạng thái   | Phần Thanh báo cáo                           | Bằng chứng                                                                      |
| --------------------------------------------------- | ------------ | -------------------------------------------- | ------------------------------------------------------------------------------- |
| Train Random Forest baseline trên monthly all-areas | Xong         | Train baseline trên dataset monthly thật     | `model/train_rf.py`, `model/experiments.csv`                                    |
| Trích xuất feature importance                       | Xong         | Lưu top features trong metadata              | `model/best_model/metadata.json`                                                |
| Lưu best model và metadata                          | Xong         | Promote model tốt nhất cho backend API       | `model/best_model/metadata.json`; `model.pkl` được generate local và gitignored |
| Sơn bổ sung audit/5 Pillars PR #12                  | Xong bởi Sơn | Thanh chỉ tham chiếu khi sync roadmap/report | `docs/discussions/5-pillars-checkpoint.md`                                      |
| Stress test real-data/API follow-up                 | Chưa xong    | Chờ frontend/backend ổn định                 | Không nhận là việc đã xong                                                      |

## 3. PR/code liên quan

| PR/Commit                     | Nội dung                                                    | Trạng thái |
| ----------------------------- | ----------------------------------------------------------- | ---------- |
| PR #7                         | Cập nhật experiment tracking và fallback temporal split     | Đã merge   |
| PR #9                         | Implement real data model baseline                          | Đã merge   |
| `model/preprocess.py`         | Normalize real schema, feature engineering, temporal split  | Đã dùng    |
| `model/train_rf.py`           | Train RF, lưu feature names/importances, promote best model | Đã dùng    |
| `model/experiment_tracker.py` | Lưu lịch sử experiment theo timestamp                       | Đã dùng    |

## 4. Kết quả baseline theo workspace hiện tại

Theo `model/best_model/metadata.json` trong workspace hiện tại:

| Mục           |                            Giá trị |
| ------------- | ---------------------------------: |
| Experiment    | `20260513_161417__rf_real_monthly` |
| Model         |            `RandomForestRegressor` |
| Train size    |                                420 |
| Test size     |                                144 |
| Feature count |                                 41 |
| MAE           |                      13,874 VND/kg |
| RMSE          |                      17,261 VND/kg |
| R²            |                            -1.0213 |

Ghi chú trình bày: R² âm cho thấy baseline chưa bắt được phân phối năm 2025 tốt. Không nên nói model đã tốt; nên nói model đã chạy thật, có metric thật, có limitation rõ.

Lưu ý triển khai: repo chỉ track metadata của best model; file `model/best_model/model.pkl` bị gitignore nên cần train/generate local hoặc cung cấp artifact ngoài repo trước khi backend dùng model thật.

## 5. Top feature importance

| Feature          | Importance | Ý nghĩa khi giải thích            |
| ---------------- | ---------: | --------------------------------- |
| `rolling_avg_7d` |     0.6799 | Giá gần đây là tín hiệu mạnh nhất |
| `lag_1d`         |     0.2863 | Giá kỳ trước ảnh hưởng lớn        |
| `month`          |     0.0099 | Có yếu tố mùa vụ nhưng nhỏ        |
| `month_sin`      |     0.0080 | Chu kỳ tháng có đóng góp nhỏ      |
| `quarter`        |     0.0056 | Quý có đóng góp nhỏ               |

Điểm cần nói rõ: model phụ thuộc nhiều vào historical price, hợp lý với bài toán giá nhưng cần cẩn thận khi thị trường biến động mạnh.

## 6. Liên hệ với 5 trụ cột AI

| Trụ cột       | Bằng chứng từ phần Thanh                                             |
| ------------- | -------------------------------------------------------------------- |
| Reliability   | Có temporal train/test split, MAE/RMSE/R²                            |
| Robustness    | Preprocess chuẩn hóa schema thật và default optional fields ở API    |
| Transparency  | Có feature importance và feature names                               |
| Bias          | Nhận biết coverage không đều qua area ranking, không claim toàn quốc |
| Social Impact | Dự báo chỉ là baseline tham khảo, không thay thế quyết định bán hàng |

## 7. Phần không nhận là việc của Thanh

| Nội dung                      | Theo roadmap là phần | Ghi chú                      |
| ----------------------------- | -------------------- | ---------------------------- |
| Real-data audit chi tiết      | Sơn                  | Thanh chỉ tham chiếu kết quả |
| Bias evidence report          | Sơn                  | Không ghi là việc Thanh làm  |
| 5 Pillars checkpoint document | Sơn                  | Không ghi là việc Thanh làm  |
| Stress/API follow-up          | Sau integration      | Chưa đánh dấu hoàn tất       |

## 8. Tin nhắn ngắn có thể gửi team

```text
Tuần 4 phần của anh đã train baseline thật trên monthly all-areas: normalize schema, tạo feature theo area/thời gian, split temporal, train Random Forest, lưu best model + metadata + feature importance. Kết quả hiện là baseline thật, MAE khoảng 13.9k VND/kg, RMSE khoảng 17.3k VND/kg, R² âm nên mình sẽ nói rõ limitation. Điểm chính là pipeline model đã chạy end-to-end và có feature importance để giải thích.
```
