from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURATED_SOURCE = ROOT / "paper" / "sources" / "table_s1_curated.xlsx"
OUTPUT_DIR = ROOT / "paper" / "supplementary"
OUTPUT = OUTPUT_DIR / "Table_S1.xlsx"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CURATED_SOURCE, OUTPUT)


if __name__ == "__main__":
    main()
