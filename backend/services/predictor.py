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
    from backend.schemas.prediction import PredictionRequest
except ModuleNotFoundError:
    from schemas.prediction import PredictionRequest


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
                version = f"{meta.get('experiment_id', 'unknown')}"
                trained_at = meta.get("timestamp", trained_at)
                feature_names = list(meta.get("feature_names", feature_names))
            except Exception:
                pass

        self.model_info = ModelInfo(
            version=version,
            trained_at=trained_at,
            feature_names=feature_names,
        )
        return True

    def is_loaded(self) -> bool:
        """Kiểm tra model đã load thành công chưa."""
        return self.model is not None

    def _build_feature_row(self, request: PredictionRequest) -> pd.DataFrame:
        """
        Biến đổi PredictionRequest thành DataFrame để đưa vào model.
        Tự động tính month_sin, month_cos và fill giá trị mặc định cho optional fields.
        """
        humidity = request.avg_humidity_percent if request.avg_humidity_percent is not None else 75.0
        soil_moisture = request.avg_soil_moisture_0_7cm if request.avg_soil_moisture_0_7cm is not None else 0.24
        soil_score = request.soil_score if request.soil_score is not None else 5.0
        latest_price = request.latest_price_vnd_per_kg if request.latest_price_vnd_per_kg is not None else 90000.0
        rolling_price = request.rolling_avg_price_vnd_per_kg if request.rolling_avg_price_vnd_per_kg is not None else latest_price

        month_sin = float(np.sin(2 * np.pi * request.month / 12))
        month_cos = float(np.cos(2 * np.pi * request.month / 12))

        row = {
            "price_observations": 0.0,
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

        feature_row: dict[str, float] = {}
        for name in feature_names:
            value = row.get(name, 0.0)
            if name.startswith("province_"):
                value = 1.0 if name == f"province_{request.province}" else 0.0
            elif name.startswith("area_"):
                value = 1.0 if name == f"area_{request.area}" else 0.0
            elif name.startswith("soil_data_confidence_") and request.soil_data_confidence:
                value = 1.0 if name == f"soil_data_confidence_{request.soil_data_confidence}" else 0.0
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
        ranked_idx = np.argsort(importances)[::-1][:3]

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
                    "explanation": f"{feature} có mức quan trọng cao ({importance:.2%}) với giá trị hiện tại {value:.2f}.",
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

        return {
            "predicted_price_vnd": round(prediction, 2),
            "confidence_interval": (round(prediction - margin, 2), round(prediction + margin, 2)),
            "top_features": self.explain(feature_row),
            "model_version": self.model_info.version if self.model_info else "unknown",
            "disclaimer": "Dự báo chỉ mang tính tham khảo, không thay thế tư vấn tài chính hoặc quyết định bán hàng thực tế.",
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

        assert self.model_info is not None
        return {
            "model_loaded": True,
            "model_path": str(self.model_path),
            "model_version": self.model_info.version,
            "features": self.model_info.feature_names,
            "trained_at": self.model_info.trained_at,
        }
