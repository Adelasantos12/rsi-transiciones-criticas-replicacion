#!/usr/bin/env python3
"""Shared utilities for SPAR/e-SPAR replication scripts."""
from __future__ import annotations

from pathlib import Path
import re
import math
import pandas as pd
import numpy as np

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
OUTPUTS_DIR = Path(__file__).resolve().parents[1] / "outputs"

PERIOD_ORDER = ["Pre-COVID (2010-2019)", "COVID (2020-2021)", "Post-COVID (2022-2025)"]
CAPACITY_COLUMNS = ["C.Legfin", "C2", "C.Vigilance", "C.LabResponse"]
CAPACITY_LABELS = {
    "C.Legfin": "Legislación+financiamiento",
    "C2": "Coordinación",
    "C.Vigilance": "Vigilancia",
    "C.LabResponse": "Laboratorio",
}


def period_for_year(year: int) -> str:
    if year <= 2019:
        return "Pre-COVID (2010-2019)"
    if year <= 2021:
        return "COVID (2020-2021)"
    return "Post-COVID (2022-2025)"


def to_number(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.integer, np.floating)):
        return float(x)
    s = str(x).strip().replace(",", ".")
    if s == "" or s.lower() in {"sin datos", "no data", "na", "nan", "none"}:
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


def extract_year(path: Path) -> int:
    m = re.search(r"(20\d{2}|201\d)", path.name)
    if not m:
        raise ValueError(f"Could not extract year from {path.name}")
    return int(m.group(1))
