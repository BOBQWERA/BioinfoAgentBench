# Data description

## Files

- `sample_metadata.csv`: trial arm, visit, participant-level baseline characteristics, tissue-composition proxies and histological measures for 65 biopsies.
- `molecular_scores.csv`: previously established molecular classifiers, pathogenesis-based transcript (PBT) scores and dd-cfDNA for the same samples; join to metadata using `sample_id`.
- `expression_log2.csv.gz`: normalized log2 expression intensities for 49,495 PrimeView U219 probe sets (rows) × 65 samples (columns); the first column is `probe_id`.
- `feature_annotation.csv.gz`: probe-set mappings to gene symbols and names; join to the expression matrix using `probe_id`. A gene may map to multiple probe sets, and 622 probe sets lack gene annotations.
- `data_dictionary.csv`: variable-level dictionary.

## Design and structure

- The observational unit is the kidney-transplant biopsy; the unit of randomization is the participant.
- There are 22 participants nested within two centers, with repeated biopsies per participant.
- Scheduled visits of interest are baseline, week 24 and week 52. The data also include two week-12 biopsies, and not every participant has all scheduled visits.
- Visit counts are: placebo, 11 at baseline, 1 at week 12, 10 at week 24 and 10 at week 52; felzartamab, 11 at baseline, 1 at week 12, 10 at week 24 and 11 at week 52.
- Treatment arm is constant within a participant. Baseline demographic, transplant and screening variables are repeated across that participant's rows.
- Expression and score tables contain continuous values. Probability classifiers usually range from 0–1; PBT scores have no common physical unit.
- Expression intensities have undergone technical normalization and are on the log2 scale. Probe filtering, aggregation of multiple probes per gene, sample-inclusion rules and inferential models are left to the analyst.
- Missing values are encoded as `NA`. Only `microvascular_inflammation_score` has missing values, in 2 samples; all other visible fields are complete.

## Score groups

- ABMR-related: `abmr_probability`, `glomerulitis_gt0_probability`, `peritubular_capillaritis_gt0_probability`, `dsa_selective_transcript_score`, `nk_cell_burden_score`.
- TCMR-related: `tcmr_probability`, `interstitial_inflammation_gt1_probability`, `tubulitis_gt1_probability`, `t_cell_burden_score`, `cytotoxic_t_cell_score`.
- Macrophage-related: `alternatively_activated_macrophage_score`, `constitutive_macrophage_score`.
- Recent injury: `injury_repair_associated_score`, `injury_repair_day3_score`, `injury_repair_day5_score`.
- Atrophy/fibrosis: `atrophy_gt1_probability`, `fibrosis_gt1_probability`.
- Normal parenchyma: `normal_kidney_transcript_score`, `normal_kidney_solute_carrier_score`.

Biological interpretation of `nk_cell_burden_score` assumes no substantial T-cell-mediated rejection activity, because some transcripts are shared by NK and T cells.
