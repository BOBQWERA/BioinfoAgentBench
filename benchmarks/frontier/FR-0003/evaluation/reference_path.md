# Authors' analytical path P*

## Estimand and cohort

| Node | Type | Content | Basis |
|---|---|---|---|
| Q1 | Q | In randomized-trial recipients with histologically confirmed late active or chronic active ABMR, estimate the effect of felzartamab versus placebo on biopsy molecular phenotypes across baseline, week 24 and week 52. The main scale is the between-arm difference in change (treatment × visit interaction). Also describe individual responses, on-treatment effects, post-withdrawal rebound and injury trajectories over the full year. | Trial design; scientific question. |
| E1 | E | The original reproduction object contains 22 participants and 65 expression profiles. Target visits are baseline, week 24 and week 52, with two additional week-12 samples. One placebo recipient lost the graft and lacks week-24/52 biopsies; one felzartamab recipient lacks a week-24 molecular biopsy. | Data inventory; article Methods, “Trial design”. |
| H1 | H | Two recipients lack the target three-visit structure; week 12 is not a target visit in Q1. | E1, Q1. |
| D1 | D | Exclude participants 15 and 18 and restrict visits to baseline, week 24 and week 52, yielding 20 participants and 60 biopsies: 10 participants per arm, each with 3 repeated measurements. | H1. |
| E2 | E | The final score/expression-analysis cohort has `n_patient=20` and `n_biopsy=60`, with 10 felzartamab and 10 placebo recipients. | D1; article Fig. 1, Methods, “Biopsies”. |

## Established molecular scores and individual responses

| Node | Type | Content | Basis |
|---|---|---|---|
| D2 | D | Group established continuous scores into ABMR, TCMR, macrophage, recent injury, atrophy/fibrosis and normal-parenchymal categories. Retain participant, treatment and visit identifiers. | Task data dictionary, D1. |
| M1 | M | For each score category, use Euclidean-distance permutational multivariate analysis of variance for treatment, visit and their interaction (10^6 permutations) as the overall category-level test. | D2; first assess overall change at category level. |
| E3 | E | Overall treatment × visit test across three visits: ABMR score category `P=0.049`; TCMR score category `P=0.89`. | M1; Extended Data Table 1 footnote. |
| H2 | H | Category-level evidence concerns ABMR rather than TCMR; estimate each score's treatment effect within specific time windows. | E3. |
| H3 | H | Normality and equal-variance assumptions do not hold for every score, and biopsies are repeated within recipients. | Distributional checks; model checks in the reproduction guide. |
| M2 | M | Fit aligned-rank transform ANOVA for each score: `score ~ visit * treatment + (1 \| patient)`. Test treatment × visit contrasts for paired time windows, using two-sided α=0.05 and FDR correction within phenotype category. Interpret changes in group medians on the original scale; define treatment effect as `ΔΔ = Δ_felzartamab - Δ_placebo`. | H2, H3, repeated-measure structure. |
| E4 | E | All five ABMR scores have negative baseline→week-24 ΔΔ with FDR<0.05: ABMR probability `-0.67 (IQR 0.35), FDR=0.001`; glomerulitis probability `-0.29 (0.29), FDR=0.003`; peritubular-capillaritis probability `-0.43 (0.26), FDR=0.003`; DSA-selective transcripts `-0.28 (0.23), FDR=0.026`; NK-cell burden `-0.80 (0.36), FDR=0.014`. Corresponding week-24→52 values are `+0.79, +0.50, +0.47, +0.32, +0.87`, all FDR<0.05. None of the five baseline→52 ΔΔ values is significant. | M2; Fig. 2b, Extended Data Table 1. |
| C1 | C | Felzartamab consistently suppresses molecular ABMR activity during treatment, but these scores rebound after withdrawal, leaving no significant net difference by week 52. | E4. |
| E5 | E | None of the five TCMR-related scores has a significant ΔΔ in any of the three time windows. Baseline→week-24 examples: TCMR probability `ΔΔ=+0.01 (IQR 0.01), FDR=0.358`; tubulitis `-0.01, FDR=1.000`; interstitial inflammation `-0.01, FDR=0.964`; QCAT `-0.50, FDR=0.425`; TCB `-0.36, FDR=0.825`. | M2; Fig. 2c, Extended Data Table 1. |
| C2 | C | There is no evidence that felzartamab activates an adverse molecular TCMR response. | E5. |
| E6 | E | Of 10 felzartamab recipients at baseline, 9 have molecular ABMR activity (patient 9 is the exception), and all 9 show lower scores at week 24. Suppression is often incomplete with high baseline activity, particularly in patients 2, 5 and 13; the Discussion also emphasizes patient 16. After withdrawal, 8 of the 9 responders show increased scores again at week 52; patient 4 is the exception. Patient 9 has low baseline activity and no rebound. Elevated baseline TCB/QCAT in patient 13 complicates attribution of NKB. | Individual trajectories in Fig. 2a–c; Supplementary Table 2. |
| C3 | C | On-treatment individual response among recipients with molecularly active ABMR is 9/9, and post-withdrawal molecular relapse is 8/9. Strong baseline activity may leave incomplete suppression. | E6. |

## Transcriptome and mechanism

| Node | Type | Content | Basis |
|---|---|---|---|
| D3 | D | In the normalized expression matrix for the D1 cohort, retain probes with across-sample IQR>0.5, keep the highest-mean-expression probe per gene, and exclude genes differing between arms at baseline (baseline empirical-Bayes test `P<0.05`). This forms the gene set for interpretation. There are 4,838 genes after IQR filtering. | Q1; prevent low variation, duplicate probes and baseline imbalance after small-sample randomization from dominating the interaction. |
| M3 | M | Fit limma expression models with `~ 0 + treatment_visit + cortex_probability`. Estimate felzartamab-versus-placebo differences in change for baseline→24, 24→52 and baseline→52 weeks. The code divides each within-arm change and ΔΔ contrast by 2. Use empirical-Bayes moderated standard errors, report unadjusted P values and apply FDR correction across all 4,838 genes. | D3; cortical tissue fraction may affect bulk expression. |
| E7 | E | No individual gene is significant after FDR correction across 4,838 genes. Among the top 20 baseline→24-week genes ranked by unadjusted P, 10 decrease and are mostly known IFNγ/NK/ABMR activity genes: `CXCL11 ΔΔlogFC=-0.85, P=0.0176`, `CXCL10=-0.77, P=0.0228`, `GZMB=-0.61, P=0.0019`, `SH2D1B=-0.51, P=0.0010`. The other 10 increase; most reverse direction during ABMR recurrence from weeks 24→52. | M3; Fig. 3a–c, Extended Data Table 2. |
| H4 | H | Single-gene evidence is insufficient for confirmatory inference, but rankings consistently implicate IFNγ-inducible and NK-cell programs and suggest recovery of some parenchymal/endothelial genes suppressed by ABMR. | E7. |
| D4 | D | Use pre-publication independent large-cohort correlations and NK/T/HUVEC expression information to define four selective transcript groups: ABMR activity, IFNγ-inducible ABMR activity, NK-cell-enriched ABMR activity and ABMR-related endothelial genes. | H4; Supplementary Tables 4–7. |
| M4 | M | Apply the three M3 ΔΔ contrasts to the selective gene sets in D4 and compare gene-effect directions and means within each set. | D4, M3. |
| E8 | E | Mean ΔΔlogFC for the IFNγ-inducible set is `-0.47` from baseline→24 weeks, `+0.30` from 24→52 weeks and `-0.17` from baseline→52 weeks. Corresponding NK-set values are `-0.28, +0.27, 0.00`, and endothelial-set values `-0.01, +0.05, +0.04`. No individual gene passes FDR correction across 4,838 genes. | M4; Fig. 3d–f, Extended Data Tables 4–6. |
| C4 | C | Felzartamab selectively suppresses IFNγ-inducible and NK-cell-expressed ABMR activity programs, with little effect on ABMR-stage-related endothelial programs. The first two rebound after withdrawal. | E8. |
| C5 | C | Combining reduced biopsy NK transcripts with prior peripheral-blood CD16bright NK-cell results, the authors propose a principal effect more consistent with NK-cell suppression than plasma-cell depletion alone. This is a mechanistic inference and does not exclude additional plasma-cell effects. | E8, C4, pre-publication trial background. |
| C6 | C | Most components increasing at week 24 correlate negatively with ABMR activity or positively with ABMR-related endothelial genes and may be suppressed by IFNγ. The authors interpret this as release from ABMR-mediated expression suppression rather than a new pathogenic program. | E7; external expression/correlation evidence in D4. |

## Ranked enrichment and delayed parenchymal injury

| Node | Type | Content | Basis |
|---|---|---|---|
| M5 | M | For whole-gene rankings in the three M3 time windows, perform GSEA using GO, Reactome, KEGG, MSigDB, DOSE, WikiPathways and independently defined AKI cell-state gene sets. Identify enrichment at FDR<0.05 and consolidate interpretation by meaning and core genes. | H4; test coordinated pathway changes when there is no single-gene FDR signal. |
| E9 | E | From baseline→24 weeks, 12 ABMR/immune-activity pathways show negative enrichment, involving 21 core genes; an example is GO defense response, `NES=-3.07, FDR=3×10^-5`. No pathway is FDR-significant from weeks 24→52, but most genes decreasing/increasing early reverse direction. | M5; Fig. 3a–c, Extended Data Table 3. |
| C7 | C | Pathway-level results support on-treatment suppression of IFNγ/NK-driven ABMR immune activity and molecular recurrence after withdrawal. | E9, C4. |
| E10 | E | Injury-score plots are closer to monotonic trajectories than the initial decline and subsequent rise in ABMR scores. ART-ANOVA time-window ΔΔ tests are nonsignificant: baseline→52-week IRRAT30 `-0.29, FDR=0.175`, IRITD3 `-0.19, FDR=0.060`, IRITD5 `-0.18, FDR=0.093`. | M2; Fig. 4a–c. |
| H5 | H | For injury scores, slopes over the full year better match the observed approximately linear pattern than separate time-window rank tests. | E10 and trajectory plots. |
| M6 | M | Code time as approximately 0, 0.46 and 0.99 years and fit `injury_score ~ treatment * time + (time \| patient)` for each score. Check residuals/normality and compare with a quadratic-time model. After confirming linear mixed-model assumptions, extract arm-specific slopes and their difference, with FDR correction across the three outcomes. | H5, repeated-measure structure. |
| E11 | E | IRRAT30: placebo slope `+0.32 (95% CI -0.04, 0.67)`, felzartamab `-0.29 (-0.64, 0.07)`, difference `-0.60 (-1.10, -0.10), FDR=0.0546`. IRITD3: `+0.06 (-0.06, 0.18)` versus `-0.14 (-0.26, -0.02)`, difference `-0.20 (-0.37, -0.02), FDR=0.0408`. IRITD5: `+0.09 (-0.04, 0.22)` versus `-0.13 (-0.26, -0.01)`, difference `-0.23 (-0.41, -0.05), FDR=0.0420`. | M6; Fig. 4d–f. |
| C8 | C | Injury trajectories decline over the year in felzartamab and rise in placebo. IRITD3/IRITD5 slope differences pass FDR correction; IRRAT30 provides borderline evidence. Temporary ABMR suppression may therefore be followed by delayed, more persistent improvement in parenchymal injury. | E11. |
| E12 | E | Of the top 20 baseline→52-week genes ranked by P, 17 are established injury-induced genes and decrease. Two genes usually suppressed in AKI/ABMR, `AADACL4` and `RERGL`, increase. The top 20 independently defined Hinze AKI markers all decrease; 14 have unadjusted P<0.05, none is FDR-significant, and 7 belong to AKI cell states associated with fibrosis, epithelial–mesenchymal transition or failed repair. | M3; Extended Data Tables 8–9. |
| E13 | E | Baseline→52-week analysis identifies 12 negatively enriched entries: 8 injury-response pathways with 56 core genes, and 4 immune-related injury-response pathways with 34 core genes. The independent AKI cellular-response set has `NES=-2.75, FDR=4×10^-5`. | M5; Fig. 4g, Extended Data Table 10. |
| C9 | C | Whole-transcriptome and independent AKI gene-set results support sustained reduction of injury-induced expression at week 52, suggesting parenchymal benefit approximately 32 weeks after withdrawal. | E12, E13. |
| C10 | C | The authors propose that even if ABMR activity returns, 20–24 weeks of felzartamab may permit injury repair and yield more durable benefit. Slower progression to kidney failure remains an inference requiring larger trials. | C8, C9; small sample and endpoint limitations. |

## Validity and interpretation boundaries

| Node | Type | Content | Basis |
|---|---|---|---|
| E14 | E | Only 20 recipients have all three visits; no individual gene passes genome-wide FDR correction; age/sex subgroups were not analyzed. | E2, E7, Methods. |
| C11 | C | Score- and pathway-level directions agree, but all efficacy, mechanism and long-term prognosis interpretations remain small-sample exploratory evidence requiring validation in larger clinical trials. | E14 and the complete evidence chain. |
