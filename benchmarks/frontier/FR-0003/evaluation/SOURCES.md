# Sources

## Article and supplementary materials

- Matthias Diebold, Patrick T. Gauthier, et al. “Effect of felzartamab on the molecular phenotype of antibody-mediated rejection in kidney transplant biopsies.” *Nature Medicine* 31, 1668–1676 (2025). DOI: https://doi.org/10.1038/s41591-025-03653-3
- Supplementary information: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-025-03653-3/MediaObjects/41591_2025_3653_MOESM1_ESM.pdf
- Reporting summary: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41591-025-03653-3/MediaObjects/41591_2025_3653_MOESM2_ESM.pdf
- Clinical background: Mayer et al., “A randomized phase 2 trial of felzartamab in antibody-mediated rejection,” *NEJM* (2024), DOI: https://doi.org/10.1056/NEJMoa2400763.

## Data

- GEO GSE275824: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE275824
  - SOFT: `GSE275824_family.soft.gz`
  - Series matrix: `GSE275824_series_matrix.txt.gz`
  - GEO contains 63 CEL samples; the authors' reproduction object also contains two week-12 samples.
- Author code and reproduction data: https://github.com/TSI-PTG/CD38-effect-of-treatment/
  - Pinned commit: `074cdeb59fae520088c97e17625ecdc52797f2a7`
  - License: GNU AGPL v3, in the repository-root `LICENSE`.
  - Main ExpressionSet: `data/cd38.RData` in the author repository.
  - Probe annotations: `data/affymap219.RData` in the author repository.
- Author analysis guide: https://tsi-ptg.github.io/CD38-effect-of-treatment/

## Standardization

- All 65 samples retain the ExpressionSet phenotype/assay order and use identifiers `S001`–`S065`.
- `expression_log2.csv.gz` only converts the supplied normalized log2 intensities to gzip CSV, retaining 6 decimal places. No probe filtering, sample exclusion or statistical modeling was applied.
- `feature_annotation.csv.gz` retains only `probe_id`, `gene_symbol` and `gene_name`, excluding the authors' PBT annotations.
- Visible molecular scores include only classifiers/PBTs established before the target article. The newly defined `ABMRact`, `ABMRifng`, `ABMRnk` and `ABMRendo` scores and their membership tables are excluded from `data/`.
