import pytest

from backend.schemas.prediction import PredictionRequest
from backend.services.predictor import PredictorService


def test_predictor_service_after_model_training() -> None:
    """
    Kiểm tra predictor service sau khi đã train model.
    Nếu model chưa tồn tại thì skip thay vì fail — để CI không bị block.
    """
    predictor = PredictorService(model_path="model/saved/rf_baseline.pkl")
    loaded = predictor.load_model()

    if not loaded:
        pytest.skip("model/saved/rf_baseline.pkl chưa có; train model trước khi chạy test này")

    # Payload mẫu: tháng 11, nhiệt độ 26°C, lượng mưa 20mm, giá TB 62k
    payload = PredictionRequest(
        avg_temp_c=26.0,
        rainfall_mm=20.0,
        humidity_pct=80.0,
        sunshine_hours=6.0,
        month=11,
        historical_price_7d_avg=62000.0,
    )

    result = predictor.predict(payload)

    # Kiểm tra cấu trúc response có đầy đủ các trường bắt buộc
    assert "predicted_price_vnd" in result
    assert "confidence_interval" in result
    assert "top_features" in result
    assert len(result["top_features"]) == 3  # top 3 features giải thích
