from __future__ import annotations

from bioinfoagentbench.pare_eval.loader import StandardQuestionImporter
from bioinfoagentbench.paths import standardized_benchmarks_dir


def test_loader_reads_standardized_record() -> None:
    importer = StandardQuestionImporter(standardized_benchmarks_dir())

    question = importer.get_question("autoba", index=0)

    assert question.benchmark == "autoba"
    assert question.id
    assert isinstance(question.question, str)
