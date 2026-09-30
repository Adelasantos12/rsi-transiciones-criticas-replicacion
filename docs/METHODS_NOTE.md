# Methods note

This repository reproduces the empirical component of the chapter using WHO SPAR/e-SPAR annual Excel files for 2010-2025.

## Parsing

Each workbook is parsed from the first worksheet. The country-level table starts at row 15, with row 14 used as the source header row. The scripts standardize the following source fields: reporting status, WHO region, country, ISO3 code, total average score, and all capacity code columns (`C.*`).

## Comparability challenge

The SPAR/e-SPAR instrument changed over time. The chapter therefore avoids interpreting the 2018 level shift as a pandemic effect. The key diagnostic for the critical-transitions argument is the absence of a sustained increase in dispersion around 2020, especially in the annual coefficient of variation series.

## C.Legfin bridge

The principal bridge variable is `C.Legfin`, which tracks legislation/policy/financing capacity. It is constructed as:

- 2010-2020: `C.1`
- 2021-2025: average of `C.1` and `C.3`

This is documented in `scripts/00_build_dataset.py`.

## Descriptive statistics

`table1_period_descriptives.csv` reports:

- total observations with a numeric total score,
- valid C.Legfin observations,
- countries represented,
- mean, standard deviation and coefficient of variation for C.Legfin,
- mean C2.

## Interpretation

The outputs support a cautious interpretation: changes in level are affected by instrument revisions, while the CV trajectory does not show a clear reorganization around the COVID-19 shock. This is compatible with metastability, not a demonstrated critical transition.
