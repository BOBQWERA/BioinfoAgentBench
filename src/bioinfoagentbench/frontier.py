"""Frontier rubric arithmetic and numerical anchor comparisons."""

import math
import re
from decimal import Decimal

from .tasks import check_evidence, check_evidence_list, index_records, number, require_text

F1_ITEMS = ("explicit_objective", "justified_steps", "validity_checks", "anchored_conclusions")
ATTRIBUTIONS = {"Q_different", "D_different", "M_different", "unanswered"}
NUMBER = re.compile(
    r"(?<![\w.])[-+−]?(?:(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|\.\d+)"
    r"(?:(?:[eE][-+]?\d+)|(?:\s*(?:×|\\times)\s*10\s*\^\s*\{?[-+−]?\d+\}?))?"
    r"(?!\w|\.\d)"
)


def _interval(values, name):
    if not isinstance(values, (list, tuple)) or len(values) != 2:
        raise ValueError(f"{name} must contain two bounds")
    if values == [None, None] or values == (None, None):
        return None
    lo, hi = (number(value, name) for value in values)
    if lo > hi:
        raise ValueError(f"Reversed {name}")
    return Decimal(str(lo)), Decimal(str(hi))


def _reference(anchor):
    reference = Decimal(str(number(anchor["reference_value"], "Reference value")))
    weight = number(anchor["weight"], "Anchor weight", minimum=0)
    if not weight:
        raise ValueError("Anchor weights must be positive")
    interval = _interval([anchor["ci_lower"], anchor["ci_upper"]], "Reference interval")
    tolerance = anchor["tolerance_absolute"]
    if tolerance is not None:
        tolerance = Decimal(str(number(tolerance, "Tolerance", minimum=0)))
    return reference, interval, tolerance


def score_anchor(anchor, estimate, *, null_value=None, agent_ci=None):
    """Pure arithmetic; callers must establish execution evidence and comparability."""
    reference, interval, tolerance = _reference(anchor)
    value = Decimal(str(number(estimate, "Estimate")))
    ci = _interval(agent_ci, "Agent interval") if agent_ci is not None else None
    if anchor["kind"] == "sample_size":
        if value == reference:
            return 1.0
        return 2/3 if abs(value-reference) <= abs(reference)*Decimal("0.05") else 0.0
    if type(null_value) not in (int, float) or null_value not in (0, 1):
        raise ValueError("Non-sample anchors require null_value=0 or 1")
    null = Decimal(str(null_value))
    same_direction = ((value > null and reference > null) or
                      (value < null and reference < null) or value == reference == null)
    score = 1/3 if same_direction else 0.0
    if same_direction and tolerance is not None and abs(value-reference) <= tolerance:
        score = 2/3
    # The fixed protocol evaluates reference-CI containment independently of direction.
    if interval is not None and interval[0] <= value <= interval[1]:
        score = 1.0
        if ci is not None and ci[1]-ci[0] > 2*(interval[1]-interval[0]):
            score = 2/3
    return score


def _quote_has(value, quote):
    for match in NUMBER.finditer(quote):
        token = match.group().replace(",", "").replace("−", "-")
        token = re.sub(r"\s*(?:×|\\times)\s*10\s*\^\s*\{?([-+]?\d+)\}?", r"e\1", token)
        observed = float(Decimal(token))
        if math.isfinite(observed) and math.isclose(value, observed, rel_tol=1e-12, abs_tol=0):
            return True
    return False


def _numerical_evidence(values, ref, root):
    check_evidence(ref, root, require_quote=True)
    for value in values:
        if not _quote_has(value, ref["quote"]):
            raise ValueError(f"Estimate or interval bound absent from execution quote: {value}")


def _rubric_item(item, root):
    if not isinstance(item, dict):
        raise ValueError("Rubric items must be objects")
    score = number(item.get("score"), "Rubric score")
    if score not in (0, 0.5, 1):
        raise ValueError("Rubric score must be 0, 0.5 or 1")
    require_text(item.get("reason"), "Rubric reason")
    check_evidence_list(item.get("evidence", []), root, required=score > 0)
    return score


def score_case(task, anchors, judgment, evidence_root):
    if judgment.get("task_id") != task["task_id"]:
        raise ValueError("Task ID mismatch")
    require_text(judgment.get("agent"), "Agent")
    canonical = index_records(anchors, "anchor_id")
    if not canonical:
        raise ValueError("No reference anchors")
    supplied = index_records(judgment.get("f2", []), "anchor_id")
    if set(supplied) - set(canonical):
        raise ValueError("Unknown anchor IDs")
    anchor_scores = []
    for anchor_id, anchor in canonical.items():
        _reference(anchor)
        item = supplied.get(anchor_id)
        score, estimate, verified_ci = 0.0, None, None
        if item is not None and item.get("estimate") is not None:
            estimate = number(item["estimate"], "Estimate")
        if item is not None and item.get("computed") is True and item.get("same_estimand") is True:
            estimate = number(item.get("estimate"), "Estimate")
            _numerical_evidence([estimate], item.get("evidence"), evidence_root)
            if item.get("ci") is not None:
                _interval(item["ci"], "Agent interval")
                if item.get("ci_computed") is True:
                    _numerical_evidence(item["ci"], item.get("ci_evidence"), evidence_root)
                    verified_ci = item["ci"]
            score = score_anchor(anchor, estimate, null_value=item.get("null_value"), agent_ci=verified_ci)
        attribution = None
        if score < 2/3:
            attribution = item.get("attribution") if item is not None else "unanswered"
            if attribution not in ATTRIBUTIONS:
                raise ValueError(f"{anchor_id}: a low score requires a mismatch attribution")
        anchor_scores.append({"anchor_id": anchor_id, "weight": anchor["weight"],
                              "reference_value": anchor["reference_value"], "estimate": estimate,
                              "score": score, "verified_ci": verified_ci,
                              "attribution": attribution, "judgment": item})
    f1 = judgment.get("f1")
    if not isinstance(f1, dict) or set(f1) != set(F1_ITEMS):
        raise ValueError(f"F1 must contain exactly {F1_ITEMS}")
    f1_score = sum(_rubric_item(f1[key], evidence_root) for key in F1_ITEMS)/4
    f3 = judgment.get("f3", [])
    if not isinstance(f3, list) or len(f3) > 3:
        raise ValueError("F3 accepts at most three designated findings in report order")
    f3_score = 0
    for item in f3:
        score = _rubric_item(item, evidence_root)
        require_text(item.get("claim"), "Additional finding")
        if score:
            if (item.get("computed") is not True or item.get("covered_by_reference") is not False
                    or item.get("implied_by_background") is not False):
                raise ValueError("Positive F3 needs executed evidence and confirmed novelty against references/background")
        f3_score += score
    return {"agent": judgment["agent"], "task_id": task["task_id"],
            "F1": f1_score,
            "F2": sum(item["weight"]*item["score"] for item in anchor_scores)/sum(a["weight"] for a in anchors),
            "F3": f3_score/3, "f1": f1, "f2": anchor_scores, "f3": f3}


def summarize(tasks, records):
    if not tasks:
        raise ValueError("No cases selected")
    if set(index_records(tasks)) != set(index_records(records)):
        raise ValueError("Case scores must cover exactly the selected cases")
    for row in records:
        for key in ("F1", "F2", "F3"):
            if not 0 <= number(row.get(key), key) <= 1:
                raise ValueError(f"{key} must be between 0 and 1")
    return {"evaluated_cases": len(tasks),
            **{key: sum(row[key] for row in records)/len(tasks) for key in ("F1", "F2", "F3")}}
