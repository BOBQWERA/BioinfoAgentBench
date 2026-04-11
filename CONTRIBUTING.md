# Contributing

This repository is organized as a release snapshot rather than an active monorepo. Keep
changes scoped, reproducible, and easy to audit.

## Before opening a pull request

1. Install the repository in editable mode: `pip install -e .[dev]`
2. Run `pytest`
3. Run `biab-validate`
4. If you changed supplementary-table scripts, rebuild the affected outputs under `paper/supplementary/`

## Expectations

- Keep paths ASCII unless an upstream source filename must be preserved.
- Do not add secrets, internal hosts, or unpublished raw data.
- Preserve benchmark record IDs and source provenance.
- Prefer additive changes over rewriting released artifacts.

## Review scope

Pull requests should state:

- which tier assets changed,
- whether any benchmark JSON was regenerated,
- whether paper results were updated,
- and which validation commands were run.
