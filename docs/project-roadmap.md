# Lộ trình Dự án và Luồng Dữ liệu

Tài liệu này mô tả roadmap tổng quan cho **AI002 - Đề tài 10: AI dự báo canh tác và giá cà phê**, tập trung vào luồng dữ liệu độc lập do Team 2 tự crawl, audit và tạo lại, sau đó đi qua model, API và frontend.

**Trạng thái hiện tại:** roadmap phản ánh trạng thái cập nhật tính đến 2026-06-07 sau khi tách nhóm và rebuild dataset độc lập.

## Bức tranh tổng quan

```mermaid
flowchart TD
    A[Team 2: Thanh và Sơn] --> B[Crawl độc lập giá cà phê và dữ liệu môi trường]
    B --> C[Raw data]
    C --> D[Processed weekly dataset]
    C --> E[Processed monthly dataset]
    E --> F[Team 2: Thanh train baseline]
    F --> G[Best model và metadata]
    G --> H[FastAPI backend]
    H --> I[Demo frontend]
    F --> J[Sơn đánh giá Robustness, Bias, 5 Pillars]
    J --> K[Báo cáo kỹ thuật]
    I --> L[Demo cuối kỳ]
    K --> L
```

## Luồng dữ liệu từ raw đến demo

```mermaid
flowchart LR
    A[Raw price data] --> D[Build processed datasets]
    B[Weather by area] --> D
    C[Soil profile] --> D

    D --> E[Weekly all-areas]
    D --> F[Monthly all-areas]
    D --> G[Per-area files]
    D --> H[Xếp hạng độ phủ khu vực]

    E --> I[Thử nghiệm tương lai]
    G --> J[Debug từng khu vực]
    H --> K[Chọn vùng có dữ liệu tốt]
    F --> L[Dataset train chính]

    L --> M[Preprocess]
    M --> N[Random Forest]
    N --> O[API /predict]
    O --> P[Frontend]
```

## Quyết định dùng dữ liệu

| Nhóm              | File                                                                        | Mục đích                        | Trạng thái                                   |
| :---------------- | :-------------------------------------------------------------------------- | :------------------------------ | :------------------------------------------- |
| Raw giá crawl     | `data/raw/independent/coffee_price_all_areas_daily_2020_2026.csv`                       | Nguồn giá public tự crawl lại   | Gitignored, không train trực tiếp trong repo |
| Weekly processed  | `data/processed/weekly/coffee_environment_independent_all_areas_weekly_2020_2026.csv`   | Tham khảo, thử nghiệm tương lai | Chưa dùng làm baseline chính                 |
| Monthly processed | `data/processed/monthly/coffee_environment_independent_all_areas_monthly_2022_2026.csv` | Dataset train chính             | Đã dùng cho baseline độc lập                 |
| Xếp hạng độ phủ   | `data/processed/independent_area_real_price_data_ranking.csv`                           | Đánh giá độ phủ khu vực         | Đã dùng để quyết định                        |

Lý do chọn monthly: ít nhiễu hơn weekly, độ phủ giá thật tốt hơn, dễ giải thích trong báo cáo, phù hợp KISS.

## Roadmap tổng thể

```mermaid
gantt
    title AI002 lộ trình dự án cà phê
    dateFormat  YYYY-MM-DD
    tickInterval 1w
    axisFormat  %d/%m

    section GĐ 1: Khởi động
    Nghiên cứu và thiết kế hệ thống          :done, a1, 2026-04-20, 7d
    Setup repo, docs, backend/model skeleton :done, a2, 2026-04-24, 7d

    section GĐ 2: Dữ liệu thật
    Crawl giá cà phê và thời tiết            :done, b1, 2026-05-04, 7d
    Build processed weekly/monthly           :done, b2, 2026-05-08, 4d
    Rebuild dataset độc lập Team 2           :done, b3, 2026-06-07, 1d

    section GĐ 3: Model baseline
    Chọn monthly dataset                     :done, c1, 2026-05-12, 1d
    Preprocess schema real-data              :done, c2, 2026-05-12, 1d
    Train Random Forest baseline             :done, c3, 2026-06-07, 1d
    Lưu best model và feature importance     :done, c4, 2026-06-07, 1d

    section GĐ 4: Backend API
    Update prediction contract               :done, d1, 2026-05-13, 1d
    Validate numeric, enum và category       :done, d2, 2026-05-13, 1d
    Handoff API cho frontend                 :done, d3, 2026-05-13, 1d

    section GĐ 5: Evaluation
    Kiểm toán dữ liệu thật và bias độ phủ         :done, e0, 2026-05-13, 1d
    Danh sách kiểm tra integration API             :done, e1, 2026-05-13, 1d
    5 Pillars checkpoint real-data           :done, e2, 2026-05-13, 1d
    Stress test API/integration evidence     :done, e3, 2026-05-14, 3d

    section GĐ 6: Integration và báo cáo
    React frontend nối /predict             :done, f1, 2026-06-03, 1d
    Demo end-to-end                          :done, f2, 2026-06-03, 1d
    Báo cáo kỹ thuật và slide                :done, f3, 2026-05-25, 10d
    Nộp bài                                  :milestone, f4, 2026-06-04, 0d
```

## Phân công trách nhiệm

```mermaid
flowchart TD
    subgraph T2Data[Team 2: Thanh và Sơn]
        A1[Crawl độc lập dữ liệu giá]
        A2[Crawl weather theo area]
        A3[Tạo processed datasets độc lập]
        A4[Frontend React/Vite/Tailwind]
    end

    subgraph Thanh[Thanh]
        B1[Chốt independent data contract]
        B2[Normalize real schema]
        B3[Feature engineering]
        B4[Train Random Forest]
        B5[FastAPI contract]
    end

    subgraph Son[Sơn]
        C1[Kiểm toán dữ liệu thật]
        C2[Bằng chứng độ phủ thiên lệch]
        C3[Danh sách kiểm tra integration API]
        C4[5 Pillars checkpoint]
        C5[Stress/API follow-up]
    end

    subgraph Team[Team 10]
        D1[Báo cáo]
        D2[Slide]
        D3[Demo]
    end

    A1 --> A3
    A2 --> A3
    A3 --> B1
    B1 --> B2 --> B3 --> B4 --> B5
    B4 --> C1 --> C2 --> C3 --> C4 --> C5
    B5 --> A4
    C4 --> D1
    A4 --> D3
    D1 --> D2 --> D3
```

## Luồng xử lý trong model

```mermaid
flowchart TD
    A[Monthly CSV] --> B[normalize_real_schema]
    B --> C[Chuẩn hóa period_start thành date]
    B --> D[Đổi avg_price thành target historical_price_vnd]
    C --> E[fill_missing]
    D --> E
    E --> F[cap_outliers]
    F --> G[feature_engineer]
    G --> H[lag và rolling theo area]
    G --> I[month_sin và month_cos]
    H --> J[encode_features one-hot]
    I --> J
    J --> K[split_temporal]
    K --> L[Train 2022-2024]
    K --> M[Test 2025]
    L --> N[RandomForestRegressor]
    N --> O[MAE, RMSE, R2]
    N --> P[feature_importance]
    N --> Q[best_model]
```

## Luồng request API

```mermaid
sequenceDiagram
    participant UI as Frontend
    participant API as FastAPI
    participant Schema as Pydantic schema
    participant Service as PredictorService
    participant Model as Random Forest

    UI->>API: POST /predict
    API->>Schema: Validate numeric ranges và enum
    Schema-->>API: Payload hợp lệ hoặc 422
    API->>Service: Build feature row
    Service->>Service: Check category trong feature_names
    Service->>Service: Map one-hot theo feature_names
    Service->>Model: Predict giá cà phê
    Model-->>Service: Giá dự báo
    Service-->>API: Giá, khoảng tin cậy, top features
    API-->>UI: JSON response + disclaimer
```

## Trạng thái theo milestone

```mermaid
stateDiagram-v2
    [*] --> Foundation
    Foundation --> RealData
    RealData --> BaselineModel
    BaselineModel --> APIContract
    APIContract --> Evaluation
    Evaluation --> FrontendIntegration
    FrontendIntegration --> ReportAndDemo
    ReportAndDemo --> Submission

    Foundation: Repo, mock pipeline, API skeleton
    RealData: Processed monthly/weekly datasets
    BaselineModel: RF baseline + feature importance
    APIContract: /predict real-data schema
    Evaluation: Kiểm toán dữ liệu thật + Bias + 5 Pillars + stress test hoàn tất
    FrontendIntegration: Frontend gọi API
    ReportAndDemo: Slide + báo cáo + demo
    Submission: Nộp bài cuối kỳ
```

## Theo dõi tiến độ tuần

### Tuần 1-2 — Khởi động

- [x] Khởi tạo repo và Git setup.
- [x] Chốt đề tài dự báo giá cà phê.
- [x] Viết PDR và 5 trụ cột AI.
- [x] Setup cấu trúc backend, model, crawler, frontend.

### Tuần nghỉ lễ — Foundation pipeline

- [x] Team 2 chạy mock pipeline.
- [x] Có FastAPI skeleton.
- [x] Có Random Forest baseline trên mock data.

### Tuần 3 — Data thật

- [x] Team 2 tự crawl và tạo lại processed weekly/monthly dataset độc lập.
- [x] Team 2 đọc và chuẩn hóa schema real-data.
- [x] Có xếp hạng độ phủ dữ liệu theo khu vực.
- [x] Ghi rõ provenance mới và không dùng dataset Phúc/Thịnh làm source-of-truth.

### Tuần 4 — Model thật

- [x] Train Random Forest baseline trên monthly all-areas độc lập.
- [x] Trích xuất feature importance.
- [x] Lưu best model và metadata.
- [x] Sơn bổ sung kiểm toán dữ liệu thật, bias độ phủ bằng chứng và 5 Pillars checkpoint trong PR #12.
- [x] Chạy stress test tự động cho kịch bản cực đoan (Black Swan) trên dữ liệu thật.

### Tuần 5 — API và Integration

- [x] Hoàn thiện `/predict`, `/health`, `/model/info` theo real-data contract.
- [x] API validate numeric ranges, enum và category đã train.
- [x] Sơn bổ sung danh sách kiểm tra integration API/frontend cho Team 1.
- [x] Có frontend demo mobile-first trong repo gọi `/predict`.
- [x] Demo end-to-end backend/frontend bằng kịch bản Lâm Đồng / Di Linh.

### Tuần 6 — Báo cáo và slide

- [x] Có 5 Pillars checkpoint real-data từ PR #12 và checkpoint độc lập 2026-06-07.
- [x] Chuyển bằng chứng 5 Pillars và stress test vào slide/report cuối kỳ.
- [x] Chuẩn bị slide thuyết trình (final_presentation_slides.md).
- [x] Tổng duyệt demo bằng API smoke test và frontend screenshot evidence.

## WBS cập nhật

| Phân hệ            | Nội dung                                    | Người phụ trách | Review cần có                      |
| :----------------- | :------------------------------------------ | :-------------- | :--------------------------------- |
| Data crawler       | Crawl giá, weather, tạo processed dataset độc lập | Thanh, Sơn      | Thanh review schema                |
| Data understanding | Giải thích raw/weekly/monthly, độ phủ       | Thanh, Sơn      | Sơn review cho evaluation          |
| AI model           | Preprocess, train RF, feature importance    | Thanh           | Sơn review metrics                 |
| Evaluation         | Stress test, bias, 5 Pillars                | Sơn             | Thanh review technical correctness |
| Backend API        | `/predict`, `/health`, `/model/info`        | Thanh           | Phúc review frontend contract      |
| Frontend           | React/Vite/Tailwind UI và gọi API          | Phúc, Thịnh     | Thanh review payload/response      |
| Report             | Kết quả, limitation, demo script            | Cả nhóm         | Cả nhóm review                     |

## Rủi ro và cách xử lý

```mermaid
flowchart TD
    A[Rủi ro dự án] --> B[Độ phủ dữ liệu không đều]
    A --> C[R2 âm ở baseline]
    A --> D[Frontend gửi giá trị ngoài range hoặc ngoài category đã train]
    A --> E[Team hiểu nhầm raw data là train trực tiếp]

    B --> B1[Dùng xếp hạng độ phủ và nói rõ thiên lệch]
    C --> C1[Trình bày là baseline, chưa phải model cuối]
    D --> D1[API trả 422 thay vì predict input không hợp lệ]
    E --> E1[Docs data flow và Mermaid roadmap]
```

## Tài liệu liên quan

- [`docs/discussions/2026-05-13-team-data-flow-roadmap.md`](discussions/2026-05-13-team-data-flow-roadmap.md)
- [`docs/discussions/2026-05-13-api-handoff-team2-real-data.md`](discussions/2026-05-13-api-handoff-team2-real-data.md)
- [`docs/discussions/2026-05-13-real-data-audit-team2-son.md`](discussions/2026-05-13-real-data-audit-team2-son.md)
- [`docs/discussions/2026-05-13-son-api-integration-qa-checklist.md`](discussions/2026-05-13-son-api-integration-qa-checklist.md)
- [`docs/discussions/2026-05-13-son-evaluation-pack-summary.md`](discussions/2026-05-13-son-evaluation-pack-summary.md)
- [`docs/discussions/5-pillars-checkpoint.md`](discussions/5-pillars-checkpoint.md)
- [`docs/discussions/2026-06-07-independent-data-contract.md`](discussions/2026-06-07-independent-data-contract.md)
- [`docs/discussions/2026-06-07-independent-data-audit.md`](discussions/2026-06-07-independent-data-audit.md)
- [`docs/discussions/2026-06-07-independent-model-results.md`](discussions/2026-06-07-independent-model-results.md)
- [`docs/discussions/2026-06-07-independent-five-pillars-checkpoint.md`](discussions/2026-06-07-independent-five-pillars-checkpoint.md)
- [`data/processed/FIELD_DESCRIPTIONS.md`](../data/processed/FIELD_DESCRIPTIONS.md)
- [`data/processed/AREA_REAL_PRICE_DATA_RANKING.md`](../data/processed/AREA_REAL_PRICE_DATA_RANKING.md)
