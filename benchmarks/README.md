# BioinfoAgentBench

Task definitions and evaluation materials for **810 Baseline tasks**, **100 Fingerprint tasks**, and **5 Frontier cases**.

```text
benchmarks/
├── README.md
├── baseline/
│   ├── tasks.jsonl          # Questions, input descriptions, deliverables and verification rules
│   └── pilot_ids.txt        # The 100 tasks used in the pilot
├── fingerprint/
│   ├── tasks.jsonl          # Questions, input descriptions, deliverables and verification rules
│   ├── loads.jsonl          # Calibrated P1–E2 task loads
│   └── load_rubric.json     # Definitions and criteria for load levels 0–5
└── frontier/
    ├── tasks.jsonl          # Case descriptions and source publications
    └── FR-0001/ … FR-0005/
        ├── task.md
        ├── data/
        └── evaluation/
```

Each line in a `.jsonl` file is one record. Use `task_id` to connect tasks with their load annotations and evaluation results.

## Baseline

[tasks.jsonl](baseline/tasks.jsonl) contains 810 tasks across 21 subjects. Each task includes its instruction, input description, expected deliverable and verification rules. [pilot_ids.txt](baseline/pilot_ids.txt) lists the 100 tasks used in the pilot.

Input filenames are given in `input_context` and the instruction. Reference outputs used for scoring are named in `verification_rules`. A `/workdir/` prefix denotes the original task's container path.

Tasks come from [AutoBA](https://github.com/JoshuaChou2018/AutoBA), [BioChatter](https://github.com/biocypher/biochatter), [BioMed-AQA](https://huggingface.co/datasets/BOBQWERA/biomed-aqa-dataset), [Biomni-Eval](https://huggingface.co/datasets/biomni/Eval1), [BixBench](https://huggingface.co/datasets/futurehouse/BixBench), [LAB-Bench](https://github.com/Future-House/LAB-Bench), and [BioDSBench](https://github.com/RyanWangZf/BioDSA). Source task IDs are retained in each record.

`verification_method` indicates whether the task primarily needs deterministic result checks (`automated_scoring`) or also requires review of a graphical deliverable (`human_judgment`).

## Fingerprint

[tasks.jsonl](fingerprint/tasks.jsonl) contains 100 tasks for evaluating PARE capabilities.

The task instruction already contains any supplied experience. Input filenames appear in the instruction or `input_context`. Fingerprint input data will be provided separately.

[loads.jsonl](fingerprint/loads.jsonl) records calibrated task loads for eight capability subdimensions on a **0–5** scale in `loads_used`. [load_rubric.json](fingerprint/load_rubric.json) contains load definitions, criteria and examples.

## Frontier

| ID | Case |
|---|---|
| FR-0001 | Postprandial glycemic responses and metabolic physiology |
| FR-0002 | Doxycycline prophylaxis and the gut resistome and microbiome |
| FR-0003 | Felzartamab and kidney-transplant rejection |
| FR-0004 | PBMC respiration and glaucoma progression |
| FR-0005 | Streptococcal antibodies and infection or carriage |

Each case includes an English translation of the pilot instruction in `task.md`, curated inputs in `data/`, and evaluation references in `evaluation/`. Paths in the catalogue are relative to `benchmarks/`.

Evaluation materials include reference analytical paths, findings and numerical anchors with their tolerances and weights.

## Using the tasks

For Baseline and Fingerprint, give the agent the instruction, input description, deliverable requirements and input files. Keep verification rules, reference outputs and load ratings with the evaluator. For Frontier, give the agent only `task.md` and `data/`.

All Frontier inputs are included. Baseline and Fingerprint input data, together with Baseline reference outputs, will be provided separately. Source data retain their original providers' terms.
