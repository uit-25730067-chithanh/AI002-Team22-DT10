from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

try:
    from backend.schemas.prediction import PredictionRequest
except ModuleNotFoundError:
    from schemas.prediction import PredictionRequest


RULES_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "farming_advisory_rules.json"
REQUIRED_MONTH_KEYS = {str(month) for month in range(1, 13)}
REQUIRED_MONTH_RULE_FIELDS = {"action", "season_type", "reasoning"}
REQUIRED_THRESHOLD_KEYS = {
    "base_confidence",
    "min_confidence",
    "max_confidence",
    "low_soil_moisture",
    "heavy_rainfall",
    "heat_stress",
    "low_soil_score",
}
REQUIRED_WARNING_KEYS = {
    "low_soil_moisture",
    "heavy_rainfall",
    "heat_stress",
    "low_soil_suitability",
    "low_soil_data_confidence",
}


def _is_number(value: Any) -> bool:
    return type(value) in (int, float)


@lru_cache(maxsize=1)
def load_farming_advisory_rules() -> dict[str, Any]:
    try:
        rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError("Không tìm thấy file rule canh tác") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("File rule canh tác không hợp lệ") from exc

    required_sections = {"month_rules", "thresholds", "penalties", "warning_labels"}
    if not isinstance(rules, dict) or not required_sections.issubset(rules.keys()):
        raise RuntimeError("File rule canh tác thiếu cấu hình bắt buộc")
    _validate_farming_advisory_rules(rules)
    return rules


def _validate_farming_advisory_rules(rules: dict[str, Any]) -> None:
    month_rules = rules["month_rules"]
    thresholds = rules["thresholds"]
    penalties = rules["penalties"]
    warning_labels = rules["warning_labels"]

    if not all(isinstance(section, dict) for section in [month_rules, thresholds, penalties, warning_labels]):
        raise RuntimeError("File rule canh tác có cấu trúc section không hợp lệ")
    if not REQUIRED_MONTH_KEYS.issubset(month_rules):
        raise RuntimeError("File rule canh tác thiếu rule cho đủ 12 tháng")
    for month in REQUIRED_MONTH_KEYS:
        if not isinstance(month_rules[month], dict):
            raise RuntimeError(f"File rule canh tác có rule tháng {month} không hợp lệ")
        if not REQUIRED_MONTH_RULE_FIELDS.issubset(month_rules[month]):
            raise RuntimeError(f"File rule canh tác thiếu field cho tháng {month}")

    if not REQUIRED_THRESHOLD_KEYS.issubset(thresholds):
        raise RuntimeError("File rule canh tác thiếu ngưỡng cảnh báo bắt buộc")
    if not REQUIRED_WARNING_KEYS.issubset(penalties):
        raise RuntimeError("File rule canh tác thiếu penalty cho cảnh báo bắt buộc")
    if not REQUIRED_WARNING_KEYS.issubset(warning_labels):
        raise RuntimeError("File rule canh tác thiếu nhãn cảnh báo bắt buộc")
    if not all(_is_number(thresholds[key]) for key in REQUIRED_THRESHOLD_KEYS):
        raise RuntimeError("File rule canh tác có ngưỡng cảnh báo không hợp lệ")
    if not all(_is_number(penalties[key]) for key in REQUIRED_WARNING_KEYS):
        raise RuntimeError("File rule canh tác có penalty cảnh báo không hợp lệ")


class FarmingAdvisoryService:
    def recommend(self, request: PredictionRequest) -> dict[str, Any]:
        rules = load_farming_advisory_rules()
        month_rules = rules["month_rules"]
        thresholds = rules["thresholds"]
        penalties_by_warning = rules["penalties"]

        month_rule = month_rules.get(
            str(request.month),
            {
                "action": "off_season",
                "season_type": "off_season",
                "reasoning": "Chưa có rule canh tác cụ thể cho tháng này.",
            },
        )
        action = month_rule["action"]
        season_type = month_rule["season_type"]
        base_reasoning = month_rule["reasoning"]
        warnings: list[str] = []
        penalties = 0.0

        if (
            request.avg_soil_moisture_0_7cm is not None
            and request.avg_soil_moisture_0_7cm < thresholds["low_soil_moisture"]
        ):
            warnings.append("low_soil_moisture")
            penalties += penalties_by_warning["low_soil_moisture"]

        if request.total_rainfall_mm > thresholds["heavy_rainfall"]:
            warnings.append("heavy_rainfall")
            penalties += penalties_by_warning["heavy_rainfall"]

        if request.avg_temperature_c >= thresholds["heat_stress"]:
            warnings.append("heat_stress")
            penalties += penalties_by_warning["heat_stress"]

        if request.soil_score is not None and request.soil_score <= thresholds["low_soil_score"]:
            warnings.append("low_soil_suitability")
            penalties += penalties_by_warning["low_soil_suitability"]

        if request.soil_data_confidence == "low":
            warnings.append("low_soil_data_confidence")
            penalties += penalties_by_warning["low_soil_data_confidence"]

        confidence = min(
            thresholds["max_confidence"],
            max(thresholds["min_confidence"], thresholds["base_confidence"] - penalties),
        )
        next_action_month = 1 if request.month == 12 else request.month + 1
        next_action = month_rules.get(str(next_action_month), {"action": "off_season"})["action"]
        reasoning = self._build_reasoning(base_reasoning, warnings, rules["warning_labels"])

        return {
            "action": action,
            "season_type": season_type,
            "confidence": round(confidence, 2),
            "reasoning": reasoning,
            "warnings": warnings,
            "next_action_month": next_action_month,
            "next_action": next_action,
            "advisory_type": "rule_based",
        }

    @staticmethod
    def fallback_recommendation(request: PredictionRequest) -> dict[str, Any]:
        next_action_month = 1 if request.month == 12 else request.month + 1
        return {
            "action": "off_season",
            "season_type": "off_season",
            "confidence": 0.4,
            "reasoning": (
                "Không thể tải cấu hình rule canh tác tại thời điểm dự báo. "
                "Hệ thống vẫn trả kết quả giá, nhưng gợi ý canh tác cần kiểm tra lại với nguồn địa phương."
            ),
            "warnings": ["advisory_config_unavailable"],
            "next_action_month": next_action_month,
            "next_action": "off_season",
            "advisory_type": "rule_based",
        }

    @staticmethod
    def _build_reasoning(base_reasoning: str, warnings: list[str], warning_labels: dict[str, str]) -> str:
        if not warnings:
            return (
                f"{base_reasoning} Điều kiện đất và thời tiết hiện tại không có cảnh báo lớn. "
                "Đây là gợi ý rule-based để tham khảo."
            )

        details = "; ".join(warning_labels.get(warning, warning) for warning in warnings)
        return (
            f"{base_reasoning} Cảnh báo hiện tại: {details}. Đây là gợi ý rule-based để tham khảo, "
            "không thay thế tư vấn nông nghiệp tại địa phương."
        )
