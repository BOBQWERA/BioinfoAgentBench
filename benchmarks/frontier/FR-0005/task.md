# Scientific question

In The Gambia, a setting with a high burden of *Streptococcus pyogenes* (group A streptococcus), what levels and age-related patterns do IgG responses to conserved antigens show from birth across age groups? In the household cohort, is antigen-specific IgG associated with subsequent culture-confirmed infection or carriage events, and what are the direction and strength of these associations?

## Background

Before this study was published, *S. pyogenes* was known to cause pharyngitis, pyoderma, invasive infection, and immune sequelae such as acute rheumatic fever and rheumatic heart disease. The burden is particularly high in low- and middle-income settings with intense transmission. Throat and skin infections, as well as asymptomatic carriage, may contribute to ongoing transmission and immune stimulation.

Pharyngitis and pyoderma are generally more common in children than in adults, suggesting that natural immunity may gradually develop after repeated exposure. However, quantifiable markers of naturally acquired protective immunity in humans remain unclear. M protein is highly diverse across types, making more conserved antigens such as SLO, SpyAD, SpyCEP, and GAC of interest as vaccine candidates. DNAseB is often used as a serological marker of prior streptococcal exposure. Maternal IgG can cross the placenta and gradually wanes after birth.

## Data

Use the six CSV files in `data/`. Full field definitions, units, values, missing-data encodings, and hierarchical structure are provided in `data/README.md`. The data come from two independent cohorts: postnatal follow-up of 94 mother–infant pairs, and a household-recruited longitudinal cohort with repeated visits, intermittent observation periods, and recurrent events. Dates and exact ages in the public data have been anonymized, while within-person time intervals, age groups, and household structure are preserved.

The data contain only time points at which IgG was actually measured; unmeasured periods have no prefilled values. Explain all data-processing and estimation choices and their rationale.

## Submission requirements

Submit:

1. A concise report. First define the outcome, contrast, population, and scale for each primary estimand. Then list claims, each with a statement, direction, point estimate, and uncertainty. Explain how the analysis handles repeated observations, household nesting, recurrent events, intermittent observation periods, time at risk, right censoring, and missing values.
2. A separate list of no more than three additional findings. If there are no reliable additional findings, explicitly state “None.”
3. Code that runs from a clean working directory, using a single entry point to read `data/` and generate the numerical outputs cited in the report. It must not depend on hidden files, the paper's main text, or manually copied results.

Every reported number must be precisely traceable to execution output or generated tables. Use CPU only; a single-core runtime of no more than 30 minutes is recommended.
