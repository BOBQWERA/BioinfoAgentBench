# Scientific question

In these adults without a previous diagnosis of diabetes, do standardized meals with equal carbohydrate loads produce reproducible differences in postprandial glycemic responses between individuals, and how are the direction and magnitude of these differences associated with baseline insulin resistance and beta-cell function?

## Background

Before this study was published, postprandial glucose elevations were already associated with type 2 diabetes and cardiovascular risk, and individuals were known to respond differently to the same food. Carbohydrate properties, food processing, dietary fiber, other macronutrients and individual metabolic status may all affect these responses. However, the relationships among food differences, within-person repeatability and baseline metabolic physiology had not been systematically characterized under standardized challenges.

Participants consumed standardized meals at home after an overnight fast. Each of the seven base meals provided approximately 50 g of total carbohydrate. Some participants also consumed a fiber, protein or fat preload before the rice meal. Challenges took place on separate days. Participants were instructed to remain seated and consume no other food or drink for 3 hours after the meal. Continuous glucose monitoring times are relative to the recorded start of the base meal, defined as minute 0.

Baseline metabolic phenotypes include steady-state plasma glucose (SSPG; higher values indicate greater insulin resistance) and the disposition index (DI; beta-cell secretory function in relation to insulin sensitivity), together with routine clinical variables. Baseline metabolomics, lipidomics and Olink proteomics may support up to three mechanistic extension findings, but are not required to answer the main question.

## Data

Use only the files in `data/`. File roles, variable types, units, observed ranges and missingness are described in `data/README.md` and `data/data_dictionary.csv`.

- `cgm_curves.csv`: continuous glucose curves. A participant may have multiple meal conditions, repeated challenges for a condition and multiple time points within each curve.
- `participant_metadata.csv`: participant-level clinical and metabolic phenotypes.
- `meal_nutrients.csv`: nutrient composition of the seven standardized base meals.
- `baseline_metabolomics.tsv`, `baseline_lipidomics.tsv`, `baseline_olink.csv`: baseline molecular measurements, with differing participant coverage and numbers of visits.
- `data_dictionary.csv`: a dictionary for each file and variable.

This is the subset whose participants consented to public sharing. Not everyone with clinical metadata has CGM data or measurements from every omics platform. Meal coverage and repeat counts are also unbalanced. Participant, meal, replicate and time hierarchies are part of the data structure.

## Submission

Please provide:

1. A report that first defines the estimand (outcome, contrast, population and scale), then lists the claims. Each claim should state its direction, point estimate and uncertainty, and explain how key validity checks affected the analysis or conclusions.
2. A separate list of up to three extension findings, each with verifiable numerical evidence and uncertainty. You may leave slots unused when evidence is insufficient.
3. Runnable code with a single entry point that reads from `data/` and generates every numerical result and output file cited in the report.
