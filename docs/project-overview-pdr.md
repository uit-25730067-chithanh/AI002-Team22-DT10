# Project Overview & Requirements (DT10)

## 1. Thông tin chung

- **Đề tài:** DT10 - AI dự báo kế hoạch canh tác mùa vụ và giá cà phê cho nông dân.
- **Môn học:** Tư duy Trí tuệ Nhân tạo (AI002).
- **Mục tiêu cốt lõi:** Thể hiện tư duy thiết kế hệ thống AI bền vững (Sustainable AI Design Thinking), KHÔNG yêu cầu giao diện phức tạp hay database đồ sộ.

## 2. Yêu cầu môn học (5 Trụ cột AI Bền vững)

Hệ thống phải thể hiện và chứng minh được 5 yếu tố sau trong thiết kế và code:

1. **Reliability (Tính tin cậy):** Độ ổn định, đánh giá bằng metrics rõ ràng (VD: MAE, RMSE). Phân chia tập Train/Test hợp lý (Train: 2022-2024, Test: 2025).
2. **Bias (Tính không thiên vị):** Đảm bảo không phân biệt đối xử hoặc thiên lệch về vùng miền khi áp dụng kết quả dự báo.
3. **Robustness (Kháng nhiễu):** Hệ thống có khả năng xử lý tốt khi dữ liệu thiếu (NaN) hoặc dữ liệu đầu vào không hợp lệ (VD: Outliers).
4. **Social Impact (Tác động xã hội):** Giúp nông dân nhỏ lẻ tiếp cận thông tin thị trường, tối ưu hóa lợi nhuận, chống ép giá.
5. **Transparency (Tính minh bạch):** Mô hình có thể giải thích được lý do đưa ra dự báo. Tránh các blackbox model nếu không cần thiết.

## 3. Kiến trúc & Công nghệ (Đề xuất)

- **Backend & Model (Team 2):**
  - Framework: FastAPI (Python) cho tốc độ phát triển và tự động hóa Docs (Transparency).
  - Models: Machine Learning truyền thống (Random Forest, XGBoost).
  - Data Storage: CSV/SQLite (đảm bảo KISS).
- **Frontend & Crawler (Team 1):**
  - Giao diện: HTML/JS/CSS cơ bản.
  - Crawler: Python (BeautifulSoup, Requests).

## 4. Phân công công việc

- **Team 1 (Phúc & Thịnh):** Thu thập dữ liệu, làm sạch cơ bản, xây dựng giao diện người dùng (Web UI) và chuẩn bị Slide báo cáo.
- **Team 2 (Thanh & Sơn):** Chịu trách nhiệm cốt lõi kỹ thuật AI, xây dựng và huấn luyện model, viết API backend (FastAPI) cung cấp endpoint dự báo.
