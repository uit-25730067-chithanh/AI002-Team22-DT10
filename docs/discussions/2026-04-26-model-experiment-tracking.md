# Thiết kế: Experiment Tracking cho Model Training (KISS)

> **Ngày:** 2026-04-26
> **Người yêu cầu:** Thanh (Lead Team 2)
> **Phạm vi:** Pipeline train/test model (`model/train_rf.py`, `model/train_xgboost.py`, `model/stress_test.py`)

---

## 1. Vấn đề hiện tại

- Mỗi lần train ghi đè `model/saved/rf_baseline.pkl` và `feature_importance_rf.png`.
- Không trace được metrics lịch sử (MAE/RMSE/R²).
- Stress test ghi đè `docs/discussions/robustness-stress-test.md`.
- Không so sánh được RF vs XGBoost qua nhiều lần chạy.

---

## 2. Các phương án đã xem xét

| Phương án                        | Ưu                                                 | Nhược                                         |
| -------------------------------- | -------------------------------------------------- | --------------------------------------------- |
| **A. Timestamped Folder + JSON** | 0 dependency; dễ review; dễ rollback; phù hợp KISS | Không UI dashboard                            |
| **B. MLflow (Local)**            | UI so sánh runs; track params chuyên nghiệp        | Thêm dependency; cần server; overkill 1 tháng |
| **C. Weights & Biases**          | Dashboard online đẹp                               | Cần API key; phụ thuộc internet               |

**Quyết định: Phương án A (KISS)** — đúng tinh thần project AI002, dễ chứng minh 5 Trụ cột, Team 1 review không cần cài tool.

---

## 3. Cấu trúc thư mục mới

```
model/
├── experiments/
│   ├── 2026-04-26_154322__rf_baseline/
│   │   ├── rf_baseline.pkl
│   │   ├── feature_importance.png
│   │   ├── metrics.json
│   │   ├── params.json
│   │   └── predictions.csv (tùy chọn)
│   └── ...
├── best_model/
│   ├── model.pkl       ← symlink/copy từ experiment tốt nhất
│   └── metadata.json
└── experiments.csv     ← tổng hợp nhanh toàn bộ lịch sử
```

**Quy tắc đặt tên:** `{YYYYMMDD}_{HHMMSS}__{tag}` (tag mặc định từ script name).

---

## 4. File artifacts

### `metrics.json`

```json
{
  "mae": 1234.56,
  "rmse": 2345.67,
  "r2": 0.8543,
  "train_size": 730,
  "test_size": 365
}
```

### `params.json`

```json
{
  "timestamp": "2026-04-26T15:43:22",
  "git_commit": "abc1234",
  "data_path": "data/sample/mock_coffee_sample.csv",
  "data_hash": "md5:...",
  "model_params": { "n_estimators": 100, "random_state": 42 }
}
```

### `experiments.csv`

| experiment_id                    | timestamp | tag         | model_type            | mae  | rmse | r2   | best  |
| -------------------------------- | --------- | ----------- | --------------------- | ---- | ---- | ---- | ----- |
| 2026-04-26_154322\_\_rf_baseline | ...       | rf_baseline | RandomForestRegressor | 1234 | 2345 | 0.85 | False |

Script tự động append dòng mới. Nếu MAE thấp nhất lịch sử → copy model vào `best_model/`.

---

## 5. Thay đổi cần code

1. **Thêm `model/experiment_tracker.py`** — module chung: tạo folder, ghi JSON/CSV, cập nhật `best_model/`.
2. **Sửa `train_rf.py`** — dùng tracker, trả về experiment_id.
3. **Sửa `train_xgboost.py`** — dùng tracker tương tự.
4. **Sửa `stress_test.py`** — lưu report vào `experiments/{id}/stress_report.md` thay vì `docs/discussions/`.
5. **Xóa `model/saved/`** (hoặc để legacy).

---

## 6. Lợi ích với 5 Trụ cột AI

- **Reliability:** Trace metrics qua từng ngày, biết model nào stable.
- **Transparency:** Mỗi experiment có params.json đầy đủ, có thể reproduce.
- **Robustness:** Stress test lưu riêng từng experiment, so sánh baseline vs stress dễ dàng.

---

## 7. Migration path

- Bước 1: Viết `experiment_tracker.py` + refactor `train_rf.py`.
- Bước 2: Refactor `train_xgboost.py` và `stress_test.py`.
- Bước 3: (Tùy chọn sau này) Parse `experiments.csv` → import vào MLflow nếu cần "lên đời".
