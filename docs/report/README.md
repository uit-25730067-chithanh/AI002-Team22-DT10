# Report Index

Thư mục này là điểm vào cho tài liệu báo cáo. Các note nội bộ theo tuần/milestone đã được gom vào [`internal-notes/`](internal-notes/) để root folder gọn hơn. **Lưu ý: Các file trong `internal-notes/` là Archive evidence (chứng cứ lưu trữ lịch sử), có thể chứa các thông báo hoặc tiến độ đã cũ (ví dụ: claim model.pkl bị ignore hoặc frontend chưa tích hợp). Vui lòng dùng README chính, docs index, roadmap, và architecture làm Current source-of-truth.**

Để đọc archive rõ hơn, dùng [Archive Evidence - Internal Notes](internal-notes/README.md).

## Cấu trúc hiện tại

```text
docs/report/
├── README.md
├── final-ai002-report/       # Báo cáo chính thức cuối kỳ (Markdown chia chương)
│   ├── README.md             # Điểm vào báo cáo và quản lý trạng thái
│   ├── ...
│   └── appendices.md
└── internal-notes/           # Note nội bộ theo tuần / milestone
    ├── week1_coffee_price_research.md
    ├── week1-2_team2_thanh_foundation-report-note.md
    ├── week1-2_team2_son_foundation-report-note.md
    ├── week3_team2_thanh_real-data-schema-report-note.md
    ├── week4_team2_thanh_real-model-baseline-report-note.md
    └── week5_team2_thanh_api-integration-report-note.md

## Bằng chứng đánh giá (Tracked PDF Evidence)

Các file sau là bằng chứng đánh giá đã được theo dõi (tracked evidence) từ Sơn, **không phải** là file tạm để cleanup:
- `evaluation-axis-formulas-and-measurement.pdf`: Công thức trục đánh giá.
- `Thực nghiệm và đánh giá.pdf`: Kết quả thực nghiệm và đánh giá hệ thống.
```

## Quy ước đọc nhanh

- **Thanh:** schema, model baseline, API contract, handoff/frontend support.
- **Sơn:** mock pipeline foundation, evaluation, robustness, bias, 5 Pillars, QA checklist.
- **Team 1:** crawler, processed dataset, frontend UI.
- **Report chung:** chỉ dùng để tổng hợp cuối kỳ, không thay thế note cá nhân.

## Mapping theo roadmap

| Roadmap                             | Report                                                                                                                 | Owner chính  | Trạng thái       |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------- |
| Week 1 research                     | [`internal-notes/week1_coffee_price_research.md`](internal-notes/week1_coffee_price_research.md)                                                     | Thịnh/Team 1 | Có               |
| Week 1-2 Foundation — Thanh         | [`internal-notes/week1-2_team2_thanh_foundation-report-note.md`](internal-notes/week1-2_team2_thanh_foundation-report-note.md)                       | Thanh        | Có               |
| Week 1-2 Foundation — Sơn           | [`internal-notes/week1-2_team2_son_foundation-report-note.md`](internal-notes/week1-2_team2_son_foundation-report-note.md)                           | Sơn          | Có               |
| Week 3 Data thật — Thanh            | [`internal-notes/week3_team2_thanh_real-data-schema-report-note.md`](internal-notes/week3_team2_thanh_real-data-schema-report-note.md)               | Thanh        | Có               |
| Week 4 Model thật — Thanh           | [`internal-notes/week4_team2_thanh_real-model-baseline-report-note.md`](internal-notes/week4_team2_thanh_real-model-baseline-report-note.md)         | Thanh        | Có               |
| Week 5 API và Integration — Thanh   | [`internal-notes/week5_team2_thanh_api-integration-report-note.md`](internal-notes/week5_team2_thanh_api-integration-report-note.md)                 | Thanh        | Có               |
| Week 3-5 Evaluation/5 Pillars — Sơn | [`../discussions/2026-05-13-son-evaluation-pack-summary.md`](../discussions/2026-05-13-son-evaluation-pack-summary.md) | Sơn          | Có ở discussions |
| Week 6 Slide/report/demo            | [`final-ai002-report/README.md`](final-ai002-report/README.md)                                                         | Cả nhóm      | Hoàn tất         |

## Nên dùng file nào khi họp

### Nếu hỏi Thanh đã làm gì

Đọc theo thứ tự:

1. [`internal-notes/week1-2_team2_thanh_foundation-report-note.md`](internal-notes/week1-2_team2_thanh_foundation-report-note.md)
2. [`internal-notes/week3_team2_thanh_real-data-schema-report-note.md`](internal-notes/week3_team2_thanh_real-data-schema-report-note.md)
3. [`internal-notes/week4_team2_thanh_real-model-baseline-report-note.md`](internal-notes/week4_team2_thanh_real-model-baseline-report-note.md)
4. [`internal-notes/week5_team2_thanh_api-integration-report-note.md`](internal-notes/week5_team2_thanh_api-integration-report-note.md)

### Nếu hỏi Sơn đã làm gì

Đọc:

1. [`internal-notes/week1-2_team2_son_foundation-report-note.md`](internal-notes/week1-2_team2_son_foundation-report-note.md)
2. [`../discussions/2026-05-13-son-evaluation-pack-summary.md`](../discussions/2026-05-13-son-evaluation-pack-summary.md)
3. [`../discussions/2026-05-13-real-data-audit-team2-son.md`](../discussions/2026-05-13-real-data-audit-team2-son.md)
4. [`../discussions/2026-05-13-son-api-integration-qa-checklist.md`](../discussions/2026-05-13-son-api-integration-qa-checklist.md)
5. [`../discussions/5-pillars-checkpoint.md`](../discussions/5-pillars-checkpoint.md)

### Nếu hỏi roadmap tổng thể

Đọc:

1. [`../project-roadmap.md`](../project-roadmap.md)
2. [`../codebase-summary.md`](../codebase-summary.md)
3. [`../discussions/2026-05-13-api-handoff-team2-real-data.md`](../discussions/2026-05-13-api-handoff-team2-real-data.md)

## Ghi chú tránh báo cáo nhầm

- Không nói Thanh làm crawler hoặc build processed dataset; đó là phần Phúc/Thịnh.
- Không nói Thanh làm evaluation pack/5 Pillars checkpoint; đó là phần Sơn.
- Không nói model đã tốt; chỉ nói baseline đã chạy thật, có metric thật và limitation rõ.
- Không nói raw data được train trực tiếp; baseline hiện dùng processed monthly dataset.
- Frontend integration/demo end-to-end đã có bằng chứng trong repo; chỉ coi note archive cũ là lịch sử.
