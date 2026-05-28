from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

# Import schema; fallback để chạy được cả từ root và từ thư mục backend
try:
    from backend.schemas.prediction import DEFAULT_PREDICTION_DISCLAIMER, PredictionRequest
    from backend.services.farming_advisory import FarmingAdvisoryService
except ModuleNotFoundError:
    from schemas.prediction import DEFAULT_PREDICTION_DISCLAIMER, PredictionRequest
    from services.farming_advisory import FarmingAdvisoryService


@dataclass
class ModelInfo:
    """Metadata của model đã train — dùng để trace version và reproducibility."""

    version: str
    trained_at: str
    feature_names: list[str]


class PredictorService:
    """
    Service chính: load model .pkl, biến đổi input -> DataFrame, predict,
    và trả về kết quả kèm lý giải (Trụ cột Transparency).
    """

    def __init__(self, model_path: str = "model/best_model/model.pkl") -> None:
        self.model_path = Path(model_path)
        self.model: Any | None = None
        self.model_info: ModelInfo | None = None
        self.farming_advisory = FarmingAdvisoryService()

    def load_model(self) -> bool:
        """Load model từ file .pkl; trả về False nếu file chưa có."""
        if not self.model_path.exists():
            self.model = None
            self.model_info = None
            return False

        self.model = joblib.load(self.model_path)
        feature_names = list(getattr(self.model, "feature_names_in_", []))

        # Đọc version ổn định từ metadata.json nếu có
        meta_path = self.model_path.parent / "metadata.json"
        version = f"unknown@{self.model_path.stat().st_mtime_ns}"
        trained_at = pd.Timestamp(self.model_path.stat().st_mtime, unit="s").isoformat()
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, TypeError):
                meta = {}
            version = f"{meta.get('experiment_id', 'unknown')}" if meta else version
            trained_at = meta.get("timestamp", trained_at) if meta else trained_at
            feature_names = list(meta.get("feature_names", feature_names)) if meta else feature_names

        self.model_info = ModelInfo(
            version=version,
            trained_at=trained_at,
            feature_names=feature_names,
        )
        return True

    def is_loaded(self) -> bool:
        """Kiểm tra model đã load thành công chưa."""
        return self.model is not None

    @staticmethod
    def _category_values(feature_names: list[str], prefix: str) -> set[str]:
        marker = f"{prefix}_"
        return {name.removeprefix(marker) for name in feature_names if name.startswith(marker)}

    @staticmethod
    def _one_hot_value(feature_name: str, prefix: str, selected_value: str) -> float:
        return 1.0 if feature_name == f"{prefix}_{selected_value}" else 0.0

    def _build_feature_row(self, request: PredictionRequest) -> pd.DataFrame:
        """
        Biến đổi PredictionRequest thành DataFrame để đưa vào model.
        Tự động tính month_sin, month_cos và fill giá trị mặc định cho optional fields.
        """
        humidity = request.avg_humidity_percent if request.avg_humidity_percent is not None else 75.0
        soil_moisture = request.avg_soil_moisture_0_7cm if request.avg_soil_moisture_0_7cm is not None else 0.24
        soil_score = request.soil_score if request.soil_score is not None else 5.0
        latest_price = request.latest_price_vnd_per_kg if request.latest_price_vnd_per_kg is not None else 90000.0
        rolling_price = (
            request.rolling_avg_price_vnd_per_kg
            if request.rolling_avg_price_vnd_per_kg is not None
            else latest_price
        )
        price_observations = request.price_observations
        if price_observations is None:
            price_observations = 1.0 if request.price_fill_method == "observed" else 0.0

        month_sin = float(np.sin(2 * np.pi * request.month / 12))
        month_cos = float(np.cos(2 * np.pi * request.month / 12))

        row = {
            "price_observations": price_observations,
            "avg_temp_c": request.avg_temperature_c,
            "rainfall_mm": request.total_rainfall_mm,
            "humidity_pct": humidity,
            "avg_soil_moisture_0_7cm": soil_moisture,
            "soil_score": soil_score,
            "month": request.month,
            "year": request.year,
            "quarter": int((request.month - 1) // 3 + 1),
            "month_sin": month_sin,
            "month_cos": month_cos,
            "rolling_avg_7d": rolling_price,
            "lag_1d": latest_price,
            "lag_7d": rolling_price,
        }

        feature_names = list(getattr(self.model, "feature_names_in_", row.keys()))
        if self.model_info and self.model_info.feature_names:
            feature_names = self.model_info.feature_names

        categorical_values = {
            "province": request.province,
            "area": request.area,
            "coffee_type": request.coffee_type,
            "price_fill_method": request.price_fill_method,
            "dominant_soil_type": request.dominant_soil_type,
        }
        if request.soil_data_confidence is not None:
            categorical_values["soil_data_confidence"] = request.soil_data_confidence

        for prefix, selected_value in categorical_values.items():
            available_values = self._category_values(feature_names, prefix)
            if available_values and selected_value not in available_values:
                allowed = ", ".join(sorted(available_values))
                raise ValueError(f"Giá trị `{prefix}` không hợp lệ: {selected_value}. Giá trị hợp lệ: {allowed}")

        feature_row: dict[str, float] = {}
        for name in feature_names:
            value = row.get(name, 0.0)
            for prefix, selected_value in categorical_values.items():
                if name.startswith(f"{prefix}_"):
                    value = self._one_hot_value(name, prefix, selected_value)
                    break
            feature_row[name] = float(value)
        return pd.DataFrame([feature_row])

    def explain(self, feature_row: pd.DataFrame) -> list[dict[str, Any]]:
        """
        Trích xuất top 3 feature importance liên quan đến input hiện tại.
        Mục tiêu: giải thích TẠI SAO model đưa ra dự báo này (Trụ cột Transparency).
        """
        if self.model is None:
            raise RuntimeError("Model chưa được load")

        importances = getattr(self.model, "feature_importances_", None)
        if importances is None:
            return []

        feature_names = list(feature_row.columns)
        usable_count = min(len(feature_names), len(importances))
        if usable_count == 0:
            return []
        ranked_idx = np.argsort(importances[:usable_count])[::-1][:3]

        explanations: list[dict[str, Any]] = []
        for idx in ranked_idx:
            feature = feature_names[idx]
            importance = float(importances[idx])
            value = float(feature_row.iloc[0][feature])
            explanations.append(
                {
                    "feature": feature,
                    "importance": round(importance, 4),
                    "input_value": round(value, 4),
                    "explanation": (
                        f"{feature} có mức quan trọng cao ({importance:.2%}) "
                        f"với giá trị hiện tại {value:.2f}."
                    ),
                }
            )
        return explanations

    def predict(self, request: PredictionRequest) -> dict[str, Any]:
        """
        Thực hiện dự báo giá cà phê + tính khoảng tin cậy ước lượng.
        Khoảng tin cậy dựa trên variance giữa các cây trong Random Forest.
        """
        if self.model is None and not self.load_model():
            raise RuntimeError(f"Không tìm thấy model: {self.model_path}")

        feature_row = self._build_feature_row(request)
        prediction = float(self.model.predict(feature_row)[0])

        # Tính độ lệch giữa các cây để ước lượng khoảng tin cậy đơn giản
        feature_values = feature_row.to_numpy(dtype=float)
        tree_preds = np.array([est.predict(feature_values)[0] for est in self.model.estimators_], dtype=float)
        pred_std = float(tree_preds.std())
        margin = 1.96 * pred_std  # ước lượng ~95% CI giả định phân phối chuẩn
        try:
            farming_recommendation = self.farming_advisory.recommend(request)
        except RuntimeError:
            farming_recommendation = self.farming_advisory.fallback_recommendation(request)

        return {
            "predicted_price_vnd": round(prediction, 2),
            "confidence_interval": (round(prediction - margin, 2), round(prediction + margin, 2)),
            "top_features": self.explain(feature_row),
            "model_version": self.model_info.version if self.model_info else "unknown",
            "farming_recommendation": farming_recommendation,
            "disclaimer": DEFAULT_PREDICTION_DISCLAIMER,
        }

    def get_model_info(self) -> dict[str, Any]:
        """Trả về metadata: đã load chưa, version, danh sách features, thời gian train."""
        if self.model is None and not self.load_model():
            return {
                "model_loaded": False,
                "model_path": str(self.model_path),
                "model_version": "unavailable",
                "features": [],
                "trained_at": None,
            }

        if self.model_info is None:
            raise RuntimeError("Model metadata chưa được load")
        return {
            "model_loaded": True,
            "model_path": str(self.model_path),
            "model_version": self.model_info.version,
            "features": self.model_info.feature_names,
            "trained_at": self.model_info.trained_at,
        }
