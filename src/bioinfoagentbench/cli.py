"""Command-line task export, judgment scoring and metric aggregation."""

import argparse
import json
import sys
from pathlib import Path

from . import baseline, fingerprint, frontier
from .tasks import (TIERS, agent_input, group_records, index_records, load_tasks,
                    read_json, read_jsonl, resolve_file)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="bioinfoagentbench")
    parser.add_argument("--benchmarks", type=Path, default=Path("benchmarks"))
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in [("tasks", "Export agent-visible task inputs"),
                            ("score", "Score checkpoint or Frontier judgments"),
                            ("summarize", "Aggregate previously adjudicated results")]:
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--tier", choices=TIERS, required=True)
        command.add_argument("--pilot", action="store_true", help="Select the Baseline pilot subset")
        command.add_argument("--task-id", action="append", dest="task_ids")
        command.add_argument("--output", type=Path, help="Default: standard output")
        if name != "tasks":
            command.add_argument("--records", type=Path, required=True)
        if name == "score":
            command.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        tasks = load_tasks(args.benchmarks, args.tier, pilot=args.pilot, task_ids=args.task_ids)
        if args.command == "tasks":
            result = [agent_input(task, args.tier, args.benchmarks) for task in tasks]
        else:
            records = read_jsonl(args.records)
            groups = group_records(tasks, records)
            if args.command == "score":
                if not args.evidence_root.is_dir():
                    raise ValueError("--evidence-root must be an existing directory")
                result = []
                for agent_records in groups.values():
                    judgments = index_records(agent_records)
                    for task in tasks:
                        judgment = judgments[task["task_id"]]
                        if args.tier == "frontier":
                            path = resolve_file(args.benchmarks, task["evaluation_directory"]+"/anchors.json")
                            result.append(frontier.score_case(task, read_json(path), judgment, args.evidence_root))
                        else:
                            result.append(baseline.score_task(task, judgment, args.evidence_root))
            else:
                result = {}
                loads = read_jsonl(args.benchmarks/"fingerprint/loads.jsonl") if args.tier == "fingerprint" else None
                for agent, agent_records in groups.items():
                    if args.tier == "fingerprint":
                        summary = fingerprint.summarize(tasks, agent_records, loads)
                    elif args.tier == "frontier":
                        summary = frontier.summarize(tasks, agent_records)
                    else:
                        summary = baseline.summarize(tasks, agent_records)
                    result[agent] = summary
        if args.command == "summarize":
            output = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n"
        else:
            output = "".join(json.dumps(row, ensure_ascii=False, allow_nan=False)+"\n" for row in result)
        if args.output:
            protected = [args.records.resolve()] if args.command != "tasks" else []
            target = args.output.resolve()
            if target.is_relative_to(args.benchmarks.resolve()) or target in protected:
                raise ValueError("Choose an output outside the task collection and input records")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
