# Scientific question

In the supplied sequencing subset of the randomized DoxyPEP trial, does doxycycline exposure over 6 months change the gut antimicrobial resistome and bacterial microbiome in rectal samples, and if so, in what direction and by how much?

## Background (knowledge cutoff: 2024-10-02)

Several randomized controlled trials have shown that doxycycline post-exposure prophylaxis after sex (doxy-PEP) reduces bacterial sexually transmitted infections in certain high-risk populations. Antimicrobial exposure may also alter human microbial ecology and select for resistance genes. Its effects on commensal communities and the antimicrobial resistome therefore need assessment before wider implementation. Previous evidence on the effects of long-term doxycycline exposure on the gut microbiome has been limited and inconsistent, and effects on resistance genes and their active expression have not been systematically evaluated.

The original clinical trial enrolled participants assigned male at birth, aged at least 18 years, who had been diagnosed with gonorrhea, chlamydia or early syphilis in the previous 12 months and were either taking HIV pre-exposure prophylaxis or living with HIV. Participants were randomized 2:1 to doxy-PEP or standard care. The doxy-PEP group was advised to take 200 mg doxycycline within 72 hours after condomless sex, no more than once per 24 hours. The standard-care group received no postcoital prophylaxis. Both groups collected their own rectal swabs at enrollment and month 6.

## Data

Use only the standardized files in `data/`. Full field definitions, units, missing-value conventions and data structures are in `data/README.md`.

This sequencing subset is not a simple random sample of the full trial. Standard-care participants were sampled randomly, while doxy-PEP selection prioritized participants reporting higher use who had available samples. Primary inference should therefore be limited to the supplied sequencing subset. Some participants have only one time point or one assay type; repeated measurements within a participant are identified by `participant_id`.

## Submission

Please provide:

1. A report that first defines the primary estimand (outcome, contrast, population and scale), then lists the claims. Each claim should state its direction, point estimate and uncertainty.
2. A separate list of up to three extension findings, explaining how each deepens the main conclusion or explains differences under alternative analytical settings.
3. A complete submission under `/workspace/submission/` containing:
   - `report.md`
   - `run.sh`
   - `src/`
   - `artifacts/`
   - `evidence.tsv`

`run.sh` must be the sole execution entry point. It must regenerate every numerical artifact cited in the report using only the public `data/` files and print those values in its execution output. Each tab-delimited row of `evidence.tsv` must record `claim_id`, `value_as_reported`, `artifact_path` and `locator`.

Do not use the original article, author code or internet materials. Complete the analysis using only the task card and `data/`.
