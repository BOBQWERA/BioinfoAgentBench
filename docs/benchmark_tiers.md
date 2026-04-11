# Benchmark Tiers

BioinfoAgentBench is organized into three progressive tiers.

## Baseline Tier

The manuscript-level Baseline Tier uses 3,238 public tasks to assess large-scale
reliability. The current repository release contains the standardized public subset
currently packaged for distribution, totaling 486 tasks across these released source
collections:

- AutoBA
- BioChatter
- BioDSBench
- BioDSBench-R
- BioMed-AQA
- Biomni-Eval
- BixBench
- LAB-Bench

## Fingerprint Tier

The manuscript-level Fingerprint Tier uses 300 structurally tuned questions to profile
capability fingerprints across the Planning, Action, Reflection, and Evolution (PARE)
dimensions. The released Fingerprint Tier assets are curated BioMed-AQA upgrade packs
that impose differential PARE loads through edited question variants:

- `biomed_aqa_e1_upgrade_top5`
- `biomed_aqa_e1_upgrade_top5_2`
- `biomed_aqa_e2_upgrade_top5`
- `biomed_aqa_e2_upgrade_top5_2`
- `biomed_aqa_r1_upgrade_top5`
- `biomed_aqa_r1_upgrade_top5_2`
- `biomed_aqa_r2_upgrade_top5`
- `biomed_aqa_r2_upgrade_top5_2`

Each pack contains 5 transformed questions plus supporting reference artifacts.

## Frontier Tier

The manuscript-level Frontier Tier introduces 216 literature-derived scientific
challenges. This release includes Frontier Tier curation metadata and manuscript-facing
results, not the full executable notebook environments. Frontier Tier assets are split
between:

- `benchmarks/frontier/` for Frontier Tier curation metadata
- `paper/sources/` for manuscript support files
- `paper/results/frontier/` for summary outputs used in figures and tables
