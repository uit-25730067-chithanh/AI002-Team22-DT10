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


@lru_cache(maxsize=1)
def load_farming_advisory_rules() -> dict[str, Any]:
    try:
        rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError("Không tìm thấy file rule canh tác") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("File rule canh tác không hợp lệ") from exc

    required_sections = {"month_rules", "thresholds", "penalties", "warning_labels"}
    if not required_sections.issubset(rules):
        raise RuntimeError("File rule canh tác thiếu cấu hình bắt buộc")
    return rules


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
        next_action = month_rules[str(next_action_month)]["action"]
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
    def _build_reasoning(base_reasoning: str, warnings: list[str], warning_labels: dict[str, str]) -> str:
        if not warnings:
            return (
                f"{base_reasoning} Điều kiện đất và thời tiết hiện tại không có cảnh báo lớn. "
                "Đây là gợi ý rule-based để tham khảo."
            )

        details = "; ".join(warning_labels[warning] for warning in warnings)
        return (
            f"{base_reasoning} Cảnh báo hiện tại: {details}. Đây là gợi ý rule-based để tham khảo, "
            "không thay thế tư vấn nông nghiệp tại địa phương."
        )
