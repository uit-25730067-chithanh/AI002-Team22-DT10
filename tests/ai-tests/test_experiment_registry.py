import crawler.area_dataset_builder as area_dataset_builder
import crawler.price_crawler_common as price_crawler_common
import model.experiment_tracker as experiment_tracker
import csv
from pathlib import Path

import pytest

from model import experiment_tracker as experiment_utils
from model import experiment_tracker as experiment_artifacts
from model import experiment_tracker as experiment_registry

@pytest.fixture
def temp_csv_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    csv_path = tmp_path / "experiments.csv"
    monkeypatch.setattr(experiment_tracker, "CSV_PATH", csv_path)
    monkeypatch.setattr(experiment_tracker, "_ensure_dirs", lambda: None)
    monkeypatch.setattr(experiment_tracker, "_datetime_iso", lambda: "2024-01-01T12:00:00")
    return csv_path

def test_append_experiment_csv_creates_new_file(temp_csv_path: Path, tmp_path: Path) -> None:
    exp_dir = tmp_path / "exp_1"
    metrics = {"mae": 1.5, "rmse": 2.0, "r2": 0.8}
    
    experiment_tracker.append_experiment_csv(exp_dir, "test_tag", "RF", metrics)
    
    assert temp_csv_path.is_file()
    with open(temp_csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 1
    assert reader[0]["experiment_id"] == "exp_1"
    assert reader[0]["timestamp"] == "2024-01-01T12:00:00"
    assert reader[0]["tag"] == "test_tag"
    assert reader[0]["model_type"] == "RF"
    assert reader[0]["mae"] == "1.5"
    assert reader[0]["best"] == "false"

def test_list_experiments(temp_csv_path: Path, tmp_path: Path) -> None:
    assert experiment_tracker.list_experiments() == []
    
    exp_dir = tmp_path / "exp_1"
    metrics = {"mae": 1.5}
    experiment_tracker.append_experiment_csv(exp_dir, "test_tag", "RF", metrics)
    
    experiments = experiment_tracker.list_experiments()
    assert len(experiments) == 1
    assert experiments[0]["experiment_id"] == "exp_1"
