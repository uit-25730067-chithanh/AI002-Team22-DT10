"""
Train Random Forest baseline cho dự báo giá cà phê.
Lưu model .pkl và in ra metrics MAE/RMSE/R^2.
Mỗi lần chạy tạo 1 timestamped experiment folder thay vì ghi đè.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Đảm bảo import preprocess và tracker từ cùng thư mục
sys.path.insert(0, str(Path(__file__).parent))
from experiment_tracker import (  # noqa: E402
    append_experiment_csv,
    build_params,
    create_experiment,
    list_experiments,
    save_metrics,
    save_params,
    update_best_model,
)
from preprocess import preprocess_pipeline, split_temporal  # noqa: E402


def _update_best_model_after_training(
        tag: str, experiment_id: str) -> Path | None:
    if tag.startswith("rf_monthly"):
        return update_best_model(
            metric_key="mae",
            mode="min",
            tag_prefix="rf_monthly",
            fallback_experiment_id=experiment_id,
        )

    if tag.startswith("rf_real"):
        return update_best_model(
            metric_key="mae",
            mode="min",
            tag_prefix="rf_real",
            fallback_experiment_id=experiment_id,
        )

    has_real_experiment = any(row.get("tag", "").startswith(
        "rf_real") for row in list_experiments())
    if has_real_experiment:
        return update_best_model(
            metric_key="mae",
            mode="min",
            tag_prefix="rf_real")

    return update_best_model(metric_key="mae", mode="min")


def train_and_evaluate(
    data_path: str,
    tag: str = "rf_baseline",
    promote: bool = True,
) -> dict:
    """
    Đọc dữ liệu, tiền xử lý, huấn luyện Random Forest, đánh giá, lưu model.

    Args:
        data_path: Đường dẫn tới CSV (mock hoặc real).
        tag: Tag cho experiment folder (mặc định 'rf_baseline').

    Returns:
        Dictionary chứa metrics, feature importances, và experiment_id.
    """
    # 0. Tạo experiment folder mới
    exp_dir = create_experiment(tag)
    print(f"Experiment folder: {exp_dir}")

    # 1. Đọc dữ liệu CSV đầu vào (mock hoặc thật)
    df = pd.read_csv(data_path)
    print(f"Đã load data: {df.shape[0]} dòng, {df.shape[1]} cột")

    # 2. Tiền xử lý: điền NaN, loại outliers, tạo features
    df_clean = preprocess_pipeline(df)
    print(f"Sau tiền xử lý: {df_clean.shape[0]} dòng (đã loại outliers)")

    # 3. Chia train/test theo thời gian — tránh data leakage
    X_train, X_test, y_train, y_test = split_temporal(df_clean)
    print(f"Train: {len(X_train)} dòng | Test: {len(X_test)} dòng")

    # 4. Huấn luyện Random Forest baseline
    model = RandomForestRegressor(
        n_estimators=100,    # 100 cây — đủ nhanh vẫn ổn định
        random_state=42,     # cố định seed để tái lập kết quả
        n_jobs=-1,           # dùng tất cả CPU cores
    )
    model.fit(X_train, y_train)

    # 5. Dự báo trên tập test
    y_pred = model.predict(X_test)

    # 6. Đánh giá metrics: MAE, RMSE, R² (Trụ cột Reliability)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "feature_count": len(X_train.columns),
    }

    print("\n=== Kết quả Random Forest Baseline ===")
    print(f"MAE  = {mae:,.0f} VND/kg")
    print(f"RMSE = {rmse:,.0f} VND/kg")
    print(f"R^2  = {r2:.4f}")

    # 7. Trích xuất feature importance — minh bạch lý do dự báo (Trụ cột
    # Transparency)
    importances = pd.Series(
        model.feature_importances_,
        index=X_train.columns,
    ).sort_values(ascending=False)

    print("\n=== Feature Importance (Top 10) ===")
    for feat, imp in importances.head(10).items():
        print(f"  {feat}: {imp:.4f}")

    importance_path = exp_dir / "feature_importance.csv"
    importances.rename("importance").to_csv(importance_path, header=True)
    feature_names_path = exp_dir / "feature_names.json"
    feature_names_path.write_text(
        json.dumps(
            list(
                X_train.columns),
            indent=2,
            ensure_ascii=False),
        encoding="utf-8")

    # 8. Vẽ và lưu biểu đồ feature importance vào experiment folder
    plt.figure(figsize=(8, 5))
    importances.head(10).plot(kind="barh")
    plt.title("Top 10 Feature Importances — Random Forest")
    plt.xlabel("Importance")
    plt.tight_layout()
    plot_path = exp_dir / "feature_importance.png"
    plt.savefig(plot_path)
    print(f"\nĐã lưu biểu đồ feature importance: {plot_path}")
    print(f"Đã lưu feature list: {feature_names_path}")

    # 9. Lưu model đã train vào experiment folder
    model_path = exp_dir / "rf_baseline.pkl"
    joblib.dump(model, model_path)
    print(f"Đã lưu model: {model_path}")

    # 10. Lưu metadata
    save_metrics(exp_dir, metrics)
    params = build_params(
        model_params=model.get_params(),
        data_path=data_path,
    )
    save_params(exp_dir, params)

    # 11. Append to experiments CSV và cập nhật best model
    append_experiment_csv(exp_dir, tag, "RandomForestRegressor", metrics)
    best_model_path = _update_best_model_after_training(
        tag, exp_dir.name) if promote else None
    print(f"Best model cập nhật: {best_model_path}")

    return {
        "experiment_id": exp_dir.name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "feature_importance": importances.to_dict(),
        "model_path": str(model_path),
        "plot_path": str(plot_path),
        "feature_names_path": str(feature_names_path),
        "exp_dir": str(exp_dir),
        "best_model_path": str(best_model_path) if best_model_path else None,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Huấn luyện RF baseline")
    parser.add_argument(
        "--data",
        default="data/processed/monthly/coffee_environment_all_areas_monthly_2020_2026.csv",
        help="Đường dẫn CSV input",
    )
    parser.add_argument(
        "--tag",
        default="rf_baseline",
        help="Tag cho experiment folder",
    )
    parser.add_argument(
        "--no-promote",
        action="store_true",
        help="Không cập nhật model/best_model sau khi train",
    )
    args = parser.parse_args()

    train_and_evaluate(args.data, args.tag, promote=not args.no_promote)
