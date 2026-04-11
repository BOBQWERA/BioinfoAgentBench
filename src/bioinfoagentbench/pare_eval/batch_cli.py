from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APITimeoutError

from bioinfoagentbench.pare_eval.loader import StandardQuestionImporter
from bioinfoagentbench.pare_eval.prompts import PromptTemplateBuilder
from bioinfoagentbench.pare_eval.scorer import GPT41Scorer
from bioinfoagentbench.pare_eval.storage import ScoreStore
from bioinfoagentbench.paths import output_dir, standardized_benchmarks_dir, templates_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Batch PARE scoring for all benchmarks or selected benchmarks.")
    parser.add_argument(
        "--bench",
        nargs="*",
        default=None,
        help="Optional benchmark names. If omitted, run all *.json under standardized dir.",
    )
    parser.add_argument(
        "--standardized-dir",
        default=str(standardized_benchmarks_dir()),
        help="Path to standardized benchmark json directory",
    )
    parser.add_argument(
        "--output-dir",
        default=str(output_dir()),
        help="Output root for persisted scores",
    )
    parser.add_argument("--model", default="gpt-4.1", help="Model name")
    parser.add_argument(
        "--base-url",
        default=None,
        help="Optional OpenAI-compatible base URL. Overrides OPENAI_BASE_URL if provided.",
    )
    parser.add_argument("--timeout", type=float, default=120.0, help="HTTP timeout in seconds")
    parser.add_argument("--max-retries", type=int, default=5, help="Max retries for transient failures")
    parser.add_argument(
        "--dotenv",
        default=".env",
        help="Path to .env file. Set to empty string to disable dotenv loading.",
    )
    parser.add_argument("--multi-round", action="store_true", help="Use two-round scoring workflow")
    parser.add_argument("--dry-run", action="store_true", help="Do not call model; only persist prompt payloads")
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop immediately on first failed record. Default: continue and report failures.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.dotenv:
        load_dotenv(dotenv_path=args.dotenv, override=False)

    importer = StandardQuestionImporter(Path(args.standardized_dir))
    benches = args.bench if args.bench else importer.list_benchmarks()
    templates = PromptTemplateBuilder(templates_dir())
    store = ScoreStore(Path(args.output_dir))

    scorer: GPT41Scorer | None = None
    if not args.dry_run:
        scorer = GPT41Scorer(
            model=args.model,
            base_url=args.base_url,
            timeout_sec=args.timeout,
            max_retries=args.max_retries,
        )

    total = 0
    success = 0
    failures: list[tuple[str, str, str]] = []

    for bench in benches:
        payload = importer.load_benchmark_json(bench)
        records = payload.get("records", [])
        print(f"[BENCH] {bench}: {len(records)} records")

        for i, record in enumerate(records):
            total += 1
            record_id = record["id"]
            try:
                question = importer.get_question(bench, record_id=record_id)
                if args.dry_run:
                    if args.multi_round:
                        round1 = templates.build_round1(question)
                        round2 = templates.build_round2(
                            question,
                            {"subdimension_evidence": {}, "dimension_evidence": {}, "ambiguities": [], "missing_information": [], "notes": ""},
                        )
                        store.persist_dry_run(
                            question,
                            mode="multi_round",
                            prompts={
                                "round1": {"system": round1.system, "user": round1.user},
                                "round2_template": {"system": round2.system, "user": round2.user},
                            },
                        )
                    else:
                        single = templates.build_single_round(question)
                        store.persist_dry_run(
                            question,
                            mode="single_round",
                            prompts={"single_round": {"system": single.system, "user": single.user}},
                        )
                else:
                    assert scorer is not None
                    if args.multi_round:
                        result = scorer.score_multi_round(question, templates)
                    else:
                        result = scorer.score_single_round(question, templates)
                    store.persist(question, result)
                success += 1
                print(f"  [{i+1}/{len(records)}] OK {record_id}")
            except (APITimeoutError, APIConnectionError, FileNotFoundError, KeyError, ValueError, IndexError) as exc:
                failures.append((bench, record_id, str(exc)))
                print(f"  [{i+1}/{len(records)}] FAIL {record_id}: {exc}")
                if args.stop_on_error:
                    break
        if args.stop_on_error and failures:
            break

    print(f"[DONE] total={total}, success={success}, failed={len(failures)}")
    if failures:
        print("[FAILED RECORDS]")
        for bench, record_id, err in failures:
            print(f"- {bench}::{record_id} -> {err}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
