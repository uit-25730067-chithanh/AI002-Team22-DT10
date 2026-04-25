"""
Train Random Forest baseline cho dự báo giá cà phê.
Lưu model .pkl và in ra metrics MAE/RMSE/R^2.
"""

import argparse
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Đảm bảo import preprocess từ cùng thư mục
sys.path.insert(0, str(Path(__file__).parent))
from preprocess import preprocess_pipeline, split_temporal


def train_and_evaluate(data_path: str, model_dir: str = "model/saved") -> dict:
    """
    Load data, preprocess, train Random Forest, evaluate, save model.

    Args:
        data_path: Đường dẫn tới CSV (mock hoặc real).
        model_dir: Thư mục lưu model .pkl.

    Returns:
        Dictionary chứa metrics và feature importances.
    """
    # 1. Load data
    df = pd.read_csv(data_path)
    print(f"Đã load data: {df.shape[0]} dòng, {df.shape[1]} cột")

    # 2. Preprocess
    df_clean = preprocess_pipeline(df)
    print(f"Sau tiền xử lý: {df_clean.shape[0]} dòng (đã loại outliers)")

    # 3. Temporal split
    X_train, X_test, y_train, y_test = split_temporal(df_clean)
    print(f"Train: {len(X_train)} dòng | Test: {len(X_test)} dòng")

    # 4. Train
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # 5. Predict
    y_pred = model.predict(X_test)

    # 6. Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"\n=== Kết quả Random Forest Baseline ===")
    print(f"MAE  = {mae:,.0f} VND/kg")
    print(f"RMSE = {rmse:,.0f} VND/kg")
    print(f"R^2  = {r2:.4f}")

    # 7. Feature importance
    importances = pd.Series(
        model.feature_importances_,
        index=X_train.columns,
    ).sort_values(ascending=False)

    print(f"\n=== Feature Importance (Top 10) ===")
    for feat, imp in importances.head(10).items():
        print(f"  {feat}: {imp:.4f}")

    # 8. Plot feature importance
    plt.figure(figsize=(8, 5))
    importances.head(10).plot(kind="barh")
    plt.title("Top 10 Feature Importances — Random Forest")
    plt.xlabel("Importance")
    plt.tight_layout()
    plot_path = Path(model_dir) / "feature_importance_rf.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_path)
    print(f"\nĐã lưu biểu đồ feature importance: {plot_path}")

    # 9. Save model
    model_path = Path(model_dir) / "rf_baseline.pkl"
    joblib.dump(model, model_path)
    print(f"Đã lưu model: {model_path}")

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "feature_importance": importances.to_dict(),
        "model_path": str(model_path),
        "plot_path": str(plot_path),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train RF baseline")
    parser.add_argument(
        "--data",
        default="data/raw/mock_coffee_data.csv",
        help="Đường dẫn CSV input",
    )
    parser.add_argument(
        "--model-dir",
        default="model/saved",
        help="Thư mục lưu model và plot",
    )
    args = parser.parse_args()

    train_and_evaluate(args.data, args.model_dir)
