from __future__ import annotations

from pathlib import Path

from model.stress_test import generate_stress_report


def test_stress_test_cli_entrypoint_is_after_helper_definitions() -> None:
    source = Path("model/stress_test.py").read_text(encoding="utf-8")

    main_pos = source.index('if __name__ == "__main__":')
    inject_pos = source.index("def inject_black_swan_on_test(")
    report_pos = source.index("def generate_stress_report(")

    assert main_pos > inject_pos
    assert main_pos > report_pos


def test_stress_report_uses_current_scenario_lift_values() -> None:
    report = "\n".join(
        generate_stress_report(
            model_path="model.pkl",
            data_path="coffee_environment.csv",
            exp_name="exp",
            mae_normal=100.0,
            rmse_normal=120.0,
            results=[
                {
                    "scenario": "price_crash",
                    "mae": 202.7,
                    "rmse": 260.5,
                    "mae_lift_pct": 102.7,
                    "rmse_lift_pct": 117.1,
                },
                {
                    "scenario": "heat_wave",
                    "mae": 100.0,
                    "rmse": 120.0,
                    "mae_lift_pct": -0.0,
                    "rmse_lift_pct": -0.0,
                },
            ],
        )
    )

    assert "+66.5%" not in report
    assert "+102.7%" in report
    assert "+-0.0%" not in report
