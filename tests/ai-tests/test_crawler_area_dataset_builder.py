from __future__ import annotations

import crawler.area_dataset_builder as area_dataset_builder

import pandas as pd


def test_add_period_columns_weekly() -> None:
    df = pd.DataFrame({"date": pd.to_datetime(["2023-01-01", "2023-01-03", "2023-01-10"])})
    res = area_dataset_builder.add_period_columns(df, "weekly")
    assert "period_start" in res.columns
    assert "period_end" in res.columns
    assert str(res["period_start"].iloc[0]) == "2022-12-26"
    assert str(res["period_end"].iloc[0]) == "2023-01-01"


def test_add_period_columns_monthly() -> None:
    df = pd.DataFrame({"date": pd.to_datetime(["2023-01-05", "2023-01-15", "2023-02-10"])})
    res = area_dataset_builder.add_period_columns(df, "monthly")
    assert str(res["period_start"].iloc[0]) == "2023-01-01"
    assert str(res["period_end"].iloc[0]) == "2023-01-31"


def test_aggregate_prices() -> None:
    prices = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-05", "2023-01-06", "2023-02-10"]),
        "province": ["Lam Dong", "Lam Dong", "Gia Lai"],
        "area": ["Di Linh", "Di Linh", "Pleiku"],
        "coffee_type": ["Robusta", "Robusta", "Robusta"],
        "price_vnd_per_kg": [40000, 42000, 45000],
    })
    start_date = pd.to_datetime("2023-01-01")
    end_date = pd.to_datetime("2023-02-28")
    agg = area_dataset_builder.aggregate_prices(prices, "monthly", start_date, end_date)
    assert len(agg) == 2
    lam_dong = agg[(agg["province"] == "Lam Dong") & (agg["area"] == "Di Linh")].iloc[0]
    assert lam_dong["avg_price_vnd_per_kg"] == 41000.0
    assert lam_dong["price_observations"] == 2
