from typing import Literal, Optional

from pydantic import BaseModel, Field


DEFAULT_PREDICTION_DISCLAIMER = "Dự báo giá và gợi ý canh tác chỉ mang tính tham khảo, không thay thế tư vấn tài chính hoặc tư vấn nông nghiệp tại địa phương."
FarmingAction = Literal[
    "post_harvest_care",
    "flowering_care",
    "growth_care",
    "harvest",
    "off_season",
]


class PredictionRequest(BaseModel):
    """Đầu vào dự báo — Pydantic validate tự động các ràng buộc (Trụ cột Robustness)."""

    province: str = Field(..., min_length=1, max_length=80)
    area: str = Field(..., min_length=1, max_length=80)
    avg_temperature_c: float = Field(..., ge=10.0, le=45.0)
    total_rainfall_mm: float = Field(..., ge=0.0, le=1000.0)
    avg_humidity_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    avg_soil_moisture_0_7cm: Optional[float] = Field(None, ge=0.0, le=1.0)
    soil_score: Optional[float] = Field(None, ge=0.0, le=5.0)
    soil_data_confidence: Optional[Literal["low", "medium", "high"]] = None
    coffee_type: str = Field("Robusta / ca phe nhan xo noi dia", min_length=1, max_length=80)
    price_fill_method: Literal["observed", "interpolated_area", "province_proxy"] = "observed"
    dominant_soil_type: str = Field("Dat do bazan", min_length=1, max_length=80)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(2025, ge=2022, le=2030)
    latest_price_vnd_per_kg: Optional[float] = Field(None, ge=30000.0, le=200000.0)
    rolling_avg_price_vnd_per_kg: Optional[float] = Field(None, ge=30000.0, le=200000.0)
    price_observations: Optional[float] = Field(None, ge=0.0)


class FeatureExplanation(BaseModel):
    """Giải thích feature importance cho từng dự báo (Trụ cột Transparency)."""

    feature: str          # tên đặc trưng
    importance: float     # mức độ quan trọng trong model
    input_value: float    # giá trị đầu vào hiện tại
    explanation: str      # diễn giải bằng ngôn ngữ tự nhiên


class FarmingRecommendation(BaseModel):
    action: FarmingAction
    season_type: Literal["dry_season", "rainy_season", "main_season", "off_season"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    warnings: list[str]
    next_action_month: int = Field(..., ge=1, le=12)
    next_action: FarmingAction
    advisory_type: Literal["rule_based"] = "rule_based"


class PredictionResponse(BaseModel):
    """Đầu ra dự báo — bao gồm giá dự đoán, khoảng tin cậy và lý giải."""

    predicted_price_vnd: float          # giá dự báo (VND/kg)
    confidence_interval: tuple[float, float]  # khoảng tin cậy 95% (ước lượng từ variance cây)
    top_features: list[FeatureExplanation]      # top 3 đặc trưng ảnh hưởng nhất
    model_version: str                  # phiên bản model để traceability
    farming_recommendation: FarmingRecommendation
    disclaimer: str = DEFAULT_PREDICTION_DISCLAIMER
