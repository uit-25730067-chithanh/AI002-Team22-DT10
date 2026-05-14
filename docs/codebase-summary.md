# 🗂 Tóm tắt Cấu trúc Code (Codebase Summary)

**Trạng thái:** Real Data Baseline + API Contract — **ĐANG TÍCH HỢP**
**Cập nhật:** 2026-05-13

---

## Kiến trúc Thư mục

### `backend/` — API Server (Team 2)

| File                    | Mô tả                                                                                                                                 | Trụ cột AI liên quan                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `main.py`               | FastAPI entry point; import fallback để chạy từ root hoặc `backend/`                                                                  | —                                                             |
| `api/routes.py`         | 3 endpoint: `/health`, `/predict`, `/model/info`                                                                                      | Robustness (Pydantic validate), Transparency (trả giải thích) |
| `schemas/prediction.py` | Pydantic models: `PredictionRequest`, `PredictionResponse`, `FeatureExplanation`                                                      | Robustness (range + enum validation)                          |
| `services/predictor.py` | `PredictorService`: load best model, validate trained categories, map feature row theo metadata, predict + CI, explain top 3 features | Transparency, Reliability, Robustness                         |

### `model/` — AI/ML Pipeline (Team 2)

| File               | Mô tả                                                                                                                        | Trụ cột AI liên quan      |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| `preprocess.py`    | Normalize real monthly schema, fill missing, cap outliers, feature engineer theo `area`, one-hot categorical, temporal split | Robustness                |
| `train_rf.py`      | Train Random Forest baseline; đánh giá MAE/RMSE/R²; lưu feature names, feature importance và promote `model/best_model`      | Reliability, Transparency |
| `train_xgboost.py` | So sánh XGBoost optional trong venv riêng; graceful fallback khi thiếu libomp                                                | Reliability               |
| `stress_test.py`   | Inject Black Swan (price crash, heat wave); đo MAE lift so với baseline, chủ yếu phục vụ evaluation                          | Robustness                |
| `best_model/`      | Metadata và model artifact được promote cho API                                                                              | Traceability              |

### `data/processed/` — Dữ liệu thật đã xử lý

| File/Folder                                                  | Mô tả                                                 |
| ------------------------------------------------------------ | ----------------------------------------------------- |
| `monthly/coffee_environment_all_areas_monthly_2022_2025.csv` | Dataset chính dùng train baseline real-data hiện tại  |
| `weekly/coffee_environment_all_areas_weekly_2022_2025.csv`   | Dataset weekly để tham khảo hoặc thử nghiệm tương lai |
| `area_real_price_data_ranking.csv`                           | Xếp hạng độ phủ giá thật theo khu vực                 |
| `FIELD_DESCRIPTIONS.md`                                      | Mô tả schema processed data                           |

### `scripts/` — Tiện ích

| File                    | Mô tả                                                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------------------------ |
| `generate_mock_data.py` | Sinh 1200 dòng mock data (Tây Nguyên, 2022-2025); inject ~5% NaN + ~2% outliers; ghi chú regional bias |

### `tests/ai-tests/` — Kiểm thử

| File                        | Mô tả                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------ |
| `test_predictor_service.py` | Kiểm tra PredictorService load model và trả đủ keys; `pytest.skip` khi model chưa có |

### `docs/discussions/` — Tài liệu nội bộ

| File                                        | Mô tả                                                        |
| ------------------------------------------- | ------------------------------------------------------------ |
| `5-pillars-checkpoint.md`                   | Kiểm điểm 5 trụ cột Sustainable AI (tiếng Việt)              |
| `robustness-stress-test.md`                 | Báo cáo stress test tự động sinh bởi `stress_test.py`        |
| `2026-05-13-team-data-flow-roadmap.md`      | Roadmap luồng dữ liệu thật từ crawler đến model/API/frontend |
| `2026-05-13-api-handoff-team2-real-data.md` | API handoff contract `/predict` cho frontend                 |

### `plans/team2-foundation-week/` — Kế hoạch

| File                                       | Mô tả                                                |
| ------------------------------------------ | ---------------------------------------------------- |
| `plan.md`                                  | Tổng quan foundation week + tracker                  |
| `phase-03-api-skeleton-5-pillars-check.md` | Chi tiết Phase 3 (API skeleton + kiểm tra 5 trụ cột) |
