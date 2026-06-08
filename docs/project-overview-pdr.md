# Project Overview & Requirements (DT10)

## 1. Thông tin chung

- **Đề tài:** DT10 - AI dự báo kế hoạch canh tác mùa vụ và giá cà phê cho nông dân.
- **Môn học:** Tư duy Trí tuệ Nhân tạo (AI002).
- **Mục tiêu cốt lõi:** Thể hiện tư duy thiết kế hệ thống AI bền vững (Sustainable AI Design Thinking), KHÔNG yêu cầu giao diện phức tạp hay database đồ sộ.

## 2. Yêu cầu môn học (5 Trụ cột AI Bền vững)

Hệ thống phải thể hiện và chứng minh được 5 yếu tố sau trong thiết kế và code:

1. **Reliability (Tính tin cậy):** Độ ổn định, đánh giá bằng metrics rõ ràng (VD: MAE, RMSE). Phân chia theo thời gian: Train 2020-2024, Test 2025, 2026 chỉ dùng cho demo/inference/audit.
2. **Bias (Tính không thiên vị):** Đảm bảo không phân biệt đối xử hoặc thiên lệch về vùng miền khi áp dụng kết quả dự báo.
3. **Robustness (Kháng nhiễu):** Hệ thống có khả năng xử lý tốt khi dữ liệu thiếu (NaN) hoặc dữ liệu đầu vào không hợp lệ (VD: Outliers).
4. **Social Impact (Tác động xã hội):** Giúp nông dân nhỏ lẻ tiếp cận thông tin thị trường, tối ưu hóa lợi nhuận, chống ép giá.
5. **Transparency (Tính minh bạch):** Mô hình có thể giải thích được lý do đưa ra dự báo. Tránh các blackbox model nếu không cần thiết.

## 3. Kiến trúc & Công nghệ (Đề xuất)

- **Backend & Model:**
  - Framework: FastAPI (Python) cho tốc độ phát triển và tự động hóa Docs (Transparency).
  - Models: Machine Learning truyền thống (Random Forest, XGBoost).
  - Data Storage: CSV/SQLite (đảm bảo KISS).
- **Frontend & Crawler:**
  - Giao diện: HTML/JS/CSS cơ bản.
  - Crawler: Python (BeautifulSoup, Requests).

## 4. Phân công công việc

- **Thanh & Sơn:** Phụ trách data pipeline, model, backend/API, evaluation và hỗ trợ demo cuối kỳ.
- **Project members:** Cùng rà soát báo cáo, slide và demo trước buổi báo cáo.
