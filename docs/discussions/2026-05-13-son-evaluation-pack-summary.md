# Sơn Evaluation Pack Summary

**Ngày:** 2026-05-13
**Owner:** Sơn
**Branch target:** `feature/evaluation-real-data-model-week`
**Plan:** Local-only evaluation plan (gitignored)
**PR #9 status:** Merged 2026-05-14 local time, merge commit `e50e8a691c8aac89edce058fbf41a3cd70af913a`

## Summary ngắn cho PR description

PR này bổ sung gói **Responsible AI Evaluation + QA** cho phần evaluation, không sửa code/model/API. Nội dung tập trung review data thật, đánh giá baseline từ PR #9 đã merge, chuẩn bị checklist API/frontend integration, và chốt readiness cho tuần 18/5-24/5.

## Deliverables mapping

| Phase | Deliverable                        | File                                                                                                                 | Status |
| ----- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------ |
| 1     | Kiểm toán dữ liệu thật             | Archived evidence                                                                                                    | Public |
| 2     | PR #9 model evaluation             | Archived evidence                                                                                                    | Public |
| 3     | Danh sách kiểm tra integration API | Archived evidence                                                                                                    | Public |
| 4     | 5 pillars checkpoint               | Archived evidence                                                                                                    | Public |
| 5     | PR package summary/conflict guard  | `docs/discussions/2026-05-13-son-evaluation-pack-summary.md`                                                         | Public |

## Key findings

- Monthly real-data dataset là baseline chính vì observed rate tốt hơn weekly: 86.5% vs 72.7%.
- Dak Nong/Dak R'lap là vùng rủi ro cao, không nên demo chính.
- PR #9 baseline có metrics thật nhưng R² âm, cần report limitation trung thực.
- Feature importance cho thấy model phụ thuộc mạnh vào `rolling_avg_7d` và `lag_1d`; weather/soil không nên bị overclaim.
- Branch hiện đã rebase trên `origin/main` sau PR #9; bước tiếp theo là API smoke test, error handling, disclaimer, và demo preset.

## 5 Pillars contribution

| Pillar        | Contribution                                                      |
| ------------- | ----------------------------------------------------------------- |
| Reliability   | Đọc metrics thật, diễn giải MAE/RMSE/R², không né R² âm           |
| Bias          | Nêu rủi ro độ phủ theo province/area, đặc biệt Dak Nong/Dak R'lap |
| Robustness    | Chuẩn bị QA checklist input validation/API failure                |
| Social Impact | Bắt buộc disclaimer AI chỉ tham khảo                              |
| Transparency  | Diễn giải feature importance và limitation                        |

## Conflict-risk note

Scope PR #12 public gồm docs/evaluation/QA thật sự cần team:

- `docs/discussions/2026-05-13-son-evaluation-pack-summary.md`
- Các review chi tiết phụ đã lưu local, không cần stage lên GitHub nếu project reviewers không cần đọc đầy đủ.
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

- Add responsible AI evaluation pack for real-data week.
- Review real data readiness and province/area coverage risk.
- Evaluate PR #9 baseline metrics and transparency limitations.
- Add API/frontend integration QA checklist for week 5.
- Update 5 pillars checkpoint and add conflict guard.

## Scope

Docs-only evaluation/QA. Public PR includes real-data audit, 5 pillars checkpoint, summary, and API QA checklist. No backend/model/API implementation changes.

## Key risks documented

- R² is negative; baseline is demo/pipeline evidence, not financial advice.
- Dak Nong/Dak R'lap độ phủ yếu; tránh làm demo chính.
- Model depends heavily on lag/rolling price features.
- Branch is rebased on `origin/main` after PR #9; next step is API smoke test, then real-data stress test when backend contract is verified.

## Test/verification

- `git diff --check -- docs/discussions/*.md`
- `python -m pytest tests/ai-tests/test_predictor_service.py -q`
```

## Verification checklist

- [x] PR package chỉ chứa docs/evaluation/QA theo intended scope.
- [x] Không sửa backend/model/test artifact.
- [x] Có summary mapping deliverables với phases.
- [x] Có conflict-risk note rõ cho reviewer.
