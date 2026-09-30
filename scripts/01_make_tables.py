#!/usr/bin/env python3
"""Generate descriptive tables from analytic SPAR/e-SPAR dataset."""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
from common import PROCESSED_DIR, OUTPUTS_DIR, PERIOD_ORDER, CAPACITY_COLUMNS, CAPACITY_LABELS


def round2(x):
    return round(float(x), 2) if pd.notna(x) else None


def compute_table1(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for period in PERIOD_ORDER:
        g = df[df["period"] == period]
        total = g[g["included_total"]]
        x = g["C.Legfin"].dropna()
        c2 = g["C2"].dropna()
        rows.append({
            "period": period,
            "n_obs_total": int(total.shape[0]),
            "n_c_legfin": int(x.shape[0]),
            "n_countries": int(total["iso3"].nunique()),
            "mean_c_legfin": round2(x.mean()),
            "sd_c_legfin": round2(x.std(ddof=1)),
            "cv_c_legfin_pct": round2(x.std(ddof=1) / x.mean() * 100),
            "mean_c2": round2(c2.mean()),
        })
    return pd.DataFrame(rows)


def compute_annual_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year, g in df.groupby("year"):
        for col in CAPACITY_COLUMNS:
            x = g[col].dropna()
            if x.empty:
                continue
            rows.append({
                "year": int(year),
                "capacity": col,
                "capacity_label": CAPACITY_LABELS[col],
                "n": int(x.shape[0]),
                "mean": round2(x.mean()),
                "sd": round2(x.std(ddof=1)),
                "cv_pct": round2(x.std(ddof=1) / x.mean() * 100),
            })
    return pd.DataFrame(rows)


def main() -> None:
    OUTPUTS_DIR.joinpath("tables").mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(PROCESSED_DIR / "analytic_spar_espar_2010_2025.csv")
    table1 = compute_table1(df)
    annual = compute_annual_summary(df)

    table1_path = PROCESSED_DIR / "table1_period_descriptives.csv"
    annual_path = PROCESSED_DIR / "annual_capacity_summary.csv"
    table1.to_csv(table1_path, index=False)
    annual.to_csv(annual_path, index=False)

    # Expected results for validation.
    expected = {row["period"]: {k: row[k] for k in row.index if k != "period"} for _, row in table1.iterrows()}
    with open(Path(__file__).resolve().parents[1] / "expected_results.json", "w", encoding="utf-8") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False)

    md = table1.to_markdown(index=False)
    tex = table1.to_latex(index=False, float_format="%.2f")
    (OUTPUTS_DIR / "tables" / "table1_period_descriptives.md").write_text(md + "\n", encoding="utf-8")
    (OUTPUTS_DIR / "tables" / "table1_period_descriptives.tex").write_text(tex, encoding="utf-8")
    print(f"Wrote {table1_path}")
    print(f"Wrote {annual_path}")


if __name__ == "__main__":
    main()
