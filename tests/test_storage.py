from __future__ import annotations

import json

from bioinfoagentbench.pare_eval.models import (
    DimensionScore,
    PareScore,
    ScoreResult,
    StandardQuestion,
)
from bioinfoagentbench.pare_eval.storage import ScoreStore


def test_score_store_persists_snapshot_and_summary(tmp_path) -> None:
    store = ScoreStore(tmp_path)
    question = StandardQuestion(
        benchmark="demo",
        schema_version="1.0.0",
        id="q1",
        question="demo question",
        data=[],
        answer="demo answer",
        has_file=False,
        metadata={},
    )
    result = ScoreResult(
        question_id="q1",
        benchmark="demo",
        model="gpt-4.1",
        scoring_mode="single_round",
        scores=PareScore(
            P=DimensionScore(score=1, evidence=[], reason=""),
            A=DimensionScore(score=2, evidence=[], reason=""),
            R=DimensionScore(score=3, evidence=[], reason=""),
            E=DimensionScore(score=0, evidence=[], reason=""),
        ),
        overall_summary="demo",
        confidence=0.5,
    )

    snapshot = store.persist(question, result)

    assert snapshot.exists()
    payload = json.loads(snapshot.read_text(encoding="utf-8"))
    assert payload["result"]["scores"]["A"]["score"] == 2
    summary = (tmp_path / "demo" / "scores.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(summary) == 1
