# Sơn API Integration QA Checklist

**Ngày:** 2026-05-13
**Owner:** Sơn
**Consumers:** Thanh, Phúc, Thịnh
**Scope:** Checklist test API/frontend cho tuần integration 18/5-24/5
**Plan:** `plans/team2-son-evaluation-pack/phase-03-api-integration-qa-checklist.md`
**PR #9 status:** Merged 2026-05-14 local time, merge commit `e50e8a691c8aac89edce058fbf41a3cd70af913a`

## Kết luận nhanh

Checklist này dùng để Team 1 nối frontend với backend mà không đoán schema và không bỏ sót edge cases. Vì PR #9 đã merge, bước tiếp theo là pull latest rồi verify contract thực tế trước khi Team 1 nối UI.

## Contract cần xác nhận trước integration

| Item | Expected | Owner | Severity | Status |
| --- | --- | --- | --- | --- |
| Endpoint `/health` | Trả `status`, `model_loaded` | Thanh | Blocker | Exists local |
| Endpoint `/predict` | Nhận request hợp lệ và trả prediction/explanation | Thanh | Blocker | PR #9 merged, verify after pull latest |
| Endpoint `/model/info` | Trả model version/features/trained_at | Thanh | Important | Exists local |
| Province/area schema | Validate province/area theo backend real-data đã merge | Thanh | Blocker | PR #9 merged, verify with API smoke test |
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
| API-14 | Confidence output | Valid request | Có confidence interval/range nếu contract hỗ trợ | Thanh | Nice-to-have |
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

## Manual curl examples cần chuẩn hóa sau pull latest

Nếu chưa pull latest, local schema có thể vẫn dùng mock-era fields:

```json
{
  "avg_temp_c": 26.0,
  "rainfall_mm": 20.0,
  "humidity_pct": 80.0,
  "sunshine_hours": 6.0,
  "month": 11,
  "historical_price_7d_avg": 62000.0
}
```

Sau khi pull merge commit `e50e8a691c8aac89edce058fbf41a3cd70af913a`, Thanh cần chạy `/docs` hoặc curl smoke test để chốt example request/response chính thức trước khi Team 1 nối UI.

## Done criteria cho tuần 5

- API-01, API-03, UI-03, UI-04 pass trước demo.
- API-04/API-05/API-06 không được silently predict sai vùng.
- UI luôn hiển thị disclaimer.
- Sơn xác nhận demo preset không dùng Dak Nong/Dak R'lap làm case chính.
- Thanh xác nhận schema cuối cùng và example request sau khi pull latest từ PR #9 đã merge.
