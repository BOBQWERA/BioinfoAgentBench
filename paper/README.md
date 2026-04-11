# Paper Assets

This directory keeps manuscript-facing artifacts separate from reusable benchmark code.

## Layout

- `sources/`: input spreadsheets and CSV files used to generate the committed
  supplementary artifacts
- `results/baseline/`: baseline-tier result summaries
- `results/frontier/`: frontier-tier result summaries and figure prompts
- `supplementary/`: generated supplementary tables and compact figures

## Scope

Large figure drafts and repeated workspace exports were intentionally excluded. The files
here are the minimal publication-facing assets needed to track provenance for the
committed supplementary outputs.

The public release intentionally omits the internal supplementary-table rebuild scripts
that previously lived under `scripts/paper/`.

`Table_S1.xlsx` in this snapshot originates from a curated canonical workbook because the
legacy raw workbook carries unstable mojibake labels from an earlier export step.
