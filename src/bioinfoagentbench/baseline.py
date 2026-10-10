"""Checkpoint judgments and Baseline correctness/resource metrics."""

from collections import defaultdict

from .tasks import check_evidence_list, index_records, number, require_text

USAGE_FIELDS = {"input_tokens", "output_tokens", "model_requests", "elapsed_seconds", "cost_usd"}


def validate_usage(usage):
    if not isinstance(usage, dict) or set(usage) - USAGE_FIELDS:
        raise ValueError(f"usage must contain only {sorted(USAGE_FIELDS)}")
    for key, value in usage.items():
        if value is None:
            continue
        number(value, key, minimum=0)
        if key in {"input_tokens", "output_tokens", "model_requests"} and type(value) is not int:
            raise ValueError(f"{key} must be an integer")
    return usage


def score_task(task, judgment, evidence_root):
    """Consume reviewed checkpoints, not an automatically interpreted prose rubric."""
    if judgment.get("task_id") != task["task_id"]:
        raise ValueError("Task ID mismatch")
    require_text(judgment.get("agent"), "Agent")
    if judgment.get("all_rules_reviewed") is not True:
        raise ValueError("Complete rule coverage must be confirmed by the evaluator")
    checks = judgment.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ValueError("At least one checkpoint judgment is required")
    labels = set()
    for check in checks:
        if not isinstance(check, dict):
            raise ValueError("Checkpoint judgments must be objects")
        criterion = require_text(check.get("criterion"), "Checkpoint criterion")
        if criterion in labels:
            raise ValueError(f"Duplicate checkpoint: {criterion}")
        labels.add(criterion)
        if type(check.get("passed")) is not bool:
            raise ValueError("Checkpoint passed must be true or false")
        require_text(check.get("reason"), "Checkpoint reason")
        check_evidence_list(check.get("evidence", []), evidence_root, required=check["passed"])
    usage = validate_usage(judgment.get("usage", {}))
    return {"agent": judgment["agent"], "task_id": task["task_id"],
            "passed": all(check["passed"] for check in checks),
            "all_rules_reviewed": True, "checks": checks, "usage": usage}


def validate_outcomes(tasks, records):
    if not tasks:
        raise ValueError("No tasks selected")
    indexed = index_records(records)
    if set(indexed) != set(index_records(tasks)):
        raise ValueError("Outcomes must cover exactly the selected tasks")
    for row in records:
        if type(row.get("passed")) is not bool:
            raise ValueError("Adjudicated outcomes require a boolean passed field")
        validate_usage(row.get("usage", {}))
    return indexed


def resource_metrics(records):
    """Missing usage stays unavailable; unsuccessful tasks contribute their costs."""
    usage = [validate_usage(row.get("usage", {})) for row in records]
    count = len(records)
    if not count:
        raise ValueError("No records to summarize")
    values = {"tokens": [], "elapsed_seconds": [], "model_requests": [], "cost_usd": []}
    for item in usage:
        if item.get("input_tokens") is not None and item.get("output_tokens") is not None:
            values["tokens"].append(item["input_tokens"] + item["output_tokens"])
        for key in ("elapsed_seconds", "model_requests", "cost_usd"):
            if item.get(key) is not None:
                values[key].append(item[key])
    means = {key: sum(items)/count if len(items) == count else None
             for key, items in values.items()}
    passed = sum(row["passed"] for row in records)
    total_cost = sum(values["cost_usd"]) if len(values["cost_usd"]) == count else None
    return {"B3": means["tokens"],
            "B4": means["elapsed_seconds"]/60 if means["elapsed_seconds"] is not None else None,
            "B5": means["model_requests"], "B6": means["cost_usd"],
            "B7": total_cost/passed if total_cost is not None and passed else None,
            "usage_coverage": {key: len(items) for key, items in values.items()}}


def summarize(tasks, records):
    outcomes = validate_outcomes(tasks, records)
    subjects = defaultdict(list)
    for task in tasks:
        subject = require_text(task.get("subject"), "Task subject")
        subjects[subject].append(outcomes[task["task_id"]]["passed"])
    stratified = {subject: {"passed": sum(values), "evaluated": len(values),
                            "success_rate": sum(values)/len(values)}
                  for subject, values in sorted(subjects.items())}
    passed = sum(row["passed"] for row in records)
    return {"evaluated_tasks": len(tasks), "passed_tasks": passed, "B1": passed/len(tasks),
            "B2": {"by_subject": stratified,
                   "macro_average": sum(x["success_rate"] for x in stratified.values())/len(stratified)},
            **resource_metrics(records)}
