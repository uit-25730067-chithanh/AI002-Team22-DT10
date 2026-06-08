from __future__ import annotations

from pathlib import Path

import pandas as pd

from model import train_rf


MONTHLY_DATASET_PATH = Path(
    "data/processed/monthly/coffee_environment_all_areas_monthly_2020_2026.csv"
)


def test_canonical_dataset_keeps_train_test_demo_windows_separate() -> None:
    df = pd.read_csv(MONTHLY_DATASET_PATH, parse_dates=["period_start"])
    train = df[df["period_start"] <= "2024-12-31"].copy()
    test = df[
        (df["period_start"] >= "2025-01-01")
        & (df["period_start"] <= "2025-12-31")
    ].copy()
    demo = df[df["period_start"] >= "2026-01-01"].copy()

    assert df["period_start"].min() == pd.Timestamp("2020-01-01")
    assert df["period_start"].max() == pd.Timestamp("2026-04-01")
    assert len(df) == 912
    assert df["area"].nunique() == 12
    assert len(train) == 720
    assert len(test) == 144
    assert len(demo) == 48

    observed_rows = df[df["price_fill_method"] == "observed"]
    assert len(observed_rows) == 711
    assert len(observed_rows) / len(df) >= 0.77
    assert train["price_observations"].sum() > 0


def test_rf_monthly_training_uses_monthly_best_model_scope(monkeypatch) -> None:
    calls = []

    def fake_update_best_model(**kwargs):
        calls.append(kwargs)
        return Path("model/best_model/model.pkl")

    monkeypatch.setattr(train_rf, "update_best_model", fake_update_best_model)
    monkeypatch.setattr(train_rf, "list_experiments", lambda: [{"tag": "rf_real_monthly"}])

    best_path = train_rf._update_best_model_after_training(
        "rf_monthly_baseline",
        "20260608_003000__rf_monthly_baseline",
    )

    assert best_path == Path("model/best_model/model.pkl")
    assert calls == [
        {
            "metric_key": "mae",
            "mode": "min",
            "tag_prefix": "rf_monthly",
            "fallback_experiment_id": "20260608_003000__rf_monthly_baseline",
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

    result = train_rf.train_and_evaluate(str(csv_path), tag="rf_monthly_validation", promote=False)

    assert result["best_model_path"] is None
