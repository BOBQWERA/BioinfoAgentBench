# Data dictionary

## File and structure

`longitudinal_observations.csv` is a UTF-8 CSV with variable names in the first row and empty fields for missing values. Each row records one eye at one standard automated visual-field examination.

- Hierarchy: 139 patients (`patient_id`) → 229 eyes (`eye_id`) → 2,310 visits.
- Groups: 144 eyes from 85 NTG patients and 85 eyes from 54 HTG patients.
- Repeats: each patient contributes 1–2 eyes; each eye has 6–20 visual-field examinations. Patient- and eye-level variables repeat across the relevant visit rows; these rows do not represent additional participants.
- Time: `visit_time_years=0` is the eye's first visual-field examination included in this file. Later times are years since that examination, at irregular intervals. Each eye spans approximately 3.0–16.2 years.
- Censoring: for eyes that subsequently underwent glaucoma surgery, the visual-field observation window ends before the date of listing for surgery. The eye-level `glaucoma_surgery` field identifies this situation. Other eyes are observed through their last available visual-field visit.
- Measurement levels: OCR, NAD, demographics, systemic conditions and systemic medications are patient-level; central corneal thickness, ocular treatment and ocular status at OCR testing are eye-level; intraocular pressure, MD, drop count, age and time are visit-level. Patient- and eye-level values repeat in the long table.
- Timing: OCR is not a prospective baseline measurement. For surgical patients, OCR testing may occur after the visual-field observation window; for nonsurgical patients, it is usually near the end of that window. The file does not provide the OCR test date.
- Missingness: `visual_acuity_at_ocr_assay`, `iop_at_ocr_assay_mmhg` and `lens_status` each lack 7 rows, representing repeated rows for the same eye. `visit_iop_mmhg` is missing for 14 visits. The two NAD columns have values for only 21 patients, appearing as 286 nonempty rows because of the long format. Other columns are complete.

## Identifiers, groups and visits

| Variable | Type | Unit / values | Definition |
|---|---|---|---|
| `patient_id` | string | 139 pseudonymous identifiers | Patient ID, shared by both eyes of the same patient. |
| `eye_id` | string | 229 pseudonymous identifiers | Eye ID, nested within `patient_id`. |
| `visit_index` | integer | 1–20 | Within-eye visit order after sorting by `visit_time_years`. |
| `glaucoma_type` | category | `NTG`, `HTG` | Primary open-angle glaucoma category: NTG denotes pretreatment pressure no greater than 21 mmHg; HTG denotes pretreatment pressure at least 21 mmHg. |
| `eye_laterality` | category | `left`, `right` | Left or right eye. |
| `visit_time_years` | numeric | years; 0–16.2355 | Time since the eye's first included visual-field examination. |

## Mitochondrial and NAD measures: patient level

Unless otherwise stated, OCR units are pmol O2 min^-1 per 100,000 cells. These summarize a patient's single PBMC Mito Stress assay and repeat across all of that patient's eyes and visits.

| Variable | Type | Range / values | Definition |
|---|---|---|---|
| `basal_ocr` | numeric | 8.9712–30.9726 | Basal OCR. |
| `atp_linked_ocr` | numeric | 8.5048–26.0880 | ATP-linked OCR. |
| `maximal_ocr` | numeric | 31.5325–208.3887 | Maximal OCR. |
| `reserve_capacity` | numeric | 22.5613–184.9427 | Respiratory reserve capacity. |
| `proton_leak` | numeric | 0–7.0025 | Proton-leak-associated OCR. |
| `coupling_efficiency_pct` | numeric | 70.4760–105.1818 | Coupling efficiency, percent. A few experimental values above 100 occur in the source and have not been truncated. |
| `nad_assay_date` | date/string | `YYYY-MM-DD`; 13 dates | Total NAD assay date; empty if no assay was performed. |
| `nad_pg_per_mg_protein` | numeric | pg NAD per mg protein; 0.0823–1.2710 | Total PBMC NAD; measured in only 21 patients. |

## Visual field, intraocular pressure and ocular variables

| Variable | Level / type | Unit / range or values | Definition |
|---|---|---|---|
| `visual_field_md_db` | Visit-level numeric | dB; -27.06–3.37 | MD from 24-2 SITA standard perimetry; more negative values indicate worse function. |
| `visit_iop_mmhg` | Visit-level numeric | mmHg; 6–31 | Goldmann applanation pressure at the visit; 14 rows are empty. |
| `visit_drop_count` | Visit-level integer | 0–4 | Number of pressure-lowering eye-drop types used at the visit. |
| `visit_age_years` | Visit-level numeric | years; 31.6–89.5 | Age at the visit. |
| `central_corneal_thickness_um` | Eye-level numeric | µm; 289–667 | Central corneal thickness. |
| `iop_at_diagnosis_mmhg` | Eye-level numeric | mmHg; 10–38 | Intraocular pressure at diagnosis. |
| `maximum_pretreatment_iop_mmhg` | Eye-level numeric | mmHg; 13–42 | Highest recorded pretreatment pressure. |
| `glaucoma_surgery` | Eye-level category | `yes`, `no` | Whether the eye underwent glaucoma surgery after its corresponding visual-field observation window. |
| `selective_laser_trabeculoplasty` | Eye-level category | `yes`, `no` | Whether the eye underwent selective laser trabeculoplasty. |
| `drop_count_at_ocr_assay` | Eye-level integer | 0–4 | Number of pressure-lowering eye-drop types at OCR testing. |
| `visual_acuity_at_ocr_assay` | Eye-level string | Numeric strings, `PL`, `NPL`; 7 empty rows | Source visual-acuity record at OCR testing. The data archive does not further specify the numerical scale. `PL`/`NPL` mean perception/no perception of light. |
| `iop_at_ocr_assay_mmhg` | Eye-level numeric | mmHg; 2–28; 7 empty rows | Intraocular pressure at OCR testing. |
| `lens_status` | Eye-level category | `iol`, `phakic`; 7 empty rows | Lens status: `iol` means intraocular lens; `phakic` means a natural lens is present. |
| `prostaglandin_analogue_drops` | Eye-level category | `yes`, `no` | Prostaglandin-analogue eye-drop use at OCR testing. |
| `carbonic_anhydrase_inhibitor_drops` | Eye-level category | `yes`, `no` | Carbonic-anhydrase-inhibitor eye-drop use at OCR testing. |
| `topical_beta_blocker_drops` | Eye-level category | `yes`, `no` | Topical beta-blocker use at OCR testing. |
| `alpha2_agonist_drops` | Eye-level category | `yes`, `no` | Alpha2-agonist eye-drop use at OCR testing. |

## Demographics, systemic conditions and medications: patient level

| Variable | Type | Unit / range or values | Definition |
|---|---|---|---|
| `sex` | category | `Female`, `Male` | Recorded sex. |
| `family_history_glaucoma` | category | `yes`, `no` | Family history of glaucoma. |
| `smoking` | category | `yes`, `no` | Smoking record; the archive does not distinguish current from former smoking. |
| `alcohol_use` | category | `yes`, `no` | Alcohol-use record. |
| `diabetes` | category | `yes`, `no` | Diabetes. |
| `hypertension` | category | `yes`, `no` | Systemic hypertension. |
| `hypercholesterolemia` | category | `yes`, `no` | Hypercholesterolemia. |
| `migraine` | category | `yes`, `no` | Migraine. |
| `vasospasm` | category | `yes`, `no` | History of vasospasm. |
| `systemic_disease_count` | integer | 0–5 | Number of recorded systemic diseases. |
| `bmi_kg_m2` | numeric | kg m^-2; 17.1468–40.4040 | Body mass index. |
| `age_at_diagnosis_years` | numeric | years; 24.1–81.7 | Age at glaucoma diagnosis. |
| `vitamin_d_supplement` | category | `yes`, `no` | Vitamin D supplementation. |
| `thyroid_disease` | category | `yes`, `no` | Thyroid disease. |
| `ace_inhibitor` | category | `yes`, `no` | ACE-inhibitor use. |
| `angiotensin_receptor_blocker` | category | `yes`, `no` | Angiotensin-receptor-blocker use. |
| `systemic_beta_blocker` | category | `yes`, `no` | Systemic beta-blocker use. |
| `calcium_channel_blocker` | category | `yes`, `no` | Calcium-channel-blocker use. |
| `diuretic` | category | `yes`, `no` | Diuretic use. |
