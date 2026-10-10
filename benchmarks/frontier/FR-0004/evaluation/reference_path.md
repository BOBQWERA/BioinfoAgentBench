# Author reference path P*

## Scope

This task covers only part 2 of the paper: PBMC mitochondrial respiration and longitudinal visual-field change in patients with POAG receiving IOP-lowering treatment. Between-diagnosis OCR differences, the external UKGTS reference cohort, and the main cross-sectional analyses of NAD against diagnosis/OCR are outside the supplied data. The small-sample analysis of NAD and visual-field progression within the supplied cohort is a branch accessible from the visible data and is included in P* and F.

## Node sequence

| ID | Type | Content | Basis |
|---|---|---|---|
| Q1 | Q | Estimand: the adjusted difference in the eye-level annual rate of VF MD change per 1 cohort standard deviation increase in patient-level PBMC OCR, among patients with POAG receiving IOP-lowering treatment and having long-term visual-field records. The population comprises patients/eyes meeting the longitudinal visual-field inclusion criteria; the primary scale is dB yr^-1. | Study design, part 2, and task instruction. |
| D1 | D | Retain eyes from the clinical POAG cohort with at least 6 reliable visual fields (false positives <15%) spanning at least 3 years. For eyes subsequently undergoing glaucoma surgery, censor from the date of listing for surgery. | Methods, Participants. |
| E1 | E | The final longitudinal sample comprises 139 patients and 229 eyes: 85 patients/144 eyes with NTG and 54 patients/85 eyes with HTG. | Main-text Table 2 and Fig. 2. |
| E2 | E | The median number of visual fields per eye is 10 (IQR 8–12), with median follow-up of 5.7 years (IQR 4.6–6.9). The mean author-derived eye-level annual rate of MD change is -0.59 (s.d. 0.33) dB yr^-1. | E1; main-text Table 2. |
| H1 | H | MD measurements repeat at irregular intervals within each eye, and some patients contribute both eyes. The validity of the primary evidence therefore requires accounting for within-eye and within-patient correlation. | Data structure in the task card; E1 and E2. |
| D2 | D | Standardize age, CCT, mean IOP over the observation window, and candidate OCR measures to zero mean and unit standard deviation. Use visit time to represent longitudinal progression within each eye. | H1; Methods, Statistical analysis; main-text Fig. 2 legend. |
| M1 | M | Model MD at each visit as the outcome. Fixed effects include time, age, CCT, mean IOP over the observation window, basal OCR, and their interactions with time. Include eye-level random slopes and nested eye/patient random intercepts to account for repeated measurements within eyes and bilateral eyes within patients. The OCR×time term answers Q1. | H1 and D2. |
| E3 | E | In the full cohort, basal OCR×time β=0.186 (s.e. 0.035, P<0.001) dB yr^-1 per 1 s.d. OCR, with a normal-approximation 95% CI of 0.1174–0.2546. 1 s.d. of basal OCR is approximately 4.3 pmol min^-1 per 100,000 cells. | M1; Supplementary Table 5 and main-text Fig. 2. |
| E4 | E | In the same model, age×time β=-0.090 (s.e. 0.029, P=0.002), mean IOP×time β=-0.069 (s.e. 0.034, P=0.042), and CCT×time β=0.008 (s.e. 0.033, P=0.82). The authors report partial R^2 values for progression rate of 0.13 for basal OCR and 0.01 for mean IOP. | M1; Supplementary Table 5 and main-text Results. |
| C1 | C | Lower basal OCR is associated with faster visual-field deterioration (more negative MD change); higher OCR corresponds to slower loss. This association remains after adjustment for age, CCT, and mean IOP during treatment. | E3 and E4. |
| C2 | C | Basal OCR is an important biomarker associated with the rate of visual-field progression in the treated cohort. This observational association does not establish causality. | E3 and E4; Discussion and limitations. |
| H2 | H | NTG and HTG differ in their pressure context, so assess whether the basal OCR association is confined to one diagnostic group. | E1; task-card `glaucoma_type`. |
| M2 | M | Repeat M1 separately in the NTG and HTG subsets, standardizing continuous covariates within each subset. | H2. |
| E5 | E | NTG: basal OCR×time β=0.176 (s.e. 0.047, P<0.001). HTG: β=0.197 (s.e. 0.061, P=0.002). | M2; Supplementary Tables 6–7 and main-text Fig. 2. |
| C3 | C | The association between basal OCR and visual-field progression has the same direction and a similar magnitude in NTG and HTG. | E5. |
| H3 | H | Basal OCR is the primary measure, but the Mito Stress assay also provides ATP-linked OCR, maximal OCR, and spare capacity. If these capture the same respiratory phenotype, their associations should have consistent directions. | E3; task-card data dictionary. |
| M3 | M | In the full cohort, replace basal OCR in turn with ATP-linked OCR, maximal OCR, and spare capacity, retaining the other M1 settings. | H3. |
| E6 | E | ATP-linked OCR×time β=0.199 (s.e. 0.034, P<0.001); maximal OCR β=0.123 (s.e. 0.036, P=0.001); spare capacity β=0.108 (s.e. 0.036, P=0.003). | M3; Supplementary Table 5. |
| C4 | C | Higher values of multiple OCR measures are associated with slower VF MD loss, supporting a result that is not restricted to basal OCR alone. | E6. |
| H4 | H | Treatment can alter the apparent association between IOP and progression. Check whether the OCR result depends on the IOP summary used or varies with IOP level. | E4; study background. |
| M4 | M | Repeat the OCR model, replacing mean IOP in turn with peak IOP, the standard deviation of IOP across visits, and relative IOP reduction. | H4. |
| E7 | E | Basal OCR×time is 0.190 (s.e. 0.034), 0.184 (s.e. 0.034), and 0.184 (s.e. 0.036) with peak IOP, IOP variability, and relative reduction, respectively; all P<0.001. | M4; Supplementary Tables 9–11. |
| M5 | M | Add a time×basal OCR×mean IOP three-way interaction in the full cohort to test whether IOP level modifies the association between OCR and progression. | H4. |
| E8 | E | The mean IOP×OCR progression term for basal OCR has β=0.001 (s.e. 0.031, P=0.98); the main text reports P=0.97 for the three-way interaction. | M5; Supplementary Table 8 and main-text Results. |
| C5 | C | There is no evidence that the OCR–visual-field progression association varies with IOP level. The authors interpret their contributions as approximately additive. | E8. |
| H5 | H | Some patients have a long interval between OCR measurement and the visual-field observation window and have undergone surgery. Test whether surgery or the measurement interval explains the primary association. | Timing and censoring structure in the task card. |
| M6 | M | Repeat the OCR model separately in groups with and without subsequent surgery, and examine surgery-status terms. | H5. |
| E9 | E | Basal OCR×time is 0.115 (s.e. 0.046, P<0.001) in the surgery group and 0.282 (s.e. 0.047, P<0.001) in the group without surgery. The main text separately reports P=0.97 for the test of OCR and surgery status. | M6; Supplementary Tables 12–14 and main-text Results. |
| C6 | C | The authors regard the direction as consistent across groups and consider surgery/the measurement interval insufficient to explain the overall OCR association. Numerical differences between groups should be presented as sensitivity results rather than causal effects. | E9. |
| H6 | H | NAD is available for only a few patients, so sample size may limit precision in the NAD–progression branch. | Missing-data structure. |
| M7 | M | Estimate NAD×time in the small subset with both NAD and visual-field data, and examine basal OCR×time in the same subset. | H6. |
| E10 | E | NAD×time β=0.44 (s.e. 0.37) dB yr^-1 per 1 s.d. NAD, P=0.25. In the same subset, basal OCR×time β=0.14 (s.e. 0.09), P=0.12. | M7; main-text Results. |
| C7 | C | The small NAD subset provides insufficient evidence to establish an association of NAD or basal OCR with VF MD progression. Nonsignificance must not be interpreted as absence of an effect. | E10. |

## Notes

- The paper's tables report estimates and s.e. values without printing every numerical confidence interval. The 95% CIs in P* and the anchors were calculated as `estimate ± 1.96 × s.e.`; the horizontal lines in Fig. 2 are also labeled as 95% CIs.
