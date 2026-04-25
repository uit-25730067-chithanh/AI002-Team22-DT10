from fastapi import FastAPI

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

# Đăng ký các endpoint từ router (health, predict, model/info)
app.include_router(router)


@app.get("/")
def root() -> dict:
    """Trang chủ — trả về thông báo API đang chạy + link tài liệu Swagger."""
    return {
        "message": "AI002 API đang chạy",
        "docs": "/docs",
    }
