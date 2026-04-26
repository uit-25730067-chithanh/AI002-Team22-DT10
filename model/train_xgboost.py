"""
So sánh XGBoost vs Random Forest baseline.
Chạy khi đã cài xgboost (optional dependency).
Mỗi lần chạy tạo 1 timestamped experiment folder thay vì ghi đè.

KHUYẾN NGHỊ: Cài xgboost trong venv riêng, KHÔNG cài global:
    python -m venv venv_test
    source venv_test/bin/activate  # macOS/Linux
    pip install xgboost
"""

import argparse
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sys.path.insert(0, str(Path(__file__).parent))
from experiment_tracker import (
    append_experiment_csv,
    build_params,
    create_experiment,
    save_metrics,
    save_params,
    update_best_model,
)
from preprocess import preprocess_pipeline, split_temporal


def try_import_xgboost():
    """Thử import xgboost; nếu thiếu runtime (libomp) thì thoát nhẹ thay vì crash."""
    try:
        import xgboost as xgb
        return xgb
    except Exception as exc:
        print(f"Không thể dùng xgboost trong môi trường hiện tại: {exc}")
        print("Gợi ý: dùng venv riêng và cài đầy đủ runtime (macOS cần libomp).")
        return None


def train_and_compare(data_path: str, tag: str = "xgboost") -> dict:
    xgb = try_import_xgboost()
    if xgb is None:
        return {}

    # Tạo experiment folder chỉ khi xgboost khả dụng
    exp_dir = create_experiment(tag)
    print(f"Experiment folder: {exp_dir}")

    df = pd.read_csv(data_path)
    df_clean = preprocess_pipeline(df)
    X_train, X_test, y_train, y_test = split_temporal(df_clean)

    # Huấn luyện XGBoost Regressor — tham số tương đương RF để so sánh công bằng
    model = xgb.XGBRegressor(
        n_estimators=100,    # số cây tương đương RF
        max_depth=6,
        learning_rate=0.1,
        random_state=42,     # cố định seed
        n_jobs=-1,           # dùng tất cả CPU cores
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Đánh giá metrics giống RF để so sánh trực tiếp
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "train_size": len(X_train),
        "test_size": len(X_test),
    }

    print(f"\n=== Kết quả XGBoost ===")
    print(f"MAE  = {mae:,.0f} VND/kg")
    print(f"RMSE = {rmse:,.0f} VND/kg")
    print(f"R^2  = {r2:.4f}")

    # Lưu model vào experiment folder
    model_path = exp_dir / "xgboost_baseline.pkl"
    joblib.dump(model, model_path)
    print(f"Đã lưu model: {model_path}")

    # Lưu metadata
    save_metrics(exp_dir, metrics)
    params = build_params(
        model_params=model.get_params(),
        data_path=data_path,
    )
    save_params(exp_dir, params)

    # Append to experiments CSV và cập nhật best model
    append_experiment_csv(exp_dir, tag, "XGBRegressor", metrics)
    best_model_path = update_best_model(metric_key="mae", mode="min")
    print(f"Best model cập nhật: {best_model_path}")

    return {
        "experiment_id": exp_dir.name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "model_path": str(model_path),
        "exp_dir": str(exp_dir),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Huấn luyện XGBoost và so sánh với RF baseline")
    parser.add_argument("--data", default="data/raw/mock_coffee_data.csv")
    parser.add_argument(
        "--tag",
        default="xgboost",
        help="Tag cho experiment folder",
    )
    args = parser.parse_args()
    train_and_compare(args.data, args.tag)
