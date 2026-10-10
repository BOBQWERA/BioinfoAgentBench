# Felzartamab and the molecular phenotype of antibody-mediated kidney-transplant rejection

## Scientific question

In kidney-transplant recipients with late active or chronic active antibody-mediated rejection (ABMR), how does 20 weeks of felzartamab treatment, compared with placebo, affect the evolution of biopsy molecular phenotypes from baseline to weeks 24 and 52? What are the direction, magnitude and persistence of these effects?

## Background

ABMR is an important cause of late kidney-allograft loss. Active disease may involve microvascular inflammation, natural-killer (NK)-cell-related transcription and interferon-gamma responses; endothelial and renal-parenchymal injury changes may emerge as disease progresses. Established expression classifiers and pathogenesis-based transcript sets represent these processes as continuous scores, but disease activity, chronic stage and tissue composition may not evolve together within a recipient.

Felzartamab is a monoclonal antibody targeting CD38. These data come from an exploratory randomized, double-blind, placebo-controlled trial: participants received nine intravenous doses over 20 weeks and were then followed through week 52. Before these molecular data were generated, the clinical-stage study had reported reduced histological ABMR activity at week 24 and suggested partial recurrence after treatment withdrawal. Effects on the biopsy transcriptome, distinct immune molecular phenotypes and subsequent parenchymal-injury trajectories remain to be determined from these data.

This is a small exploratory study. Randomization occurred at participant level, recipients have repeated biopsies, and visits and tissue composition vary. These are properties of the data, not prescribed analytical methods.

## Data

All available inputs are in `data/`:

- `sample_metadata.csv`
- `molecular_scores.csv`
- `expression_log2.csv.gz`
- `feature_annotation.csv.gz`
- `README.md` and `data_dictionary.csv`

Read `data/README.md` before analysis. There is no training/test split or predefined objective function. Choose estimands, sample handling, statistical scales and uncertainty assessments that address the scientific question.

## Submission

Submit a report and reproducible code:

1. Present the report as a list of claims, each with a statement, direction, point estimate and uncertainty.
2. Separately list up to three extension findings, each with the same elements.
3. Provide a single code entry point callable from the case root. It must read `data/` and generate the numerical results or tables cited in the report, allowing every reported value to be checked against execution outputs.
