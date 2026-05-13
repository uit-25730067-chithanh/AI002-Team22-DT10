import json

import joblib
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestRegressor

from backend.schemas.prediction import PredictionRequest
from backend.services.predictor import PredictorService


FEATURE_NAMES = [
    "price_observations",
    "avg_temp_c",
    "rainfall_mm",
    "humidity_pct",
    "avg_soil_moisture_0_7cm",
    "soil_score",
    "month",
    "year",
    "quarter",
    "month_sin",
    "month_cos",
    "rolling_avg_7d",
    "lag_1d",
    "lag_7d",
    "province_Dak Lak",
    "area_Buon Ho",
    "coffee_type_Robusta / ca phe nhan xo noi dia",
    "price_fill_method_observed",
    "dominant_soil_type_Dat do bazan",
    "soil_data_confidence_medium",
]


def _make_test_predictor(tmp_path) -> PredictorService:
    model_dir = tmp_path / "best_model"
    model_dir.mkdir()
    model_path = model_dir / "model.pkl"

    X_train = pd.DataFrame(
        [
            [1.0, 26.0, 20.0, 80.0, 0.24, 5.0, 11, 2025, 4, -0.5, 0.866, 88000, 90000, 88000, 1, 1, 1, 1, 1, 1],
            [1.0, 25.0, 30.0, 78.0, 0.25, 4.8, 10, 2025, 4, -0.866, 0.5, 87000, 88000, 87000, 1, 1, 1, 1, 1, 1],
        ],
        columns=FEATURE_NAMES,
    )
    model = RandomForestRegressor(n_estimators=5, random_state=42)
    model.fit(X_train, [90000.0, 88000.0])
    joblib.dump(model, model_path)

    metadata = {
        "experiment_id": "test_rf_fixture",
        "timestamp": "2026-05-13T00:00:00+00:00",
        "feature_names": FEATURE_NAMES,
    }
    (model_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

    predictor = PredictorService(model_path=str(model_path))
    loaded = predictor.load_model()
    assert loaded
    return predictor


def test_predictor_service_after_model_training(tmp_path) -> None:
    predictor = _make_test_predictor(tmp_path)
    payload = PredictionRequest(
        province="Dak Lak",
        area="Buon Ho",
        avg_temperature_c=26.0,
        total_rainfall_mm=20.0,
        avg_humidity_percent=80.0,
        avg_soil_moisture_0_7cm=0.24,
        soil_score=5.0,
        soil_data_confidence="medium",
        coffee_type="Robusta / ca phe nhan xo noi dia",
        price_fill_method="observed",
        dominant_soil_type="Dat do bazan",
        month=11,
        year=2025,
        latest_price_vnd_per_kg=90000.0,
        rolling_avg_price_vnd_per_kg=88000.0,
        price_observations=1.0,
    )

    result = predictor.predict(payload)

    # Kiểm tra cấu trúc response có đầy đủ các trường bắt buộc
    assert "predicted_price_vnd" in result
    assert "confidence_interval" in result
    assert "top_features" in result
    assert "disclaimer" in result
    assert len(result["top_features"]) == 3  # top 3 features giải thích


def test_predictor_service_rejects_unknown_area(tmp_path) -> None:
    predictor = _make_test_predictor(tmp_path)
    payload = PredictionRequest(
        province="Dak Lak",
        area="Unknown Area",
        avg_temperature_c=26.0,
        total_rainfall_mm=20.0,
        soil_data_confidence="medium",
        month=11,
    )

    with pytest.raises(ValueError, match="area"):
        predictor.predict(payload)
