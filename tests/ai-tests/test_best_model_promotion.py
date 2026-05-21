import csv
import json
from pathlib import Path

from model import experiment_tracker


HEADERS = ["experiment_id", "timestamp", "tag", "model_type", "mae", "rmse", "r2", "best"]


def _write_experiments_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _make_experiment(
    root: Path,
    experiment_id: str,
    *,
    feature_names: list[str] | None = None,
    with_model: bool = True,
) -> None:
    exp_dir = root / experiment_id
    exp_dir.mkdir(parents=True)
    if with_model:
        (exp_dir / "rf_baseline.pkl").write_bytes(b"model-bytes")
    (exp_dir / "metrics.json").write_text(
        json.dumps({"train_size": 10, "test_size": 3, "feature_count": len(feature_names or [])}),
        encoding="utf-8",
    )
    if feature_names is not None:
        (exp_dir / "feature_names.json").write_text(json.dumps(feature_names), encoding="utf-8")
    (exp_dir / "feature_importance.csv").write_text(
        ",importance\nlag_1d,0.9\nrolling_avg_7d,0.8\nmonth,0.1\n",
        encoding="utf-8",
    )


def _configure_tracker(tmp_path, monkeypatch) -> tuple[Path, Path, Path]:
    experiments_root = tmp_path / "experiments"
    best_model_dir = tmp_path / "best_model"
    csv_path = tmp_path / "experiments.csv"
    experiments_root.mkdir()
    best_model_dir.mkdir()
    monkeypatch.setattr(experiment_tracker, "EXPERIMENTS_ROOT", experiments_root)
    monkeypatch.setattr(experiment_tracker, "BEST_MODEL_DIR", best_model_dir)
    monkeypatch.setattr(experiment_tracker, "CSV_PATH", csv_path)
    return experiments_root, best_model_dir, csv_path


def test_best_model_selection_filters_real_tags(tmp_path, monkeypatch) -> None:
    experiments_root, best_model_dir, csv_path = _configure_tracker(tmp_path, monkeypatch)
    _make_experiment(experiments_root, "20260510_000000__rf_test")
    _make_experiment(experiments_root, "20260513_000000__rf_real_monthly")
    _write_experiments_csv(
        csv_path,
        [
            {
                "experiment_id": "20260510_000000__rf_test",
                "timestamp": "2026-05-10T00:00:00+00:00",
                "tag": "rf_test",
                "model_type": "RandomForestRegressor",
                "mae": "1000",
                "rmse": "1200",
                "r2": "0.1",
                "best": "false",
            },
            {
                "experiment_id": "20260513_000000__rf_real_monthly",
                "timestamp": "2026-05-13T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "5000",
                "rmse": "5500",
                "r2": "-0.1",
                "best": "false",
            },
        ],
    )

    best_path = experiment_tracker.update_best_model(metric_key="mae", mode="min", tag_prefix="rf_real")

    metadata = json.loads((best_model_dir / "metadata.json").read_text(encoding="utf-8"))
    assert best_path == best_model_dir / "model.pkl"
    assert metadata["experiment_id"] == "20260513_000000__rf_real_monthly"


def test_best_model_selection_picks_lowest_mae_real_run(tmp_path, monkeypatch) -> None:
    experiments_root, best_model_dir, csv_path = _configure_tracker(tmp_path, monkeypatch)
    _make_experiment(experiments_root, "20260513_000000__rf_real_monthly")
    _make_experiment(experiments_root, "20260514_000000__rf_real_monthly")
    _write_experiments_csv(
        csv_path,
        [
            {
                "experiment_id": "20260513_000000__rf_real_monthly",
                "timestamp": "2026-05-13T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "5000",
                "rmse": "5500",
                "r2": "-0.1",
                "best": "true",
            },
            {
                "experiment_id": "20260514_000000__rf_real_monthly",
                "timestamp": "2026-05-14T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "4000",
                "rmse": "4500",
                "r2": "0.0",
                "best": "false",
            },
        ],
    )

    experiment_tracker.update_best_model(metric_key="mae", mode="min", tag_prefix="rf_real")

    metadata = json.loads((best_model_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["experiment_id"] == "20260514_000000__rf_real_monthly"
    assert metadata["mae"] == 4000.0


def test_best_model_selection_marks_single_best_row(tmp_path, monkeypatch) -> None:
    experiments_root, _, csv_path = _configure_tracker(tmp_path, monkeypatch)
    _make_experiment(experiments_root, "20260513_000000__rf_real_monthly")
    _make_experiment(experiments_root, "20260514_000000__rf_real_monthly")
    _write_experiments_csv(
        csv_path,
        [
            {
                "experiment_id": "20260513_000000__rf_real_monthly",
                "timestamp": "2026-05-13T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "5000",
                "rmse": "5500",
                "r2": "-0.1",
                "best": "true",
            },
            {
                "experiment_id": "20260514_000000__rf_real_monthly",
                "timestamp": "2026-05-14T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "4000",
                "rmse": "4500",
                "r2": "0.0",
                "best": "true",
            },
        ],
    )

    experiment_tracker.update_best_model(metric_key="mae", mode="min", tag_prefix="rf_real")

    with open(csv_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [row["best"] for row in rows].count("true") == 1
    assert next(row for row in rows if row["best"] == "true")["experiment_id"] == "20260514_000000__rf_real_monthly"


def test_best_model_selection_picks_newer_real_run_when_mae_ties(tmp_path, monkeypatch) -> None:
    experiments_root, best_model_dir, csv_path = _configure_tracker(tmp_path, monkeypatch)
    _make_experiment(experiments_root, "20260513_000000__rf_real_monthly")
    _make_experiment(experiments_root, "20260514_000000__rf_real_monthly")
    _write_experiments_csv(
        csv_path,
        [
            {
                "experiment_id": "20260513_000000__rf_real_monthly",
                "timestamp": "2026-05-13T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "4000",
                "rmse": "4500",
                "r2": "0.0",
                "best": "false",
            },
            {
                "experiment_id": "20260514_000000__rf_real_monthly",
                "timestamp": "2026-05-14T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "4000",
                "rmse": "4600",
                "r2": "-0.1",
                "best": "false",
            },
        ],
    )

    experiment_tracker.update_best_model(metric_key="mae", mode="min", tag_prefix="rf_real")

    metadata = json.loads((best_model_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["experiment_id"] == "20260514_000000__rf_real_monthly"


def test_best_model_metadata_keeps_backend_fields(tmp_path, monkeypatch) -> None:
    experiments_root, best_model_dir, csv_path = _configure_tracker(tmp_path, monkeypatch)
    _make_experiment(experiments_root, "20260514_000000__rf_real_monthly", feature_names=["lag_1d", "month"])
    _write_experiments_csv(
        csv_path,
        [
            {
                "experiment_id": "20260514_000000__rf_real_monthly",
                "timestamp": "2026-05-14T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "4000",
                "rmse": "4500",
                "r2": "0.0",
                "best": "false",
            }
        ],
    )

    experiment_tracker.update_best_model(metric_key="mae", mode="min", tag_prefix="rf_real")

    metadata = json.loads((best_model_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["feature_names"] == ["lag_1d", "month"]
    assert metadata["top_features"] == {"lag_1d": 0.9, "rolling_avg_7d": 0.8, "month": 0.1}
    assert metadata["model_path"] == str(best_model_dir / "model.pkl")
    assert metadata["source_experiment"] == str(experiments_root / "20260514_000000__rf_real_monthly")
    assert metadata["train_size"] == 10
    assert metadata["test_size"] == 3
    assert metadata["feature_count"] == 2


def test_best_model_falls_back_when_metric_best_artifact_missing(tmp_path, monkeypatch) -> None:
    experiments_root, best_model_dir, csv_path = _configure_tracker(tmp_path, monkeypatch)
    _make_experiment(experiments_root, "20260513_000000__rf_real_monthly", with_model=False)
    _make_experiment(experiments_root, "20260514_000000__rf_real_monthly")
    _write_experiments_csv(
        csv_path,
        [
            {
                "experiment_id": "20260513_000000__rf_real_monthly",
                "timestamp": "2026-05-13T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "3000",
                "rmse": "3500",
                "r2": "0.1",
                "best": "false",
            },
            {
                "experiment_id": "20260514_000000__rf_real_monthly",
                "timestamp": "2026-05-14T00:00:00+00:00",
                "tag": "rf_real_monthly",
                "model_type": "RandomForestRegressor",
                "mae": "4000",
                "rmse": "4500",
                "r2": "0.0",
                "best": "false",
            },
        ],
    )

    best_path = experiment_tracker.update_best_model(
        metric_key="mae",
        mode="min",
        tag_prefix="rf_real",
        fallback_experiment_id="20260514_000000__rf_real_monthly",
    )

    metadata = json.loads((best_model_dir / "metadata.json").read_text(encoding="utf-8"))
    assert best_path == best_model_dir / "model.pkl"
    assert metadata["experiment_id"] == "20260514_000000__rf_real_monthly"
    assert metadata["selection_note"] == "fallback_current_run_missing_best_artifact"
