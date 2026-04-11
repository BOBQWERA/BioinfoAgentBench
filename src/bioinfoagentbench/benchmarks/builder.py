import argparse
import json
from pathlib import Path
from typing import Any

from bioinfoagentbench.paths import standardized_benchmarks_dir


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_input_json(input_dir: Path, explicit_file: str | None) -> Path:
    if explicit_file:
        p = input_dir / explicit_file
        if not p.exists():
            raise FileNotFoundError(f"Input file not found: {p}")
        return p

    candidates = sorted(
        p
        for p in input_dir.glob("*.json")
        if p.name not in {"score_snapshot.json", "workflow_reference_snapshot.json"}
    )
    if not candidates:
        raise FileNotFoundError(
            f"No candidate JSON found in {input_dir}. "
            "Provide --input-file explicitly."
        )
    if len(candidates) > 1:
        names = ", ".join(p.name for p in candidates)
        raise ValueError(
            f"Multiple candidate JSON files found in {input_dir}: {names}. "
            "Provide --input-file explicitly."
        )
    return candidates[0]


def _build_answer_lookup(source_path: Path | None) -> dict[str, str]:
    if source_path is None or not source_path.exists():
        return {}
    source_obj = _load_json(source_path)
    records = source_obj.get("records", [])
    lookup: dict[str, str] = {}
    for item in records:
        rid = str(item.get("id", ""))
        if not rid:
            continue
        answer = item.get("answer", "")
        if not isinstance(answer, str):
            answer = json.dumps(answer, ensure_ascii=False)
        lookup[rid] = answer
    return lookup


def _extract_edit_context(record: dict[str, Any]) -> dict[str, Any]:
    context: dict[str, Any] = {}
    for key in (
        "r1_mechanism",
        "r2_mechanism",
        "data_repair_methods",
        "workflow_reference",
        "original_question",
    ):
        if key in record:
            context[key] = record[key]
    return context


def _transform_records(
    records: list[dict[str, Any]],
    source_benchmark: str,
    edit_target: str,
    selection_basis: str,
    answers_by_id: dict[str, str],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for r in records:
        rid = str(r.get("id", ""))
        if not rid:
            raise ValueError("Each record must have a non-empty 'id'.")

        question = r.get("rewritten_question") or r.get("question")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"Record {rid} has empty rewritten question.")

        data = r.get("data", [])
        if not isinstance(data, list):
            raise ValueError(f"Record {rid} has non-list 'data'.")

        metadata = dict(r.get("metadata", {}))
        metadata["bench_builder"] = {
            "source_benchmark": source_benchmark,
            "edit_target": edit_target,
            "selection_basis": selection_basis,
            "edit_context": _extract_edit_context(r),
        }

        out.append(
            {
                "id": rid,
                "question": question,
                "data": data,
                "answer": answers_by_id.get(rid, ""),
                "has_file": bool(r.get("has_file", False)),
                "metadata": metadata,
            }
        )
    return out


def build_standardized_bench(
    input_dir: Path,
    output_name: str,
    standardized_dir: Path,
    input_file: str | None,
    source_file_override: str | None,
) -> Path:
    input_json = _find_input_json(input_dir, input_file)
    src_obj = _load_json(input_json)

    records = src_obj.get("records")
    if not isinstance(records, list):
        raise ValueError(f"'records' must be a list in {input_json}")

    source_benchmark = str(src_obj.get("benchmark", "unknown"))
    edit_target = str(src_obj.get("edit_target", ""))
    selection_basis = str(
        src_obj.get("selection_basis", src_obj.get("selection_constraints", ""))
    )

    source_path: Path | None = None
    if source_file_override:
        source_path = Path(source_file_override)
    else:
        sf = src_obj.get("source_file")
        if isinstance(sf, str) and sf.strip():
            source_path = Path(sf)

    answers_by_id = _build_answer_lookup(source_path)
    normalized_records = _transform_records(
        records=records,
        source_benchmark=source_benchmark,
        edit_target=edit_target,
        selection_basis=selection_basis,
        answers_by_id=answers_by_id,
    )

    output_obj = {
        "benchmark": output_name,
        "schema_version": "1.0.0",
        "count": len(normalized_records),
        "records": normalized_records,
    }

    standardized_dir.mkdir(parents=True, exist_ok=True)
    out_path = standardized_dir / f"{output_name}.json"
    out_path.write_text(
        json.dumps(output_obj, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Convert fixed upgrade folder format (R1/R2) into standardized benchmark JSON."
        )
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Folder containing one upgraded benchmark JSON.",
    )
    parser.add_argument(
        "--output-name",
        required=True,
        help="Output benchmark name; writes <standardized-dir>/<output-name>.json",
    )
    parser.add_argument(
        "--standardized-dir",
        default=str(standardized_benchmarks_dir()),
        help="Destination standardized directory.",
    )
    parser.add_argument(
        "--input-file",
        default=None,
        help="Optional explicit input filename inside --input-dir.",
    )
    parser.add_argument(
        "--source-file-override",
        default=None,
        help="Optional source standardized JSON to recover answers by id.",
    )
    args = parser.parse_args()

    out_path = build_standardized_bench(
        input_dir=Path(args.input_dir),
        output_name=args.output_name,
        standardized_dir=Path(args.standardized_dir),
        input_file=args.input_file,
        source_file_override=args.source_file_override,
    )
    print(f"OK: wrote {out_path}")


if __name__ == "__main__":
    main()
