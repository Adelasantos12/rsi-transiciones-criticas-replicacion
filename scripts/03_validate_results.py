#!/usr/bin/env python3
"""Validate computed results against expected_results.json."""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
from common import PROCESSED_DIR, OUTPUTS_DIR

TOL = 0.005


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    expected_path = root / "expected_results.json"
    if not expected_path.exists():
        raise FileNotFoundError("expected_results.json not found. Run 01_make_tables.py first.")
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    actual = pd.read_csv(PROCESSED_DIR / "table1_period_descriptives.csv")

    rows = []
    all_pass = True
    for _, row in actual.iterrows():
        p = row["period"]
        exp = expected[p]
        for k, ev in exp.items():
            av = row[k]
            if isinstance(ev, float):
                ok = abs(float(av) - float(ev)) <= TOL
            else:
                ok = av == ev
            all_pass = all_pass and ok
            rows.append({"period": p, "metric": k, "expected": ev, "actual": av, "pass": ok})
    report = pd.DataFrame(rows)
    out = OUTPUTS_DIR / "validation_report.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(out, index=False)
    status = "PASS" if all_pass else "FAIL"
    print(f"Validation: {status}. Wrote {out}")
    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
