# Reference analytical path P*

## Study population

- **Content**: The scoring population is the public subset of 38 participants in `data/` who consented to sharing and have CGM data. The article describes the full study cohort of 55 participants.
- **Rationale**: Numerical anchors describe the 38-participant public subset.
- **Evidence**: `reference_results.json::data_checks`; article Methods/Results (848 curves, 55 participants); the public subset in the CGM Data Portal.

Public-subset estimates and 95% CIs are provided in `reference_results.json`. Full-cohort results are cited from the article.

## Main-question path: public subset, within the scoring scope

### Q01 | Question and estimand

- **Content**: The outcome is each curve's postprandial peak increment above its minute-0 baseline (mg/dL), calculated per replicate and then averaged within participant × meal. Main contrasts are within-participant differences between base meals, mean differences between metabolic groups, and correlations between replicates or with continuous physiological measures.
- **Rationale**: This addresses meal differences, within-person repeatability and associations with baseline metabolic physiology while retaining the participant as the independent unit of inference.
- **Evidence**: Hierarchical structure in `data/README.md`; methods M01–M02.

### D01 | Data audit and analysis set

- **Content**: CGM data contain 23,520 rows, 588 curves and 38 participants. Each curve has 40 points (−25 to 170 minutes at 5-minute intervals). The seven base meals contribute 393 curves, summarized into 219 participant × meal observations.
- **Rationale**: Confirm the time grid, curve keys and unbalanced replicates to avoid treating time points or replicates as independent samples.
- **Evidence**: `reference_results.json::data_checks`; anchors A01, A02.

### H01 | Hierarchy and missingness assumptions

- **Content**: Time points are nested within curves, and curves within participants; clinical and omics coverage is incomplete. The main analysis neither assigns missing SSPG/DI values to a healthy group nor requires all seven meals for a participant to be retained.
- **Rationale**: Incorrect missing-value coding or pseudoreplication inflates the effective sample size and biases group differences.
- **Evidence**: Missing-value counts in `data/data_dictionary.csv`.

### M01 | Curve-feature construction

- **Content**: Use the minute-0 value as baseline. The peak increment is maximum glucose from 0–170 minutes minus baseline. Negative time-specific increments are truncated to 0 when calculating area above baseline. Peak increment is the primary outcome; area is only a candidate robustness measure.
- **Rationale**: The common time grid permits direct recomputation from the curves, and this definition matches the study's quantitative PPGR scale.
- **Evidence**: Article Methods, “CGM data preprocessing and PPGR feature extraction”.

### M02 | Replicate handling and repeatability

- **Content**: Meal ranking and physiological associations use the mean across replicates for each participant × meal. Repeatability is the Pearson correlation between peak increments from repetitions 1 and 2 of the same meal, with a Fisher-transformed 95% CI.
- **Rationale**: Averaging replicates reduces within-day noise. Examining the first two repetitions separately tests whether the signal is stable within a person.
- **Evidence**: `reference_results.json::replicate_peak_increment_correlations`.

### E01 | Overall responses to base meals

- **Content**: Curve-level mean peak increments range from Beans 32.69 and Berries 35.20 to Rice 66.95 mg/dL. The paired mean Rice−Beans difference is 39.25 mg/dL (95% CI 30.66–47.84, n=21).
- **Rationale**: This shows substantial average differences between meals despite equal carbohydrate loads, with paired estimates controlling for baseline differences between individuals.
- **Evidence**: `reference_results.json::meal_peak_increment_summary` and `paired_meal_peak_increment_contrasts.rice_minus_beans`; anchor A04.

### E02 | Individual response types

- **Content**: Define each participant's response type by the measured base meal with the highest mean peak increment. The public subset has 13/10/8/5/2 Rice/Bread/Grapes/Potatoes/Pasta spikers, respectively, and 0 Beans or Berries spikers.
- **Rationale**: Overall means do not represent every participant. The distribution of highest-response meals directly demonstrates differences in meal ranking between people.
- **Evidence**: `reference_results.json::spiker_counts`.

### E03 | Repeatability evidence

- **Content**: Potatoes repetitions have n=21 and r=0.691 (95% CI 0.370–0.865); Pasta has n=18 and r=0.716 (0.373–0.886). Correlations for the other base meals are also positive, but the Beans interval crosses 0.
- **Rationale**: Positive correlations across several meals suggest that differences are not solely random day-to-day fluctuations. Low-response meals have greater uncertainty.
- **Evidence**: `reference_results.json::replicate_peak_increment_correlations`; anchor A03.

### C01 | Reproducible individual heterogeneity

- **Content**: The public subset supports large average meal differences, differences between people in their highest-response meal, and moderate correlations between repeats of the same meal. Individual responses to equal carbohydrate loads therefore contain a reproducible component, whose strength varies by meal.
- **Rationale**: Combine E01–E03 rather than inferring individual specificity from overall means or a single measurement.
- **Evidence**: E01, E02, E03.

### D02 | Physiological strata

- **Content**: SSPG >120 mg/dL defines IR and ≤120 defines IS. DI <1.2 defines dysfunction, 1.2–2.2 an intermediate group, and >2.2 normal function. Include only participants with the relevant measurement in each comparison.
- **Rationale**: Translate continuous physiological measurements into the article's predefined clinical strata while retaining continuous SSPG analysis as a supplement.
- **Evidence**: Article Methods, “Metabolic subgrouping”.

### M03 | Between-group effects and uncertainty

- **Content**: For each meal, first average a participant's replicates, then estimate the IR−IS or dysfunctional−normal mean difference in peak increment. Use Welch standard errors for 95% CIs; rank tests between the groups serve only as distributional robustness checks.
- **Rationale**: Mean differences and their CIs directly match the requested units and uncertainty while allowing unequal group variances and sample sizes.
- **Evidence**: `reference_results.json::physiology_peak_increment_contrasts`.

### E04 | Insulin resistance: Potatoes

- **Content**: IR: n=14, mean 71.29 mg/dL; IS: n=17, mean 48.39 mg/dL. The difference is 22.90 mg/dL (95% CI 4.76–41.04), with a mean ratio of 1.47; exact Mann–Whitney P=0.0053.
- **Rationale**: The consistent direction and CI excluding 0 provide the clearest meal-specific physiological association in the public subset.
- **Evidence**: `reference_results.json::physiology_peak_increment_contrasts.potatoes_IR_vs_IS`; anchor A05.

### E05 | Insulin resistance: Pasta and negative-control meals

- **Content**: The Pasta IR−IS difference is 19.73 mg/dL (95% CI −0.46–39.91; n=13 vs 9), in the same direction as Potatoes but with an interval just crossing 0. Differences are −6.31 (−22.68–10.06) for Grapes and 8.07 (−10.60–26.74) mg/dL for Rice.
- **Rationale**: The association is not equally strong for every meal. Pasta provides only directional/borderline evidence in the public subset.
- **Evidence**: `reference_results.json::physiology_peak_increment_contrasts`; anchor A07.

### M04 | Covariate robustness

- **Content**: Among complete Potatoes cases, regress peak increment on the IR indicator, adjusting for BMI, age and sex; n=29.
- **Rationale**: Check whether the simple stratified difference is fully explained by the available demographic and body-size variables.
- **Evidence**: `reference_results.json::potato_IR_adjusted_for_BMI_age_sex`.

### E06 | Adjusted Potatoes association

- **Content**: The adjusted IR coefficient is 38.95 mg/dL (95% CI 17.48–60.41; n=29).
- **Rationale**: The direction is not attenuated, supporting that these covariates do not explain the Potatoes association. The observational analysis still does not establish causality.
- **Evidence**: `reference_results.json::potato_IR_adjusted_for_BMI_age_sex`; anchor A06.

### C02 | Conclusion on insulin resistance

- **Content**: In the public subset, greater insulin resistance is reliably associated with a larger Potatoes peak increment. Pasta shows the same direction with greater uncertainty; Grapes and Rice lack equally clear evidence, indicating meal specificity.
- **Rationale**: Combine unadjusted, adjusted and negative-control-meal results, distinguishing supported from suggestive conclusions by CI strength.
- **Evidence**: E04, E05, E06.

### E07 | Beta-cell function

- **Content**: For Potatoes, the dysfunctional-DI group has n=11 and a mean of 71.00 mg/dL; the normal group has n=8 and a mean of 44.22 mg/dL. The difference is 26.79 mg/dL (95% CI 5.73–47.84), with a mean ratio of 1.61. Corresponding intervals for the other three meals all cross 0.
- **Rationale**: The dysfunctional group responds more strongly to Potatoes, with a CI excluding 0, but the small sample requires cautious wording.
- **Evidence**: `reference_results.json::physiology_peak_increment_contrasts.*_beta_dysfunctional_vs_normal`; anchor A08.

### C03 | Conclusion on beta-cell function

- **Content**: Poorer beta-cell function is associated with a greater Potatoes response. The public subset does not support extending this association indiscriminately to all base meals.
- **Rationale**: Only Potatoes has clear interval support, and the normal group contains just 8 participants.
- **Evidence**: E07.

### M05 | Continuous physiological gradient

- **Content**: For participants with Potatoes, Grapes and SSPG measurements, calculate the ratio of the two meals' mean peak increments and its Spearman correlation with SSPG. Obtain a CI using 5,000 participant-level bootstrap samples with a fixed random seed.
- **Rationale**: Avoid information loss from grouping thresholds and construct a within-person meal ratio with physiological contrast.
- **Evidence**: `reference_results.json::potato_grape_ratio_SSPG_spearman`.

### E08 | PG ratio and SSPG

- **Content**: n=31; Spearman ρ=0.673 (bootstrap 95% CI 0.409–0.803).
- **Rationale**: Higher SSPG accompanies a relatively stronger Potatoes-versus-Grapes response, reinforcing continuous evidence for meal specificity.
- **Evidence**: `reference_results.json::potato_grape_ratio_SSPG_spearman`; anchor A09.

### C04 | Main-question synthesis

- **Content**: Individual PPGR differences contain a reproducible component, and their associations with baseline metabolic physiology are concentrated in particular carbohydrate sources. In the public subset, evidence is strongest for Potatoes associations with IR/beta-cell function; Pasta has a directionally consistent but imprecise IR association, and the PG ratio increases with SSPG.
- **Rationale**: Synthesize C01–C03 and E08 while preserving effect sizes, uncertainty and the noncausal interpretation.
- **Evidence**: C01, C02, C03, E08.

## Optional extension path: also recomputed from the public subset

### M06 | Paired preload comparisons

- **Content**: Among participants who completed both Rice and Rice plus a preload, compare participant-level mean peak increments and estimate the paired preload−Rice mean difference with its 95% CI.
- **Rationale**: Pairing reduces baseline differences between individuals. Estimate the three preloads separately rather than pooling them as a single intervention.
- **Evidence**: `reference_results.json::paired_mitigator_peak_increment_contrasts`.

### E09 | Preload results

- **Content**: Protein: n=23, difference −11.45 mg/dL (95% CI −20.72 to −2.18); Fiber: n=23, −8.79 (−19.65 to 2.08); Fat: n=22, −6.34 (−14.43 to 1.76).
- **Rationale**: All three estimates indicate reductions, but only the Protein CI excludes 0 in the public subset. Agreement in direction does not establish an effect for every preload.
- **Evidence**: `reference_results.json::paired_mitigator_peak_increment_contrasts`.

### C05 | Extension: preload heterogeneity

- **Content**: The public subset supports a reduction in mean Rice peak increment after a protein preload. Fiber and fat estimates also indicate reductions, but uncertainty includes no effect. These mean results do not rule out substantial individual heterogeneity.
- **Rationale**: Grade the conclusions by CI strength and avoid interpreting an observed paired mean effect as a mechanism or universal clinical benefit.
- **Evidence**: E09.

## Article coverage checks: full cohort, outside scoring

### E10 | Main physiological results in the full cohort

- **Content**: In the full study cohort, the Potatoes IR−IS peak-increment difference is 32.80 mg/dL (95% CI 16.39–49.21; n=16 vs 14), and the Pasta difference is 20.26 (3.69–36.83; n=16 vs 12). The Potatoes beta-cell dysfunctional−normal difference is 38.77 (10.33–67.20; n=12 vs 5).
- **Rationale**: Confirm agreement in the main direction with the public subset. These values concern a different population and must not be used as A anchors.
- **Evidence**: Article Fig. 3 and its source data, sheet `b`.

### C06 | Full-cohort reproduction boundary

- **Content**: Potatoes results have the same direction in the public subset and full cohort. Pasta is clearer in the full cohort, while its public-subset interval just crosses 0. This reflects differing sample coverage rather than a computational failure.
- **Rationale**: Explain in advance why the recomputable answer differs from the exact article values, avoiding calibration across populations.
- **Evidence**: E04, E05, E10.

### E11 | Nutrition and response types in the full cohort

- **Content**: The article reports the highest mean response for Rice and the lowest for Beans/Berries. Across seven meals, dietary fiber versus peak increment has Spearman ρ=−0.75 (95% CI −0.96–0.04, P=0.066). Rice/Bread/Grape spikers account for 35%/24%/22%, and Beans/Berries for 0%.
- **Rationale**: Cover overall meal ranking, the nutrient gradient and individual response types.
- **Evidence**: Article Figs. 1–2; [Supplementary Tables 1 and 6](https://pmc.ncbi.nlm.nih.gov/articles/PMC12283382/#MOESM3).

### C07 | Meal heterogeneity in the full cohort

- **Content**: Equal total carbohydrate does not imply equal PPGR. The fiber gradient is consistent with a lower response, but there are only seven meals and the CI crosses 0, so the association cannot be attributed to fiber alone.
- **Rationale**: Separate descriptive meal differences from weak evidence for a nutrient association.
- **Evidence**: E11.

### E12 | Preload results in the full cohort

- **Content**: Paired P values for Fiber, Protein and Fat versus Rice are 0.014, 0.004 and 0.017. The IR group benefits less on average. In the IS group, Fiber has P=0.031 for peak increment and P=0.057 for area above baseline. Protein has P=0.028 in the normal beta-cell group, and a stronger effect in Rice spikers (FDR P=0.027).
- **Rationale**: Cover mean effects, individual heterogeneity and metabolic strata. Some article results provide only P values, which cannot substitute for effect sizes.
- **Evidence**: Article Fig. 4; [Supplementary Table 8](https://pmc.ncbi.nlm.nih.gov/articles/PMC12283382/#MOESM3).

### C08 | Stratified preload effects in the full cohort

- **Content**: Preloads can modestly reduce mean Rice PPGR, with substantial individual variation and generally weaker mitigation among those with poorer metabolic function. These remain association/subgroup findings and do not establish a particular absorption or hormonal mechanism.
- **Rationale**: Preserve the reported direction while limiting mechanistic extrapolation.
- **Evidence**: E12.

### E13 | Clinical response types

- **Content**: Potato spikers have higher HbA1c, fasting glucose and free fatty acids during the SSPG test. Grape spikers have lower SSPG and fasting glucose. Asian participants are more often Rice spikers, and Bread spikers have higher blood pressure.
- **Rationale**: Cover clinical phenotype associations after classification by the meal eliciting the highest response.
- **Evidence**: Article Fig. 3, Supplementary Figs. 8, 13, 14; Supplementary Table 2.

### C09 | Exploratory interpretation of clinical response types

- **Content**: Response types may mark different metabolic characteristics, but classification uses the maximum response, groups are small and comparisons are numerous. Ethnicity and blood-pressure results in particular should be treated as exploratory associations rather than diagnostic classes.
- **Rationale**: Classification by a maximum is sensitive to measurement noise and missing meals; multiple comparisons reduce certainty.
- **Evidence**: E13; article Discussion on confounding and validation in larger cohorts.

### E14 | Metabolomics, lipidomics and proteomics

- **Content**: The article reports higher N1-methyladenosine in Bread spikers. Potato spikers show enrichment of several TAG/fatty acids and hepatic stellate/fibroblast activation protein pathways. Beans PPGR is associated with ketone-body/amino-acid and histidine metabolites, while Berries PPGR is associated with unsaturated-fatty-acid biosynthesis and unsaturated TAG.
- **Rationale**: Cover baseline multiomics signatures of meal responses, acknowledging differing participant coverage across molecular layers.
- **Evidence**: Article Fig. 5, Supplementary Figs. 9–11, 21, and Supplementary Data 1.

### C10 | Molecular signatures rather than established causal mechanisms

- **Content**: Baseline molecular profiles are associated with specific meal-response types and magnitudes. Small groups, multiple testing, missing measurements across platforms and the cross-sectional design make these results more suitable as candidate mechanisms or stratification markers.
- **Rationale**: Omics associations do not automatically establish biological mechanisms or intervention targets.
- **Evidence**: E14; article Discussion.

### E15 | Microbial functional and genus-level associations

- **Content**: The article reports positive associations of PPGR for most meals with glycosyl hydrolase family 85, lactate utilization domain and heme exporter protein B, and negative associations with D-alanyl-D-alanine carboxypeptidase. Slackia/Tyzzerella are positively associated with glucose or IR; Butyrivibrio, Asaccharobacter, Adlercreutzia and Fusicatenibacter are negatively associated. Klebsiella/Sutterella and Eubacterium hallii starch degradation III are associated with some preload effects.
- **Rationale**: Include the article's microbial functional and taxonomic findings in the reference set.
- **Evidence**: Article Fig. 5, Extended Data Fig. 7, Supplementary Table 5; BioProject PRJNA1189566.

### C11 | Boundaries of microbiome conclusions

- **Content**: Microbial functions have candidate associations with PPGR/preload effects. In this task, these serve only as article coverage checks, not scored reproduction conclusions.
- **Rationale**: The supplied data include CGM, clinical and baseline omics measurements; processed microbiome measurements are not included.
- **Evidence**: BioProject PRJNA1189566; the files listed in `data/README.md`.

### E16 | Metabolic physiology across omics

- **Content**: Tyrosine, hydroxybutyric acid, glutamic acid and TAG are positively associated with glucose/IR. Phosphatidylcholine, lysophosphatidylcholine, lysophosphatidylethanolamine and threonic acid are negatively associated. The authors' joint SSPG model also selects fasting insulin, BMI, FFA and TAG as IR-associated predictors, and phosphatidylcholine as an IS-associated predictor.
- **Rationale**: Cover metabolic-physiology findings from univariate associations through prediction across data types.
- **Evidence**: Article Extended Data Figs. 8–10; Supplementary Data 1.

### C12 | Synthesis of metabolic-physiology omics

- **Content**: Multiomics results are internally consistent with known IR physiology. Predictive models and associations still require external validation and cannot be interpreted directly as causal chains from this study sample.
- **Rationale**: Small training samples, many features and no independent external cohort.
- **Evidence**: E16; article Discussion/limitations.

### E17 | Exploratory mediation analysis

- **Content**: The article's exploratory mediation analysis suggests that several Bacteroides thetaiotaomicron functions may be linked to hepatic IR/fasting insulin through a metabolic feature with putative molecular formula C9H15NO3 that lacks a database annotation.
- **Rationale**: Cover the result closest to a mechanistic chain while retaining the central uncertainty: the mediator is putative and unannotated.
- **Evidence**: Article Fig. 5c; Supplementary Table 4.

### C13 | Boundaries of the mediation result

- **Content**: This mediation pathway is a hypothesis-generating statistical chain, not a confirmed microbe–metabolite–clinical causal mechanism.
- **Rationale**: Exposure, mediator and outcome lack randomized or temporal-intervention validation, and the central metabolite is unannotated.
- **Evidence**: E17.

## Minimum sufficient answer

- Cover C01–C04 and report the main effects and uncertainty represented by at least A03, A05, A08 and A09.
- C05 provides an optional extension.
