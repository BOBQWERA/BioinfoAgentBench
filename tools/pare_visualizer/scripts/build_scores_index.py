from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _load_record(path: Path) -> dict[str, Any] | None:
    if path.name == "scores.jsonl" or path.name.endswith(".dry_run_prompts.json"):
        return None
    if path.suffix.lower() != ".json":
        return None

    payload = json.loads(path.read_text(encoding="utf-8"))
    question = payload.get("question", {})
    result = payload.get("result", {})
    record = question.get("record", {})
    scores = result.get("scores", {})

    core = {
        "bench": question.get("benchmark", result.get("benchmark")),
        "id": record.get("id", result.get("question_id", path.stem)),
        "question": record.get("question", ""),
        "scores": {
            "P": _safe_int(scores.get("P", {}).get("score")),
            "A": _safe_int(scores.get("A", {}).get("score")),
            "R": _safe_int(scores.get("R", {}).get("score")),
            "E": _safe_int(scores.get("E", {}).get("score")),
        },
        "subdimensions": {
            "P": scores.get("P", {}).get("subdimension_breakdown", {}),
            "A": scores.get("A", {}).get("subdimension_breakdown", {}),
            "R": scores.get("R", {}).get("subdimension_breakdown", {}),
            "E": scores.get("E", {}).get("subdimension_breakdown", {}),
        },
        "reason": {
            "P": scores.get("P", {}).get("reason", ""),
            "A": scores.get("A", {}).get("reason", ""),
            "R": scores.get("R", {}).get("reason", ""),
            "E": scores.get("E", {}).get("reason", ""),
        },
        "evidence": {
            "P": scores.get("P", {}).get("evidence", []),
            "A": scores.get("A", {}).get("evidence", []),
            "R": scores.get("R", {}).get("evidence", []),
            "E": scores.get("E", {}).get("evidence", []),
        },
        "overall_summary": result.get("overall_summary", ""),
        "confidence": result.get("confidence"),
        "token_usage": result.get("token_usage", {}),
        "model": result.get("model"),
        "scoring_mode": result.get("scoring_mode"),
        "scored_at": result.get("scored_at"),
        "metadata": record.get("metadata", {}),
        "input_count": len(record.get("data", [])),
        "source_file": str(path.as_posix()),
    }
    return core


def _calc_bench_stats(records: list[dict[str, Any]]) -> dict[str, Any]:
    bucket: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        bucket[r["bench"]].append(r)

    stats: dict[str, Any] = {}
    for bench, items in bucket.items():
        n = len(items)
        if n == 0:
            continue
        avg = {
            "P": round(sum(x["scores"]["P"] for x in items) / n, 3),
            "A": round(sum(x["scores"]["A"] for x in items) / n, 3),
            "R": round(sum(x["scores"]["R"] for x in items) / n, 3),
            "E": round(sum(x["scores"]["E"] for x in items) / n, 3),
        }
        stats[bench] = {"count": n, "avg_scores": avg}
    return stats


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    outputs_dir = project_root / "examples" / "pare_outputs"
    out_file = project_root / "tools" / "pare_visualizer" / "data" / "scores_index.json"

    records: list[dict[str, Any]] = []
    for path in outputs_dir.rglob("*.json"):
        row = _load_record(path)
        if row:
            records.append(row)

    records.sort(key=lambda x: (x["bench"], x["id"]))
    bench_stats = _calc_bench_stats(records)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scale_min": 0,
        "scale_max": 5,
        "record_count": len(records),
        "bench_count": len(bench_stats),
        "bench_stats": bench_stats,
        "records": records,
    }
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Indexed {len(records)} records into {out_file}")


if __name__ == "__main__":
    main()

