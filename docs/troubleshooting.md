# 🚑 Hướng dẫn Sửa lỗi (Troubleshooting)

_(Bản nháp - Sẽ được bổ sung liên tục trong quá trình dev)_

## 1. Lỗi kẹt Cổng (Port 8000 already in use)

**Lỗi:** `[Errno 98] Address already in use` khi chạy lệnh Uvicorn.
**Cách sửa:** Chạy API trên một cổng khác bằng lệnh: `uvicorn main:app --port 8001`, hoặc tìm và tắt tiến trình đang chiếm port 8000.

## 2. Thiếu thư viện (Missing Dependencies)

**Lỗi:** `ModuleNotFoundError: No module named 'fastapi'` (hoặc tên thư viện khác).
**Cách sửa:** Đảm bảo bạn đã kích hoạt môi trường ảo (virtual environment) và chạy lệnh: `pip install -r requirements.txt`.

## 3. Lỗi không tìm thấy Model (Model Loading Errors)

**Lỗi:** `FileNotFoundError: model.pkl not found`
**Cách sửa:** Đảm bảo bạn đang mở terminal và chạy code từ thư mục gốc của dự án, hoặc kiểm tra lại đường dẫn file (dùng absolute path) trong code `backend/services/`.

## 4. Lỗi CORS ở Frontend

**Lỗi:** Trình duyệt báo đỏ `Blocked by CORS policy` khi Frontend (HTML) gọi API.
**Cách sửa:** Báo cho Team 2 thêm domain của Frontend vào phần cấu hình `CORSMiddleware` bên trong file `main.py` của FastAPI.
