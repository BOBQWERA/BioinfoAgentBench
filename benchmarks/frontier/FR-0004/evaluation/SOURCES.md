# Sources

## Article and data

- Petriti B, Rabiolo A, Chau K-Y, et al. *Peripheral blood mononuclear cell respiratory function is associated with progressive glaucomatous vision loss*. Nature Medicine. 2024;30:2362–2370. [Article](https://doi.org/10.1038/s41591-024-03068-6).
- Data: [Figshare](https://figshare.com/s/145fd5cfbd9eaadeb857), DOI `10.6084/m9.figshare.25761519`; source file `Main_Paper_Data.csv`.
- Article and data license: CC BY 4.0.

The task uses the longitudinal cohort of 139 treated POAG patients in part 2 of the article.

## Data transformations

- `data/longitudinal_observations.csv` retains 2,310 visits from 139 patients and 229 eyes after removing 2,310 entirely empty rows from the source CSV.
- The authors' derived or summary fields are omitted: `MEAN_IOP`, `PEAK_IOP`, `SD_IOP`, `VF_MAX`, `FU_MAX`, `BASELINE_MD`, `BASELINE_IOP`, `IOP_REDUCTION`, `FINAL_MD`, `FINAL_IOP`, `LMM_RATES` and `NAD_PRESENT`.
- `FU` is renamed to `visit_time_years`. Excel serial `Date_NAD` values are converted to ISO dates, and `visit_index` records the time-sorted row order within each eye.
- Other numerical measurements retain their original values and precision.
