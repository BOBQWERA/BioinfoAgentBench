"""Read task collections and prepare agent-visible inputs."""

import json
import math
from pathlib import Path

TIERS = ("baseline", "fingerprint", "frontier")


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_number(value):
    raise ValueError(f"Non-finite JSON number: {value}")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=_object, parse_constant=_invalid_number)


def read_jsonl(path):
    records = []
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line, object_pairs_hook=_object, parse_constant=_invalid_number)
            if not isinstance(row, dict):
                raise ValueError("Each record must be an object")
            records.append(row)
        except ValueError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return records


def index_records(records, key="task_id"):
    result = {}
    for row in records:
        value = row.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing or invalid {key}")
        if value in result:
            raise ValueError(f"Duplicate {key}: {value}")
        result[value] = row
    return result


def load_tasks(benchmarks, tier, *, pilot=False, task_ids=None):
    if tier not in TIERS:
        raise ValueError(f"Unknown tier: {tier}")
    root = Path(benchmarks)
    tasks = read_jsonl(root / tier / "tasks.jsonl")
    index_records(tasks)
    if pilot:
        if tier != "baseline":
            raise ValueError("--pilot selects the Baseline subset only")
        selected = (root / "baseline/pilot_ids.txt").read_text().splitlines()
        if len(selected) != len(set(selected)):
            raise ValueError("Duplicate pilot task IDs")
        if set(selected) - set(index_records(tasks)):
            raise ValueError("Unknown task in pilot_ids.txt")
        tasks = [task for task in tasks if task["task_id"] in selected]
    if task_ids is not None:
        if len(task_ids) != len(set(task_ids)):
            raise ValueError("Duplicate requested task IDs")
        unknown = set(task_ids) - set(index_records(tasks))
        if unknown:
            raise ValueError(f"Task IDs outside the selected cohort: {sorted(unknown)}")
        tasks = [task for task in tasks if task["task_id"] in task_ids]
    if not tasks:
        raise ValueError("No tasks selected")
    return tasks


def resolve_file(root, relative):
    if not isinstance(relative, str) or not relative:
        raise ValueError("A relative file path is required")
    if Path(relative).is_absolute():
        raise ValueError(f"Expected a relative path: {relative}")
    base = Path(root).resolve()
    path = (base / relative).resolve()
    if not path.is_relative_to(base) or not path.is_file():
        raise ValueError(f"File is missing or outside the supplied root: {relative}")
    return path


def agent_input(task, tier, benchmarks):
    """Export a whitelist of fields; evaluation references stay with the evaluator."""
    if tier == "frontier":
        instruction = resolve_file(benchmarks, task["agent_task"]).read_text(encoding="utf-8")
        for path in task["input_files"]:
            resolve_file(benchmarks, path)
        return {"task_id": task["task_id"], "instruction": instruction,
                "input_files": task["input_files"]}
    return {key: task[key] for key in
            ("task_id", "instruction", "input_context", "deliverable_specification")}


def group_records(tasks, records):
    """Require each represented agent to cover exactly the selected task cohort."""
    expected = set(index_records(tasks))
    groups = {}
    for row in records:
        agent = row.get("agent")
        if not isinstance(agent, str) or not agent.strip():
            raise ValueError("Every record needs an agent name")
        groups.setdefault(agent, []).append(row)
    if not groups:
        raise ValueError("No evaluation records supplied")
    for agent, rows in groups.items():
        observed = set(index_records(rows))
        if observed != expected:
            raise ValueError(f"{agent}: cohort mismatch; missing={sorted(expected-observed)}, "
                             f"unexpected={sorted(observed-expected)}")
    return groups


def number(value, name, *, minimum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def require_text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")
    return value


def check_evidence(ref, root, *, require_quote=False):
    """Validate an evidence path and its locator or verbatim quote."""
    if not isinstance(ref, dict):
        raise ValueError("Evidence must be an object")
    path = resolve_file(root, ref.get("path"))
    quote = ref.get("quote")
    if quote is not None:
        require_text(quote, "Evidence quote")
        if quote not in path.read_text(encoding="utf-8"):
            raise ValueError(f"Evidence quote not found in {ref['path']}")
    elif require_quote:
        raise ValueError("A verbatim execution quote is required")
    else:
        require_text(ref.get("locator"), "Evidence locator")
    return ref


def check_evidence_list(refs, root, *, required=False):
    if not isinstance(refs, list) or (required and not refs):
        raise ValueError("An evidence list is required")
    return [check_evidence(ref, root) for ref in refs]
