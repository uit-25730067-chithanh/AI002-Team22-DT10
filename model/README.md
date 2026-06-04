# 🧠 Model (Machine Learning Core)

Thư mục chịu trách nhiệm huấn luyện (Training), tiền xử lý (Preprocessing), đánh giá (Evaluation) và quản lý vòng đời (Experiment Tracking) cho mô hình AI dự báo giá cà phê của Team 2.

## 1. Vai trò

- Làm sạch dữ liệu từ thư mục `data/processed/`.
- Thực thi pipeline chia tập dữ liệu (Temporal Split) để tránh Data Leakage (không dùng giá tương lai để đoán quá khứ).
- Huấn luyện thuật toán (Random Forest, XGBoost) và ghi nhận lại các bản ghi thực nghiệm.
- Lựa chọn mô hình tốt nhất (Best Model) để Promote đưa vào sản xuất (cho Backend sử dụng).
- Kiểm tra độ bền bỉ của mô hình bằng các kịch bản cực đoan (Stress Test / Robustness).

## 2. Sơ đồ luồng xử lý (Data Flow & Architecture)

```mermaid
flowchart TD
    Data[(../data/processed/)] --> Preprocess[preprocess.py\nĐiền Khuyết & Tạo Feature]
    
    Preprocess --> Split[Temporal Split\nTrain / Test]
    Split --> TrainRF[train_rf.py\n(Baseline Random Forest)]
    Split --> TrainXGB[train_xgboost.py\n(Thực nghiệm XGBoost)]
    
    TrainRF --> Tracker[experiment_tracker.py]
    TrainXGB --> Tracker
    
    Tracker -->|Lưu log chạy, metrics, model .pkl| Exps[(experiments/)]
    Tracker -->|Promote tự động model tốt nhất| Best[(best_model/)]
    
    Best --> Stress[stress_test.py\nKiểm tra Robustness]
    Stress -.->|In ra Terminal / Log| Result[Stress Test Reports]
```

## 3. Chức năng các file chính

- **`preprocess.py`**: Chứa các hàm tạo thêm đặc trưng (feature engineering như độ trễ, biến động), xử lý missing values.
- **`train_rf.py`**: Kịch bản chạy mô hình Random Forest làm Baseline, đánh giá (MAE, RMSE, R2), và trích xuất Feature Importance (Tính minh bạch).
- **`train_xgboost.py`**: Script huấn luyện model nâng cao (cần cài đặt XGBoost trong venv).
- **`experiment_tracker.py`**: Hệ thống quản lý thực nghiệm nhẹ nhàng (KISS), tự động log các metrics, siêu tham số và phiên bản mô hình vào `experiments.csv` thay vì phải cài cắm MLflow phức tạp.
- **`stress_test.py`**: Đánh giá hiệu suất mô hình trong các kịch bản Black Swan (sốc nhiệt, hạn hán kéo dài). Đảm bảo trụ cột Robustness.

## 4. Hướng dẫn chạy nhanh

Để chạy huấn luyện mô hình Baseline:

```bash
python model/train_rf.py --data data/processed/monthly/coffee_environment_dak_lak_monthly_2022_2025.csv --tag rf_real_monthly
```

Để chạy Stress Test (Đánh giá khả năng chịu đựng):

```bash
python model/stress_test.py
```

## 5. Roadmap Tiến độ

- [x] Hoàn thiện Pipeline Tiền xử lý
- [x] Implement Random Forest Baseline (Reliability Pillar)
- [x] Xây dựng Experiment Tracking System siêu nhẹ
- [x] Tích hợp Robustness Stress Test
- [x] Tự động Promote "Best Model" cập nhật cho Backend
- [ ] Mở rộng Grid Search để tối ưu siêu tham số Hyperparameters (Tương lai)
