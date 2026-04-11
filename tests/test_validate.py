from __future__ import annotations

from bioinfoagentbench.benchmarks.validate import validate_directory
from bioinfoagentbench.paths import standardized_benchmarks_dir


def test_standardized_directory_passes_validation() -> None:
    summaries, errors = validate_directory(standardized_benchmarks_dir())

    assert not errors
    assert len(summaries) == 16
    assert sum(item["count"] for item in summaries) == 526
