from __future__ import annotations

from bioinfoagentbench.benchmarks.manifest import build_manifest
from bioinfoagentbench.paths import standardized_benchmarks_dir


def test_manifest_counts_match_snapshot() -> None:
    manifest = build_manifest(standardized_benchmarks_dir())

    assert manifest["benchmark_count"] == 16
    assert manifest["record_count"] == 526
    assert manifest["benchmarks"][0]["benchmark"] == "autoba"
