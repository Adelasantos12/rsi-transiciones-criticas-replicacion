# Critical transitions and the International Health Regulations (IHR/RSI), 2010–2025

Replication materials for the chapter **“Gobernanza sanitaria global en el umbral: resiliencia y límites estructurales del Reglamento Sanitario Internacional”**.

The repository rebuilds the analytic dataset from the uploaded WHO SPAR/e-SPAR Excel workbooks, computes the period-level descriptive statistics, validates the results against `expected_results.json`, and generates the figures used to support the chapter’s argument.

## Core claim reproduced here

The empirical analysis does **not** show a sustained increase in dispersion around 2020 compatible with a critical transition. Instead, the results are more consistent with **metastability with persistent heterogeneity**: reported capacities change in level across instrument revisions, but the relative structure of dispersion does not reorganize around the COVID-19 shock.

## Data inputs

Raw Excel workbooks are stored in `data/raw/`:

- `IHRScoreperCapacity_2010.xlsx` … `IHRScoreperCapacity_2025.xlsx`

These files are treated as the source data. The repository does not download or modify the raw workbooks.

## Main constructed variable

`C.Legfin` is a bridge variable for legislation/policy/financing capacity across instrument editions:

- **2010–2020:** `C.Legfin = C.1` because legislation and financing are integrated in the available instrument structure.
- **2021–2025:** `C.Legfin = mean(C.1, C.3)` because the second SPAR edition separates policy/legal/normative instruments (`C.1`) and financing (`C.3`).

The scripts also extract:

- `C2`: IHR coordination / National IHR Focal Point functions
- `C.Vigilance`: mapped to the comparable surveillance capacity by instrument edition
- `C.LabResponse`: mapped to the comparable laboratory capacity by instrument edition

See `docs/METHODS_NOTE.md` and `docs/DATA_DICTIONARY.md`.

## Reproduce

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python scripts/run_all.py
```

Or run step by step:

```bash
python scripts/00_build_dataset.py
python scripts/01_make_tables.py
python scripts/02_make_figures.py
python scripts/03_validate_results.py
```

## Key outputs

Processed data:

- `data/processed/analytic_spar_espar_2010_2025.csv`
- `data/processed/annual_capacity_summary.csv`
- `data/processed/table1_period_descriptives.csv`

Tables:

- `outputs/tables/table1_period_descriptives.md`
- `outputs/tables/table1_period_descriptives.tex`

Figures:

- `outputs/figures/fig1_global_capacity_trends.png`
- `outputs/figures/fig2_clegfin_region_period.png`
- `outputs/figures/fig3_annual_cv.png`

Validation:

- `expected_results.json`
- `outputs/validation_report.csv`
- `docs/VALIDATION.md`

## Corrected Table 1 produced by the scripts

| period | n_obs_total | n_c_legfin | n_countries | mean_c_legfin | sd_c_legfin | cv_c_legfin_pct | mean_c2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pre-COVID (2010-2019) | 1515 | 1389 | 196 | 76.04 | 26.42 | 34.74 | 74.35 |
| COVID (2020-2021) | 358 | 358 | 189 | 61.61 | 23.69 | 38.45 | 67.85 |
| Post-COVID (2022-2025) | 762 | 762 | 196 | 59.15 | 20.63 | 34.88 | 66.32 |

These values are computed directly from the Excel workbooks in `data/raw/`.

## Manuscript note

If the accepted manuscript still reports earlier Table 1 values, use `docs/MANUSCRIPT_PATCH_SUGGESTED.md` to update the relevant paragraphs and table while preserving the chapter’s main argument.

## Citation

See `CITATION.cff`.
