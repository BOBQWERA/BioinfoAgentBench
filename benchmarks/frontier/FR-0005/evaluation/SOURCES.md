# Sources

## Article and data

- Keeley, A. J. et al. “Early-life serological profiles and the development of natural protective humoral immunity to Streptococcus pyogenes in a high-burden setting.” Nature Medicine 31, 3360–3371 (2025). [Article](https://doi.org/10.1038/s41591-025-03868-4).
- Public anonymized data: [Zenodo](https://doi.org/10.5281/zenodo.14887949), licensed under CC BY 4.0.
- The source remaps identifiers, shifts all dates uniformly and replaces exact ages with pseudo-ages sampled within each retained age group. Time intervals and household/participant structure are preserved.

## Author code

- [Author repository](https://github.com/Clinical-Infection-Research-UoSheffield/Development_natural_protective_immunity_Streptococcus_pyogenes), source commit `cf7d33b3f51415dc170f6afb41982372019e34bc`.
- The repository README declares CC BY-NC-ND 4.0 for its materials.
- Raw functional-assay data used by `06_functional_assays.R` are owned by GSK Vaccines and are not publicly available.

## Data transformations

- The six CSV files in `data/` select fields for the two cohort structures, use descriptive column names and convert R factors to strings.
- `household_id` uses the source's three-character household prefix.
- `study_day` is the shifted IgG sampling date minus the public participant entry date.
- Repeated `entry_1`–`entry_7` and `exit_1`–`exit_7` fields become continuous observation intervals relative to first entry.
- IgG measurements retain their observed sampling times, without carry-forward imputation.
