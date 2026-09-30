#!/usr/bin/env python3
"""Build analytic SPAR/e-SPAR dataset from WHO Excel workbooks."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np
from common import RAW_DIR, PROCESSED_DIR, extract_year, to_number, period_for_year


def read_workbook(path: Path) -> pd.DataFrame:
    year = extract_year(path)
    raw = pd.read_excel(path, sheet_name=0, header=None, engine="openpyxl")

    # Source workbooks use rows 1-6 for titles/capacity labels and row 14 (0-index=13)
    # as the country table header. Country rows start at row 15 (0-index=14).
    header = raw.iloc[13].tolist()
    rows = raw.iloc[14:].copy()
    rows.columns = [str(x).strip() if pd.notna(x) else "" for x in header]

    # Standard columns. The Spanish source file uses "Datos recividos" in row 14.
    rename = {
        rows.columns[0]: "reported",
        rows.columns[1]: "region",
        rows.columns[2]: "country",
        rows.columns[3]: "iso3",
        "Promedio total": "promedio_total",
    }
    rows = rows.rename(columns=rename)
    rows = rows[rows["country"].notna()].copy()
    rows["country"] = rows["country"].astype(str).str.strip()
    rows["iso3"] = rows["iso3"].astype(str).str.strip()
    rows["region"] = rows["region"].astype(str).str.strip()
    rows["year"] = year
    rows["period"] = rows["year"].apply(period_for_year)

    # Convert all capacity-like columns to numeric where possible.
    for col in list(rows.columns):
        if col == "promedio_total" or col.startswith("C."):
            rows[col] = rows[col].map(to_number)

    # Derived bridge variable. This follows the manuscript's final method note:
    # 2010-2020 integrated legislation/financing; from 2021 financing split from C1.
    if year <= 2020:
        rows["C.Legfin"] = rows.get("C.1", np.nan)
        rows["C2"] = rows.get("C.2", np.nan)
        rows["C.Vigilance"] = rows.get("C.3", np.nan) if year <= 2017 else rows.get("C.6", np.nan)
        rows["C.LabResponse"] = rows.get("C.8", np.nan) if year <= 2017 else rows.get("C.5", np.nan)
    else:
        c1 = rows.get("C.1", pd.Series(np.nan, index=rows.index))
        c3 = rows.get("C.3", pd.Series(np.nan, index=rows.index))
        rows["C.Legfin"] = pd.concat([c1, c3], axis=1).mean(axis=1, skipna=True)
        rows["C2"] = rows.get("C.2", np.nan)
        rows["C.Vigilance"] = rows.get("C.5", np.nan)
        rows["C.LabResponse"] = rows.get("C.4", np.nan)

    # Observation with an overall reported score; used for total N by period.
    rows["included_total"] = rows["promedio_total"].notna()

    keep_front = [
        "year", "period", "reported", "region", "country", "iso3", "promedio_total",
        "C.Legfin", "C2", "C.Vigilance", "C.LabResponse", "included_total",
    ]
    other_cols = [c for c in rows.columns if c not in keep_front]
    return rows[keep_front + other_cols]


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    paths = sorted(RAW_DIR.glob("IHRScoreperCapacity_*.xlsx"))
    if not paths:
        raise FileNotFoundError(f"No IHRScoreperCapacity_*.xlsx files found in {RAW_DIR}")
    frames = [read_workbook(p) for p in paths]
    df = pd.concat(frames, ignore_index=True)
    out = PROCESSED_DIR / "analytic_spar_espar_2010_2025.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out} ({len(df):,} country-year rows).")


if __name__ == "__main__":
    main()
