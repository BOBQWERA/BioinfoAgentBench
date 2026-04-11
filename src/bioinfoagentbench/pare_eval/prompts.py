from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from bioinfoagentbench.pare_eval.models import StandardQuestion


@dataclass
class PromptBundle:
    system: str
    user: str


class PromptTemplateBuilder:
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir

    def _load(self, name: str) -> str:
        path = self.template_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Prompt template not found: {path}")
        return path.read_text(encoding="utf-8")

    def build_single_round(self, question: StandardQuestion) -> PromptBundle:
        system = self._load("system_single_round.txt")
        user = json.dumps(question.to_payload(), ensure_ascii=False, indent=2)
        return PromptBundle(system=system, user=user)

    def build_round1(self, question: StandardQuestion) -> PromptBundle:
        system = self._load("system_round1_analysis.txt")
        user = json.dumps(question.to_payload(), ensure_ascii=False, indent=2)
        return PromptBundle(system=system, user=user)

    def build_round2(self, question: StandardQuestion, round1_json: dict) -> PromptBundle:
        system = self._load("system_round2_scoring.txt")
        merged = {
            "question_payload": question.to_payload(),
            "round1_analysis": round1_json,
        }
        user = json.dumps(merged, ensure_ascii=False, indent=2)
        return PromptBundle(system=system, user=user)
