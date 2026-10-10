# Peripheral blood mononuclear cell respiration and glaucomatous visual-field progression

## Scientific question

Among patients with primary open-angle glaucoma receiving standard intraocular-pressure-lowering treatment, is mitochondrial respiration in peripheral blood mononuclear cells associated with long-term change in visual-field mean deviation, and what are the direction and magnitude of the association?

## Background

Glaucoma is a progressive optic neuropathy. Mean deviation (MD) from standard automated perimetry summarizes visual-field function; increasingly negative values indicate worsening over time. Intraocular pressure and age are established factors associated with progression. Lowering intraocular pressure slows visual-field loss, but some patients continue to progress despite treatment.

Before this study was published, patient samples, animal models and ex vivo studies had implicated mitochondrial bioenergetic changes in glaucoma susceptibility. Peripheral blood mononuclear cells can be used to measure systemic mitochondrial respiration. Oxygen consumption rate (OCR) can be separated into basal respiration, ATP-linked respiration, maximal respiration and reserve capacity, among other measures. However, the relationship between these peripheral measures and patients' long-term visual-field changes remained unclear.

This task asks only for associations in the supplied observational cohort; it neither requires nor supports causal claims.

## Data

- `data/longitudinal_observations.csv`: a long-format table of 2,310 visual-field visits from 229 eyes of 139 patients.
- `data/data_dictionary.md`: variable definitions, units, missing-value conventions and data structure.

Pay particular attention to the patient–eye–visit hierarchy, repeated measurements within an eye, correlation between a patient's two eyes, irregular visit intervals and censoring of observation windows described in the dictionary.

## Submission

Please provide:

1. A report presenting results as a list of claims. Each claim must give its statement, direction, point estimate, uncertainty, population, contrast and scale. Distinguish the main analysis, supporting results and limitations; do not describe observational associations as causal effects.
2. A separate list of up to three extension findings, each with verifiable numerical outputs and uncertainty. You may omit this list if no reliable extension is available.
3. Complete code runnable from a single entry point. It must read `data/longitudinal_observations.csv` and generate all reported numerical results and necessary diagnostic outputs in one run. State the execution command in the report.

Every reported numerical value must be traceable to the code's execution output or generated artifacts at the same precision.
