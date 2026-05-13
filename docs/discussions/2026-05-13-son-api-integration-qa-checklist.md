# Sơn API Integration QA Checklist

**Ngày:** 2026-05-13
**Owner:** Sơn
**Consumers:** Thanh, Phúc, Thịnh
**Scope:** Checklist test API/frontend cho tuần integration 18/5-24/5
**Plan:** Local-only `plans/team2-son-evaluation-pack/phase-03-api-integration-qa-checklist.md` (gitignored)
**PR #9 status:** Merged 2026-05-14 local time, merge commit `e50e8a691c8aac89edce058fbf41a3cd70af913a`

## Kết luận nhanh

Checklist này dùng để Team 1 nối frontend với backend mà không đoán schema và không bỏ sót edge cases. Branch hiện đã rebase trên `origin/main` sau PR #9, nên checklist dưới đây bám theo schema real-data hiện tại và còn cần smoke test trước khi Team 1 nối UI.

## Contract cần xác nhận trước integration

| Item | Expected | Owner | Severity | Status |
| --- | --- | --- | --- | --- |
| Endpoint `/health` | Trả `status`, `model_loaded` | Thanh | Blocker | Exists local |
| Endpoint `/predict` | Nhận request real-data hợp lệ và trả prediction/explanation/disclaimer | Thanh | Blocker | Schema available, verify with API smoke test |
| Endpoint `/model/info` | Trả model version/features/trained_at | Thanh | Important | Exists local |
| Province/area validation | Pydantic schema có `province`/`area` dạng string; allowed-value check chạy trong `PredictorService` theo model features | Thanh | Blocker | Service validation available, verify with API smoke test |
| Disclaimer in response/UI | UI phải hiển thị cảnh báo AI chỉ tham khảo | Phúc/Thịnh | Important | Needs frontend work |
| Data limitation warning | Dak Nong/Dak R'lap/ngoài Tây Nguyên có warning | Phúc/Thịnh/Sơn | Important | Needs frontend work |

## API test cases

| ID | Case | Input | Expected behavior | Owner | Severity |
| --- | --- | --- | --- | --- | --- |
| API-01 | Health check | `GET /health` | HTTP 200, có `status`, có `model_loaded` | Thanh | Blocker |
| API-02 | Model info | `GET /model/info` | HTTP 200, có model version và feature list nếu model loaded | Thanh | Important |
| API-03 | Happy path demo-safe area | Valid monthly-style input cho Lam Dong/Di Linh hoặc Dak Lak/Ea H'leo | HTTP 200, có predicted price, model version, top features | Thanh/Phúc | Blocker |
| API-04 | Unknown province | Province ngoài training set nếu schema real-data có field này | HTTP 422 hoặc error message rõ cho UI | Thanh | Blocker |
| API-05 | Unknown area | Area không nằm trong training set | HTTP 422 hoặc error message rõ cho UI | Thanh | Blocker |
| API-06 | Province/area mismatch | Province Lam Dong nhưng area thuộc Dak Lak | Reject hoặc warning rõ, không silently predict | Thanh | Important |
| API-07 | Missing optional environment | Thiếu optional weather/soil field nếu API hỗ trợ default | HTTP 200 nếu thật sự optional, hoặc 422 nếu required | Thanh | Important |
| API-08 | Invalid temperature | Nhiệt độ quá thấp/quá cao | HTTP 422 với validation detail | Thanh | Important |
| API-09 | Invalid rainfall | Rainfall âm hoặc cực lớn | HTTP 422 với validation detail | Thanh | Important |
| API-10 | Invalid humidity | Humidity ngoài 0-100 | HTTP 422 với validation detail | Thanh | Important |
| API-11 | Invalid month/period | Month ngoài 1-12 hoặc date sai format | HTTP 422 với validation detail | Thanh | Important |
| API-12 | Model missing | Tạm đổi path hoặc chạy khi model chưa có | HTTP 503, message hiểu được | Thanh | Important |
| API-13 | Response transparency | Valid request | Response có top features/explanation hoặc model info đủ để UI giải thích | Thanh/Sơn | Important |
| API-14 | Confidence output | Valid request | Response bắt buộc có `confidence_interval` theo `PredictionResponse` | Thanh | Important |
| API-15 | Bias warning | Request vùng yếu coverage | UI/API hiển thị limitation | Phúc/Thịnh/Sơn | Important |

## Frontend integration checklist

| ID | Check | Expected behavior | Owner | Severity |
| --- | --- | --- | --- | --- |
| UI-01 | Form validation trước khi gọi API | Không gửi giá trị rõ ràng sai range | Phúc/Thịnh | Important |
| UI-02 | Loading state | Người dùng thấy đang dự báo | Phúc/Thịnh | Nice-to-have |
| UI-03 | Error display | Hiển thị lỗi 422/503 dễ hiểu, không show stack trace | Phúc/Thịnh | Blocker |
| UI-04 | Prediction display | Hiển thị VND/kg, model version, top features | Phúc/Thịnh | Blocker |
| UI-05 | Disclaimer | Luôn hiện câu AI chỉ tham khảo | Phúc/Thịnh | Important |
| UI-06 | Coverage warning | Cảnh báo khi chọn Dak Nong/Dak R'lap hoặc vùng yếu | Phúc/Thịnh/Sơn | Important |
| UI-07 | Demo preset | Có preset Di Linh/Ea H'leo/Buon Ho để demo nhanh | Phúc/Thịnh | Nice-to-have |
| UI-08 | API unavailable | Nếu backend down, UI báo lỗi thân thiện | Phúc/Thịnh | Important |

## Manual curl example theo schema hiện tại

Request mẫu cho `POST /predict` sau PR #9:

```json
{
  "province": "Dak Lak",
  "area": "Buon Ho",
  "avg_temperature_c": 26.0,
  "total_rainfall_mm": 20.0,
  "avg_humidity_percent": 80.0,
  "avg_soil_moisture_0_7cm": 0.24,
  "soil_score": 5.0,
  "soil_data_confidence": "medium",
  "coffee_type": "Robusta / ca phe nhan xo noi dia",
  "price_fill_method": "observed",
  "dominant_soil_type": "Dat do bazan",
  "month": 11,
  "year": 2025,
  "latest_price_vnd_per_kg": 90000.0,
  "rolling_avg_price_vnd_per_kg": 90000.0,
  "price_observations": 1
}
```

Expected response cần có `predicted_price_vnd`, `confidence_interval`, `top_features`, `model_version`, và `disclaimer`. Thanh cần chạy `/docs` hoặc curl smoke test để chốt response mẫu chính thức trước khi Team 1 nối UI.

## Done criteria cho tuần 5

- API-01, API-03, UI-03, UI-04 pass trước demo.
- API-04/API-05/API-06 không được silently predict sai vùng.
- UI luôn hiển thị disclaimer.
- Sơn xác nhận demo preset không dùng Dak Nong/Dak R'lap làm case chính.
- Thanh xác nhận schema/response mẫu bằng API smoke test trên branch đã rebase từ `origin/main`.
