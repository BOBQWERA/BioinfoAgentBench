# Data description

## Files and observational units

### `cgm_curves.csv`

Each row is one time point within a meal-challenge curve. The curve key is `subject + foods + rep`.

- `subject`: de-identified participant ID.
- `foods`: the complete meal condition, either a base meal or a base meal plus a preload.
- `food`: the base meal.
- `mitigator`: preload type; an empty value indicates no preload.
- `rep`: replicate number within the same participant and condition.
- `mins_since_start`: minutes relative to the start of the base meal; negative values precede the meal.
- `glucose`: continuous glucose measurement in mg/dL.

Each released curve contains 40 equally spaced time points, from -25 to 170 minutes at 5-minute intervals. Participants may complete multiple meal conditions and repeat the same condition on different days. Meal coverage and repeat counts are not fully balanced across participants. Curves are already on the common time grid supplied by the data provider; raw device timestamps are not available.

The seven standardized base-meal conditions are `Beans`, `Berries`, `Bread`, `Grapes`, `Pasta`, `Potatoes` and `Rice`. The file also includes a small number of other base-meal and preload conditions. Their inclusion depends on the analytical question.

### `participant_metadata.csv`

Each row represents one participant. Join `id` to `subject` in the CGM file. The table contains 74 participants, of whom 38 appear in the CGM file. Clinical variables are not measured for every participant; blank values and `NA` indicate missingness. When a clinical measure has multiple visits, the released table supplies a participant-level summary.

SSPG is measured in mg/dL; higher values indicate greater peripheral insulin resistance. DI is the disposition index, which relates insulin secretion to insulin sensitivity. Units for other variables are listed in `data_dictionary.csv`.

### `meal_nutrients.csv`

Each row represents one standardized base meal. Nutrient values refer to the portions actually provided in the study, each containing approximately 50 g of total carbohydrate. Units are included in the column names. Join `meal` to the base-meal name in the CGM file.

### `baseline_metabolomics.tsv`

Each row is a mass-spectrometry feature. Initial columns contain feature annotations; columns such as `XB59_1` contain sample measurements. Sample column names combine a participant ID with a visit/sample number. Measurements are the instrument intensities supplied by the provider, in arbitrary intensity units. Annotation confidence and retention flags appear in the row's metadata columns. The file is tab-delimited.

### `baseline_lipidomics.tsv`

Each row is a lipid molecular species. `X` contains the lipid name, and columns such as `XB59_1` identify participant visits/samples. The release documentation reports abundance in nmol/g. The file is tab-delimited.

### `baseline_olink.csv`

This is a long-format table with one participant–protein measurement per row. `SampleID` links to participant IDs; `OlinkID`/`Assay` identify the protein; `NPX` is log2 NPX. Panel, detection-limit and quality-control fields accompany each row. Proteins and participants may have missing measurements or quality warnings.

## Missing values and structure

- Empty strings, empty CSV fields and `NA` represent missing values, not 0.
- Individual time points are not independent CGM analysis units: time points are nested within curves, and curves/replicates are nested within participants.
- Clinical and omics tables have incomplete participant overlap. Report the sample size after each join.
- Metabolomics and lipidomics may include multiple visits/samples per participant. This Olink release uses participant-level `SampleID` values.
- `data_dictionary.csv` lists each column's storage type, role, unit, observed range or number of levels, and missing-value count.
