# 📚 Trung tâm Tài liệu Dự án

Thư mục này chứa toàn bộ tài liệu kỹ thuật và quản lý của dự án **AI Dự báo Canh tác & Giá Cà phê (Đề tài 10 - Team 10)**.

## 📖 Mục lục

- [Project Overview (PDR)](project-overview-pdr.md): Kiến trúc cốt lõi, 5 Trụ cột AI Bền vững và phân công nhiệm vụ.
- [Tiêu chuẩn Code (Code Standards)](code-standards.md): Các quy tắc lập trình, quy trình Git và ràng buộc AI.
- [Tóm tắt Codebase (Codebase Summary)](codebase-summary.md): Giải thích chi tiết các phân hệ (`backend`, `model`, `crawler`, `frontend`).
- [Lộ trình Dự án (Roadmap)](project-roadmap.md): Lịch trình phát triển, biểu đồ Gantt và phân công WBS.
- [Team Data Flow Roadmap](discussions/2026-05-13-team-data-flow-roadmap.md): Luồng dữ liệu thật từ crawler → processed dataset → model → API → frontend.
- [API Handoff Real Data](discussions/2026-05-13-api-handoff-team2-real-data.md): Contract `/predict` cho frontend khi dùng model real-data.
- [Sửa lỗi (Troubleshooting)](troubleshooting.md): Hướng dẫn khắc phục các lỗi thường gặp khi chạy dự án.

## 🧭 Luồng đọc nhanh cho thành viên mới

```mermaid
flowchart TD
    A[Bắt đầu đọc repo] --> B[README.md]
    B --> C[docs/project-overview-pdr.md]
    C --> D[docs/project-roadmap.md]
    D --> E[Team data flow roadmap]
    E --> F[API handoff real data]
    F --> G[Codebase summary]
```

## 🔗 Tài liệu theo vai trò

```mermaid
flowchart LR
    A[Phúc và Thịnh] --> B[Data flow roadmap]
    A --> C[API handoff real data]
    A --> D[Frontend integration]

    E[Thanh] --> B
    E --> F[Project roadmap]
    E --> G[Codebase summary]

    H[Sơn] --> B
    H --> I[5 Pillars checkpoint]
    H --> J[Robustness stress test]
```
