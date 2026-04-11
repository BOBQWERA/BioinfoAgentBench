# Benchmark Standard Schema

All standardized benchmark files in this folder follow the same top-level and record-level structure.

## Top-level structure
- `benchmark` (string): benchmark name
- `schema_version` (string): schema version
- `records` (array): normalized records

## Record structure
- `id` (string): original benchmark id, preserved
- `question` (string): task question/prompt
- `data` (array): normalized data entries, each item has:
  - `type` (string): data field source name
  - `value` (string): normalized content
- `answer` (string): expected answer/output converted to string
- `has_file` (boolean): whether the original sample contains file-like references
- `metadata` (object): original metadata, preserved as-is

## Rules
- `environment` is removed.
- `expected_output` is moved into `answer`.
- Nested `input` lists are flattened into multiple entries inside `data`.
- Benchmark-specific rules are applied where needed (for example, path rewriting or moving distractors to metadata).
