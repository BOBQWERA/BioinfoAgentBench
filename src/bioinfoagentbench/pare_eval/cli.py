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
    parser = argparse.ArgumentParser(description="PARE scoring for standardized benchmark questions.")
    parser.add_argument("--bench", required=True, help="Benchmark name, e.g. biodsbench/autoba/labbench")
    parser.add_argument("--record-id", help="Record id to score")
    parser.add_argument("--index", type=int, help="Record index to score (0-based)")
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
        "--mode",
        choices=["single_round", "multi_round"],
        default="single_round",
        help="Scoring mode. `--multi-round` is still supported for backward compatibility.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Optional OpenAI-compatible base URL. Overrides OPENAI_BASE_URL if provided.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="HTTP timeout in seconds for OpenAI API requests.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Max retries for transient OpenAI API failures.",
    )
    parser.add_argument(
        "--dotenv",
        default=".env",
        help="Path to .env file. Set to empty string to disable dotenv loading.",
    )
    parser.add_argument("--multi-round", action="store_true", help="Use two-round scoring workflow")
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="When scoring a whole bench, continue processing even if one record fails.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call model; only materialize prompt payloads into output dir",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.dotenv:
        load_dotenv(dotenv_path=args.dotenv, override=False)

    if args.record_id is not None and args.index is not None:
        raise SystemExit("Please provide only one of --record-id or --index.")

    importer = StandardQuestionImporter(Path(args.standardized_dir))
    templates = PromptTemplateBuilder(templates_dir())
    store = ScoreStore(Path(args.output_dir))
    is_multi_round = args.multi_round or args.mode == "multi_round"
    scorer = None
    if not args.dry_run:
        scorer = GPT41Scorer(
            model=args.model,
            base_url=args.base_url,
            timeout_sec=args.timeout,
            max_retries=args.max_retries,
        )

    def _run_one(question) -> None:
        if args.dry_run:
            if is_multi_round:
                round1 = templates.build_round1(question)
                round2 = templates.build_round2(
                    question,
                    {"subdimension_evidence": {}, "dimension_evidence": {}, "ambiguities": [], "missing_information": [], "notes": ""},
                )
                path = store.persist_dry_run(
                    question,
                    mode="multi_round",
                    prompts={
                        "round1": {"system": round1.system, "user": round1.user},
                        "round2_template": {"system": round2.system, "user": round2.user},
                    },
                )
            else:
                single = templates.build_single_round(question)
                path = store.persist_dry_run(
                    question,
                    mode="single_round",
                    prompts={"single_round": {"system": single.system, "user": single.user}},
                )
            print(f"[DRY-RUN] Prompt payload persisted: {path}")
            return

        try:
            assert scorer is not None
            if is_multi_round:
                result = scorer.score_multi_round(question, templates)
            else:
                result = scorer.score_single_round(question, templates)
        except APITimeoutError as exc:
            raise SystemExit(
                "OpenAI request timed out during TLS/HTTP phase. "
                "Check network stability or increase --timeout (e.g. 120) and --max-retries."
            ) from exc
        except APIConnectionError as exc:
            raise SystemExit(
                "OpenAI connection failed. Verify --base-url/OPENAI_BASE_URL and outbound network access."
            ) from exc
        saved = store.persist(question, result)
        print(f"Scored and persisted: {saved}")

    # Single-record mode
    if args.record_id is not None or args.index is not None:
        question = importer.get_question(args.bench, record_id=args.record_id, index=args.index)
        _run_one(question)
        return

    # Whole-bench mode (no record selector provided)
    payload = importer.load_benchmark_json(args.bench)
    records = payload.get("records", [])
    print(f"[BENCH] {args.bench}: {len(records)} records, mode={'multi_round' if is_multi_round else 'single_round'}")
    failures: list[tuple[str, str]] = []
    for i, record in enumerate(records):
        rid = record.get("id", f"index_{i}")
        print(f"[{i+1}/{len(records)}] {rid}")
        try:
            question = importer.get_question(args.bench, record_id=rid)
            _run_one(question)
        except Exception as exc:
            failures.append((rid, str(exc)))
            print(f"  FAIL: {exc}")
            if not args.continue_on_error:
                raise

    if failures:
        print(f"[DONE] failed={len(failures)}")
        for rid, msg in failures:
            print(f"- {rid}: {msg}")
        raise SystemExit(1)
    print("[DONE] all records processed.")


if __name__ == "__main__":
    main()
