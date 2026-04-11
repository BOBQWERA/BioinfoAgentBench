from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def standardized_benchmarks_dir() -> Path:
    return repo_root() / "benchmarks" / "standardized"


def source_collections_dir() -> Path:
    return repo_root() / "benchmarks" / "source_collections"


def fingerprint_dir() -> Path:
    return repo_root() / "benchmarks" / "fingerprint"


def output_dir() -> Path:
    return repo_root() / "outputs" / "pare_eval"


def templates_dir() -> Path:
    return repo_root() / "src" / "bioinfoagentbench" / "templates"
