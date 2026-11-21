"""Run the evaluation: a throw-away ontology, a confirmed ingestion, then the scoring (FR-38).

The ontology lives in a temporary data folder and is never committed. The answer key is loaded
only after the last ingestion run has finished, so nothing the LLM sees can come from it.
"""

from __future__ import annotations

import tempfile
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import yaml

from ontology_builder.evaluation.answer_key import ANSWER_KEY, REPO_ROOT, load_answer_key
from ontology_builder.evaluation.report import ReportInput, write_report
from ontology_builder.evaluation.score import Score, score
from ontology_builder.workflows import (
    ScratchEstimate,
    ScratchRun,
    Workspace,
    actor_of,
    create_scratch,
)

NAME = "pets-and-house-rules"
MANUALS = tuple(
    f"user-manuals-pets-and-house-rules/{name}"
    for name in ("dog-owners-manual", "cat-owners-manual", "building-and-house-rules")
)
"""The three manuals, each ingested as its own corpus, in this order."""
REPORTS_DIR = REPO_ROOT / "apps" / "ontology-builder" / "docs" / "evaluations"
EVALUATOR = actor_of("evaluation", "domain_admin")


def _scope() -> dict[str, Any]:
    data: dict[str, Any] = yaml.safe_load(
        Path(__file__).with_name("pet_scope.yaml").read_text(encoding="utf-8")
    )
    return data


SCOPE = _scope()


@dataclass(frozen=True)
class EvaluationResult:
    model: str
    estimate: ScratchEstimate
    runs: list[ScratchRun]
    scores: list[Score]
    report: Path

    @property
    def passed(self) -> int:
        return sum(s.passed for s in self.scores)

    @property
    def total(self) -> int:
        return len(self.scores)


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def evaluate(
    workspace: Workspace,
    confirm: Callable[[ScratchEstimate], bool],
    *,
    reports_dir: Path = REPORTS_DIR,
    answer_key: Path = ANSWER_KEY,
) -> EvaluationResult | None:
    """Estimate, ask ``confirm``, ingest the manuals, score and write the dated report.

    The manuals are read from the workspace's sources root; the ontology is made in a temporary
    folder. Returns ``None`` when the estimate is declined: then no LLM answer was asked for.
    """
    with tempfile.TemporaryDirectory(prefix="ontology-builder-eval-") as tmp:
        scratch_workspace = replace(
            workspace,
            data_dir=Path(tmp) / "data",
            work_dir=Path(tmp) / "work",
            sources_root=workspace.sources(),
        )
        scratch = create_scratch(scratch_workspace, NAME, SCOPE, EVALUATOR)
        estimate = scratch.estimate(EVALUATOR, MANUALS)
        if not confirm(estimate):
            return None
        runs = scratch.ingest(EVALUATOR, MANUALS, confirm=True)
        key = load_answer_key(answer_key)  # only now, after the last LLM call
        scores = score(key, scratch.store.read())
        day = scratch.store.clock.now().date()
    data = ReportInput(day, scratch.model, estimate, runs, scores, _relative(answer_key))
    report = write_report(reports_dir, data)
    return EvaluationResult(scratch.model, estimate, runs, scores, report)
