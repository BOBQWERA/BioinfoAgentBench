from __future__ import annotations

from bioinfoagentbench.benchmarks.standardize import normalize_record


def test_normalize_record_rewrites_biomed_aqa_input_paths() -> None:
    record = {
        "id": "sample",
        "question": "Run the task.",
        "data": {
            "input_files": [{"path": "downloaded_files/index_0001/files/example.csv"}],
            "expected_output": {"value": 1},
        },
        "metadata": {},
    }

    normalized = normalize_record(record, "biomed_aqa")

    assert normalized["data"] == [
        {"type": "input", "value": "biomed_aqa/downloaded_files/index_0001/files/example.csv"}
    ]
    assert normalized["answer"] == '{"value": 1}'
