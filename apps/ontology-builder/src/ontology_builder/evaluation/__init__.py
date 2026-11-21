"""evaluation component.

Scores a live ingestion of the pet manuals against the answer key.

``evaluate`` creates a throw-away ontology in a temporary folder (no git, no commit), shows the
estimate to ``confirm``, ingests the three manuals and only then loads the answer key
(``docs/research/notes/pet-manuals-corpus/answer-key.yaml``) and scores each item: the ignorable
passages, the content kept next to them, the leash/lead synonym and senses, the expected concepts
and rules, and the traps. It writes the dated report
``apps/ontology-builder/docs/evaluations/YYYY-MM-DD-<model>.md``. It is not a gate (FR-38).
Only this component may refer to the answer key (AC-33).
"""

from __future__ import annotations

from ontology_builder.evaluation.answer_key import (
    ANSWER_KEY,
    AnswerKey,
    AnswerKeyError,
    load_answer_key,
)
from ontology_builder.evaluation.report import summary_lines
from ontology_builder.evaluation.run import (
    MANUALS,
    REPORTS_DIR,
    SCOPE,
    EvaluationResult,
    evaluate,
)
from ontology_builder.evaluation.score import SECTIONS, Score, score

__all__ = [
    "ANSWER_KEY",
    "MANUALS",
    "REPORTS_DIR",
    "SCOPE",
    "SECTIONS",
    "AnswerKey",
    "AnswerKeyError",
    "EvaluationResult",
    "Score",
    "evaluate",
    "load_answer_key",
    "score",
    "summary_lines",
]
