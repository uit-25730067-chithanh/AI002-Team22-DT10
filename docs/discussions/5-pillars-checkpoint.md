# Kiểm điểm 5 Trụ cột AI (Real Data Week)

**Ngày:** 2026-05-13
**Người cập nhật:** Sơn
**Phạm vi:** Team 2 real data model week - Phase 4
**Nguồn số liệu:** PR #9 và note kiểm toán `docs/discussions/2026-05-13-real-data-audit-team2-son.md`
**PR #9 status:** Merged 2026-05-14 local time, merge commit `e50e8a691c8aac89edce058fbf41a3cd70af913a`

## Tóm tắt bằng chứng dữ liệu thật

Team 2 đã chuyển từ mock data sang real processed data cho baseline chính:

- Dataset chính: `data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv`.
- Monthly dataset: **576** rows, **16** columns, **498/576** rows có observed price (**86.5%**).
- Weekly dataset: **2,520** rows, **1,831/2,520** rows có observed price (**72.7%**), dùng cho phân tích phụ.
- Model baseline: Random Forest `20260513_155830__rf_real_monthly` sau PR #14.
- Split: train 2022-2024, test 2025.

## Bảng chứng minh (Ma trận bằng chứng)

| Trụ cột           | Bằng chứng dữ liệu thật                                                                                                                                                                      | File liên quan                                                                                               | Rủi ro còn lại                                                                                    |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| **Reliability**   | Có split temporal train 2022-2024/test 2025; metrics thật: MAE **13,552 VND/kg**, RMSE **16,754 VND/kg**, R² **-0.9044**                                                                     | `model/train_rf.py`, `model/best_model/metadata.json`, PR #9/#14                                                 | R² âm cho thấy giá 2025 lệch mạnh; baseline chưa phải model final                                 |
| **Bias**          | Kiểm toán độ phủ area-row theo tỉnh: Lam Dong/Kon Tum mạnh, Dak Lak/Gia Lai dùng được, Dak Nong yếu                                                                                          | `docs/discussions/2026-05-13-real-data-audit-team2-son.md`, `data/processed/AREA_REAL_PRICE_DATA_RANKING.md` | Không áp dụng bừa cho vùng ngoài Tây Nguyên; không demo chính bằng Dak R'lap                      |
| **Robustness**    | Đã stress test gây nhiễu tập Test 2025: price_crash (MAE +66.5%), heat_wave (MAE +0.0%). Pydantic validate range/type và allowed-value validation trong PredictorService tránh input ngoài tập train. | model/preprocess.py, backend/schemas/prediction.py, backend/services/predictor.py, model/stress_test.py | Dữ liệu cực đoan như giá sụp đổ (price crash) làm MAE tăng 66.5%, mô hình cần thêm cơ chế cảnh báo khi giá trượt. |
| **Social Impact** | Dự báo giúp nông dân nhỏ lẻ có thêm tham khảo về giá cà phê và tránh phụ thuộc một nguồn thông tin                                                                                           | `README.md`, `docs/discussions/2026-05-13-api-handoff-team2-real-data.md`                                    | Không dùng như lời khuyên giao dịch bắt buộc; UI phải hiển thị disclaimer                         |
| **Transparency**  | Metadata có 41 features và top feature importance; top features là `rolling_avg_7d`, `lag_1d`, `year`, `month`, `month_sin`                                                               | `model/best_model/metadata.json`, `model/train_rf.py`                                                        | Model đang phụ thuộc mạnh vào lag/rolling price context, cần giải thích rõ                        |

## Reliability

| Metric        |                              Value |
| ------------- | ---------------------------------: |
| Experiment    | `20260513_155830__rf_real_monthly` |
| Train size    |                                432 |
| Test size     |                                144 |
| MAE           |                      13,552 VND/kg |
| RMSE          |                      16,754 VND/kg |
| R²            |                            -0.9044 |
| Feature count |                                 41 |

Kết luận: baseline đã có đánh giá định lượng thật, nhưng R² âm phải được trình bày trung thực. Nguyên nhân hợp lý là phân phối giá năm 2025 lệch mạnh so với train period 2022-2024.

## Bias

| Province | Monthly area-row observed rate | Weekly area-row observed rate | Nhận xét                  |
| -------- | -----------------------------: | ----------------------------: | ------------------------- |
| Lam Dong |                         100.0% |                         94.0% | Mạnh, nên ưu tiên demo    |
| Kon Tum  |                         100.0% |                         92.4% | Mạnh nhưng ít khu vực hơn |
| Dak Lak  |                          93.1% |                         76.5% | Dùng được                 |
| Gia Lai  |                          93.1% |                         75.4% | Dùng được                 |
| Dak Nong |                          39.6% |                         21.0% | Yếu, cần cảnh báo         |

Khu vực nên ưu tiên khi giải thích/demo: Di Linh, Ea H'leo, Buon Ho, Bao Loc, Lam Ha, Pleiku.

Khu vực không nên dùng làm ví dụ chính: Dak R'lap vì không có observed price riêng.

## Robustness

Robustness hiện có:

- Dataset processed không thiếu các feature chính dùng để train.
- `avg_price_vnd_per_kg` đã được fill để phục vụ train thử nghiệm.
- `observed_price_vnd_per_kg` được giữ để đánh giá độ tin cậy dữ liệu, không dùng làm target chính.
- Pydantic schema validate type/range cho request; `PredictorService` validate province/area/category theo `model_info.feature_names` để tránh input ngoài tập train.

Kết quả Stress Test trên dữ liệu thật (gây nhiễu tập Test 2025):
- Baseline (Normal Test Set): MAE = 13,552 VND/kg, RMSE = 16,754 VND/kg
- price_crash (Giá giảm đột ngột 50%): MAE = 22,566 VND/kg (+66.5% error lift), RMSE = 29,398 VND/kg (+75.5% error lift)
- heat_wave (Nhiệt độ tăng vọt lên 45°C): MAE = 13,549 VND/kg (+0.0%), RMSE = 16,752 VND/kg (+0.0%)
- both (Cả hai yếu tố trên): MAE = 22,569 VND/kg (+66.5% error lift), RMSE = 29,403 VND/kg (+75.5% error lift)

Nhận xét: Biến động giá cực đoan có tác động lớn nhất tới sai số dự báo (+66.5%), trong khi biến động nhiệt độ không làm thay đổi dự báo của baseline do mức độ quan trọng (feature importance) của nhiệt độ trong mô hình Random Forest baseline rất thấp (khoảng 0.09%). Cần bổ sung cảnh báo trên UI khi input giá vượt quá khoảng lịch sử.

## Social Impact

Mục tiêu xã hội của hệ thống là hỗ trợ nông dân nhỏ lẻ có thêm góc nhìn dữ liệu về giá cà phê.

Disclaimer bắt buộc cho UI/report:

> Dự báo AI chỉ mang tính tham khảo; không thay thế tư vấn tài chính, thông tin thương lái địa phương, hoặc quyết định giao dịch thực tế.

## Transparency

Top feature importance từ baseline real monthly:

| Feature          | Importance |
| ---------------- | ---------: |
| `rolling_avg_7d` |     0.7280 |
| `lag_1d`         |     0.2223 |
| `year`           |     0.0196 |
| `month`          |     0.0113 |
| `month_sin`      |     0.0078 |
| `quarter`        |     0.0043 |
| `month_cos`      |     0.0025 |
| `lag_7d`         |     0.0022 |
| `rainfall_mm`    |     0.0009 |
| `humidity_pct`   |     0.0008 |

Diễn giải ngắn: model hiện dựa chủ yếu vào lịch sử giá gần nhất và trung bình trượt. Weather/soil có vai trò nhỏ trong baseline này, nên không nên diễn giải quá mức rằng thời tiết là yếu tố quyết định chính.

## Hạn chế bắt buộc ghi trong slide/report

- `avg_price_vnd_per_kg` là target đã fill, không phải mọi dòng đều là giá crawl trực tiếp.
- `observed_price_vnd_per_kg` mới là giá crawl thật trực tiếp.
- Dak Nong và Dak R'lap có độ phủ yếu, không nên dùng làm ví dụ chính.
- Soil score là feature giáo dục/minh họa, không thay thế khảo sát đất thật.
- R² âm nghĩa là baseline chưa đủ tốt để ra quyết định tài chính.

## Bước tiếp theo

- Branch hiện đã rebase trên `origin/main` sau PR #9; chạy API smoke test và stress test trên backend real-data schema.
- Nếu có thêm thời gian, so sánh monthly vs weekly hoặc top-area-only để xem metrics có ổn hơn không.
- Đưa bảng Reliability/Bias/Transparency ở trên vào slide cuối kỳ.
