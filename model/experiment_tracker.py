"""
Công cụ theo dõi thử nghiệm KISS dành cho quy trình huấn luyện mô hình AI002.

Cung cấp khả năng theo dõi thử nghiệm gọn nhẹ mà không cần các phụ thuộc bên ngoài.
Mỗi lần chạy huấn luyện sẽ tạo một thư mục có dấu thời gian trong thư mục model/experiments/.
"""

import csv
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Hằng số
# ---------------------------------------------------------------------------

EXPERIMENTS_ROOT = Path("model/experiments")
BEST_MODEL_DIR = Path("model/best_model")
CSV_PATH = Path("model/experiments.csv")


# ---------------------------------------------------------------------------
# Hàm tiện ích
# ---------------------------------------------------------------------------

def _git_commit() -> str:
    """Trả về git commit hash ngắn, hoặc 'unknown'."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def _data_hash(path: str | Path) -> str:
    """Tính toán mã băm MD5 của một tập tin (để theo dõi khả năng tái tạo)."""
    try:
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return f"md5:{h.hexdigest()}"
    except FileNotFoundError:
        return "md5:file_not_found"


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _datetime_iso() -> str:
    from datetime import timezone
    return datetime.now(timezone.utc).isoformat()


def _ensure_dirs() -> None:
    EXPERIMENTS_ROOT.mkdir(parents=True, exist_ok=True)
    BEST_MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# API công khai
# ---------------------------------------------------------------------------

def create_experiment(tag: str) -> Path:
    """Tạo một thư mục thử nghiệm mới có dấu thời gian.

    Args:
        tag: Định danh cho thử nghiệm (ví dụ: 'rf_baseline', 'xgboost').

    Returns:
        Đường dẫn tới thư mục thử nghiệm đã tạo.
    """
    _ensure_dirs()
    ts = _timestamp()
    exp_dir = EXPERIMENTS_ROOT / f"{ts}__{tag}"
    exp_dir.mkdir(parents=True, exist_ok=False)
    return exp_dir


def save_metrics(exp_dir: Path, metrics: dict[str, Any]) -> Path:
    """Lưu dictionary metrics dưới dạng metrics.json trong thư mục thử nghiệm.

    Args:
        exp_dir: Đường dẫn thư mục thử nghiệm.
        metrics: Dictionary chứa các chỉ số (ví dụ: {'mae': 1234.5, 'rmse': ...}).

    Returns:
        Đường dẫn tới file metrics.json đã lưu.
    """
    path = exp_dir / "metrics.json"
    path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def save_params(exp_dir: Path, params: dict[str, Any]) -> Path:
    """Lưu tham số / metadata dưới dạng params.json trong thư mục thử nghiệm.

    Args:
        exp_dir: Đường dẫn thư mục thử nghiệm.
        params: Dictionary chứa các tham số (data_path, model_params, v.v.).

    Returns:
        Đường dẫn tới file params.json đã lưu.
    """
    path = exp_dir / "params.json"
    path.write_text(json.dumps(params, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def build_params(
    model_params: dict[str, Any],
    data_path: str | Path,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Xây dựng dictionary tham số chuẩn với git commit, data hash, timestamp.

    Args:
        model_params: Siêu tham số dùng cho huấn luyện.
        data_path: Đường dẫn tới tập dữ liệu huấn luyện.
        extra: Các trường bổ sung tùy chọn.

    Returns:
        Dictionary tham số đầy đủ, sẵn sàng cho save_params().
    """
    params = {
        "timestamp": _datetime_iso(),
        "git_commit": _git_commit(),
        "data_path": str(data_path),
        "data_hash": _data_hash(data_path),
        "model_params": model_params,
    }
    if extra:
        params.update(extra)
    return params


def save_artifact(exp_dir: Path, name: str, source: str | Path | bytes) -> Path:
    """Lưu một file artifact vào thư mục thử nghiệm.

    Args:
        exp_dir: Đường dẫn thư mục thử nghiệm.
        name: Tên file artifact (ví dụ: 'model.pkl', 'plot.png').
        source: Đường dẫn file (str/Path) để copy, hoặc bytes thô để ghi.

    Returns:
        Đường dẫn tới artifact đã lưu trong exp_dir.
    """
    dest = exp_dir / name
    if isinstance(source, (str, Path)) and Path(source).is_file():
        shutil.copy2(source, dest)
    elif isinstance(source, bytes):
        dest.write_bytes(source)
    else:
        raise TypeError(f"source phải là đường dẫn file hoặc bytes, nhận được {type(source)}")
    return dest


def append_experiment_csv(
    exp_dir: Path,
    tag: str,
    model_type: str,
    metrics: dict[str, Any],
) -> Path:
    """Thêm một dòng vào model/experiments.csv tóm tắt lần chạy.

    Args:
        exp_dir: Đường dẫn thư mục thử nghiệm (dùng làm experiment_id).
        tag: Tag của thử nghiệm.
        model_type: Tên lớp model (ví dụ: 'RandomForestRegressor').
        metrics: Phải chứa ít nhất 'mae', 'rmse', 'r2'.

    Returns:
        Đường dẫn tới experiments.csv.
    """
    _ensure_dirs()
    experiment_id = exp_dir.name
    timestamp = _datetime_iso()

    headers = ["experiment_id", "timestamp", "tag", "model_type", "mae", "rmse", "r2", "best"]
    row = {
        "experiment_id": experiment_id,
        "timestamp": timestamp,
        "tag": tag,
        "model_type": model_type,
        "mae": metrics.get("mae", ""),
        "rmse": metrics.get("rmse", ""),
        "r2": metrics.get("r2", ""),
        "best": "false",
    }

    file_exists = CSV_PATH.is_file()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, lineterminator="\n")
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    return CSV_PATH


def get_latest_experiment() -> Path | None:
    """Trả về thư mục thử nghiệm gần nhất, hoặc None nếu chưa có."""
    _ensure_dirs()
    dirs = [d for d in EXPERIMENTS_ROOT.iterdir() if d.is_dir()]
    if not dirs:
        return None
    return max(dirs, key=lambda d: d.name)


def update_best_model(
    metric_key: str = "mae",
    mode: str = "min",
    tag_prefix: str | None = None,
    fallback_experiment_id: str | None = None,
) -> Path | None:
    """Đánh giá tất cả thử nghiệm và copy model tốt nhất vào model/best_model/.

    Args:
        metric_key: Chỉ số để tối ưu ('mae', 'rmse', hoặc 'r2').
        mode: 'min' cho càng thấp càng tốt, 'max' cho càng cao càng tốt.

    Returns:
        Đường dẫn tới model tốt nhất vừa copy, hoặc None nếu chưa có thử nghiệm.
    """
    _ensure_dirs()
    if mode not in {"min", "max"}:
        raise ValueError("mode phải là 'min' hoặc 'max'")

    if not CSV_PATH.is_file():
        return None

    # Đọc tất cả thử nghiệm từ CSV
    experiments: list[dict[str, Any]] = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            if tag_prefix and not row.get("tag", "").startswith(tag_prefix):
                continue
            try:
                row[metric_key] = float(row[metric_key])
            except (ValueError, KeyError):
                continue
            experiments.append(row)

    if not experiments:
        return None

    # Xác định thử nghiệm tốt nhất
    target_metric = (
        min(row[metric_key] for row in experiments)
        if mode == "min"
        else max(row[metric_key] for row in experiments)
    )
    tied = [row for row in experiments if row[metric_key] == target_metric]
    best = max(tied, key=lambda r: (r.get("timestamp", ""), r.get("experiment_id", "")))
    selection_note = None

    best_artifact = _get_experiment_model_file(best["experiment_id"])
    if best_artifact is None and fallback_experiment_id:
        fallback = next((row for row in experiments if row["experiment_id"] == fallback_experiment_id), None)
        fallback_artifact = _get_experiment_model_file(fallback_experiment_id)
        if fallback and fallback_artifact is not None:
            best = fallback
            best_artifact = fallback_artifact
            selection_note = "fallback_current_run_missing_best_artifact"

    if best_artifact is None:
        return None

    exp_id = best["experiment_id"]
    exp_dir = EXPERIMENTS_ROOT / exp_id

    dest_model = BEST_MODEL_DIR / "model.pkl"
    shutil.copy2(best_artifact, dest_model)

    # Ghi metadata cho model tốt nhất (đảm bảo tất cả metrics là float)
    experiment_metadata = _load_experiment_metadata(exp_dir)
    metadata = {
        "experiment_id": exp_id,
        "timestamp": best.get("timestamp", _datetime_iso()),
        "tag": best["tag"],
        "model_type": best["model_type"],
        "mae": float(best["mae"]),
        "rmse": float(best["rmse"]),
        "r2": float(best["r2"]),
        "model_path": str(dest_model),
        "source_experiment": str(exp_dir),
    }
    metadata.update(experiment_metadata)
    if selection_note:
        metadata["selection_note"] = selection_note
    meta_path = BEST_MODEL_DIR / "metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    # Cập nhật CSV: đánh dấu best=True cho dòng này, reset các dòng khác
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or fieldnames
        for row in reader:
            row["best"] = "true" if row["experiment_id"] == exp_id else "false"
            rows.append(row)

    if "best" not in fieldnames:
        fieldnames = [*fieldnames, "best"]

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    return dest_model


def _get_experiment_model_file(experiment_id: str) -> Path | None:
    exp_dir = EXPERIMENTS_ROOT / experiment_id
    if not exp_dir.is_dir():
        return None
    model_files = sorted(exp_dir.glob("*.pkl"), key=lambda p: p.name)
    return model_files[0] if model_files else None


def _load_experiment_metadata(exp_dir: Path) -> dict[str, Any]:
    metadata: dict[str, Any] = {}

    metrics_path = exp_dir / "metrics.json"
    if metrics_path.is_file():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        for key in ("train_size", "test_size", "feature_count"):
            if key in metrics:
                metadata[key] = metrics[key]

    feature_names_path = exp_dir / "feature_names.json"
    if feature_names_path.is_file():
        feature_names = json.loads(feature_names_path.read_text(encoding="utf-8"))
        metadata["feature_names"] = feature_names

    importance_path = exp_dir / "feature_importance.csv"
    if importance_path.is_file():
        with open(importance_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            feature_col = reader.fieldnames[0] if reader.fieldnames else None
            if feature_col is not None:
                top_features = {}
                for row in reader:
                    if len(top_features) >= 10:
                        break
                    try:
                        top_features[row[feature_col]] = float(row["importance"])
                    except (KeyError, ValueError):
                        continue
                metadata["top_features"] = top_features

    return metadata


def list_experiments() -> list[dict[str, Any]]:
    """Trả về danh sách tất cả thử nghiệm đã ghi từ CSV."""
    if not CSV_PATH.is_file():
        return []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))
