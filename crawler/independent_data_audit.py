"""Audit helpers for independent processed coffee datasets."""

from __future__ import annotations

from collections.abc import Sequence
import argparse
from pathlib import Path

import pandas as pd

try:
    from .independent_data_quality import summarize_observed_data_completeness
except ImportError:
    from independent_data_quality import summarize_observed_data_completeness


def compare_observed_data_completeness(
    old: pd.DataFrame,
    new: pd.DataFrame,
    group_cols: Sequence[str],
) -> pd.DataFrame:
    old_summary = summarize_observed_data_completeness(old, group_cols)
    new_summary = summarize_observed_data_completeness(new, group_cols)
    old_summary = old_summary.rename(
        columns={
            "total_rows": "old_total_rows",
            "observed_rows": "old_observed_rows",
            "observed_rate": "old_observed_rate",
        }
    )
    new_summary = new_summary.rename(
        columns={
            "total_rows": "new_total_rows",
            "observed_rows": "new_observed_rows",
            "observed_rate": "new_observed_rate",
        }
    )
    merged = old_summary.merge(new_summary, on=list(group_cols), how="outer").fillna(0)
    merged["delta_observed_rate"] = (
        merged["new_observed_rate"] - merged["old_observed_rate"]
    ).round(4)
    return merged.sort_values(list(group_cols)).reset_index(drop=True)


def fill_method_table(frame: pd.DataFrame) -> pd.DataFrame:
    counts = frame["price_fill_method"].value_counts().rename_axis("fill_method")
    table = counts.reset_index(name="rows")
    table["rate"] = (table["rows"] / len(frame)).round(4)
    return table


def candidate_range_summary(frame: pd.DataFrame) -> pd.DataFrame:
    work = frame.copy()
    work["period_start"] = pd.to_datetime(work["period_start"])
    candidates = [
        ("2020-2026_04", "2020-01-01", "2026-04-30"),
        ("2021-2026_04", "2021-01-01", "2026-04-30"),
        ("2022-2026_04", "2022-01-01", "2026-04-30"),
    ]
    rows = []
    for label, start, end in candidates:
        subset = work[
            (work["period_start"] >= pd.Timestamp(start))
            & (work["period_start"] <= pd.Timestamp(end))
        ]
        observed = subset["price_fill_method"].eq("observed").sum()
        rows.append(
            {
                "candidate": label,
                "start": start,
                "end": end,
                "rows": len(subset),
                "observed_rows": int(observed),
                "observed_rate": round(float(observed / len(subset)), 4) if len(subset) else 0,
            }
        )
    return pd.DataFrame(rows)


def dataframe_to_markdown(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows_"
    columns = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for _, row in frame.iterrows():
        values = [str(row[column]) for column in frame.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown_report(
    old: pd.DataFrame,
    new: pd.DataFrame,
    output: Path,
    province_summary: pd.DataFrame,
    area_summary: pd.DataFrame,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Independent Data Audit - Team 2",
        "",
        "**Ngay:** 2026-06-07",
        "**Trang thai:** Phase 4 audit",
        "",
        "## Summary",
        "",
        "- Dataset moi la public reference dataset do Team 2 tu crawl lai.",
        "- Old dataset chi dung lam baseline so sanh.",
        "- Monthly dataset moi co source evidence fields: `source_url_count`, `source_names`.",
        "",
        "## Dataset size",
        "",
        f"- Old monthly rows: `{len(old)}`",
        f"- New monthly rows: `{len(new)}`",
        f"- New period range: `{new['period_start'].min()}` -> `{new['period_start'].max()}`",
        "",
        "## New fill-method distribution",
        "",
        dataframe_to_markdown(fill_method_table(new)),
        "",
        "## Province comparison",
        "",
        dataframe_to_markdown(province_summary),
        "",
        "## Area comparison top changes",
        "",
        dataframe_to_markdown(
            area_summary.sort_values("delta_observed_rate", ascending=False).head(20)
        ),
        "",
        "## Baseline candidate ranges",
        "",
        dataframe_to_markdown(candidate_range_summary(new)),
        "",
        "## Area replacement decision",
        "",
        "- Chua thay area trong Phase 4.",
        "- Ly do: 12 area hien tai deu co processed rows va weather day du.",
        "- Phase 5 se chon baseline range dua tren candidate table.",
        "",
        "## Known limitations",
        "",
        "- Raw price moi phu thuoc nhieu vao Nong Nghiep Moi Truong.",
        "- Kinh Te Do Thi timeout trong Phase 3.",
        "- Vinanet seed URLs chua parse duoc rows.",
        "",
        "## Unresolved Questions",
        "",
        "- Phase 5 chon 2020-2026/04 hay 2022-2026/04 dua tren trade-off observed rate vs thoi gian dai hon.",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--old-monthly",
        default="data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv",
    )
    parser.add_argument(
        "--new-monthly",
        default="data/processed/monthly/coffee_environment_independent_all_areas_monthly_2020_2026.csv",
    )
    parser.add_argument(
        "--output-csv",
        default="data/processed/independent_area_real_price_data_ranking.csv",
    )
    parser.add_argument(
        "--report",
        default="docs/discussions/2026-06-07-independent-data-audit.md",
    )
    args = parser.parse_args()

    old = pd.read_csv(args.old_monthly)
    new = pd.read_csv(args.new_monthly)
    province_summary = compare_observed_data_completeness(old, new, ["province"])
    area_summary = compare_observed_data_completeness(old, new, ["province", "area"])
    area_summary.to_csv(args.output_csv, index=False, encoding="utf-8-sig")
    write_markdown_report(
        old,
        new,
        Path(args.report),
        province_summary,
        area_summary,
    )
    print(f"Wrote {args.output_csv}")
    print(f"Wrote {args.report}")


if __name__ == "__main__":
    main()
