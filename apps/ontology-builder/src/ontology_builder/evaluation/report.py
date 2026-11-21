"""The dated Markdown report and the console summary of an evaluation (FR-38)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from ontology_builder.evaluation.score import SECTIONS, Score
from ontology_builder.workflows import ScratchEstimate, ScratchRun


@dataclass(frozen=True)
class ReportInput:
    day: date
    model: str
    estimate: ScratchEstimate
    runs: Sequence[ScratchRun]
    scores: Sequence[Score]
    answer_key: str
    """The answer key's path, relative to the repository."""


def _tally(scores: Sequence[Score]) -> str:
    return f"{sum(s.passed for s in scores)} / {len(scores)}"


def _cost(estimate: ScratchEstimate) -> str:
    return f"${estimate.cost_usd:.2f}" if estimate.cost_usd is not None else "unknown"


def summary_lines(scores: Sequence[Score]) -> list[str]:
    """One line per section and the total, for the console."""
    lines = [
        f"{title}: {_tally([s for s in scores if s.section == section])}"
        for section, title in SECTIONS.items()
    ]
    return [*lines, f"Total: {_tally(scores)}"]


def _escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _header(data: ReportInput) -> list[str]:
    estimate = data.estimate
    used_in = sum(run.input_tokens for run in data.runs)
    used_out = sum(run.output_tokens for run in data.runs)
    runs = ", ".join(f"`{run.run_id}` ({run.source_path}: {run.status})" for run in data.runs)
    return [
        f"# Evaluation {data.day.isoformat()} · {data.model}",
        "",
        "Live ingestion of the three pet manuals into a throw-away ontology (not committed),",
        f"scored against [`{data.answer_key}`](../../../../{data.answer_key}). Not a gate (FR-38).",
        "",
        f"- **Model:** {data.model}",
        f"- **Sources:** {estimate.documents} documents, {estimate.units} source units",
        f"- **Estimate:** {estimate.input_tokens} input tokens, up to {estimate.output_tokens}"
        f" output tokens, {_cost(estimate)}",
        f"- **Used:** {used_in} input tokens, {used_out} output tokens",
        f"- **Runs:** {runs}",
        "",
    ]


def _summary(scores: Sequence[Score]) -> list[str]:
    rows = [
        f"| {title} | {_tally([s for s in scores if s.section == section])} |"
        for section, title in SECTIONS.items()
    ]
    total = f"| **Total** | **{_tally(scores)}** |"
    return ["## Summary", "", "| Section | Score |", "|---|---|", *rows, total, ""]


def _section(title: str, scores: Sequence[Score]) -> list[str]:
    rows = [
        f"| `{s.item}` | {'pass' if s.passed else 'FAIL'} | {_escape(s.detail)} |" for s in scores
    ]
    return [f"## {title}", "", "| Item | Result | Detail |", "|---|---|---|", *rows, ""]


def render_report(data: ReportInput) -> str:
    lines = [*_header(data), *_summary(data.scores)]
    for section, title in SECTIONS.items():
        lines += _section(title, [s for s in data.scores if s.section == section])
    return "\n".join(lines)


def write_report(reports_dir: Path, data: ReportInput) -> Path:
    """Write ``<reports_dir>/YYYY-MM-DD-<model>.md`` and return its path."""
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{data.day.isoformat()}-{data.model}.md"
    path.write_text(render_report(data), encoding="utf-8")
    return path
