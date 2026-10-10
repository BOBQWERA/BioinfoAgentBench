"""Capability-weighted success using fixed, calibrated task loads."""

from .baseline import resource_metrics, validate_outcomes
from .tasks import index_records

DIMENSIONS = ("P1", "P2", "A1", "A2", "R1", "R2", "E1", "E2")
AXES = {"P": ("P1", "P2"), "A": ("A1", "A2"),
        "R": ("R1", "R2"), "E": ("E1", "E2")}


def summarize(tasks, records, loads):
    outcomes = validate_outcomes(tasks, records)
    load_index = index_records(loads)
    weighted_pass = {key: 0 for key in (*DIMENSIONS, *AXES)}
    total_load = dict(weighted_pass)
    for task in tasks:
        task_id = task["task_id"]
        if task_id not in load_index:
            raise ValueError(f"Missing loads for {task_id}")
        weights = load_index[task_id].get("loads_used")
        if not isinstance(weights, dict) or set(weights) != set(DIMENSIONS):
            raise ValueError(f"{task_id}: loads_used must contain P1–E2 exactly")
        if any(type(value) is not int or not 0 <= value <= 5 for value in weights.values()):
            raise ValueError(f"{task_id}: loads must be integers from 0 to 5")
        weights = {**weights, **{axis: max(weights[a], weights[b]) for axis, (a, b) in AXES.items()}}
        for key, weight in weights.items():
            total_load[key] += weight
            weighted_pass[key] += weight * outcomes[task_id]["passed"]
    scores = {key: weighted_pass[key]/weight if weight else None for key, weight in total_load.items()}
    passed = sum(row["passed"] for row in records)
    return {"evaluated_tasks": len(tasks), "passed_tasks": passed,
            "success_rate": passed/len(tasks),
            "subdimensions": {key: scores[key] for key in DIMENSIONS},
            "dimensions": {key: scores[key] for key in AXES},
            "weighted_pass": weighted_pass, "total_load": total_load,
            **resource_metrics(records)}
