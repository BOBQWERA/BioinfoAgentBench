from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bioinfoagentbench.pare_eval.models import ScoreResult, StandardQuestion


class ScoreStore:
    def __init__(self, output_root: Path):
        self.output_root = output_root

    def persist(self, question: StandardQuestion, result: ScoreResult) -> Path:
        bench_dir = self.output_root / question.benchmark
        bench_dir.mkdir(parents=True, exist_ok=True)

        snapshot_path = bench_dir / f"{question.id}.json"
        snapshot_payload = {
            "question": question.to_payload(),
            "result": result.to_dict(),
        }
        snapshot_path.write_text(
            json.dumps(snapshot_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        summary_path = bench_dir / "scores.jsonl"
        summary = {
            "question_id": question.id,
            "benchmark": question.benchmark,
            "scoring_mode": result.scoring_mode,
            "model": result.model,
            "scores": {
                "P": result.scores.P.score,
                "A": result.scores.A.score,
                "R": result.scores.R.score,
                "E": result.scores.E.score,
            },
            "confidence": result.confidence,
            "token_usage": result.token_usage,
        }
        with summary_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(summary, ensure_ascii=False) + "\n")

        return snapshot_path

    def persist_dry_run(
        self,
        question: StandardQuestion,
        mode: str,
        prompts: dict[str, dict[str, Any]],
    ) -> Path:
        bench_dir = self.output_root / question.benchmark
        bench_dir.mkdir(parents=True, exist_ok=True)
        path = bench_dir / f"{question.id}.dry_run_prompts.json"
        payload = {
            "question": question.to_payload(),
            "mode": mode,
            "prompts": prompts,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
