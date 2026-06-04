# 🗂 Tóm tắt Cấu trúc Code (Codebase Summary)

**Trạng thái:** Real Data Baseline + Protected API Contract + React Frontend + Maintainability Cleanup.
**Cập nhật:** 2026-06-04

---

## Kiến trúc Thư mục

### `backend/` — API Server (Team 2)

| File | Mô tả | Trụ cột AI liên quan |
| --- | --- | --- |
| `main.py` | FastAPI entry point; import fallback để chạy từ root hoặc `backend/` | — |
| `api/routes.py` | Endpoint `/health`, `/predict`, `/model/info`; `/predict` và `/model/info` yêu cầu header `X-API-Key` | Robustness, Transparency |
| `schemas/prediction.py` | `PredictionRequest`, `PredictionResponse`, `FeatureExplanation` | Robustness |
| `services/predictor.py` | Facade load model, build feature row, predict + CI, explain top 3 features | Reliability, Robustness, Transparency |
| `services/prediction_features.py` | Build feature row, validate trained categories, one-hot mapping | Robustness, Transparency |
| `services/prediction_explanations.py` | Trích xuất top feature importances cho response | Transparency |
| `services/farming_advisory.py` | Rule-based khuyến nghị canh tác theo tháng, lượng mưa và chất lượng đất | Social Impact, Robustness |

### `model/` — AI/ML Pipeline (Team 2)

| File | Mô tả | Trụ cột AI liên quan |
| --- | --- | --- |
| `preprocess.py` | Wrapper backward-compatible cho pipeline real-data | Robustness |
| `preprocess_schema.py` | Normalize schema, rename cột, validate metadata | Robustness |
| `preprocess_features.py` | Fill missing, cap outliers, feature engineering | Robustness |
| `preprocess_encoding.py` | One-hot encode và split temporal | Robustness |
| `train_rf.py` | Train Random Forest baseline; đánh giá MAE/RMSE/R²; promote model tốt nhất | Reliability, Transparency |
| `train_xgboost.py` | XGBoost comparison optional trong venv riêng | Reliability |
| `stress_test.py` | CLI stress test wrapper | Robustness |
| `stress_scenarios.py` | Inject Black Swan scenarios | Robustness |
| `stress_reporting.py` | Markdown report generator cho stress test | Robustness |
| `experiment_tracker.py` | Compatibility facade cho registry/artifact/best-model helpers | Traceability |
| `experiment_utils.py` | Paths, hashes, timestamps, git metadata | Traceability |
| `experiment_registry.py` | Append/list experiments CSV | Traceability |
| `experiment_artifacts.py` | Create experiment folder, save metrics/params/artifacts | Traceability |
| `best_model_promotion.py` | Chọn và promote model tốt nhất từ registry | Traceability |
| `best_model/` | Metadata và model artifact được promote cho API | Traceability |

### `crawler/` — Crawl và Build Dataset

| File | Mô tả |
| --- | --- |
| `crawl_coffee_prices.py` | CLI crawl chính, orchestrate sitemap/seed/url file và xuất CSV theo area |
| `price_crawler_common.py` | Shared async crawl helpers, fetch, run_site, CLI glue |
| `price_html_parsers.py` | Parse article HTML/table/text thành rows giá |
| `price_date_parsing.py` | Parse ngày từ URL/meta |
| `price_normalization.py` | Normalize tên area, parse price/change, ánh xạ vùng |
| `price_csv_io.py` | Append/finalize/merge CSV outputs |
| `price_crawler_discovery.py` | Discover URLs từ sitemap và search |
| `area_dataset_builder.py` | CLI build weekly/monthly processed datasets |
| `area_dataset_helpers.py` | Helper load/aggregate/fill missing cho dataset builder |

### `frontend/` — Giao diện người dùng di động (Mobile-first UI)

| File/Folder | Mô tả |
| --- | --- |
| `src/app/` | App shell và routing đơn giản |
| `src/features/` | welcome/menu, `price-advisory`, `farming-advisory`, `history` |
| `src/shared/` | UI components, constants, types, API client, storage repository |
| `src/main.tsx` | Entry point của ứng dụng React |
| `tailwind.config.js` | Theme coffee/cream/leaf |
| `vite.config.ts` | Cấu hình Vite + Vitest |

### `scripts/` — Tiện ích

| File | Mô tả |
| --- | --- |
| `generate_mock_data.py` | Sinh 1200 dòng mock data (Tây Nguyên, 2022-2025); inject NaN + outliers; ghi chú regional bias |

### `tests/ai-tests/` — Kiểm thử

| File | Mô tả |
| --- | --- |
| `test_predictor_service.py` | Kiểm tra PredictorService load model và trả đủ keys |
| `test_best_model_promotion.py` | Kiểm tra best model promotion chọn đúng real-data run |
| `test_api_security.py` | Kiểm tra endpoint public/protected, API key và lỗi thiếu config |
| `test_farming_advisory_service.py` | Kiểm tra rule-based farming advice |
| `test_experiment_registry.py` | Kiểm tra registry CSV helper |
| `test_experiment_artifacts.py` | Kiểm tra artifact helper |
| `test_crawler_price_normalization.py` | Kiểm tra normalize/parse helper |
| `test_crawler_area_dataset_builder.py` | Kiểm tra build dataset helper |
| `test_price_html_parsers.py` | Kiểm tra date parsing và parse_article mẫu |

### `docs/` — Tài liệu vận hành và bàn giao

| File | Mô tả |
| --- | --- |
| `README.md` | Chỉ mục tài liệu theo vai trò và nhu cầu đọc |
| `project-roadmap.md` | Trạng thái milestone hiện tại |
| `deployment.md` | Tổng quan deploy Render backend + Cloudflare frontend |
| `self-host-guide.md` | Hướng dẫn chạy API local/self-host |
| `troubleshooting.md` | Lỗi thường gặp khi chạy API/front-end integration |

### `docs/report/` và `docs/slides/` — Báo cáo và thuyết trình

| File/Folder | Mô tả |
| --- | --- |
| `docs/slides/final_presentation_slides.md` | Slides thuyết trình cuối kỳ |
| `docs/report/README.md` | Chỉ mục report notes và tracked PDF evidence |
| `docs/report/internal-notes/` | Báo cáo tiến độ nội bộ theo tuần (archive evidence) |
| `docs/report/final-ai002-report/` | Cấu trúc báo cáo cuối kỳ chính thức |

### `plans/` — Kế hoạch

| File | Mô tả |
| --- | --- |
| `plans/260604-1026-ai002-maintainability-cleanup-and-refactor/plan.md` | Kế hoạch cleanup/refactor hiện tại |
| `plans/260604-1026-ai002-maintainability-cleanup-and-refactor/reports/` | Baseline, validation, handoff và các report liên quan |
