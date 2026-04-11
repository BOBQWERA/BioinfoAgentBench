# Release Scope

This repository is intentionally narrower than the full internal manuscript workspace.

## Included

- Standardized benchmark JSON files under `benchmarks/standardized/`
- Source collection subsets under `benchmarks/source_collections/`
- Fingerprint upgrade packs under `benchmarks/fingerprint/`
- PARE scoring engine and benchmark utilities under `src/bioinfoagentbench/`
- Paper result summaries and committed supplementary assets under `paper/`
- Static PARE visualizer and committed example outputs

## Excluded

- `.env` and any credential-bearing configuration
- large raw task inputs from `data/`
- internal fetch scripts tied to unpublished infrastructure
- supplementary-table rebuild scripts under `scripts/paper/`
- large figure drafts and duplicated workspace artifacts
- temporary rebalance directories and scratch notebooks
- full Frontier notebook environments not present in this workspace snapshot

## Release philosophy

This snapshot is designed to be honest and uploadable:

- every committed directory is meant to be inspectable on GitHub,
- large unpublished or infrastructure-bound assets are not silently referenced as if they
  were bundled,
- and manuscript-facing artifacts are separated from reusable benchmark code.
