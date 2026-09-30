# Data dictionary

## Raw files

`data/raw/IHRScoreperCapacity_YYYY.xlsx` are annual WHO SPAR/e-SPAR score workbooks for 2010-2025.

## Analytic dataset

`data/processed/analytic_spar_espar_2010_2025.csv` contains one row per country-year.

Main columns:

| Column | Description |
|---|---|
| `year` | Reporting year. |
| `period` | `Pre-COVID (2010-2019)`, `COVID (2020-2021)`, or `Post-COVID (2022-2025)`. |
| `reported` | Original source value indicating whether data were received. |
| `region` | WHO region code from the source workbook. |
| `country` | State Party name as reported in the source workbook. |
| `iso3` | ISO3 code as reported in the source workbook. |
| `promedio_total` | Total average score in the source workbook. |
| `included_total` | `True` if `promedio_total` is numeric; used for total observation counts. |
| `C.Legfin` | Bridge variable for legislation/policy/financing capacity. |
| `C2` | IHR coordination / National IHR Focal Point functions. |
| `C.Vigilance` | Comparable surveillance capacity, mapped by instrument edition. |
| `C.LabResponse` | Comparable laboratory capacity, mapped by instrument edition. |

## Bridge variable: C.Legfin

- 2010-2020: `C.Legfin = C.1`
- 2021-2025: `C.Legfin = mean(C.1, C.3)`

This follows the final method note in the manuscript: financing is treated as integrated in the earlier instrument structure and separated from 2021 onward.

## Periods

- Pre-COVID: 2010-2019
- COVID: 2020-2021
- Post-COVID: 2022-2025
