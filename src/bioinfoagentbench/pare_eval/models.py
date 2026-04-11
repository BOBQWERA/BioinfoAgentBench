from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class StandardQuestion:
    benchmark: str
    schema_version: str
    id: str
    question: str
    data: list[dict[str, Any]]
    answer: str
    has_file: bool
    metadata: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return {
            "benchmark": self.benchmark,
            "schema_version": self.schema_version,
            "record": {
                "id": self.id,
                "question": self.question,
                "data": self.data,
                "answer": self.answer,
                "has_file": self.has_file,
                "metadata": self.metadata,
            },
        }


@dataclass
class DimensionScore:
    score: int
    evidence: list[str]
    reason: str


@dataclass
class PareScore:
    P: DimensionScore
    A: DimensionScore
    R: DimensionScore
    E: DimensionScore


@dataclass
class ScoreResult:
    question_id: str
    benchmark: str
    model: str
    scoring_mode: str
    scores: PareScore
    overall_summary: str
    confidence: float
    token_usage: dict[str, Any] | None = None
    raw_round1: dict[str, Any] | None = None
    raw_round2: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id,
            "benchmark": self.benchmark,
            "model": self.model,
            "scoring_mode": self.scoring_mode,
            "scores": {
                "P": asdict(self.scores.P),
                "A": asdict(self.scores.A),
                "R": asdict(self.scores.R),
                "E": asdict(self.scores.E),
            },
            "overall_summary": self.overall_summary,
            "confidence": self.confidence,
            "token_usage": self.token_usage,
            "raw_round1": self.raw_round1,
            "raw_round2": self.raw_round2,
            "scored_at": datetime.now(timezone.utc).isoformat(),
        }
