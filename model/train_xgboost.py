"""
So sánh XGBoost vs Random Forest baseline.
Chạy khi đã cài xgboost (optional dependency).
"""

import argparse
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sys.path.insert(0, str(Path(__file__).parent))
from preprocess import preprocess_pipeline, split_temporal


def try_import_xgboost():
    try:
        import xgboost as xgb
        return xgb
    except ImportError:
        print("xgboost chưa được cài. Bỏ qua so sánh.")
        return None


def train_and_compare(data_path: str) -> dict:
    df = pd.read_csv(data_path)
    df_clean = preprocess_pipeline(df)
    X_train, X_test, y_train, y_test = split_temporal(df_clean)

    xgb = try_import_xgboost()
    if xgb is None:
        return {}

    # XGBoost Regressor
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"\n=== Kết quả XGBoost ===")
    print(f"MAE  = {mae:,.0f} VND/kg")
    print(f"RMSE = {rmse:,.0f} VND/kg")
    print(f"R^2  = {r2:.4f}")

    # Save
    model_dir = Path("model/saved")
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "xgboost_baseline.pkl"
    joblib.dump(model, model_path)
    print(f"Đã lưu model: {model_path}")

    return {"mae": mae, "rmse": rmse, "r2": r2}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/mock_coffee_data.csv")
    args = parser.parse_args()
    train_and_compare(args.data)
