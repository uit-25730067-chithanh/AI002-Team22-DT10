# 🗂 Tóm tắt Cấu trúc Code (Codebase Summary)

**Trạng thái:** Foundation Week (Phase 1-3) — **HOÀN THÀNH**  
**Cập nhật:** 2026-04-26

---

## Kiến trúc Thư mục

### `backend/` — API Server (Team 2)

| File                    | Mô tả                                                                                | Trụ cột AI liên quan                                          |
| ----------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| `main.py`               | FastAPI entry point; import fallback để chạy từ root hoặc `backend/`                 | —                                                             |
| `api/routes.py`         | 3 endpoint: `/health`, `/predict`, `/model/info`                                     | Robustness (Pydantic validate), Transparency (trả giải thích) |
| `schemas/prediction.py` | Pydantic models: `PredictionRequest`, `PredictionResponse`, `FeatureExplanation`     | Robustness (ràng buộc range)                                  |
| `services/predictor.py` | `PredictorService`: load .pkl, transform input, predict + CI, explain top 3 features | Transparency, Reliability                                     |

### `model/` — AI/ML Pipeline (Team 2)

| File               | Mô tả                                                                                                       | Trụ cột AI liên quan      |
| ------------------ | ----------------------------------------------------------------------------------------------------------- | ------------------------- |
| `preprocess.py`    | Fill missing, remove outliers (IQR/Z-score), feature engineer (month_sin/cos, lag, rolling), temporal split | Robustness                |
| `train_rf.py`      | Train Random Forest baseline; đánh giá MAE/RMSE/R²; lưu .pkl + plot feature importance                      | Reliability, Transparency |
| `train_xgboost.py` | So sánh XGBoost (optional); graceful fallback khi thiếu libomp                                              | Reliability               |
| `stress_test.py`   | Inject Black Swan (price crash, heat wave); đo MAE lift so với baseline                                     | Robustness                |
| `saved/`           | Chứa `rf_baseline.pkl` và `feature_importance_rf.png`                                                       | —                         |

### `scripts/` — Tiện ích

| File                    | Mô tả                                                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------------------------ |
| `generate_mock_data.py` | Sinh 1200 dòng mock data (Tây Nguyên, 2022-2025); inject ~5% NaN + ~2% outliers; ghi chú regional bias |

### `tests/ai-tests/` — Kiểm thử

| File                        | Mô tả                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------ |
| `test_predictor_service.py` | Kiểm tra PredictorService load model và trả đủ keys; `pytest.skip` khi model chưa có |

### `docs/discussions/` — Tài liệu nội bộ (Ignored by Git)

| File                        | Mô tả                                                 |
| --------------------------- | ----------------------------------------------------- |
| `5-pillars-checkpoint.md`   | Kiểm điểm 5 trụ cột Sustainable AI (tiếng Việt)       |
| `robustness-stress-test.md` | Báo cáo stress test tự động sinh bởi `stress_test.py` |

### `plans/team2-foundation-week/` — Kế hoạch

| File                                       | Mô tả                                                |
| ------------------------------------------ | ---------------------------------------------------- |
| `plan.md`                                  | Tổng quan foundation week + tracker                  |
| `phase-03-api-skeleton-5-pillars-check.md` | Chi tiết Phase 3 (API skeleton + kiểm tra 5 trụ cột) |
