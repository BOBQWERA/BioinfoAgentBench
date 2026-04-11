# Paper Assets

This directory keeps manuscript-facing artifacts separate from reusable benchmark code.

## Layout

- `sources/`: input spreadsheets and CSV files used to build supplementary tables
- `results/baseline/`: baseline-tier result summaries
- `results/frontier/`: frontier-tier result summaries and figure prompts
- `supplementary/`: generated supplementary tables and compact figures

## Rebuild supplementary tables

```bash
python scripts/paper/build_all.py
```

## Scope

Large figure drafts and repeated workspace exports were intentionally excluded. The files
here are the minimal publication-facing assets needed to track provenance and regenerate
the committed supplementary outputs.

`Table_S1.xlsx` is rebuilt from a curated canonical workbook in this snapshot because the
legacy raw workbook carries unstable mojibake labels from an earlier export step.
