# Reference finding set F

## Recomputable from the supplied data: scoring scope

### C01 | Reproducible individual heterogeneity

- **Finding**: PPGR differs substantially across the seven base meals with equal total carbohydrate and across individuals. The meal eliciting the highest response varies by person, and correlations between the first two repetitions of the same meal are mostly positive.
- **Key results**: Paired Rice−Beans difference, 39.25 mg/dL (95% CI 30.66–47.84, n=21); Potatoes repeat correlation, r=0.691 (0.370–0.865, n=21).
- **Limitations**: Repeat correlations vary by meal; the Beans interval crosses 0. Missing meals affect classification of the highest-response meal.
- **Sources**: P* E01–E03; A03, A04.

### C02 | Meal-specific associations with insulin resistance

- **Finding**: IR participants have a greater peak increment after Potatoes. Pasta shows the same direction but is estimated less precisely in the public subset; Rice/Grapes do not show equally clear differences.
- **Key results**: Potatoes IR−IS, 22.90 mg/dL (4.76–41.04; n=14 vs 17); Pasta, 19.73 (−0.46–39.91; n=13 vs 9).
- **Limitations**: Observational, nonrandomized strata; small groups and no broad adjustment for confounding.
- **Sources**: P* E04–E06; A05–A07.

### C03 | Beta-cell function and the Potatoes response

- **Finding**: The group with dysfunctional DI has a greater peak increment after Potatoes than the normal group. The public subset does not support generalization to all base meals.
- **Key results**: Difference, 26.79 mg/dL (5.73–47.84; n=11 vs 8).
- **Limitations**: Small sample; categorization loses continuous information.
- **Sources**: P* E07; A08.

### C04 | Continuous SSPG gradient

- **Finding**: A higher response to Potatoes relative to Grapes is associated with higher SSPG.
- **Key results**: Spearman ρ=0.673 (bootstrap 95% CI 0.409–0.803; n=31).
- **Limitations**: The ratio may be unstable when the Grapes response is very small; correlation does not establish causality.
- **Sources**: P* E08; A09.

### C05 | Extension: Rice preloads

- **Finding**: A protein preload reduces the mean Rice peak increment. Fiber and fat estimates also indicate reductions, but their public-subset CIs include 0.
- **Key results**: Protein, −11.45 mg/dL (−20.72 to −2.18, n=23); Fiber, −8.79 (−19.65 to 2.08, n=23); Fat, −6.34 (−14.43 to 1.76, n=22).
- **Limitations**: Few paired participants; mean effects mask individual heterogeneity and do not establish mechanisms.
- **Sources**: P* E09.

## Findings from the full study cohort: coverage checks, outside the scoring scope

### C06 | Reproduction boundary between the full cohort and public subset

- **Finding**: Potatoes associations with IR/beta-cell function have the same direction in the full cohort and public subset. Evidence for Pasta is clearer in the full cohort.
- **Key results**: Full-cohort Potatoes IR−IS, 32.80 mg/dL (16.39–49.21); Pasta, 20.26 (3.69–36.83); Potatoes beta-cell dysfunctional−normal, 38.77 (10.33–67.20).
- **Limitations**: The full cohort of 55 and public CGM subset of 38 are different scoring populations; their values are not interchangeable.
- **Sources**: P* E10; article Fig. 3/source data.

### C07 | Meal composition and overall PPGR

- **Finding**: Mean PPGR is highest for Rice and lowest for Beans/Berries. Across the seven meals, fiber content is negatively associated with PPGR.
- **Key results**: Fiber versus peak increment, ρ=−0.75 (95% CI −0.96–0.04, P=0.066); Rice/Bread/Grape spikers account for 35%/24%/22%, and Beans/Berries for 0%.
- **Limitations**: Only seven meal-level observations; fiber covaries with other food properties, preventing causal attribution to a single nutrient.
- **Sources**: P* E11; article Figs. 1–2, Supplementary Tables 1/6.

### C08 | Mean preload effects and physiological strata

- **Finding**: All three preloads modestly reduce mean Rice PPGR, but benefits are highly heterogeneous. Participants with IR/beta-cell dysfunction generally benefit less, and Rice spikers show a stronger response to protein preloads.
- **Key results**: Full-cohort paired P values: Fiber 0.014, Protein 0.004, Fat 0.017; Fiber effect on peak response in IS participants, P=0.031; protein effect in Rice spikers, FDR P=0.027.
- **Limitations**: Some evidence consists only of P values; subgroups are small and multiple comparisons are involved. These findings do not establish clinical efficacy.
- **Sources**: P* E12; article Fig. 4, Supplementary Table 8.

### C09 | Clinical phenotypes associated with response types

- **Finding**: Potato spikers have less favorable glucose-metabolism/lipolysis measures, while Grape spikers are more insulin-sensitive. Asian ethnicity is exploratorily associated with Rice-spiker status, and higher blood pressure with Bread-spiker status.
- **Key results**: Directions are supported by group comparisons in article Fig. 3. The ethnicity result was nominally significant but had pFDR=0.21.
- **Limitations**: Classification by the maximum response, small groups, many comparisons, and lifestyle/genetic confounding; unsuitable for diagnosis.
- **Sources**: P* E13; article Fig. 3, Supplementary Figs. 8/13/14.

### C10 | Meal-specific multiomics signatures

- **Finding**: Bread-spiker status is associated with N1-methyladenosine; Potato-spiker status with TAG/fatty acids and hepatic stellate/fibroblast activation pathways; Beans responses with histidine/amino-acid metabolism; and Berries responses with unsaturated-lipid pathways.
- **Key results**: Many selected results use Holm or FDR correction; feature-level results are in Supplementary Data 1.
- **Limitations**: High dimensionality, small samples and incomplete platform coverage. These are candidate markers and mechanistic leads.
- **Sources**: P* E14; article Fig. 5, Supplementary Figs. 9–11/21.

### C11 | Candidate microbial functions

- **Finding**: Microbial functions such as GH85 are positively associated with PPGR for most meals, while D-alanyl-D-alanine carboxypeptidase is negatively associated. Several genera are associated with metabolic physiology or preload effects.
- **Key results**: The authors selected function/genus-level associations after multiple-testing correction. The task bundle does not include raw reads needed to rerun these results.
- **Limitations**: Associations only.
- **Sources**: P* E15; PRJNA1189566; article Extended Data Fig. 7, Supplementary Table 5.

### C12 | Metabolic-physiology consistency across omics

- **Finding**: Amino acids/hydroxybutyrate/TAG are mostly positively associated with glucose and IR, while phospholipids are mostly negatively associated. Joint models select fasting insulin, BMI, FFA and TAG, among others, as variables associated with IR.
- **Key results**: Correlation matrices and model coefficients are in Extended Data Figs. 8–10 and Supplementary Data 1.
- **Limitations**: Few observations relative to the number of features and no external validation; these models are not established clinical predictors.
- **Sources**: P* E16.

### C13 | Exploratory microbe–metabolite mediation chain

- **Finding**: Some Bacteroides thetaiotaomicron functions form a statistical mediation chain with hepatic IR/fasting insulin through a putative C9H15NO3 feature.
- **Key results**: The article reports FDR support for selected chains; the mediator has not been assigned a database annotation.
- **Limitations**: No randomized or longitudinal causal validation. The unannotated mediator makes biological interpretation highly preliminary.
- **Sources**: P* E17; article Fig. 5c, Supplementary Table 4.

