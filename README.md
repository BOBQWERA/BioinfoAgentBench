# BioinfoAgentBench

BioinfoAgentBench is a unified black-box evaluation framework for heterogeneous bioinformatics agents. It is organized into three progressive tiers: the Baseline Tier uses large-scale standardized public tasks to assess end-to-end reliability, the Fingerprint Tier uses structurally tuned questions to construct capability fingerprints across the Planning, Action, Reflection, and Evolution (PARE) dimensions, and the Frontier Tier introduces literature-derived scientific challenges to evaluate the gap between workflow reproduction and open-ended scientific discovery.

This repository packages the public benchmark assets, evaluation code, example outputs, and manuscript-facing release materials needed to inspect the framework and reproduce the released evaluation bundle.

## Framework Overview

![BioinfoAgentBench framework overview](docs/figure1.png)

See the manuscript version in [Figure 1 (PDF)](paper/supplementary/Figure_1.pdf).

## What this repository contains

- `benchmarks/`: standardized benchmark JSON files, source collection subsets, and curated fingerprint upgrade packs.
- `src/bioinfoagentbench/`: PARE evaluation utilities plus benchmark standardization, validation, and manifest utilities.
- `paper/`: source spreadsheets and CSV files, result summaries, and committed supplementary tables and figures.
- `tools/pare_visualizer/`: static viewer for committed PARE capability fingerprints and example outputs.
- `examples/pare_outputs/`: example scoring outputs used by the visualizer.

This release includes standalone Python source code. No compiled binary is required.
It also includes small public benchmark subsets and committed example outputs that can
be used to inspect and demo the software without downloading the full internal
manuscript workspace.

## Important Release Scope Note

The manuscript describes a 3,238-task Baseline Tier. This public repository release does not contain that full raw corpus. It contains the currently shareable subset packaged in this release:

- 486 standardized Baseline Tier tasks across 8 released source collections
- 8 Fingerprint Tier upgrade packs, each with 5 transformed BioMed-AQA questions
- frontier curation tables, supplementary results, and pilot metadata

## Quick start

### System requirements

- Operating systems: macOS 14 or newer, Ubuntu 22.04/24.04 LTS, or Windows 11 with PowerShell.
- Python: 3.10 or newer. The package metadata requires Python `>=3.10`.
- Required Python packages: `openai>=1.40.0`, `python-dotenv>=1.0.1`,
  `openpyxl>=3.1.0`, and `pandas>=2.0.0`.
- Development and validation packages: `pytest>=8.0.0` and `ruff>=0.6.0`,
  installed through the `dev` extra.
- Tested software versions for this release: Python 3.10, 3.11, and 3.12 with the
  dependency versions listed above.
- Non-standard hardware: none. The validation tools, dry-run demo, and static
  visualizer are CPU-only and run on a normal laptop or desktop. Live PARE scoring
  requires network access to an OpenAI or OpenAI-compatible API endpoint.

### Installation guide

```bash
python -m venv .venv
```

Activate the environment on macOS / Linux:

```bash
source .venv/bin/activate
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install and validate:

```bash
pip install -e .[dev]
pytest
biab-validate
```

Typical install time on a normal desktop computer is 3-5 minutes with a fresh Python
environment and stable internet access. If Python wheels are already cached, the
editable install is usually under 1 minute.

### Demo

Run a single PARE scoring job:

```bash
pare-eval --bench biodsbench --record-id biodsbench_28481359_0 --dry-run
```

This demo uses the bundled `benchmarks/standardized/biodsbench.json` data and does
not call an external model because `--dry-run` is set. Expected output is a message
similar to:

```text
[DRY-RUN] Prompt payload persisted: outputs/pare_eval/biodsbench/biodsbench_28481359_0.dry_run_prompts.json
```

The expected runtime for this dry-run demo on a normal desktop computer is less than
10 seconds after installation. The generated JSON contains the standardized question
payload and the prompt text that would be sent to the scorer.

Batch-score one or more benchmarks:

```bash
pare-eval-batch --bench autoba biochatter --dry-run
```

Expected batch dry-run output reports each processed record and ends with a summary
similar to:

```text
[DONE] total=<record_count>, success=<record_count>, failed=0
```

The expected runtime for the `autoba biochatter` dry-run batch is about 1-3 minutes
on a normal desktop computer. Live scoring without `--dry-run` depends on API
latency, model throughput, retry settings, and the number of records scored.

Regenerate the benchmark manifest:

```bash
biab-manifest
```

Launch the visualizer locally:

```bash
cd tools/pare_visualizer
python -m http.server 8090
```

Then open `http://127.0.0.1:8090`.

### Instructions for use on your own data

BioinfoAgentBench scoring utilities expect standardized benchmark JSON files. Each
file should follow the schema documented in
[`benchmarks/standardized/SCHEMA.md`](benchmarks/standardized/SCHEMA.md) and contain
top-level `benchmark`, `schema_version`, `count`, and `records` fields. Each record
must include `id`, `question`, `data`, `answer`, `has_file`, and `metadata`.

To score your own benchmark:

1. Create a standardized JSON file, for example `my_benchmark.json`.
2. Put it in `benchmarks/standardized/`, or keep it in another directory and pass
   that directory with `--standardized-dir`.
3. Validate the file:

   ```bash
   biab-validate --directory benchmarks/standardized
   ```

4. Run a dry-run prompt generation pass:

   ```bash
   pare-eval --bench my_benchmark --record-id my_record_id --dry-run
   ```

5. For live model scoring, set `OPENAI_API_KEY` in the environment or in `.env`,
   optionally pass `--base-url` for an OpenAI-compatible endpoint, and omit
   `--dry-run`:

   ```bash
   pare-eval --bench my_benchmark --record-id my_record_id --model gpt-4.1
   ```

Live scoring writes per-record JSON snapshots and appends summary rows to
`outputs/pare_eval/<benchmark>/scores.jsonl`. Local output directories are ignored by
Git.

### Reproduction instructions

The public repository is narrower than the internal manuscript workspace, but the
released evaluation bundle can be reproduced and checked with the committed assets:

```bash
pip install -e .[dev]
pytest
biab-validate
biab-manifest --output benchmarks/manifest.json
python tools/pare_visualizer/scripts/build_scores_index.py
```

The resulting benchmark manifest summarizes the bundled standardized datasets. The
visualizer index is rebuilt from `examples/pare_outputs/`, which contains committed
example PARE scoring outputs.

## License

The BioinfoAgentBench source code is released under the MIT License. Source benchmark
data, literature-derived resources, and third-party metadata remain subject to the
terms and licenses of their original providers.

## Repository layout

- [benchmarks/README.md](benchmarks/README.md)
- [docs/benchmark_tiers.md](docs/benchmark_tiers.md)
- [paper/README.md](paper/README.md)
- [tools/pare_visualizer/README.md](tools/pare_visualizer/README.md)
