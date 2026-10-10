# Data dictionary

## Files and structure

All files are UTF-8, comma-delimited, with field names in the first row. Empty fields represent missing values. No sentinel codes such as `-9`, `999` or `unknown` are used for missingness. String values are case-sensitive.

| File | Rows excluding header | Observational unit | Key relationships |
|---|---:|---|---|
| `participants.csv` | 99 | One row per participant | Primary key: `participant_id` |
| `samples.csv` | 213 | One row per sequencing sample | Primary key: `sample_id`; `participant_id` links to participants |
| `arg_calls.csv` | 7,991 | One resistance-gene call passing upstream quality control in a sample | Many-to-one join on `sample_id` |
| `microbiome_genera.csv` | 56,417 | One bacterial-genus call in a sample | Many-to-one join on `sample_id`; includes DNA and RNA |
| `microbiome_species.csv` | 79,879 | One bacterial-species call in a sample | Many-to-one join on `sample_id`; DNA only |

There are two assay types: `dna` denotes metagenomic DNA sequencing, representing detected genetic content; `rna` denotes metatranscriptomic RNA sequencing, representing detected transcripts. The assays cover different sample sets and must not be treated as two completely paired channels for identical samples.

Visits are enrollment (`day_0`) and month 6 (`month_6`). Within an assay, a `participant_id` may have both time points or only one. No additional follow-up times or censoring-time variable are supplied. Study arm is randomized at participant level, but inclusion in this sequencing subset is affected by sample availability and subset selection.

Microbial and resistance-gene tables have undergone host-read removal, reference alignment, negative-control background assessment and basic call quality control. `background_p_value` and `background_fdr` describe evidence for a call relative to negative-control background; they do not test an intervention effect.

## `participants.csv`

| Variable | Type; range/values | Meaning |
|---|---|---|
| `participant_id` | String; `P001`–`P099` | De-identified participant ID |
| `study_arm` | Categorical; `doxy_pep`, `standard_care` | Randomized arm |
| `living_with_hiv` | Integer; 0/1 | 1: living with HIV; 0: receiving HIV pre-exposure prophylaxis |
| `age_years` | Integer; 23–74 | Age at enrollment, years |
| `race_ethnicity` | Categorical | De-identified race/ethnicity category; `Unknown` is an originally reported category, not a missing-value code |
| `baseline_cd4_available` | Integer; 1 or empty | 1: baseline CD4 count available; empty: unavailable or not applicable |
| `baseline_cd4_cells_per_mm3` | Numeric; 197–1,424 or empty | Baseline CD4 count in cells/mm³, recorded when available |

## `samples.csv`

| Variable | Type; range/values | Meaning |
|---|---|---|
| `sample_id` | String; `S001`–`S213` | De-identified sequencing-sample ID |
| `participant_id` | String | Corresponding participant ID |
| `assay` | Categorical; `dna`, `rna` | Assay type |
| `study_arm` | Categorical | Participant's randomized arm, consistent with `participants.csv` |
| `visit` | Categorical; `day_0`, `month_6` | Sampling time |
| `doxycycline_doses_since_enrollment` | Integer; 0–200 | Cumulative doxycycline exposure units at sampling; one 200 mg PEP dose counts as 1, and each therapeutic treatment day counts as 1 |
| `quinolone_days_during_followup` | Integer; 0–3 | Quinolone treatment days over the entire 6-month follow-up |
| `cephalosporin_days_during_followup` | Integer; 0–4 | Cephalosporin treatment days over the entire 6-month follow-up |
| `tetracycline_treatment_days_during_followup` | Integer; 0–14 | Therapeutic tetracycline treatment days over the entire 6-month follow-up; relevant treatment days are already incorporated in the cumulative doxycycline variable under the study's rules |
| `clindamycin_days_during_followup` | Integer; 0–1 | Clindamycin treatment days over the entire 6-month follow-up |
| `penicillin_days_during_followup` | Integer; 0–14 | Penicillin treatment days over the entire 6-month follow-up |
| `vancomycin_days_during_followup` | Integer; 0–4 | Vancomycin treatment days over the entire 6-month follow-up |
| `azithromycin_days_during_followup` | Integer; 0–1 | Azithromycin treatment days over the entire 6-month follow-up |
| `sequencing_reads` | Integer; 456,796–150,000,000 | Total sequencing reads in the sample |
| `ercc_reads` | Integer; 12–136,782,376 | Reads from the exogenous ERCC standard |
| `total_arg_mass_pg_per_million_reads` | Numeric; 0–4.060433777 | Total standard-normalized resistance-gene mass, pg per million total sequencing reads |

## `arg_calls.csv`

A sample with no corresponding row has no resistance-gene calls passing upstream quality control; this does not mean that its sample record is missing. Only `card_aro_accession` has missing values in this table.

| Variable | Type; range/values | Meaning |
|---|---|---|
| `sample_id` | String | Corresponding sequencing-sample ID |
| `gene_name` | String | Resistance-gene name |
| `gene_family` | String | CARD gene-family annotation |
| `drug_class` | String | Original drug-class annotation; one gene may have multiple classes |
| `resistance_mechanism` | Categorical | CARD resistance-mechanism annotation |
| `mean_reference_depth` | Numeric; 0.01–392.84 | Mean reference-sequence coverage depth |
| `reads_per_million` | Numeric; 0.01–296.0 | RPM: read count normalized by total sequencing reads |
| `depth_per_million` | Numeric; 0–17.75 | DPM: coverage depth normalized by total sequencing reads and reference-sequence length |
| `card_aro_accession` | String or empty | CARD Antibiotic Resistance Ontology accession; absent for some calls |
| `arg_class` | Categorical | Consolidated main resistance-drug class, including `tetracycline`, `beta-lactam`, `MLS` and others |
| `tetracycline_scope` | Categorical; `tetracycline_only`, `tetracycline_plus_other`, `non_tetracycline` | Whether the call concerns tetracycline resistance only, tetracycline plus other classes, or no tetracycline resistance |
| `expected_background_count` | Numeric; 0–14.21008786 | Expected read count from the negative-control background model |
| `background_p_value` | Numeric; 0–0.0455593 | Unadjusted P value for the call relative to background |
| `background_fdr` | Numeric; 0–0.04609529 | Benjamini–Hochberg FDR for the call relative to background |
| `arg_mass_pg_per_million_reads` | Numeric; greater than 0, maximum 0.685231922 | Standard-normalized mass of an individual resistance gene, pg per million total sequencing reads |

## `microbiome_genera.csv`

| Variable | Type; range/values | Meaning |
|---|---|---|
| `sample_id` | String | Corresponding sequencing-sample ID |
| `assay` | Categorical; `dna`, `rna` | Assay type |
| `ncbi_tax_id` | Integer | NCBI Taxonomy genus ID |
| `genus_name` | String | Bacterial genus name |
| `known_pathogen_species_count` | Integer; 0–16 | Number of species in the genus annotated as known pathogens in the database; not a diagnosis of infection in the sample |
| `nucleotide_reads_per_million` | Numeric | Nucleotide-alignment RPM |
| `nucleotide_read_count` | Integer; at least 10 | Nucleotide-alignment read count |
| `nucleotide_alignment_length` | Numeric; at least 70 | Nucleotide-alignment length, bp |
| `protein_reads_per_million` | Numeric | Protein-alignment RPM |
| `protein_read_count` | Integer; at least 1 | Protein-alignment read count |
| `expected_background_count` | Numeric | Expected read count from the negative-control background model |
| `background_p_value` | Numeric; 0–0.09856789568 | Unadjusted P value for the call relative to background |
| `background_fdr` | Numeric; 0–0.09997338921 | Benjamini–Hochberg FDR for the call relative to background |

## `microbiome_species.csv`

Fields match the genus table, except that `species_name` replaces `genus_name` and a 0/1 `known_pathogen_flag` replaces `known_pathogen_species_count`. This table contains only `dna` results. Nucleotide read counts range from 10–3,932,007 and background FDR from 0–0.09973092371.

## Relationships and integrity constraints

- `participants.csv:participant_id` and `samples.csv:sample_id` are unique.
- Every `samples.csv:participant_id` must occur in the participant table.
- Every `sample_id` in the three call tables must occur in the sample table. Species calls link only to `assay=dna` samples.
- A participant's `study_arm` remains constant across all files and visits.
- `doxycycline_doses_since_enrollment` varies with sampling time: it is 0 at `day_0` and the cumulative exposure from enrollment to sampling at `month_6`. The other `*_days_during_followup` fields are participant-level totals over the full 6 months, repeated across that participant's sample rows. They do not represent exposure already accrued at day 0.
