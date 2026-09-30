#!/usr/bin/env python3
"""Generate figures for SPAR/e-SPAR chapter."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from common import PROCESSED_DIR, OUTPUTS_DIR, PERIOD_ORDER, CAPACITY_COLUMNS, CAPACITY_LABELS

FIG_DIR = OUTPUTS_DIR / "figures"


def fig1_trends(annual: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    for cap in CAPACITY_COLUMNS:
        d = annual[annual["capacity"] == cap].sort_values("year")
        ax.plot(d["year"], d["mean"], marker="o", label=CAPACITY_LABELS[cap])
        ax.fill_between(d["year"], d["mean"] - d["sd"], d["mean"] + d["sd"], alpha=0.12)
    ax.axvline(2020, linestyle="--", alpha=0.6)
    ax.set_title("Tendencias globales de capacidades RSI (2010-2025)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Puntaje medio reportado")
    ax.set_ylim(0, 100)
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig1_global_capacity_trends.png", dpi=300)
    plt.close(fig)


def fig2_region_period(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(10, 6), sharey=True)
    regions = [r for r in ["AFRO", "AMRO", "EMRO", "EURO", "SEARO", "WPRO"] if r in set(df["region"].dropna())]
    for ax, region in zip(axes.flatten(), regions):
        data = []
        labels = []
        for p in PERIOD_ORDER:
            x = df[(df["region"] == region) & (df["period"] == p)]["C.Legfin"].dropna()
            data.append(x)
            labels.append(p.replace(" ", "\n"))
        ax.violinplot(data, showmeans=False, showmedians=True)
        ax.set_title(f"Región {region}")
        ax.set_xticks(range(1, len(labels)+1))
        ax.set_xticklabels(labels, fontsize=7)
        ax.axhline(40, linestyle="--", alpha=0.5)
        ax.grid(True, axis="y", alpha=0.25)
    for ax in axes[:,0]:
        ax.set_ylabel("C.Legfin")
    fig.suptitle("Distribución de C.Legfin por región OMS")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIG_DIR / "fig2_clegfin_region_period.png", dpi=300)
    plt.close(fig)


def fig3_cv(annual: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    for cap in CAPACITY_COLUMNS:
        d = annual[annual["capacity"] == cap].sort_values("year")
        ax.plot(d["year"], d["cv_pct"], marker="o", label=CAPACITY_LABELS[cap])
    ax.axvline(2020, linestyle="--", alpha=0.6)
    ax.set_title("Coeficiente de variación de capacidades RSI (2010-2025)")
    ax.set_xlabel("Año")
    ax.set_ylabel("CV (%)")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig3_annual_cv.png", dpi=300)
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(PROCESSED_DIR / "analytic_spar_espar_2010_2025.csv")
    annual = pd.read_csv(PROCESSED_DIR / "annual_capacity_summary.csv")
    fig1_trends(annual)
    fig2_region_period(df)
    fig3_cv(annual)
    print(f"Wrote figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
