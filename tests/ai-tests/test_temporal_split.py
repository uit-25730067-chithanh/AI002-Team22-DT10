from __future__ import annotations

import pandas as pd

from model.preprocess import split_temporal


def build_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-02-01",
                    "2025-01-01",
                    "2025-02-01",
                    "2026-01-01",
                ]
            ),
            "historical_price_vnd": [80000, 82000, 100000, 101000, 95000],
            "avg_temp_c": [20, 21, 22, 23, 24],
        }
    )


def test_default_temporal_split_uses_2025_test_only() -> None:
    X_train, X_test, y_train, y_test = split_temporal(build_frame())

    assert len(X_train) == 2
    assert len(X_test) == 2
    assert list(y_test) == [100000, 101000]


def test_temporal_split_can_include_2026_when_explicit() -> None:
    X_train, X_test, y_train, y_test = split_temporal(
        build_frame(),
        test_end="2026-04-30",
    )

    assert len(X_train) == 2
    assert len(X_test) == 3
    assert list(y_test) == [100000, 101000, 95000]
