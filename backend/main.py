from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router từ module routes; fallback để chạy được cả từ root và từ thư mục backend
try:
    from backend.api.routes import router
except ModuleNotFoundError:
    from api.routes import router

# Khởi tạo ứng dụng FastAPI — entry point của toàn bộ backend
app = FastAPI(
    title="AI002 Coffee Price Forecast API",
    version="0.1.0",
    description="FastAPI skeleton cho Team 2 foundation week",
)

# CORS cho phép mọi origin để có thể mở file index.html trực tiếp (origin 'null')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "null"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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
