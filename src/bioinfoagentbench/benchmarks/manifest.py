from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from bioinfoagentbench.benchmarks.validate import summarize_standardized_file
from bioinfoagentbench.paths import standardized_benchmarks_dir


def build_manifest(directory: Path) -> dict[str, Any]:
    rows = [summarize_standardized_file(path) for path in sorted(directory.glob("*.json"))]
    return {
        "benchmark_count": len(rows),
        "record_count": sum(item["count"] for item in rows),
        "benchmarks": rows,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a lightweight manifest for the bundled standardized benchmark files."
    )
    parser.add_argument(
        "--directory",
        default=str(standardized_benchmarks_dir()),
        help="Directory containing standardized benchmark JSON files.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional output path for the manifest JSON file.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    manifest = build_manifest(Path(args.directory))
    payload = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
        print(f"Wrote manifest to {output_path}")
        return
    print(payload)


if __name__ == "__main__":
    main()
