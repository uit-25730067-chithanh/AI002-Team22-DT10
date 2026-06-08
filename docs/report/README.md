# Report Index

Thư mục này là điểm vào cho tài liệu báo cáo cuối kỳ.

## Cấu trúc hiện tại

```text
docs/report/
├── README.md
├── final-ai002-report/
│   ├── README.md
│   ├── 01-introduction.md
│   ├── 02-theoretical-background.md
│   ├── 03-data-and-design.md
│   ├── 04-implementation.md
│   ├── 05-experiments-and-evaluation.md
│   ├── 06-conclusion-and-future-work.md
│   └── appendices.md
├── evaluation-axis-formulas-and-measurement.pdf
└── Thực nghiệm và đánh giá.pdf
```

## Source-of-truth khi báo cáo

- Roadmap hiện tại: [`../project-roadmap.md`](../project-roadmap.md)
- Codebase summary: [`../codebase-summary.md`](../codebase-summary.md)
- Báo cáo chính thức: [`final-ai002-report/README.md`](final-ai002-report/README.md)
- Slide thuyết trình: [`../slides/final_presentation_slides.md`](../slides/final_presentation_slides.md)

## Bằng chứng đánh giá

Các file PDF sau là tracked evidence:

- `evaluation-axis-formulas-and-measurement.pdf`: Công thức trục đánh giá.
- `Thực nghiệm và đánh giá.pdf`: Kết quả thực nghiệm và đánh giá hệ thống.

## Ghi chú tránh báo cáo nhầm

- Dataset chính thức là `data/processed/monthly/coffee_environment_all_areas_monthly_2020_2026.csv`.
- Dữ liệu được thu thập/tái tạo từ nguồn public, gồm giá cà phê, thời tiết lịch sử và hồ sơ đất theo khu vực.
- Baseline hiện tại là `rf_monthly_baseline`, experiment `20260608_004601__rf_monthly_baseline`.
- Không nói raw data được train trực tiếp; baseline dùng processed monthly dataset.
- Không nói model đã tốt; nói rõ đây là baseline có metric thật và limitation rõ.
