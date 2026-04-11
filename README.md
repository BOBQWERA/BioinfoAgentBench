# BioinfoAgentBench

BioinfoAgentBench is a black-box benchmarking framework for heterogeneous bioinformatics
agents. This repository snapshot is organized for GitHub release and manuscript support:
it separates benchmark assets, PARE scoring code, example outputs, and frontier curation
metadata into a clean, reviewable structure.

## What this snapshot contains

- `benchmarks/`: standardized benchmark JSON files, source collection subsets, and
  curated fingerprint upgrade packs.
- `src/bioinfoagentbench/`: PARE scoring engine plus benchmark standardization,
  validation, and manifest utilities.
- `paper/`: source spreadsheets and CSV files, result summaries, and generated
  supplementary tables and figures.
- `tools/pare_visualizer/`: static viewer for committed example PARE outputs.
- `examples/pare_outputs/`: example scoring outputs used by the visualizer.

## Important scope note

The manuscript describes a 3,238-task Baseline Tier. The current workspace snapshot does
not contain that full raw corpus. It contains the curated public subset available in this
workspace:

- 486 standardized baseline/fingerprint-ready records across 8 benchmark sources
- 8 fingerprint upgrade packs, each with 5 transformed BioMed-AQA records
- frontier curation tables, supplementary results, and pilot metadata

See [RELEASE_SCOPE.md](RELEASE_SCOPE.md) for the exact release boundary.

## Quick start

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -e .[dev]
pytest
biab-validate
```

Run a single PARE scoring job:

```bash
pare-eval --bench biodsbench --record-id biodsbench_28481359_0 --dry-run
```

Batch-score one or more benchmarks:

```bash
pare-eval-batch --bench autoba biochatter --dry-run
```

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

## Online visualizer

The repository includes a GitHub Pages workflow at
`.github/workflows/deploy-visualizer.yml`. After pushing the repository to GitHub:

1. Open `Settings -> Pages`.
2. Set `Source` to `GitHub Actions`.
3. Push to `main` or manually run the `Deploy PARE Visualizer` workflow from `Actions`.

The workflow rebuilds `tools/pare_visualizer/data/scores_index.json` from
`examples/pare_outputs/` and publishes `tools/pare_visualizer/` as a static site.

## Repository layout

- [benchmarks/README.md](benchmarks/README.md)
- [docs/benchmark_tiers.md](docs/benchmark_tiers.md)
- [paper/README.md](paper/README.md)
- [tools/pare_visualizer/README.md](tools/pare_visualizer/README.md)

## Citation

Citation metadata is in [CITATION.cff](CITATION.cff). Replace the placeholder GitHub URL
before public release.
