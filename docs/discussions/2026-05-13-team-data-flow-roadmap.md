# Team Data Flow Roadmap — 13/05/2026

## Mục tiêu

Tài liệu này giúp Thanh, Sơn, Phúc, Thịnh nhìn cùng một bức tranh: dữ liệu từ crawler đi vào đâu, Team 2 xử lý thế nào, model sinh ra API gì, và frontend cần dùng phần nào.

Đây là bản draft để Team 2 unblock hiểu biết nội bộ. Phúc nên review lại phần crawler, nguồn dữ liệu và giả định processed dataset.

## Quyết định dữ liệu hiện tại

| Nhóm dữ liệu      | File chính                                                                  | Vai trò hiện tại                                                 |
| :---------------- | :-------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| Raw giá crawl     | `data/raw/coffee_price_all_areas_daily_2022_2025.csv`                       | Nguồn gốc giá thật, gitignored, không train trực tiếp trong repo |
| Weekly processed  | `data/processed/weekly/coffee_environment_all_areas_weekly_2022_2025.csv`   | Tham khảo, future experiment, coverage thấp hơn monthly          |
| Monthly processed | `data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv` | Dataset chính để train baseline hiện tại                         |
| Ranking coverage  | `data/processed/area_real_price_data_ranking.csv`                           | Kiểm tra khu vực nào có giá thật tốt                             |
| Field spec        | `data/processed/FIELD_DESCRIPTIONS.md`                                      | Giải thích schema cho team                                       |

## Vì sao chọn monthly thay vì dùng hết raw/weekly

- Raw nhiều nguồn và nhiều dòng, nhưng nằm trong `data/raw/` gitignored và chưa đồng đều theo khu vực/thời gian.
- Weekly có nhiều dòng hơn nhưng coverage giá thật thấp hơn monthly.
- Monthly có ít dòng hơn nhưng ổn định hơn, dễ giải thích hơn, hợp baseline Random Forest hơn.
- Mục tiêu môn học là chứng minh tư duy AI bền vững, không phải nhồi dữ liệu tối đa bằng mọi giá.

```mermaid
flowchart TD
    A[Raw nhiều nguồn] --> B{Có dùng trực tiếp để train không?}
    B -->|Không| C[Lý do: nhiễu, thiếu kỳ, khác nguồn]
    B -->|Có thể sau| D[Future experiment nếu có thời gian]
    C --> E[Chọn processed monthly]
    E --> F[Train baseline dễ giải thích]
    F --> G[API demo ổn định hơn]
```

## Luồng dữ liệu tổng quan

```mermaid
flowchart TD
    A[Phúc và Thịnh crawl giá cà phê] --> B[Raw daily price data]
    C[Crawler thời tiết theo khu vực] --> D[Daily weather features]
    E[Soil profile theo khu vực] --> F[Static soil features]

    B --> G[Build area datasets]
    D --> G
    F --> G

    G --> H[Weekly processed dataset]
    G --> I[Monthly processed dataset]
    G --> J[Area data ranking]

    H --> K[Tham khảo và future experiment]
    J --> L[Chọn khu vực có coverage tốt]
    I --> M[Thanh train baseline hiện tại]

    M --> N[Preprocess real schema]
    N --> O[Feature engineering theo area]
    O --> P[Train Random Forest]
    P --> Q[Best model và metadata]
    Q --> R[FastAPI predict]
    R --> S[Frontend demo]
```

## Luồng model chi tiết

```mermaid
flowchart TD
    A[Monthly all-areas CSV] --> B[normalize_real_schema]
    B --> C[fill_missing]
    C --> D[cap_outliers]
    D --> E[feature_engineer]
    E --> F[lag_1d, lag_7d, rolling_avg_7d theo area]
    F --> G[month_sin, month_cos]
    G --> H[encode_features one-hot]
    H --> I[split_temporal]
    I --> J[Train: 2022-2024]
    I --> K[Test: 2025]
    J --> L[RandomForestRegressor]
    K --> M[Đánh giá MAE, RMSE, R2]
    L --> N[feature_importance]
    L --> O[model/best_model/metadata.json]
    L --> P[model/best_model/model.pkl]
```

## Luồng API và frontend

```mermaid
sequenceDiagram
    participant UI as Frontend của Phúc/Thịnh
    participant API as FastAPI backend
    participant P as PredictorService
    participant M as Random Forest model
    participant Meta as metadata.json

    UI->>API: POST /predict với thời tiết, tháng, giá gần nhất
    API->>API: Pydantic validate numeric ranges và enum
    API->>P: predict(payload)
    P->>Meta: đọc feature_names đã train
    P->>P: check category nằm trong feature_names
    P->>P: build feature row theo các cột model đã train
    P->>M: model.predict(feature_row)
    M-->>P: giá dự báo
    P-->>API: predicted_price, confidence_interval, top_features
    API-->>UI: response kèm disclaimer
```

## Phân công trách nhiệm

```mermaid
flowchart LR
    subgraph T1[Team 1: Phúc và Thịnh]
        A[Crawl giá cà phê]
        B[Crawl hoặc chuẩn bị thời tiết]
        C[Build frontend]
        D[Nối frontend với API]
    end

    subgraph T2A[Thanh]
        E[Chốt schema processed]
        F[Preprocess real data]
        G[Train Random Forest]
        H[FastAPI prediction contract]
        I[API handoff docs]
    end

    subgraph T2B[Sơn]
        J[Real data audit]
        K[Bias coverage evidence]
        L[API integration QA checklist]
        M[5 Pillars checkpoint]
        Q[Stress/API follow-up]
    end

    subgraph ALL[Cả nhóm]
        N[Báo cáo kỹ thuật]
        O[Slide]
        P[Demo cuối]
    end

    A --> E
    B --> E
    E --> F --> G --> H --> D
    G --> J --> K --> L --> M --> Q
    H --> I --> N
    D --> P
    M --> O
    N --> O --> P
```

## Trạng thái hiện tại sau PR real-data baseline

```mermaid
stateDiagram-v2
    [*] --> DaCoDataProcessed
    DaCoDataProcessed --> DaTrainBaseline
    DaTrainBaseline --> DaCoBestModel
    DaCoBestModel --> DaCapNhatAPI
    DaCapNhatAPI --> DaCoEvaluationPack
    DaCoEvaluationPack --> ChoFrontendNoiAPI
    ChoFrontendNoiAPI --> ChoStressTestAPI
    ChoStressTestAPI --> ChoBaoCao

    DaCoDataProcessed: Có monthly và weekly processed dataset
    DaTrainBaseline: Đã train RF baseline trên monthly all-areas
    DaCoBestModel: Đã có metadata và feature importance
    DaCapNhatAPI: /predict dùng real-data contract
    DaCoEvaluationPack: Sơn đã có audit, QA checklist và 5 Pillars evidence
    ChoFrontendNoiAPI: Phúc/Thịnh nối UI
    ChoStressTestAPI: Sơn/Thanh kiểm tra stress/API integration follow-up
    ChoBaoCao: Cả nhóm chuyển evidence vào slide/report
```

## Cột mốc theo tuần

```mermaid
gantt
    title Lộ trình team theo dữ liệu thật
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m

    section Data - Phúc/Thịnh
    Crawl raw price và weather                  :done, d1, 2026-05-04, 7d
    Build processed weekly/monthly              :done, d2, 2026-05-08, 4d
    Review docs data flow                        :active, d3, 2026-05-14, 2d

    section Model - Thanh
    Chọn monthly all-areas dataset               :done, m1, 2026-05-12, 1d
    Normalize schema và feature engineering      :done, m2, 2026-05-12, 1d
    Train Random Forest baseline                 :done, m3, 2026-05-13, 1d
    Update API contract real data                :done, m4, 2026-05-13, 1d

    section Evaluation - Sơn/Thanh
    Real data audit và bias coverage             :done, e0, 2026-05-13, 1d
    API integration QA checklist                 :done, e1, 2026-05-13, 1d
    Viết 5 Pillars checkpoint                    :done, e2, 2026-05-13, 1d
    Stress test API/integration follow-up        :e3, 2026-05-14, 3d

    section Integration - Team 1 và Team 2
    Frontend gọi /predict                        :i1, 2026-05-18, 4d
    Demo end-to-end                              :i2, 2026-05-21, 2d

    section Report - Cả nhóm
    Tổng hợp báo cáo kỹ thuật                    :r1, 2026-05-25, 7d
    Slide và tổng duyệt                          :r2, 2026-05-28, 7d
    Nộp bài                                      :milestone, r3, 2026-06-04, 0d
```

## Những điểm Phúc cần review

- Raw source list và nguồn nào là chính.
- Cách build `data/processed/weekly` và `data/processed/monthly`.
- Ý nghĩa `price_fill_method` và khi nào là `observed`, `interpolated_area`, `province_proxy`.
- Có cần expose thêm `price_observations` trên frontend hay backend tự default theo `price_fill_method`.
- Các khu vực có coverage yếu, đặc biệt `Dak R'lap`.
- Frontend nên cho user chọn field nào, field nào để default backend.

## Phần Sơn đã cover trong PR #12 và follow-up

- Đã có real data audit cho monthly/weekly, coverage theo tỉnh/khu vực và cảnh báo Dak Nong/Dak R'lap.
- Đã có 5 Pillars checkpoint real-data, gồm Reliability metrics, Bias risk, Robustness validation, Social Impact disclaimer và Transparency feature importance.
- Đã có API/frontend integration QA checklist cho `/health`, `/predict`, `/model/info`, unknown category, invalid range và model missing.
- Follow-up còn lại: chạy smoke test/stress test ở tuần integration, rồi chuyển evidence vào slide/report cuối kỳ.

Tài liệu Sơn liên quan:

- [`2026-05-13-real-data-audit-team2-son.md`](2026-05-13-real-data-audit-team2-son.md)
- [`2026-05-13-son-api-integration-qa-checklist.md`](2026-05-13-son-api-integration-qa-checklist.md)
- [`2026-05-13-son-evaluation-pack-summary.md`](2026-05-13-son-evaluation-pack-summary.md)
- [`5-pillars-checkpoint.md`](5-pillars-checkpoint.md)

## Nguyên tắc báo cáo

- Nói rõ model hiện tại là baseline, chưa phải model cuối.
- Nói rõ monthly được chọn vì ổn định và dễ giải thích hơn weekly.
- Không nói “dùng hết data” mà nói “dùng bản processed phù hợp nhất cho baseline”.
- Nhấn mạnh API có validation và disclaimer để tránh hiểu nhầm dự báo là lời khuyên tài chính.
