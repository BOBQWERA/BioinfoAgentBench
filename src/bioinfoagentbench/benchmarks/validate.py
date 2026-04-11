from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from bioinfoagentbench.paths import standardized_benchmarks_dir

REQUIRED_TOP_LEVEL_KEYS = {"benchmark", "schema_version", "count", "records"}
REQUIRED_RECORD_KEYS = {"id", "question", "data", "answer", "has_file", "metadata"}


def validate_standardized_payload(payload: dict[str, Any], source: str) -> list[str]:
    errors: list[str] = []
    missing_top_level = REQUIRED_TOP_LEVEL_KEYS - payload.keys()
    if missing_top_level:
        errors.append(f"{source}: missing top-level keys: {sorted(missing_top_level)}")

    records = payload.get("records")
    if not isinstance(records, list):
        errors.append(f"{source}: 'records' must be a list")
        return errors

    count = payload.get("count")
    if not isinstance(count, int):
        errors.append(f"{source}: 'count' must be an integer")
    elif count != len(records):
        errors.append(f"{source}: 'count'={count} does not match record length={len(records)}")

    seen_ids: set[str] = set()
    for idx, record in enumerate(records):
        label = f"{source} record[{idx}]"
        if not isinstance(record, dict):
            errors.append(f"{label}: record must be an object")
            continue

        missing_record_keys = REQUIRED_RECORD_KEYS - record.keys()
        if missing_record_keys:
            errors.append(f"{label}: missing keys: {sorted(missing_record_keys)}")
            continue

        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id.strip():
            errors.append(f"{label}: 'id' must be a non-empty string")
        elif record_id in seen_ids:
            errors.append(f"{label}: duplicate id '{record_id}'")
        else:
            seen_ids.add(record_id)

        if not isinstance(record.get("question"), str):
            errors.append(f"{label}: 'question' must be a string")
        if not isinstance(record.get("answer"), str):
            errors.append(f"{label}: 'answer' must be a string")
        if not isinstance(record.get("has_file"), bool):
            errors.append(f"{label}: 'has_file' must be a boolean")
        if not isinstance(record.get("metadata"), dict):
            errors.append(f"{label}: 'metadata' must be an object")

        data = record.get("data")
        if not isinstance(data, list):
            errors.append(f"{label}: 'data' must be a list")
            continue
        for entry_index, entry in enumerate(data):
            entry_label = f"{label} data[{entry_index}]"
            if not isinstance(entry, dict):
                errors.append(f"{entry_label}: entry must be an object")
                continue
            if set(entry.keys()) != {"type", "value"}:
                errors.append(f"{entry_label}: keys must be exactly ['type', 'value']")
            if not isinstance(entry.get("type"), str):
                errors.append(f"{entry_label}: 'type' must be a string")
            if not isinstance(entry.get("value"), str):
                errors.append(f"{entry_label}: 'value' must be a string")

    return errors


def validate_standardized_file(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return [f"{path}: root JSON payload must be an object"]
    return validate_standardized_payload(payload, str(path))


def summarize_standardized_file(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    with_files = sum(1 for record in records if record.get("has_file"))
    return {
        "benchmark": payload.get("benchmark", path.stem),
        "count": payload.get("count", len(records)),
        "with_file_references": with_files,
    }


def validate_directory(directory: Path) -> tuple[list[dict[str, Any]], list[str]]:
    summaries: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted(directory.glob("*.json")):
        errors.extend(validate_standardized_file(path))
        summaries.append(summarize_standardized_file(path))
    return summaries, errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the standardized benchmark JSON files bundled with BioinfoAgentBench."
    )
    parser.add_argument(
        "--directory",
        default=str(standardized_benchmarks_dir()),
        help="Directory containing standardized benchmark JSON files.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summaries, errors = validate_directory(Path(args.directory))

    total_records = sum(item["count"] for item in summaries)
    print(f"Validated {len(summaries)} benchmark file(s) with {total_records} total record(s).")
    for item in summaries:
        print(
            f"- {item['benchmark']}: {item['count']} records "
            f"({item['with_file_references']} with file references)"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print("All standardized benchmarks passed validation.")


if __name__ == "__main__":
    main()
