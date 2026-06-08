from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import router từ module routes; fallback để chạy được cả từ root và từ thư mục backend
try:
    from backend.api.routes import router
except ModuleNotFoundError:
    from api.routes import router

# Khởi tạo ứng dụng FastAPI — entry point của toàn bộ backend
app = FastAPI(
    title="AI002 Coffee Price Forecast API",
    version="0.1.0",
    description="FastAPI service for AI002 coffee price forecasting",
)

# CORS cho phép origin từ env
allow_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in allow_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["X-API-Key", "Content-Type", "Accept"],
)

# Đăng ký các endpoint từ router (health, predict, model/info)
app.include_router(router)


@app.get("/")
def root() -> dict:
    """Trang chủ — trả về thông báo API đang chạy + link tài liệu Swagger."""
    return {
        "message": "AI002 API đang chạy",
        "docs": "/docs",
    }
