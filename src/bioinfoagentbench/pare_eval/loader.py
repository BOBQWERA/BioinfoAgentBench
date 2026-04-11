from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bioinfoagentbench.pare_eval.models import StandardQuestion


class StandardQuestionImporter:
    def __init__(self, standardized_dir: Path):
        self.standardized_dir = standardized_dir

    def list_benchmarks(self) -> list[str]:
        return sorted(p.stem for p in self.standardized_dir.glob("*.json"))

    def load_benchmark_json(self, benchmark: str) -> dict[str, Any]:
        path = self.standardized_dir / f"{benchmark}.json"
        if not path.exists():
            raise FileNotFoundError(f"Benchmark file not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def get_question(
        self,
        benchmark: str,
        record_id: str | None = None,
        index: int | None = None,
    ) -> StandardQuestion:
        if (record_id is None and index is None) or (record_id is not None and index is not None):
            raise ValueError("Provide exactly one of `record_id` or `index`.")

        payload = self.load_benchmark_json(benchmark)
        records = payload.get("records", [])
        record: dict[str, Any] | None = None

        if record_id is not None:
            record = next((r for r in records if r.get("id") == record_id), None)
            if record is None:
                raise KeyError(f"record_id '{record_id}' not found in benchmark '{benchmark}'.")
        else:
            if index is None or index < 0 or index >= len(records):
                raise IndexError(f"index out of range: {index}; record count={len(records)}")
            record = records[index]

        return StandardQuestion(
            benchmark=payload["benchmark"],
            schema_version=payload["schema_version"],
            id=record["id"],
            question=record["question"],
            data=record.get("data", []),
            answer=record.get("answer", ""),
            has_file=bool(record.get("has_file", False)),
            metadata=record.get("metadata", {}),
        )
