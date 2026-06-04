import json

import pytest

from backend.schemas.prediction import PredictionRequest
import backend.services.farming_advisory as farming_advisory
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


def test_rule_loader_rejects_missing_month_rule(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["month_rules"].pop("12")
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="đủ 12 tháng"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_invalid_section_shape(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["thresholds"] = []
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="section không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_invalid_top_level_shape(tmp_path, monkeypatch) -> None:
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(["month_rules", "thresholds", "penalties", "warning_labels"]), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="thiếu cấu hình bắt buộc"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_non_numeric_thresholds(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["thresholds"]["heavy_rainfall"] = "250"
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="ngưỡng cảnh báo không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_boolean_thresholds(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["thresholds"]["heavy_rainfall"] = True
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="ngưỡng cảnh báo không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_non_numeric_penalties(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["penalties"]["heavy_rainfall"] = None
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="penalty cảnh báo không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_boolean_penalties(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["penalties"]["heavy_rainfall"] = False
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="penalty cảnh báo không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_invalid_action(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["month_rules"]["11"]["action"] = "unknown_action"
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="action tháng 11 không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_invalid_season_type(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["month_rules"]["11"]["season_type"] = "future_season"
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="season_type tháng 11 không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_non_string_reasoning(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["month_rules"]["11"]["reasoning"] = None
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="reasoning tháng 11 không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_rule_loader_rejects_non_string_warning_label(tmp_path, monkeypatch) -> None:
    rules = json.loads(farming_advisory.RULES_PATH.read_text(encoding="utf-8"))
    rules["warning_labels"]["heavy_rainfall"] = None
    rule_path = tmp_path / "farming_advisory_rules.json"
    rule_path.write_text(json.dumps(rules), encoding="utf-8")

    monkeypatch.setattr(farming_advisory, "RULES_PATH", rule_path)
    farming_advisory.load_farming_advisory_rules.cache_clear()

    try:
        with pytest.raises(RuntimeError, match="nhãn cảnh báo không hợp lệ"):
            farming_advisory.load_farming_advisory_rules()
    finally:
        farming_advisory.load_farming_advisory_rules.cache_clear()


def test_reasoning_falls_back_when_warning_label_missing() -> None:
    reasoning = FarmingAdvisoryService._build_reasoning(
        "Base reasoning.",
        ["new_warning_code"],
        {},
    )

    assert "new_warning_code" in reasoning


def test_fallback_recommendation_keeps_response_shape() -> None:
    result = FarmingAdvisoryService.fallback_recommendation(_make_request(month=12))

    assert result["action"] == "off_season"
    assert result["season_type"] == "off_season"
    assert result["warnings"] == ["advisory_config_unavailable"]
    assert result["next_action_month"] == 1
    assert result["advisory_type"] == "rule_based"
