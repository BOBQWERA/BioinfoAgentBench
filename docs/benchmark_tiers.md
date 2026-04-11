# Benchmark Tiers

BioinfoAgentBench is organized around three benchmark layers.

## Baseline Tier

The manuscript-level design targets 3,238 public tasks spanning multiple benchmark
sources. The current repository snapshot contains the standardized public subset present
in this workspace, totaling 486 records across:

- AutoBA
- BioChatter
- BioDSBench
- BioDSBench-R
- BioMed-AQA
- Biomni-Eval1
- BixBench
- LAB-Bench

## Fingerprint Tier

The fingerprint assets in this snapshot are curated BioMed-AQA upgrade packs that probe
PARE subdimensions through edited question variants:

- `biomed_aqa_e1_upgrade_top5`
- `biomed_aqa_e1_upgrade_top5_2`
- `biomed_aqa_e2_upgrade_top5`
- `biomed_aqa_e2_upgrade_top5_2`
- `biomed_aqa_r1_upgrade_top5`
- `biomed_aqa_r1_upgrade_top5_2`
- `biomed_aqa_r2_upgrade_top5`
- `biomed_aqa_r2_upgrade_top5_2`

Each pack contains 5 transformed records plus supporting snapshots.

## Frontier Tier

This snapshot includes frontier curation metadata and manuscript-facing results, not the
full notebook execution environments. Frontier assets are split between:

- `benchmarks/frontier/` for release-friendly metadata
- `paper/sources/` for manuscript support files
- `paper/results/frontier/` for summary outputs used in figures and tables
