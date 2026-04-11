from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from bioinfoagentbench.paths import source_collections_dir, standardized_benchmarks_dir

BENCHES = (
    "autoba",
    "biochatter",
    "biodsbench",
    "biodsbench-r",
    "biomed_aqa",
    "biomni_eval1",
    "bixbench",
    "labbench",
)

ANSWER_KEYS = {"expected_output", "answer"}
FILE_KEY_TOKENS = ("file", "path", "figure", "image", "archive")
FILE_EXTENSIONS = (
    ".fastq",
    ".fq",
    ".fasta",
    ".fa",
    ".gtf",
    ".gff",
    ".bam",
    ".sam",
    ".vcf",
    ".maf",
    ".csv",
    ".tsv",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".h5ad",
    ".h5",
    ".rds",
    ".gz",
    ".zip",
    ".tar",
    ".tar.gz",
)


def to_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def maybe_parse_json_list(text: str) -> list[Any] | None:
    stripped = text.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return None
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, list) else None


def normalize_slashes(text: str) -> str:
    return text.replace("\\", "/")


def autoba_relpath(text: str, case_name: str) -> str:
    normalized = normalize_slashes(text)
    if ":" in normalized:
        normalized = normalized.split(":", 1)[0].strip()
    match = re.search(r"(case\d+(?:\.\d+)?/.*)$", normalized)
    if match:
        return f"autoba/{match.group(1)}"
    if case_name:
        return f"autoba/{case_name}/{Path(normalized).name}"
    return f"autoba/{Path(normalized).name}"


def add_bench_prefix(path_text: str, bench: str) -> str:
    normalized = normalize_slashes(path_text).strip()
    if not normalized:
        return normalized
    if normalized.startswith(f"{bench}/"):
        return normalized
    trimmed = re.sub(r"^\.?/", "", normalized)
    return f"{bench}/{trimmed}"


def extract_path_like_value(value: Any) -> str:
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and value["path"].strip():
            return value["path"]
        if isinstance(value.get("name"), str) and value["name"].strip():
            return value["name"]
    return to_str(value)


def flatten_field(field_name: str, value: Any) -> list[dict[str, str]]:
    if value is None:
        return []

    entries: list[dict[str, str]] = []
    if field_name == "input" and isinstance(value, str):
        parsed = maybe_parse_json_list(value)
        if parsed is not None:
            for item in parsed:
                entries.append({"type": "input", "value": to_str(item)})
            return entries

    if isinstance(value, list):
        for item in value:
            if item is not None:
                entries.append({"type": field_name, "value": to_str(item)})
        return entries

    entries.append({"type": field_name, "value": to_str(value)})
    return entries


def contains_file_reference(obj: Any) -> bool:
    if obj is None:
        return False

    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = str(key).lower()
            if any(token in key_lower for token in FILE_KEY_TOKENS) and value not in (None, ""):
                return True
            if contains_file_reference(value):
                return True
        return False

    if isinstance(obj, list):
        return any(contains_file_reference(item) for item in obj)

    if isinstance(obj, str):
        stripped = obj.strip().lower()
        if not stripped:
            return False
        if any(ext in stripped for ext in FILE_EXTENSIONS):
            return True
        return bool(re.search(r"[/\\]", stripped) and re.search(r"\.[a-z0-9]{1,8}(\b|\s|:|$)", stripped))

    return False


def normalize_record(item: dict[str, Any], bench: str) -> dict[str, Any]:
    raw_data = item.get("data")
    data_entries: list[dict[str, str]] = []
    metadata = dict(item.get("metadata", {}))
    question = to_str(item.get("question"))

    if bench == "biochatter":
        if isinstance(raw_data, dict) and raw_data.get("input") is not None:
            input_text = to_str(raw_data["input"])
            if input_text and input_text not in question:
                question = f"{question}\n\n[template_input]\n{input_text}"
    elif bench in {"bixbench", "labbench"}:
        if isinstance(raw_data, dict) and "distractors" in raw_data:
            metadata["distractors"] = raw_data["distractors"]

    if bench in {"biochatter", "bixbench", "labbench"}:
        data_entries = []
    elif isinstance(raw_data, dict):
        for key, value in raw_data.items():
            if key in ANSWER_KEYS:
                continue
            if bench == "autoba" and key == "output_dir":
                continue
            if bench == "biomed_aqa" and key == "input_files":
                if isinstance(value, list):
                    for file_item in value:
                        data_entries.append(
                            {
                                "type": "input",
                                "value": add_bench_prefix(extract_path_like_value(file_item), bench),
                            }
                        )
                else:
                    data_entries.append(
                        {
                            "type": "input",
                            "value": add_bench_prefix(extract_path_like_value(value), bench),
                        }
                    )
                continue
            data_entries.extend(flatten_field(key, value))
    elif raw_data is not None:
        data_entries.extend(flatten_field("data", raw_data))

    if bench == "autoba":
        case_name = to_str(metadata.get("case_name"))
        for entry in data_entries:
            if entry["type"] == "input":
                entry["value"] = autoba_relpath(entry["value"], case_name)

    if bench in {"biodsbench", "biodsbench-r"}:
        for entry in data_entries:
            if entry["type"] == "input":
                entry["value"] = add_bench_prefix(entry["value"], bench)

    answer_value = None
    if isinstance(raw_data, dict):
        answer_value = raw_data.get("answer", raw_data.get("expected_output"))
    if answer_value is None and "answer" in item:
        answer_value = item["answer"]

    return {
        "id": to_str(item.get("id")),
        "question": question,
        "data": data_entries,
        "answer": to_str(answer_value),
        "has_file": contains_file_reference(raw_data),
        "metadata": metadata,
    }


def schema_doc() -> str:
    return """# Benchmark Standard Schema

All standardized benchmark files in this folder follow the same top-level and record-level structure.

## Top-level structure
- `benchmark` (string): benchmark name
- `schema_version` (string): schema version
- `count` (integer): number of normalized records
- `records` (array): normalized records

## Record structure
- `id` (string): original benchmark id, preserved
- `question` (string): task question or prompt
- `data` (array): normalized data entries, each item has:
  - `type` (string): data field source name
  - `value` (string): normalized content
- `answer` (string): expected answer or output converted to string
- `has_file` (boolean): whether the original sample contains file-like references
- `metadata` (object): original metadata, preserved as-is

## Rules
- `environment` is removed.
- `expected_output` is moved into `answer`.
- Nested `input` lists are flattened into multiple entries inside `data`.
- Benchmark-specific rules are applied where needed, such as path rewriting and moving distractors into metadata.
"""


def write_standardized_benchmarks(
    source_dir: Path,
    output_dir: Path,
    benches: Iterable[str] = BENCHES,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for bench in benches:
        input_path = source_dir / bench / "all_benchmarks.json"
        if not input_path.exists():
            raise FileNotFoundError(f"Missing input file: {input_path}")

        records = json.loads(input_path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError(f"Expected list in {input_path}")

        normalized_records = [normalize_record(item, bench) for item in records]
        output_obj = {
            "benchmark": bench,
            "schema_version": "1.0.0",
            "count": len(normalized_records),
            "records": normalized_records,
        }

        output_path = output_dir / f"{bench}.json"
        output_path.write_text(json.dumps(output_obj, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(output_path)

    (output_dir / "SCHEMA.md").write_text(schema_doc(), encoding="utf-8")
    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize source benchmark collections into the unified BioinfoAgentBench schema."
    )
    parser.add_argument(
        "--source-dir",
        default=str(source_collections_dir()),
        help="Directory containing source benchmark collections.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(standardized_benchmarks_dir()),
        help="Destination directory for standardized benchmark JSON files.",
    )
    parser.add_argument(
        "--bench",
        nargs="*",
        default=list(BENCHES),
        help="Optional subset of benchmark names to process.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    written = write_standardized_benchmarks(
        source_dir=Path(args.source_dir),
        output_dir=Path(args.output_dir),
        benches=args.bench,
    )
    print(f"Wrote {len(written)} standardized benchmark file(s).")


if __name__ == "__main__":
    main()
