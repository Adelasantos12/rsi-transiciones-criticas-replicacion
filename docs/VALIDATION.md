# Validation

Run:

```bash
python scripts/run_all.py
```

The validation step compares `data/processed/table1_period_descriptives.csv` against `expected_results.json`.

A successful run writes:

- `outputs/validation_report.csv`

and prints:

```text
Validation: PASS.
```

The expected values are generated from the same deterministic pipeline after parsing the raw workbooks. If the raw data or bridge-variable logic changes, rerun `01_make_tables.py` to regenerate `expected_results.json` and document the change.
