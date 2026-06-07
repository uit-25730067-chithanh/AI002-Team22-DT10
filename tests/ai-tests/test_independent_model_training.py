from __future__ import annotations

from pathlib import Path

import pandas as pd

from model import train_rf


INDEPENDENT_MONTHLY_PATH = Path(
    "data/processed/monthly/coffee_environment_independent_all_areas_monthly_2020_2026.csv"
)


def test_selected_independent_baseline_range_keeps_real_price_rows() -> None:
    df = pd.read_csv(INDEPENDENT_MONTHLY_PATH, parse_dates=["period_start"])
    selected = df[df["period_start"] >= "2022-01-01"].copy()

    assert selected["period_start"].min() == pd.Timestamp("2022-01-01")
    assert selected["period_start"].max() == pd.Timestamp("2026-04-01")
    assert len(selected) == 624
    assert selected["area"].nunique() == 12

    real_price_rows = selected[selected["price_fill_method"] == "observed"]
    assert len(real_price_rows) == 587
    assert len(real_price_rows) / len(selected) >= 0.94
    assert selected["price_observations"].sum() > 0


def test_rf_independent_training_uses_independent_best_model_scope(monkeypatch) -> None:
    calls = []

    def fake_update_best_model(**kwargs):
        calls.append(kwargs)
        return Path("model/best_model/model.pkl")

    monkeypatch.setattr(train_rf, "update_best_model", fake_update_best_model)
    monkeypatch.setattr(train_rf, "list_experiments", lambda: [{"tag": "rf_real_monthly"}])

    best_path = train_rf._update_best_model_after_training(
        "rf_independent_monthly",
        "20260607_230000__rf_independent_monthly",
    )

    assert best_path == Path("model/best_model/model.pkl")
    assert calls == [
        {
            "metric_key": "mae",
            "mode": "min",
            "tag_prefix": "rf_independent",
            "fallback_experiment_id": "20260607_230000__rf_independent_monthly",
        }
    ]


def test_training_can_skip_best_model_promotion(monkeypatch, tmp_path) -> None:
    csv_path = tmp_path / "training.csv"
    rows = []
    for year in range(2022, 2026):
        for month in range(1, 13):
            rows.append(
                {
                    "period_start": f"{year}-{month:02d}-01",
                    "area": "Kon Tum",
                    "province": "Kon Tum",
                    "avg_price_vnd_per_kg": 40000 + (year - 2022) * 10000 + month * 100,
                    "avg_temperature_c": 24.0,
                    "total_rainfall_mm": 120.0,
                    "avg_humidity_percent": 75.0,
                    "price_fill_method": "observed",
                }
            )
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    exp_root = tmp_path / "experiments"

    def fake_create_experiment(tag: str) -> Path:
        exp_dir = exp_root / f"run__{tag}"
        exp_dir.mkdir(parents=True)
        return exp_dir

    monkeypatch.setattr(train_rf, "create_experiment", fake_create_experiment)
    monkeypatch.setattr(train_rf, "append_experiment_csv", lambda *args, **kwargs: tmp_path / "experiments.csv")
    monkeypatch.setattr(train_rf, "save_metrics", lambda exp_dir, metrics: exp_dir.joinpath("metrics.json").write_text("{}"))
    monkeypatch.setattr(train_rf, "save_params", lambda exp_dir, params: exp_dir.joinpath("params.json").write_text("{}"))
    monkeypatch.setattr(train_rf, "build_params", lambda **kwargs: {})
    monkeypatch.setattr(
        train_rf,
        "_update_best_model_after_training",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("should not promote")),
    )

    result = train_rf.train_and_evaluate(str(csv_path), tag="rf_independent_validation", promote=False)

    assert result["best_model_path"] is None
