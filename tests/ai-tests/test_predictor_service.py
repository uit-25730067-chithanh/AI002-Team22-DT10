import pytest

from backend.schemas.prediction import PredictionRequest
from backend.services.predictor import PredictorService


def test_predictor_service_after_model_training() -> None:
    """
    Kiểm tra predictor service sau khi đã train model.
    Nếu model chưa tồn tại thì skip thay vì fail — để CI không bị block.
    """
    predictor = PredictorService(model_path="model/best_model/model.pkl")
    loaded = predictor.load_model()

    if not loaded:
        pytest.skip("model/best_model/model.pkl chưa có; train model trước khi chạy test này")

    payload = PredictionRequest(
        province="Dak Lak",
        area="Buon Ho",
        avg_temperature_c=26.0,
        total_rainfall_mm=20.0,
        avg_humidity_percent=80.0,
        avg_soil_moisture_0_7cm=0.24,
        soil_score=5.0,
        soil_data_confidence="medium",
        month=11,
        year=2025,
        latest_price_vnd_per_kg=90000.0,
        rolling_avg_price_vnd_per_kg=88000.0,
    )

    result = predictor.predict(payload)

    # Kiểm tra cấu trúc response có đầy đủ các trường bắt buộc
    assert "predicted_price_vnd" in result
    assert "confidence_interval" in result
    assert "top_features" in result
    assert "disclaimer" in result
    assert len(result["top_features"]) == 3  # top 3 features giải thích
