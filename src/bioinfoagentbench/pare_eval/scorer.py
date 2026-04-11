from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from bioinfoagentbench.pare_eval.models import (
    DimensionScore,
    PareScore,
    ScoreResult,
    StandardQuestion,
)
from bioinfoagentbench.pare_eval.prompts import PromptBundle, PromptTemplateBuilder


class GPT41Scorer:
    def __init__(
        self,
        model: str = "gpt-4.1",
        api_key: str | None = None,
        base_url: str | None = None,
        timeout_sec: float = 60.0,
        max_retries: int = 3,
    ):
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise OSError("OPENAI_API_KEY is not set.")
        resolved_base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.model = model
        self.client = OpenAI(
            api_key=key,
            base_url=resolved_base_url,
            timeout=timeout_sec,
            max_retries=max_retries,
        )

    @staticmethod
    def _usage_from_response(rsp: Any) -> dict[str, int]:
        usage = getattr(rsp, "usage", None)
        if usage is None:
            return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        return {
            "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
            "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
            "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
        }

    @staticmethod
    def _sum_usage(*usages: dict[str, int]) -> dict[str, int]:
        return {
            "prompt_tokens": sum(u.get("prompt_tokens", 0) for u in usages),
            "completion_tokens": sum(u.get("completion_tokens", 0) for u in usages),
            "total_tokens": sum(u.get("total_tokens", 0) for u in usages),
        }

    def _completion_json(self, bundle: PromptBundle) -> tuple[dict[str, Any], dict[str, int]]:
        rsp = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": bundle.system},
                {"role": "user", "content": bundle.user},
            ],
        )
        content = rsp.choices[0].message.content
        if not content:
            raise ValueError("Model returned empty content.")
        return json.loads(content), self._usage_from_response(rsp)

    @staticmethod
    def _to_dimension_score(obj: dict[str, Any], dim: str) -> DimensionScore:
        return DimensionScore(
            score=int(obj[dim]["score"]),
            evidence=[str(x) for x in obj[dim].get("evidence", [])],
            reason=str(obj[dim].get("reason", "")),
        )

    def _to_score_result(
        self,
        question: StandardQuestion,
        scoring_mode: str,
        scored_json: dict[str, Any],
        token_usage: dict[str, Any] | None = None,
        round1_json: dict[str, Any] | None = None,
    ) -> ScoreResult:
        scores = scored_json["scores"]
        result = ScoreResult(
            question_id=question.id,
            benchmark=question.benchmark,
            model=self.model,
            scoring_mode=scoring_mode,
            scores=PareScore(
                P=self._to_dimension_score(scores, "P"),
                A=self._to_dimension_score(scores, "A"),
                R=self._to_dimension_score(scores, "R"),
                E=self._to_dimension_score(scores, "E"),
            ),
            overall_summary=str(scored_json.get("overall_summary", "")),
            confidence=float(scored_json.get("confidence", 0.0)),
            token_usage=token_usage,
            raw_round1=round1_json,
            raw_round2=scored_json,
        )
        self._validate(result)
        return result

    @staticmethod
    def _validate(result: ScoreResult) -> None:
        for dim in (result.scores.P, result.scores.A, result.scores.R, result.scores.E):
            if dim.score < 0 or dim.score > 5:
                raise ValueError(f"score out of range [0,5]: {dim.score}")
        if result.confidence < 0 or result.confidence > 1:
            raise ValueError(f"confidence out of range [0,1]: {result.confidence}")

    def score_single_round(self, question: StandardQuestion, templates: PromptTemplateBuilder) -> ScoreResult:
        bundle = templates.build_single_round(question)
        scored_json, usage = self._completion_json(bundle)
        return self._to_score_result(
            question,
            scoring_mode="single_round",
            scored_json=scored_json,
            token_usage={"total": usage},
        )

    def score_multi_round(self, question: StandardQuestion, templates: PromptTemplateBuilder) -> ScoreResult:
        round1_bundle = templates.build_round1(question)
        round1_json, usage_round1 = self._completion_json(round1_bundle)
        round2_bundle = templates.build_round2(question, round1_json)
        round2_json, usage_round2 = self._completion_json(round2_bundle)
        usage_total = self._sum_usage(usage_round1, usage_round2)
        return self._to_score_result(
            question,
            scoring_mode="multi_round",
            scored_json=round2_json,
            token_usage={
                "round1": usage_round1,
                "round2": usage_round2,
                "total": usage_total,
            },
            round1_json=round1_json,
        )
