from backend.schemas.prediction import PredictionRequest
from backend.services.farming_advisory import FarmingAdvisoryService


def _make_request(**overrides) -> PredictionRequest:
    payload = {
        "province": "Dak Lak",
        "area": "Buon Ho",
        "avg_temperature_c": 26.0,
        "total_rainfall_mm": 20.0,
        "avg_humidity_percent": 80.0,
        "avg_soil_moisture_0_7cm": 0.24,
        "soil_score": 5.0,
        "soil_data_confidence": "medium",
        "coffee_type": "Robusta / ca phe nhan xo noi dia",
        "price_fill_method": "observed",
        "dominant_soil_type": "Dat do bazan",
        "month": 11,
        "year": 2025,
        "latest_price_vnd_per_kg": 90000.0,
        "rolling_avg_price_vnd_per_kg": 88000.0,
        "price_observations": 1.0,
    }
    payload.update(overrides)
    return PredictionRequest(**payload)


def test_recommends_harvest_in_main_season() -> None:
    result = FarmingAdvisoryService().recommend(_make_request(month=11))

    assert result["action"] == "harvest"
    assert result["season_type"] == "main_season"
    assert result["advisory_type"] == "rule_based"
    assert 0.4 <= result["confidence"] <= 0.95
    assert result["warnings"] == []


def test_recommends_flowering_care_with_low_soil_moisture_warning() -> None:
    result = FarmingAdvisoryService().recommend(
        _make_request(month=3, total_rainfall_mm=5.0, avg_soil_moisture_0_7cm=0.12)
    )

    assert result["action"] == "flowering_care"
    assert result["season_type"] == "dry_season"
    assert "low_soil_moisture" in result["warnings"]
    assert result["confidence"] < 0.85


def test_recommends_growth_care_with_heavy_rainfall_warning() -> None:
    result = FarmingAdvisoryService().recommend(_make_request(month=7, total_rainfall_mm=300.0))

    assert result["action"] == "growth_care"
    assert result["season_type"] == "rainy_season"
    assert "heavy_rainfall" in result["warnings"]


def test_recommends_post_harvest_care() -> None:
    result = FarmingAdvisoryService().recommend(_make_request(month=1))

    assert result["action"] == "post_harvest_care"
    assert result["season_type"] == "dry_season"


def test_low_soil_suitability_reduces_confidence() -> None:
    baseline = FarmingAdvisoryService().recommend(_make_request(soil_score=5.0))
    result = FarmingAdvisoryService().recommend(_make_request(soil_score=3.0))

    assert "low_soil_suitability" in result["warnings"]
    assert result["confidence"] < baseline["confidence"]


def test_missing_optional_soil_fields_still_returns_valid_output() -> None:
    result = FarmingAdvisoryService().recommend(
        _make_request(avg_soil_moisture_0_7cm=None, soil_score=None, soil_data_confidence=None)
    )

    assert result["action"] == "harvest"
    assert result["warnings"] == []
    assert result["next_action_month"] == 12
