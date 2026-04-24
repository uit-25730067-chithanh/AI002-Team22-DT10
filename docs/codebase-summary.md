# 🗂 Tóm tắt Cấu trúc Code (Codebase Summary)

_(Bản nháp - Sẽ được cập nhật khi dự án phát triển)_

## Kiến trúc Thư mục

### `backend/` (Team 2 - Thanh & Sơn)

- Xây dựng bằng **FastAPI**.
- Cung cấp các RESTful API (VD: `/predict`) cho frontend giao tiếp.
- Sử dụng Pydantic để kiểm tra và chuẩn hóa dữ liệu đầu vào (Đảm bảo **Robustness**).

### `model/` (Team 2 - Thanh & Sơn)

- Chứa các pipeline huấn luyện AI (`train.py`), script đánh giá sai số, và các model đã lưu (`.pkl`).
- Sử dụng thuật toán Machine Learning truyền thống (Scikit-learn: Random Forest / XGBoost) để đảm bảo khả năng giải thích (Đảm bảo **Transparency**).

### `crawler/` (Team 1 - Phúc & Thịnh)

- Script Python (BeautifulSoup/Requests) để tự động cào dữ liệu thời tiết và giá cà phê từ các trang nông nghiệp.
- Xuất dữ liệu đã làm sạch vào thư mục `data/raw/`.

### `frontend/` (Team 1 - Phúc & Thịnh)

- Giao diện web thuần HTML/JS/CSS để biểu diễn khả năng dự báo của mô hình AI cho người dùng cuối.
