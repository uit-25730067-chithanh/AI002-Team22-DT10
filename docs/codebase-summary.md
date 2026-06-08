# 🗂 Tóm tắt Cấu trúc Code (Codebase Summary)

**Trạng thái:** Canonical Data Baseline + Protected API Contract + React Frontend + Balanced Repo Cleanup.
**Cập nhật:** 2026-06-08

---

## Kiến trúc Thư mục

### `backend/` — API Server

| File | Mô tả | Trụ cột AI liên quan |
| --- | --- | --- |
| `main.py` | FastAPI entry point; import fallback để chạy từ root hoặc `backend/` | — |
| `api/routes.py` | Endpoint `/health`, `/predict`, `/model/info`; `/predict` và `/model/info` yêu cầu header `X-API-Key` | Robustness, Transparency |
| `schemas/prediction.py` | `PredictionRequest`, `PredictionResponse`, `FeatureExplanation` | Robustness |
| `services/predictor.py` | Facade load model, build feature row, predict + CI, explain top 3 features | Reliability, Robustness, Transparency |
| `services/farming_advisory.py` | Rule-based khuyến nghị canh tác theo tháng, lượng mưa và chất lượng đất | Social Impact, Robustness |

### `model/` — AI/ML Pipeline

| File | Mô tả | Trụ cột AI liên quan |
| --- | --- | --- |
| `preprocess.py` | Wrapper backward-compatible cho pipeline real-data | Robustness |
| `train_rf.py` | Train Random Forest baseline; đánh giá MAE/RMSE/R²; promote model tốt nhất theo scope `rf_real` hoặc `rf_monthly` | Reliability, Transparency |
| `stress_test.py` | CLI stress test, inject Black Swan scenarios và ghi report | Robustness |
| `experiment_tracker.py` | Create/list experiments, save artifacts/metrics/params, promote best model | Traceability |
| `best_model/` | Metadata và model artifact được promote cho API | Traceability |

### `crawler/` — Crawl và Build Dataset

| File | Mô tả |
| --- | --- |
| `price_crawler_common.py` | Shared parser/helpers: parse date, price/change, article rows, area mapping |
| `area_dataset_builder.py` | Build monthly dataset chính và weekly reference khi cần từ raw price/weather/soil |
| `build_area_datasets.py` | CLI wrapper cho dataset builder |
| `build_soil_profile.py` | Sinh static soil profile theo vùng cà phê |
| `crawl_weather_by_area.py` | Crawl daily weather theo area |
| `coffee_areas.py` | Danh sách vùng cà phê, tọa độ và soil metadata |
| `coffee_data_contract.py` | Contract schema, mốc thời gian và canonical paths cho dataset chính thức |
| `source_manifest.json` | Seed/source manifest cho crawl từ nguồn public |
| `run_price_crawlers.py` | Runner crawl giá chính theo manifest |
| `data_audit.py` | Audit độ phủ, range baseline và ranking area |
| `data_quality.py` | Helper kiểm tra chất lượng dataset |

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

Không còn script active trong danh sách file chính. Mock data generator và XGBoost comparison cũ đã đưa ra khỏi repo hiện tại vì dataset canonical + Random Forest monthly baseline là luồng hiện tại.

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
| `test_coffee_data_contract.py` | Kiểm tra contract dataset chính thức |
| `test_canonical_model_training.py` | Kiểm tra train/test/demo windows và promote `rf_monthly` |
| `test_stress_test_cli_structure.py` | Regression test cho CLI stress test |

### `docs/` — Tài liệu vận hành và bàn giao

| File | Mô tả |
| --- | --- |
| `README.md` | Chỉ mục tài liệu theo vai trò và nhu cầu đọc |
| `project-roadmap.md` | Trạng thái milestone hiện tại |
| `discussions/robustness-stress-test.md` | Kết quả stress test với baseline hiện tại |
| `deployment.md` | Tổng quan deploy Render backend + Cloudflare frontend |
| `troubleshooting.md` | Lỗi thường gặp khi chạy API/front-end integration |

### `docs/report/` và `docs/slides/` — Báo cáo và thuyết trình

| File/Folder | Mô tả |
| --- | --- |
| `docs/slides/final_presentation_slides.md` | Slides thuyết trình cuối kỳ |
| `docs/report/README.md` | Chỉ mục report và tracked PDF evidence |
| `docs/report/final-ai002-report/` | Cấu trúc báo cáo cuối kỳ chính thức |

### `plans/` — Kế hoạch

| File | Mô tả |
| --- | --- |
| `plans/260608-1551-balanced-repo-cleanup/plan.md` | Kế hoạch cleanup mức Balanced hiện tại |
| `plans/260608-1551-balanced-repo-cleanup/reports/` | Báo cáo kiểm kê, archive và validation theo từng phase |
