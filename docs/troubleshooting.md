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

## 5. Gọi `/predict` hoặc `/model/info` bị `401 Unauthorized`

**Lỗi:** Backend trả `{"detail":"Invalid API key"}`.
**Cách sửa:** Frontend hoặc `curl` phải gửi header `X-API-Key` đúng với key demo nội bộ. Không đặt key thật trong file được commit lên Git.

## 6. Gọi endpoint protected bị `503 Service Unavailable`

**Lỗi:** Backend trả thông báo thiếu `AI002_API_KEY` hoặc model chưa sẵn sàng.
**Cách sửa:** Kiểm tra biến môi trường `AI002_API_KEY` đã được set trong terminal/server chưa. Nếu lỗi liên quan model, kiểm tra `model/best_model/model.pkl` (file này đã được commit sẵn trong repo để demo tiện lợi, nhưng có thể bị hỏng hoặc mất trong quá trình clone/merge). Nếu bị mất hoặc hỏng, hãy chạy lệnh train và promote model để tạo lại.

## 7. Frontend gửi request bị `422 Unprocessable Entity`

**Lỗi:** Payload sai field, sai range hoặc category không nằm trong tập train.
**Cách sửa:** So lại request với `docs/discussions/2026-05-13-api-handoff-team2-real-data.md`. Các field như `province`, `area`, `coffee_type`, `price_fill_method`, `dominant_soil_type` phải khớp nhóm giá trị backend đã train.
