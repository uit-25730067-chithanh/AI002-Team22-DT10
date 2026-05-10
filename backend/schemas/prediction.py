from typing import Optional

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Đầu vào dự báo — Pydantic validate tự động các ràng buộc (Trụ cột Robustness)."""

    avg_temp_c: float = Field(..., ge=15.0, le=40.0)          # nhiệt độ trung bình (°C)
    rainfall_mm: float = Field(..., ge=0.0, le=500.0)        # lượng mưa (mm)
    humidity_pct: Optional[float] = Field(None, ge=0.0, le=100.0)   # độ ẩm (%), tùy chọn
    sunshine_hours: Optional[float] = Field(None, ge=0.0, le=14.0) # giờ nắng, tùy chọn
    month: int = Field(..., ge=1, le=12)                     # tháng trong năm
    historical_price_7d_avg: float = Field(..., ge=30000.0, le=100000.0)  # giá TB 7 ngày


class FeatureExplanation(BaseModel):
    """Giải thích feature importance cho từng dự báo (Trụ cột Transparency)."""

    feature: str          # tên đặc trưng
    importance: float     # mức độ quan trọng trong model
    input_value: float    # giá trị đầu vào hiện tại
    explanation: str      # diễn giải bằng ngôn ngữ tự nhiên


class PredictionResponse(BaseModel):
    """Đầu ra dự báo — bao gồm giá dự đoán, khoảng tin cậy và lý giải."""

    predicted_price_vnd: float          # giá dự báo (VND/kg)
    confidence_interval: tuple[float, float]  # khoảng tin cậy 95% (ước lượng từ variance cây)
    top_features: list[FeatureExplanation]      # top 3 đặc trưng ảnh hưởng nhất
    model_version: str                  # phiên bản model để traceability
