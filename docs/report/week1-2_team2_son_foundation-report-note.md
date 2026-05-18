# Note báo cáo phần việc của Sơn gửi Phúc / Team 1 - Foundation Week 1-2

**Ngày:** 2026-05-10  
**Người báo cáo:** Sơn  
**Người nhận chính:** Phúc / Team 1  
**Phạm vi:** Chỉ tổng kết các phần Sơn đã làm trong foundation week  
**Lưu ý:** Thanh sẽ tự báo cáo phần của Thanh, nên note này không gom chung toàn bộ việc Team 2.

## 1. Tóm tắt ngắn để nói với Phúc

Anh đã làm các phần nền tảng thuộc nhánh kỹ thuật AI/backend để khi em Phúc có data thật thì Team 2 có thể thay vào chạy lại nhanh. Phần của anh tập trung vào mock data, preprocessing, train Random Forest baseline, stress test Robustness, predictor service cho API, và checkpoint 5 trụ cột AI.

## 2. Roadmap phần Sơn đã làm

| Giai đoạn | Việc Sơn làm | Mục tiêu | Trạng thái |
| --- | --- | --- | --- |
| Phase 1 | Tạo mock dataset | Có data giả lập để không chờ crawler thật | Xong |
| Phase 2 | Viết preprocessing pipeline | Làm sạch data, tạo feature, split train/test | Xong |
| Phase 2 | Train Random Forest baseline | Có model baseline + metrics + feature importance | Xong |
| Phase 2 | Stress test Robustness | Đo model phản ứng khi gặp biến động cực đoan | Xong |
| Phase 3 | Viết `PredictorService` | Load model, predict, giải thích top features | Xong |
| Phase 3 | Viết checkpoint 5 pillars | Có bằng chứng cho slide/báo cáo cuối kỳ | Xong |

## 3. Chi tiết công việc đã hoàn thành

### 3.1. Mock dataset cho Team 2 test pipeline

| Nội dung | Chi tiết |
| --- | --- |
| Việc đã làm | Tạo mock dataset mô phỏng giá cà phê + thời tiết |
| Quy mô | 1200 dòng |
| Mục đích | Train/test pipeline khi chưa có data thật từ Team 1 |
| Robustness | Có thêm khoảng 5% missing values và 2% outliers |
| Bias note | Mock data giả định vùng Tây Nguyên, không đại diện toàn quốc |
| File liên quan | `scripts/generate_mock_data.py`, `data/sample/mock_coffee_sample.csv` |

**Điểm cần báo em Phúc:** mock data chỉ dùng để dựng khung kỹ thuật. Khi em Phúc gửi data thật, anh sẽ thay vào pipeline và chạy lại toàn bộ metrics.

### 3.2. Preprocessing pipeline

| Hạng mục | Cách xử lý |
| --- | --- |
| Missing values | Điền bằng median cho cột số |
| Outliers | Lọc bằng IQR hoặc Z-score |
| Seasonality | Tạo `month_sin`, `month_cos` |
| Short-term trend | Tạo `rolling_avg_7d` |
| Historical signal | Tạo `lag_1d`, `lag_7d` |
| Train/test split | Chia theo thời gian, tránh data leakage |

**File liên quan:** `model/preprocess.py`

**Giá trị báo cáo:** phần này cover trực tiếp **Robustness** và **Reliability** vì data được làm sạch, tạo feature nhất quán, và split theo thời gian thay vì random shuffle.

### 3.3. Train Random Forest baseline

| Nội dung | Kết quả |
| --- | --- |
| Model | `RandomForestRegressor` |
| Input | Mock coffee data sau preprocessing |
| Metrics | MAE, RMSE, R² |
| Transparency | Có feature importance |
| Experiment tracking | Mỗi lần train tạo experiment folder, lưu metrics/params/model |
| Best model | Có cập nhật `model/best_model/` |

**File liên quan:**

| File | Vai trò |
| --- | --- |
| `model/train_rf.py` | Train model baseline và in metrics |
| `model/experiment_tracker.py` | Theo dõi experiment |
| `model/experiments.csv` | Lưu lịch sử experiment |
| `model/best_model/metadata.json` | Metadata model tốt nhất |

**Điểm cần nói rõ:** metrics hiện tại là trên mock data, chưa phải kết quả cuối. Sau khi có data thật từ em Phúc, anh sẽ train lại và cập nhật số liệu thật cho slide.

### 3.4. Stress test Robustness

| Kịch bản | MAE | RMSE | Nhận xét |
| --- | ---: | ---: | --- |
| Baseline bình thường | 2,538 VND/kg | 3,170 VND/kg | Model ổn trong phân bố lịch sử |
| `price_crash` | 4,778 VND/kg | 7,895 VND/kg | MAE tăng 88.3%, RMSE tăng 149.1% |
| `heat_wave` | 2,535 VND/kg | 3,166 VND/kg | Gần như không đổi trên mock data |
| `both` | 4,743 VND/kg | 7,766 VND/kg | MAE tăng 86.9%, RMSE tăng 145.0% |

**File liên quan:**

| File | Vai trò |
| --- | --- |
| `model/stress_test.py` | Chạy stress test |
| `docs/discussions/robustness-stress-test.md` | Báo cáo kết quả stress test |

**Thông điệp cho slide:** model hoạt động được trong điều kiện bình thường, nhưng khi thị trường biến động cực đoan thì sai số tăng mạnh. Vì vậy UI nên có cảnh báo để người dùng không xem dự báo là quyết định duy nhất.

### 3.5. Predictor service cho backend

| Nội dung | Chi tiết |
| --- | --- |
| Service | `PredictorService` |
| Chức năng chính | Load model, build feature row, predict giá |
| Output | Giá dự đoán, confidence interval, top features, model version |
| Transparency | Trả về top 3 feature importance để giải thích dự đoán |
| Robustness | Báo lỗi rõ nếu model chưa load được |

**File liên quan:** `backend/services/predictor.py`

**Điểm cần báo em Phúc:** phần route/API contract có thể Team 1 dùng để chuẩn bị UI, nhưng phần anh làm chính là service xử lý predict bên dưới API.

### 3.6. Checkpoint 5 trụ cột AI

| Trụ cột | Phần Sơn đóng góp | Bằng chứng |
| --- | --- | --- |
| Reliability | Train/test theo thời gian, metrics MAE/RMSE/R² | `model/train_rf.py` |
| Bias | Ghi nhận giới hạn data Tây Nguyên | Mock data + note trong checkpoint |
| Robustness | Missing/outlier handling + stress test | `model/preprocess.py`, `model/stress_test.py` |
| Social Impact | Đề xuất cảnh báo để nông dân chỉ dùng AI tham khảo | `docs/discussions/5-pillars-checkpoint.md` |
| Transparency | Feature importance + top feature explanations | `model/train_rf.py`, `backend/services/predictor.py` |

**File liên quan:** `docs/discussions/5-pillars-checkpoint.md`

## 4. Những điểm Sơn cần nhờ Phúc / Team 1 phối hợp

| Việc cần từ em Phúc | Lý do cần | Mức ưu tiên |
| --- | --- | --- |
| Gửi sample data thật 20-50 dòng sớm | Anh test xem pipeline có đọc được không | Cao |
| Xác nhận format CSV | Tránh lệch tên cột khi train lại | Cao |
| Xác nhận nguồn giá cà phê | Biết giá nội địa Tây Nguyên hay giá quốc tế quy đổi | Cao |
| Xác nhận tần suất data | Pipeline hiện ưu tiên dữ liệu theo ngày | Cao |
| Báo sớm nếu thiếu cột thời tiết | Anh chỉnh preprocessing/model input kịp | Cao |
| Thêm disclaimer trên UI | Cover Bias + Social Impact | Trung bình |

## 5. Format data anh cần em Phúc lưu ý

| Cột | Ý nghĩa | Ghi chú |
| --- | --- | --- |
| `date` | Ngày ghi nhận | Ưu tiên `YYYY-MM-DD` |
| `avg_temp_c` | Nhiệt độ trung bình | Nếu thiếu cần báo sớm |
| `rainfall_mm` | Lượng mưa | Nếu không có theo ngày cần báo rõ |
| `humidity_pct` | Độ ẩm | Có thể xử lý thiếu, nhưng nên có |
| `sunshine_hours` | Số giờ nắng | Có thể thiếu, nhưng cần thống nhất |
| `month` | Tháng | Có thể tự sinh từ `date` nếu cần |
| `historical_price_vnd` | Giá cà phê VND/kg | Cột quan trọng nhất |

**Tài liệu tham chiếu:** `docs/discussions/data-format-spec.md`

## 6. Roadmap tiếp theo sau khi nhận data thật

| Bước | Việc Sơn sẽ làm | Output |
| --- | --- | --- |
| 1 | Nhận sample data thật từ em Phúc | Kiểm tra format |
| 2 | Chạy preprocessing trên data thật | Báo lỗi thiếu cột/missing/outlier nếu có |
| 3 | Train lại Random Forest | Metrics thật: MAE/RMSE/R² |
| 4 | Cập nhật feature importance | Dữ liệu cho phần Transparency |
| 5 | Chạy lại stress test | Số liệu Robustness thật |
| 6 | Kiểm tra `PredictorService` với model thật | API predict dùng được cho frontend |
| 7 | Gửi số liệu cuối cho slide | Team 1 đưa vào báo cáo/thuyết trình |

## 7. Kết luận

Phần anh đã hoàn thành đủ foundation kỹ thuật để chuyển từ mock data sang data thật. Rủi ro lớn nhất hiện tại là data thật từ Team 1 thiếu cột, sai format, hoặc không đủ theo ngày. Việc cần ưu tiên bây giờ là em Phúc gửi sample data thật sớm để anh kiểm tra và train lại model.
