"""
Stress Test: Đo lường model phản ứng khi data nhiễm cực đoan (Black Swan).
Cover Trụ cột Robustness bằng báo cáo thay vì module phức tạp.
"""

import argparse
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

sys.path.insert(0, str(Path(__file__).parent))
from preprocess import feature_engineer, fill_missing, split_temporal


def inject_black_swan(df: pd.DataFrame, scenario: str) -> pd.DataFrame:
    """
    Bơm outliers cực đoan vào test set.
    """
    df = df.copy()
    np.random.seed(42)

    if scenario == "price_crash":
        # Giá giảm đột ngột 50%
        n = max(1, len(df) // 20)
        idx = np.random.choice(df.index, size=n, replace=False)
        df.loc[idx, "historical_price_vnd"] *= 0.5
    elif scenario == "heat_wave":
        # Nhiệt độ tăng lên 45°C (vượt ngoài lịch sử)
        n = max(1, len(df) // 20)
        idx = np.random.choice(df.index, size=n, replace=False)
        df.loc[idx, "avg_temp_c"] = 45.0
    elif scenario == "both":
        n = max(1, len(df) // 20)
        idx = np.random.choice(df.index, size=n, replace=False)
        df.loc[idx, "historical_price_vnd"] *= 0.5
        df.loc[idx, "avg_temp_c"] = 45.0
    else:
        raise ValueError(f"scenario không hợp lệ: {scenario}")

    return df


def run_stress_test(data_path: str, model_path: str, output_dir: str = "docs/discussions"):
    # Load dữ liệu và model đã train
    df_raw = pd.read_csv(data_path)
    model = joblib.load(model_path)

    # Pipeline bình thường (không inject outliers) để có baseline
    df_normal = fill_missing(df_raw)
    df_normal = feature_engineer(df_normal)
    X_train, X_test_normal, y_train, y_test_normal = split_temporal(df_normal)

    # Đánh giá baseline trên dữ liệu không nhiễm
    y_pred_normal = model.predict(X_test_normal)
    mae_normal = mean_absolute_error(y_test_normal, y_pred_normal)
    rmse_normal = np.sqrt(mean_squared_error(y_test_normal, y_pred_normal))

    results = []
    for scenario in ["price_crash", "heat_wave", "both"]:
        df_stress = fill_missing(df_raw)
        df_stress = inject_black_swan(df_stress, scenario)
        df_stress = feature_engineer(df_stress)
        _, X_test_stress, _, y_test_stress = split_temporal(df_stress)

        y_pred_stress = model.predict(X_test_stress)
        mae_stress = mean_absolute_error(y_test_stress, y_pred_stress)
        rmse_stress = np.sqrt(mean_squared_error(y_test_stress, y_pred_stress))

        mae_lift = ((mae_stress - mae_normal) / mae_normal) * 100
        rmse_lift = ((rmse_stress - rmse_normal) / rmse_normal) * 100

        results.append({
            "scenario": scenario,
            "mae": mae_stress,
            "rmse": rmse_stress,
            "mae_lift_pct": mae_lift,
            "rmse_lift_pct": rmse_lift,
        })

        print(f"\n=== Scenario: {scenario} ===")
        print(f"MAE  = {mae_stress:,.0f} VND/kg (+{mae_lift:.1f}%)")
        print(f"RMSE = {rmse_stress:,.0f} VND/kg (+{rmse_lift:.1f}%)")

    # Write report
    report_lines = [
        "# Stress Test Report — Robustness Pillar",
        "",
        "**Date:** 2026-04-26",
        "**Model:** Random Forest Baseline",
        "**Dataset:** mock_coffee_data.csv",
        "",
        "## Baseline (Normal Test Set)",
        "",
        f"- MAE:  {mae_normal:,.0f} VND/kg",
        f"- RMSE: {rmse_normal:,.0f} VND/kg",
        "",
        "## Black Swan Scenarios",
        "",
    ]
    for r in results:
        report_lines.extend([
            f"### {r['scenario']}",
            "",
            f"- MAE:  {r['mae']:,.0f} VND/kg (+{r['mae_lift_pct']:.1f}%)",
            f"- RMSE: {r['rmse']:,.0f} VND/kg (+{r['rmse_lift_pct']:.1f}%)",
            "",
        ])
    report_lines.extend([
        "## Ghi nhận",
        "",
        "> Khi thị trường biến động cực đoan (giá sụp 50%, nhiệt độ 45°C),",
        "> model dự báo lệch đáng kể so với baseline. Điều này là bình thường",
        "> vì model được huấn luyện trên phân bố lịch sử, không phải sự kiện hiếm.",
        "",
        "## Khuyến nghị cho Slide Tuần 6",
        "",
        "- Trình bày MAE lift % như bằng chứng Robustness.",
        "- Giải thích: 'Model hoạt động tốt trong phân bố lịch sử,",
        "  nhưng cần cảnh báo người dùng khi input nằm ngoài phân bố đã thấy.'",
    ])

    output_path = Path(output_dir) / "robustness-stress-test.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nĐã lưu báo cáo: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/raw/mock_coffee_data.csv")
    parser.add_argument("--model", default="model/saved/rf_baseline.pkl")
    args = parser.parse_args()
    run_stress_test(args.data, args.model)
