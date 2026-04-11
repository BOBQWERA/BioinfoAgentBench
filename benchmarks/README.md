# Benchmarks

This directory separates released benchmark assets by role.

## Layout

- `source_collections/`: source-format benchmark subsets preserved for public release
- `standardized/`: unified JSON schema used by the PARE evaluation utilities
- `fingerprint/`: curated upgrade packs used for Fingerprint Tier capability fingerprinting
- `frontier/`: Frontier Tier curation metadata

## Validation

Run:

```bash
biab-validate
```

## Manifest

Generate a benchmark inventory:

```bash
biab-manifest --output benchmarks/manifest.json
```

## Notes

- Standardized files preserve original record IDs.
- Source collections in this release are the curated public subset available for
  distribution, not the full manuscript-scale raw corpus.
- Fingerprint upgrade packs are stored separately because they are transformed question
  sets for the Fingerprint Tier, not original source collections.
