#!/usr/bin/env python3
"""Run full replication pipeline."""
from __future__ import annotations

import subprocess
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
for script in ["00_build_dataset.py", "01_make_tables.py", "02_make_figures.py", "03_validate_results.py"]:
    print(f"\n--- Running {script} ---")
    subprocess.run([sys.executable, str(HERE / script)], check=True)
print("\nReplication pipeline completed successfully.")
