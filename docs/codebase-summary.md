# 🗂 Tóm tắt Cấu trúc Code (Codebase Summary)

**Trạng thái:** Real Data Baseline + Protected API Contract + React Frontend.
**Cập nhật:** 2026-06-03

---

## Kiến trúc Thư mục

### `backend/` — API Server (Team 2)

| File                           | Mô tả                                                                                                                                 | Trụ cột AI liên quan                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `main.py`                      | FastAPI entry point; import fallback để chạy từ root hoặc `backend/`                                                                  | —                                                             |
| `api/routes.py`                | Endpoint `/health`, `/predict`, `/model/info`; `/predict` và `/model/info` yêu cầu header `X-API-Key`                                 | Robustness (Pydantic validate), Transparency (trả giải thích) |
| `schemas/prediction.py`        | Pydantic models: `PredictionRequest`, `PredictionResponse`, `FeatureExplanation`                                                      | Robustness (range + enum validation)                          |
| `services/predictor.py`        | `PredictorService`: load best model, validate trained categories, map feature row theo metadata, predict + CI, explain top 3 features | Transparency, Reliability, Robustness                         |
| `services/farming_advisory.py` | `FarmingAdvisoryService`: cung cấp khuyến nghị canh tác theo luật (rule-based) dựa trên tháng, lượng mưa và điểm chất lượng đất       | Social Impact, Robustness                                     |

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

### `frontend/` — Giao diện người dùng di động (Mobile-first UI)

| File/Folder          | Mô tả                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------- |
| `src/app/`           | App shell và routing đơn giản.                                                                    |
| `src/features/`      | Chứa 4 nhóm màn hình/chức năng: welcome/menu, `price-advisory`, `farming-advisory`, và `history`. |
| `src/shared/`        | Các thành phần dùng chung (UI components, constants, types, API client, storage repository).      |
| `src/main.tsx`       | Entry point của ứng dụng React.                                                                   |
| `tailwind.config.js` | Theme coffee/cream/leaf theo phong cách Farmer Neo-Brutal Friendly.                               |
| `vite.config.ts`     | Cấu hình Vite + Vitest cho component tests.                                                       |

### `scripts/` — Tiện ích

| File                    | Mô tả                                                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------------------------ |
| `generate_mock_data.py` | Sinh 1200 dòng mock data (Tây Nguyên, 2022-2025); inject ~5% NaN + ~2% outliers; ghi chú regional bias |

### `tests/ai-tests/` — Kiểm thử

| File                               | Mô tả                                                                                              |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| `test_predictor_service.py`        | Kiểm tra PredictorService load model và trả đủ keys; sử dụng model fixture trong tmp_path để test  |
| `test_best_model_promotion.py`     | Kiểm tra best model promotion chọn đúng real-data run theo metric                                  |
| `test_api_security.py`             | Kiểm tra endpoint public/protected, API key đúng/sai và lỗi thiếu config                           |
| `test_farming_advisory_service.py` | Kiểm tra FarmingAdvisoryService trả về khuyến nghị đúng theo quy tắc lượng mưa, tháng, và điểm đất |

### `docs/discussions/` — Tài liệu nội bộ

| File                                        | Mô tả                                                        |
| ------------------------------------------- | ------------------------------------------------------------ |
| `5-pillars-checkpoint.md`                   | Kiểm điểm 5 trụ cột Sustainable AI (tiếng Việt)              |
| `robustness-stress-test.md`                 | Báo cáo stress test tự động sinh bởi `stress_test.py`        |
| `2026-05-13-team-data-flow-roadmap.md`      | Roadmap luồng dữ liệu thật từ crawler đến model/API/frontend |
| `2026-05-13-api-handoff-team2-real-data.md` | API handoff contract `/predict` cho frontend                 |

### `docs/` — Tài liệu vận hành và bàn giao

| File                 | Mô tả                                                        |
| -------------------- | ------------------------------------------------------------ |
| `README.md`          | Chỉ mục tài liệu theo vai trò và nhu cầu đọc                 |
| `self-host-guide.md` | Hướng dẫn chạy backend local, test API key, systemd và Nginx |
| `troubleshooting.md` | Lỗi thường gặp khi chạy API/front-end integration            |

### `docs/report/` và `docs/slides/` — Báo cáo và thuyết trình

| File/Folder                       | Mô tả                                                        |
| --------------------------------- | ------------------------------------------------------------ |
| `docs/slides/`                    | Slides thuyết trình cuối kỳ (`final_presentation_slides.md`) |
| `docs/report/README.md`           | Chỉ mục report notes theo roadmap, owner và trạng thái       |
| `docs/report/internal-notes/`     | Báo cáo tiến độ nội bộ theo tuần (Week 1-6)                  |
| `docs/report/final-ai002-report/` | Cấu trúc báo cáo cuối kỳ chính thức (Chương 1-6)             |

### `plans/team2-foundation-week/` — Kế hoạch

| File                                       | Mô tả                                                |
| ------------------------------------------ | ---------------------------------------------------- |
| `plan.md`                                  | Tổng quan foundation week + tracker                  |
| `phase-03-api-skeleton-5-pillars-check.md` | Chi tiết Phase 3 (API skeleton + kiểm tra 5 trụ cột) |
