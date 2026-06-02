# Note báo cáo phần việc của Thanh — Foundation Week 1-2

**Ngày note:** 2026-05-10  
**Người báo cáo:** Thanh  
**Báo cho:** em Phúc / Team 1  
**Phạm vi:** Chỉ ghi các phần Thanh phụ trách hoặc Thanh trực tiếp chốt theo plan. Phần của anh Sơn để anh Sơn tự báo cáo.

## 1. Tóm tắt ngắn để báo miệng

Trong Foundation Week, anh Thanh đã chuẩn bị phần nền tảng để Team 2 sẵn sàng chạy với data thật: setup dependencies, chốt hướng lưu trữ CSV/SQLite, thống nhất format CSV với Team 1, làm EDA notebook, dựng FastAPI skeleton, viết Pydantic schema validation, định nghĩa các API endpoint chính và chuẩn bị note tích hợp cho UI. Các phần model training/preprocessing/stress test/predictor service chi tiết sẽ để anh Sơn báo cáo riêng theo phân công.

## 2. Roadmap phần Thanh đã làm

```mermaid
flowchart LR
    A[Setup môi trường] --> B[Chốt lưu trữ CSV/SQLite]
    B --> C[Chuẩn CSV cho Team 1]
    C --> D[EDA notebook]
    D --> E[FastAPI skeleton]
    E --> F[Pydantic validation]
    F --> G[API contract: health/predict/model-info]
    G --> H[Note UI disclaimer cho em Phúc]
```

## 3. Bảng công việc Thanh cần báo cáo

| Mốc                | Việc Thanh đã làm                 | Kết quả cụ thể                                                        | File/bằng chứng                                                        | Ý nghĩa với dự án                               |
| ------------------ | --------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------- |
| Phase 1 / Task 1.1 | Chuẩn bị dependencies             | Có `requirements.txt` cho stack Python, FastAPI, ML, EDA              | `requirements.txt`                                                     | Team 2 có môi trường chạy thống nhất            |
| Phase 1 / Task 1.3 | Chốt hướng lưu trữ                | Quyết định dùng CSV cho data chính, SQLite nếu cần query có cấu trúc  | `docs/discussions/data-format-spec.md`                                 | Giữ KISS, không over-engineer database          |
| Phase 1 / Task 1.4 | Thống nhất format data với Team 1 | Định nghĩa các cột CSV cần crawler xuất ra                            | `docs/discussions/data-format-spec.md`                                 | Team 1 biết format data để giao cho Team 2      |
| Phase 2 / Task 2.1 | Làm EDA notebook                  | Notebook đọc mock data, xem thống kê, tương quan, mùa vụ, outlier     | `notebooks/eda_baseline.ipynb`                                         | Chuẩn bị bước phân tích khi có data thật        |
| Phase 3 / Task 3.1 | Dựng FastAPI project structure    | Có cấu trúc `backend/` gồm `main.py`, `api/`, `schemas/`, `services/` | `backend/main.py`, `backend/api/routes.py`                             | Team 1 có backend skeleton để chuẩn bị tích hợp |
| Phase 3 / Task 3.2 | Viết Pydantic schemas             | Có request/response schema và validate range input                    | `backend/schemas/prediction.py`                                        | Cover Robustness, tránh input vô lý             |
| Phase 3 / Task 3.4 | Định nghĩa API endpoints          | Có contract cho `/health`, `/predict`, `/model/info`                  | `backend/api/routes.py`                                                | Em Phúc có thể chuẩn bị UI gọi API              |
| Phase 3 / Task 3.4 | Ghi chú disclaimer cho UI         | Đề xuất dòng cảnh báo AI chỉ mang tính tham khảo                      | `plans/team2-foundation-week/phase-03-api-skeleton-5-pillars-check.md` | Cover Bias, Robustness, Social Impact           |

## 4. Format data cần nhắc em Phúc

Team 1 cần xuất CSV theo các cột sau để Team 2 train lại model trên data thật:

| Cột                    | Kiểu mong muốn | Ý nghĩa                    |
| ---------------------- | -------------- | -------------------------- |
| `date`                 | `YYYY-MM-DD`   | Ngày ghi nhận              |
| `avg_temp_c`           | float          | Nhiệt độ trung bình        |
| `rainfall_mm`          | float          | Lượng mưa                  |
| `humidity_pct`         | float          | Độ ẩm                      |
| `sunshine_hours`       | float          | Số giờ nắng                |
| `month`                | int, 1-12      | Tháng                      |
| `historical_price_vnd` | float          | Giá cà phê nội địa, VND/kg |

File mẫu để em Phúc xem nhanh:

| Mục        | Đường dẫn                              |
| ---------- | -------------------------------------- |
| Spec chính | `docs/discussions/data-format-spec.md` |
| CSV sample | `data/sample/mock_coffee_sample.csv`   |

## 5. Các câu cần hỏi em Phúc / Team 1

| Nhóm câu hỏi     | Nội dung cần xác nhận                         | Vì sao cần hỏi                    |
| ---------------- | --------------------------------------------- | --------------------------------- |
| Thời gian data   | Có crawl được từ 2022 đến hiện tại không?     | Để chia train/test theo thời gian |
| Vùng giá         | Giá là Tây Nguyên, toàn quốc hay giá quốc tế? | Tránh bias vùng miền              |
| Vùng thời tiết   | Weather data lấy theo tỉnh nào?               | Cần khớp với vùng giá             |
| Độ thiếu dữ liệu | Có thiếu nhiều ngày không?                    | Ảnh hưởng preprocessing           |
| Đơn vị           | Có thống nhất VND/kg, mm, °C, % không?        | Tránh sai scale khi train         |

## 6. API contract cần báo cho em Phúc

| Endpoint      | Method | Mục đích                                      | Ghi chú cho UI                      |
| ------------- | ------ | --------------------------------------------- | ----------------------------------- |
| `/health`     | GET    | Kiểm tra backend và model load state          | UI có thể dùng để check server sống |
| `/predict`    | POST   | Gửi input thời tiết/giá lịch sử để lấy dự báo | UI form cần map đúng field          |
| `/model/info` | GET    | Lấy thông tin model, version, features        | Dùng nếu muốn hiển thị metadata     |

Swagger UI khi chạy backend:

```text
http://localhost:8000/docs
```

## 7. Disclaimer UI nên nhờ em Phúc thêm

| Vị trí             | Nội dung đề xuất                                                                                                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gần kết quả dự báo | Dự báo AI chỉ mang tính tham khảo. Dữ liệu huấn luyện chủ yếu từ vùng Tây Nguyên; khi áp dụng cho vùng khác hoặc thị trường biến động mạnh, kết quả có thể sai lệch. |

Lý do: dòng này giúp team cover **Bias**, **Robustness**, **Social Impact** mà không cần build thêm module phức tạp.

## 8. Những phần không đưa vào báo cáo của Thanh

Các mục dưới đây có thể đã nằm trong pipeline chung, nhưng theo plan là phần anh Sơn hoặc phần phối hợp, nên Thanh không cần nhận là việc cá nhân:

| Mục                           | Lý do không báo cáo dưới tên Thanh         |
| ----------------------------- | ------------------------------------------ |
| Tạo mock dataset full         | Theo plan Task 1.2 là phần Sơn             |
| Preprocessing pipeline        | Theo plan Task 2.2 là phần Sơn             |
| Train Random Forest baseline  | Theo plan Task 2.3 là phần Sơn             |
| Stress test robustness        | Theo plan Task 2.5 là phần Sơn             |
| Predictor service             | Theo plan Task 3.3 là phần Sơn             |
| 5 Pillars checkpoint document | Theo plan Task 3.5 là phần Sơn             |
| Metrics MAE/RMSE/R² hiện tại  | Nên để Sơn báo khi nói phần model training |

## 9. Việc tiếp theo của Thanh sau khi có data thật

| Thứ tự | Việc Thanh nên làm tiếp                              | Phụ thuộc               |
| ------ | ---------------------------------------------------- | ----------------------- |
| 1      | Nhận file CSV thật từ em Phúc/Thịnh                  | Team 1 giao data        |
| 2      | Kiểm tra data có đúng schema đã thống nhất không     | `data-format-spec.md`   |
| 3      | Chạy lại EDA notebook trên data thật                 | CSV thật                |
| 4      | Cập nhật API contract nếu field thực tế thay đổi     | Kết quả kiểm tra schema |
| 5      | Phối hợp Sơn train lại model và kiểm tra output API  | Model/data thật         |
| 6      | Chốt với em Phúc format response cuối cùng để nối UI | Backend chạy ổn         |

---
