import json
from pathlib import Path

import model.experiment_tracker as experiment_tracker
import pytest


@pytest.fixture
def mock_utils(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    exp_root = tmp_path / "experiments"
    monkeypatch.setattr(experiment_tracker, "EXPERIMENTS_ROOT", exp_root)
    monkeypatch.setattr(experiment_tracker, "_ensure_dirs", lambda: exp_root.mkdir(parents=True, exist_ok=True))
    monkeypatch.setattr(experiment_tracker, "_timestamp", lambda: "20240101_120000")
    monkeypatch.setattr(experiment_tracker, "_datetime_iso", lambda: "2024-01-01T12:00:00")
    monkeypatch.setattr(experiment_tracker, "_git_commit", lambda: "abcdef")
    monkeypatch.setattr(experiment_tracker, "_data_hash", lambda path: "hash123")
    return exp_root


def test_create_experiment(mock_utils: Path) -> None:
    exp_dir = experiment_tracker.create_experiment("test")
    assert exp_dir.exists()
    assert exp_dir.name == "20240101_120000__test"


def test_save_metrics_and_params(mock_utils: Path) -> None:
    exp_dir = experiment_tracker.create_experiment("test")
    metrics = {"mae": 1.5}
    params = {"n_estimators": 100}

    experiment_tracker.save_metrics(exp_dir, metrics)
    experiment_tracker.save_params(exp_dir, params)

    with open(exp_dir / "metrics.json", "r") as f:
        assert json.load(f) == metrics
    with open(exp_dir / "params.json", "r") as f:
        assert json.load(f) == params


def test_build_params(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(experiment_tracker, "_datetime_iso", lambda: "2024-01-01T12:00:00")
    monkeypatch.setattr(experiment_tracker, "_git_commit", lambda: "abcdef")
    monkeypatch.setattr(experiment_tracker, "_data_hash", lambda path: "hash123")

    params = experiment_tracker.build_params({"n": 10}, "data.csv", extra={"foo": "bar"})
    assert params["timestamp"] == "2024-01-01T12:00:00"
    assert params["git_commit"] == "abcdef"
    assert params["data_path"] == "data.csv"
    assert params["data_hash"] == "hash123"
    assert params["model_params"] == {"n": 10}
    assert params["foo"] == "bar"


def test_save_artifact(mock_utils: Path, tmp_path: Path) -> None:
    exp_dir = experiment_tracker.create_experiment("test")

    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")
    experiment_tracker.save_artifact(exp_dir, "test1.txt", file_path)
    assert (exp_dir / "test1.txt").read_text() == "hello"

    experiment_tracker.save_artifact(exp_dir, "test2.bin", b"world")
    assert (exp_dir / "test2.bin").read_bytes() == b"world"


def test_get_latest_experiment(mock_utils: Path) -> None:
    assert experiment_tracker.get_latest_experiment() is None

    (mock_utils / "20230101__old").mkdir(parents=True)
    (mock_utils / "20240101__new").mkdir(parents=True)

    latest = experiment_tracker.get_latest_experiment()
    assert latest is not None
    assert latest.name == "20240101__new"
