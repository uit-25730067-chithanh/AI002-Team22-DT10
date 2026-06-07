# 🗂 Tóm tắt Cấu trúc Code (Codebase Summary)

**Trạng thái:** Independent Data Baseline + Protected API Contract + React Frontend + Maintainability Cleanup.
**Cập nhật:** 2026-06-07

---

## Kiến trúc Thư mục

### `backend/` — API Server (Team 2)

| File | Mô tả | Trụ cột AI liên quan |
| --- | --- | --- |
| `main.py` | FastAPI entry point; import fallback để chạy từ root hoặc `backend/` | — |
| `api/routes.py` | Endpoint `/health`, `/predict`, `/model/info`; `/predict` và `/model/info` yêu cầu header `X-API-Key` | Robustness, Transparency |
| `schemas/prediction.py` | `PredictionRequest`, `PredictionResponse`, `FeatureExplanation` | Robustness |
| `services/predictor.py` | Facade load model, build feature row, predict + CI, explain top 3 features | Reliability, Robustness, Transparency |
| `services/farming_advisory.py` | Rule-based khuyến nghị canh tác theo tháng, lượng mưa và chất lượng đất | Social Impact, Robustness |

### `model/` — AI/ML Pipeline (Team 2)

| File | Mô tả | Trụ cột AI liên quan |
| --- | --- | --- |
| `preprocess.py` | Wrapper backward-compatible cho pipeline real-data | Robustness |
| `train_rf.py` | Train Random Forest baseline; đánh giá MAE/RMSE/R²; promote model tốt nhất theo scope `rf_real` hoặc `rf_independent` | Reliability, Transparency |
| `train_xgboost.py` | XGBoost comparison optional trong venv riêng | Reliability |
| `stress_test.py` | CLI stress test, inject Black Swan scenarios và ghi report | Robustness |
| `experiment_tracker.py` | Create/list experiments, save artifacts/metrics/params, promote best model | Traceability |
| `best_model/` | Metadata và model artifact được promote cho API | Traceability |

### `crawler/` — Crawl và Build Dataset

| File | Mô tả |
| --- | --- |
| `crawl_coffee_prices.py` | CLI crawl chính, orchestrate sitemap/seed/url file và xuất CSV theo area |
| `price_crawler_common.py` | Shared parser/helpers: parse date, price/change, article rows, area mapping |
| `area_dataset_builder.py` | Build weekly/monthly processed datasets từ raw price/weather/soil |
| `build_area_datasets.py` | CLI wrapper cho dataset builder |
| `build_soil_profile.py` | Sinh static soil profile theo vùng cà phê |
| `crawl_weather_by_area.py` | Crawl daily weather theo area |
| `coffee_areas.py` | Danh sách vùng cà phê, tọa độ và soil metadata |
| `independent_data_contract.py` | Contract schema và mốc thời gian cho dataset độc lập |
| `source_manifest_independent.json` | Seed/source manifest cho crawl độc lập |
| `run_independent_price_crawlers.py` | Runner crawl giá độc lập theo manifest |
| `build_independent_area_datasets.py` | CLI tạo processed dataset độc lập |
| `independent_data_audit.py` | Audit độ phủ, range baseline và ranking area độc lập |
| `independent_data_quality.py` | Helper kiểm tra chất lượng dataset độc lập |

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
| `test_independent_data_contract.py` | Kiểm tra contract dataset độc lập |
| `test_independent_model_training.py` | Kiểm tra chọn range baseline và promote `rf_independent` |
| `test_stress_test_cli_structure.py` | Regression test cho CLI stress test |

### `docs/` — Tài liệu vận hành và bàn giao

| File | Mô tả |
| --- | --- |
| `README.md` | Chỉ mục tài liệu theo vai trò và nhu cầu đọc |
| `project-roadmap.md` | Trạng thái milestone hiện tại |
| `discussions/2026-06-07-independent-five-pillars-checkpoint.md` | Checkpoint 5 trụ cột với dataset/model độc lập |
| `discussions/2026-06-07-independent-model-results.md` | Kết quả train RF độc lập và quyết định promote |
| `deployment.md` | Tổng quan deploy Render backend + Cloudflare frontend |
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
