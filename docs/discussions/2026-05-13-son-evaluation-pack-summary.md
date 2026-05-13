# Sơn Evaluation Pack Summary

**Ngày:** 2026-05-13
**Owner:** Sơn
**Branch target:** `feature/team2-son_real-data-model-week`
**Plan:** Local-only `plans/team2-son-evaluation-pack/` (gitignored)
**PR #9 status:** Merged 2026-05-14 local time, merge commit `e50e8a691c8aac89edce058fbf41a3cd70af913a`

## Summary ngắn cho PR description

PR này bổ sung gói **Responsible AI Evaluation + QA** cho phần Sơn, không sửa code/model/API của Thanh. Nội dung tập trung review data thật, đánh giá baseline từ PR #9 đã merge, chuẩn bị checklist API/frontend integration, và chốt readiness cho tuần 18/5-24/5.

## Deliverables mapping

| Phase | Deliverable | File | Status |
| --- | --- | --- | --- |
| 1 | Real data audit | `docs/discussions/2026-05-13-real-data-audit-team2-son.md` | Public |
| 2 | PR #9 model evaluation | Covered in `docs/discussions/2026-05-13-real-data-audit-team2-son.md` and `docs/discussions/5-pillars-checkpoint.md` | Public |
| 3 | API integration QA checklist | `docs/discussions/2026-05-13-son-api-integration-qa-checklist.md` | Public |
| 4 | 5 pillars checkpoint | `docs/discussions/5-pillars-checkpoint.md` | Public |
| 5 | PR package summary/conflict guard | `docs/discussions/2026-05-13-son-evaluation-pack-summary.md` | Public |

## Key findings

- Monthly real-data dataset là baseline chính vì observed rate tốt hơn weekly: 86.5% vs 72.7%.
- Dak Nong/Dak R'lap là vùng rủi ro cao, không nên demo chính.
- PR #9 baseline có metrics thật nhưng R² âm, cần report limitation trung thực.
- Feature importance cho thấy model phụ thuộc mạnh vào `rolling_avg_7d` và `lag_1d`; weather/soil không nên bị overclaim.
- Branch hiện đã rebase trên `origin/main` sau PR #9; bước tiếp theo là API smoke test, error handling, disclaimer, và demo preset.

## 5 Pillars contribution

| Pillar | Contribution |
| --- | --- |
| Reliability | Đọc metrics thật, diễn giải MAE/RMSE/R², không né R² âm |
| Bias | Nêu coverage risk theo province/area, đặc biệt Dak Nong/Dak R'lap |
| Robustness | Chuẩn bị QA checklist input validation/API failure |
| Social Impact | Bắt buộc disclaimer AI chỉ tham khảo |
| Transparency | Diễn giải feature importance và limitation |

## Conflict-risk note

Scope PR #12 public gồm docs/evaluation/QA thật sự cần team:

- `docs/discussions/2026-05-13-son-evaluation-pack-summary.md`
- `docs/discussions/2026-05-13-son-api-integration-qa-checklist.md`
- `docs/discussions/2026-05-13-real-data-audit-team2-son.md`
- `docs/discussions/5-pillars-checkpoint.md`
- Các review chi tiết phụ đã lưu local ở `tmp/term/son-evaluation-pack/`, không cần stage lên GitHub nếu team không cần đọc đầy đủ.
- Không force-add `plans/` vì đây là planning local-only và đang gitignored.

Không stage các file implementation/artifact nếu xuất hiện modified local:

- `backend/*`
- `model/preprocess.py`
- `model/train_rf.py`
- `model/best_model/*`
- `model/experiments.csv`
- `tests/ai-tests/*`

## Suggested PR body

```markdown
## Summary
- Add Sơn responsible AI evaluation pack for real-data week.
- Review Team 1 real data readiness and province/area coverage risk.
- Evaluate PR #9 baseline metrics and transparency limitations.
- Add API/frontend integration QA checklist for week 5.
- Update 5 pillars checkpoint and add conflict guard.

## Scope
Docs-only evaluation/QA. Public PR includes real-data audit, 5 pillars checkpoint, summary, and API QA checklist. No backend/model/API implementation changes.

## Key risks documented
- R² is negative; baseline is demo/pipeline evidence, not financial advice.
- Dak Nong/Dak R'lap coverage is weak; avoid as main demo.
- Model depends heavily on lag/rolling price features.
- Branch is rebased on `origin/main` after PR #9; next step is API smoke test, then real-data stress test when backend contract is verified.

## Test/verification
- `git diff --check -- docs/discussions/*.md`
- `python -m pytest tests/ai-tests/test_predictor_service.py -q`
```

## Verification checklist

- [x] PR package chỉ chứa docs/evaluation/QA phần Sơn theo intended scope.
- [x] Không sửa backend/model/test artifact của Thanh.
- [x] Có summary mapping deliverables với phases.
- [x] Có conflict-risk note rõ cho reviewer.
