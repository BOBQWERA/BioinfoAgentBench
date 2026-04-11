from __future__ import annotations

import runpy
from pathlib import Path

SCRIPTS = (
    "build_table_s1.py",
    "build_table_s2.py",
    "build_table_s3.py",
    "build_table_s4.py",
    "build_table_s5.py",
    "build_table_s6.py",
    "build_table_s7.py",
)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    for name in SCRIPTS:
        path = script_dir / name
        print(f"[RUN] {path.name}")
        runpy.run_path(str(path), run_name="__main__")


if __name__ == "__main__":
    main()
