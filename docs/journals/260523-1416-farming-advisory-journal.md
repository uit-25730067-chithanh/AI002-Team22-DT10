---
date: "2026-05-23T14:16:00+07:00"
tags: ["team2", "backend", "api", "farming-advisory", "rule-based"]
---

# Farming Advisory Layer Implementation Journal

## Context

Thanh cần hoàn tất plan `plans/2026-05-23-01-farming-advisory-layer-and-api-handoff/plan.md` để API `/predict` có thêm phần gợi ý canh tác, nhưng vẫn minh bạch là rule-based advisory, không phải model AI canh tác đã train. Sau trao đổi với Thanh, UI mode được chốt là web form nhập thông số + advisory card, không phải chatbot hay Q&A tự do.

## What happened

- Thêm schema `FarmingRecommendation` và field `farming_recommendation` vào `PredictionResponse`.
- Tạo `FarmingAdvisoryService` tách khỏi `PredictorService` để giữ separation of concerns.
- Tích hợp service vào `PredictorService.predict()` sau bước dự báo giá.
- Cập nhật handoff doc cho Phúc/Frontend với sample response, field table và wording tránh claim sai.
- Cập nhật framing cho Phúc/Frontend: user nhập/chọn thông số có cấu trúc, UI render card dự báo giá và card gợi ý chăm sóc mùa vụ.
- Theo góp ý của Thanh, tách rule/config sang `data/processed/farming_advisory_rules.json` để dễ tìm và chỉnh sau này.
- Thêm error boundary cho missing/corrupt/missing-section JSON config.
- Chạy review tổng thể theo tinh thần `ck-agent-dev-code-reviewer`.

## Decisions

| Decision                                                        | Rationale                                                        |
| --------------------------------------------------------------- | ---------------------------------------------------------------- |
| Dùng field `farming_recommendation`                             | Rõ nghĩa, không đụng field cũ trong API.                         |
| Giữ `advisory_type = rule_based`                                | Minh bạch, tránh hiểu nhầm là trained farming model.             |
| Chốt UI form + advisory card                                    | Phù hợp JSON response hiện tại, tránh overbuild chatbot.         |
| Đưa rule data sang `data/processed/farming_advisory_rules.json` | Dễ tìm, dễ audit, vẫn KISS, không thêm DB/dependency.            |
| Cache JSON bằng `lru_cache(maxsize=1)`                          | Tránh đọc file mỗi request, config read-only trong runtime demo. |
| Không xử lý phần evaluation của Sơn                             | Plan giao Thanh phần API contract/backend/handoff.               |

## Verification

- `python3 -m json.tool data/processed/farming_advisory_rules.json >/dev/null` pass.
- `python3 -m pytest tests/ai-tests -q` pass với `17 passed`.
- `python3 -m compileall backend model` pass.
- `git diff --check` pass.
- Smoke test `/predict`-style payload trả `action=harvest`, `advisory_type=rule_based`, reasoning đọc từ JSON config.

## Impact

- Frontend có thể render phần canh tác ngay trong response `/predict`, không cần endpoint mới.
- Scope UI rõ hơn: advisory card theo mùa vụ, không promise trả lời câu hỏi tự do như "vặt chồi bao lâu".
- Team report có wording rõ: “gợi ý canh tác dựa trên rule”.
- Feature hỗ trợ Social Impact và Transparency trong 5 Pillars nhưng không làm phình scope thành model canh tác riêng.

## Next

- Commit các file code/test/data/doc liên quan khi Thanh muốn ship PR.
- Nếu cần tinh chỉnh rule nông nghiệp, sửa `data/processed/farming_advisory_rules.json` trước, rồi chạy lại service tests.
- Sau này nếu có nguồn nông nghiệp chính thức hơn, có thể cập nhật thresholds/reasoning trong JSON mà không đổi API contract.
