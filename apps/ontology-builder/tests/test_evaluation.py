"""The evaluation of the pet manuals against the answer key (T21: AC-33, AC-11/AC-13 scoring).

The live command is not a gate (FR-38). Here the scoring runs on a replayed run: pass 1 of each
manual replays the curated fixtures; pass 2 of each single-manual run has no fixture, so the pet
client answers it with no synonym groups. The leash/lead items are therefore also scored on a
dataset built from the curated three-manual pass 2 fixture.
"""

from __future__ import annotations

import builtins
import io
import pathlib
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
import yaml
from ontology_builder import evaluation
from ontology_builder.cli import make_app
from ontology_builder.model import (
    FixedClock,
    ScopeRecord,
    UlidMinter,
    validate_element,
    validate_record,
)
from ontology_builder.store import DatasetStore
from ontology_builder.workflows import Workspace
from typer.testing import CliRunner

APP = Path(__file__).resolve().parents[1]
REPO = APP.parents[1]
AT = datetime(2026, 11, 21, 12, 0, tzinfo=UTC)
REPORT_NAME = "2026-11-21-claude-opus-5-5.md"


class Clients:
    """Makes pet clients and counts every LLM call they get."""

    def __init__(self, pet_kit: Any) -> None:
        self.pet_kit = pet_kit
        self.made: list[Any] = []

    def __call__(self) -> Any:
        self.made.append(self.pet_kit.client())
        return self.made[-1]

    @property
    def calls(self) -> int:
        return sum(client.calls for client in self.made)

    @property
    def scripted_titles(self) -> set[str]:
        return {r.schema.get("title") for c in self.made for r in c.scripted}


def _store(data_dir: Path, name: str) -> DatasetStore:
    clock = FixedClock(AT)
    return DatasetStore(
        data_dir, name, clock=clock, minter=UlidMinter(clock, lambda n: b"\x11" * n)
    )


def _workspace(tmp_path: Path, pet_kit: Any) -> tuple[Workspace, Clients]:
    clients = Clients(pet_kit)
    workspace = Workspace(
        data_dir=tmp_path / "data",
        work_dir=tmp_path / "work",
        llm=clients,
        sources_root=pet_kit.manuals_root,
        open_store=_store,
    )
    return workspace, clients


def _key() -> dict[str, Any]:
    data: dict[str, Any] = yaml.safe_load(evaluation.ANSWER_KEY.read_text(encoding="utf-8"))
    return data


def _key_items() -> set[str]:
    key = _key()
    items = {i["id"] for s in ("ignorable", "kept", "concepts", "rules", "traps") for i in key[s]}
    return items | {"leash-lead-synonym", "lead-senses", "lead-rule-on-leash"}


@pytest.fixture(scope="module")
def replayed(tmp_path_factory: pytest.TempPathFactory, pet_kit: Any) -> Any:
    tmp = tmp_path_factory.mktemp("eval")
    workspace, clients = _workspace(tmp, pet_kit)
    result = evaluation.evaluate(workspace, lambda _estimate: True, reports_dir=tmp / "reports")
    assert result is not None
    return result, clients, tmp


def _by_item(scores: list[Any]) -> dict[str, Any]:
    return {score.item: score for score in scores}


# ---------- the replayed run and its report (AC-33) ----------


def test_eval_scope_is_the_frozen_pet_scope(pet_kit: Any) -> None:
    """The fixtures' request hashes cover the scope record, so the evaluation uses PET_SCOPE."""
    assert pet_kit.scope == evaluation.SCOPE


def test_report_scores_each_answer_key_item(replayed: Any) -> None:
    result, clients, tmp = replayed
    assert clients.scripted_titles <= {"TermResolutionOutput"}, "pass 1 replays the fixtures"
    assert result.model == "claude-opus-5-5"
    assert [run.status for run in result.runs] == ["completed"] * 3
    assert result.report == tmp / "reports" / REPORT_NAME
    report = result.report.read_text(encoding="utf-8")
    assert report.startswith("# Evaluation 2026-11-21 · claude-opus-5-5")
    scored = {score.item for score in result.scores}
    assert scored == _key_items()
    for item in scored:
        assert re.search(rf"\| `{re.escape(item)}` \| (pass|FAIL) \|", report), item
    assert f"| **Total** | **{result.passed} / {result.total}** |" in report


def test_replayed_run_scores_the_ignorable_passages_and_the_traps(replayed: Any) -> None:
    result, _, _ = replayed
    for score in result.scores:
        if score.section in ("ignorable", "kept", "traps"):
            assert score.passed, f"{score.item}: {score.detail}"
    by_item = _by_item(result.scores)
    assert by_item["lead-at-most-2-m"].passed
    assert by_item["dog"].passed and by_item["house-management"].passed


def test_declined_estimate_runs_nothing(tmp_path: Path, pet_kit: Any) -> None:
    workspace, clients = _workspace(tmp_path, pet_kit)
    shown: list[Any] = []

    def decline(estimate: Any) -> bool:
        shown.append(estimate)
        return False

    assert evaluation.evaluate(workspace, decline, reports_dir=tmp_path / "reports") is None
    [estimate] = shown
    assert estimate.documents == 37 and estimate.units > 0 and estimate.input_tokens > 0
    assert clients.calls == 0
    assert not (tmp_path / "reports").exists()


# ---------- the leash/lead items on the curated pass 2 (AC-11 scoring) ----------


def _seed(store: DatasetStore, pet_extraction: Any, elements: list[Any]) -> None:
    with store.transaction() as files:
        for corpus in pet_extraction.corpora:
            files.write_corpus(corpus.folder, corpus.corpus)
            for item in corpus.documents:
                files.write_document(corpus.folder, item.document)
                files.write_units(corpus.folder, item.document.id, item.units)
        for element in elements:
            files.write_element(element)


def _scores(tmp_path: Path, pet_extraction: Any, elements: list[Any]) -> dict[str, Any]:
    store = _store(tmp_path, "pets-and-house-rules")
    store.create(validate_record(ScopeRecord, evaluation.SCOPE))
    _seed(store, pet_extraction, elements)
    key = evaluation.load_answer_key(evaluation.ANSWER_KEY)
    return _by_item(evaluation.score(key, store.read()))


def test_leash_lead_scored_on_the_resolved_pets(
    tmp_path: Path, pet_extraction: Any, pet_kit: Any
) -> None:
    resolved = pet_kit.resolve(pet_kit.replay(), pet_extraction)
    scores = _scores(tmp_path, pet_extraction, resolved.elements)
    for item in ("leash-lead-synonym", "lead-senses", "lead-rule-on-leash"):
        assert scores[item].passed, f"{item}: {scores[item].detail}"


def test_leash_lead_synonym_fails_without_pass_2(tmp_path: Path, pet_extraction: Any) -> None:
    scores = _scores(tmp_path, pet_extraction, pet_extraction.elements)
    assert not scores["leash-lead-synonym"].passed


def test_traps_and_ignorable_fail_when_the_story_is_used(
    tmp_path: Path, pet_extraction: Any
) -> None:
    [bodza] = [
        unit.id
        for unit in pet_extraction.units.values()
        if unit.text.startswith("I still remember the rainy October evening")
    ]
    concept = validate_element(
        "concept",
        {
            "id": "cn_01JDK7F3Q8ZX5N6M2W4R9T0BDZ",
            "label": "Bodza",
            "definition": "A shelter dog who lived thirteen years.",
            "level": "level-3",
            "level_reason": "anecdote",
            "status": "proposed",
            "evidence": [{"unit": bodza}],
            "origin": {"kind": "llm", "created_at": "2026-11-21T12:00:00Z"},
        },
    )
    scores = _scores(tmp_path, pet_extraction, [*pet_extraction.elements, concept])
    assert not scores["no-bodza-concept"].passed
    assert not scores["thirteen-years-not-lifespan-evidence"].passed
    assert not scores["dog-1-bodza"].passed
    assert "cited by" in scores["dog-1-bodza"].detail


# ---------- the answer key stays out of ingestion (AC-33) ----------


def test_ingestion_never_opens_answer_key(
    tmp_path: Path, pet_kit: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace, clients = _workspace(tmp_path, pet_kit)
    key = evaluation.ANSWER_KEY.resolve()
    opened_at: list[int] = []

    def spy(original: Any) -> Any:
        def wrapper(file: Any, *args: Any, **kwargs: Any) -> Any:
            if isinstance(file, (str, Path)) and Path(file).resolve() == key:
                opened_at.append(clients.calls)
            return original(file, *args, **kwargs)

        return wrapper

    monkeypatch.setattr(builtins, "open", spy(builtins.open))
    monkeypatch.setattr(io, "open", spy(io.open))
    original_path_open = pathlib.Path.open

    def path_open(self: Path, *args: Any, **kwargs: Any) -> Any:
        if self.resolve() == key:
            opened_at.append(clients.calls)
        return original_path_open(self, *args, **kwargs)

    monkeypatch.setattr(pathlib.Path, "open", path_open)

    result = evaluation.evaluate(workspace, lambda _e: True, reports_dir=tmp_path / "reports")

    assert result is not None and clients.calls > 0
    assert opened_at, "the answer key is read for the scoring"
    assert min(opened_at) == clients.calls, "the answer key is opened only after the last call"


_KEY_PATTERNS = ("pet-manuals-corpus", "answer-key", "answer_key")


def test_only_evaluation_mentions_answer_key_path() -> None:
    src = APP / "src" / "ontology_builder"
    offenders = []
    for path in sorted(src.rglob("*")):
        if not path.is_file() or path.suffix not in {".py", ".yaml", ".j2", ".md", ".json"}:
            continue
        if (src / "evaluation") in path.parents:
            continue
        text = path.read_text(encoding="utf-8")
        offenders += [f"{path.relative_to(APP)}: {p}" for p in _KEY_PATTERNS if p in text]
    for path in sorted((APP / "tests" / "fixtures" / "llm").glob("*.json")):
        if "pet-manuals-corpus" in path.read_text(encoding="utf-8"):
            offenders.append(str(path.relative_to(APP)))
    assert offenders == []


# ---------- the ``eval`` command ----------


def _invoke(workspace: Workspace, *args: str, answer: str | None = None) -> Any:
    return CliRunner().invoke(make_app(lambda: workspace), ["eval", *args], input=answer)


def test_eval_command_shows_the_estimate_and_asks(tmp_path: Path, pet_kit: Any) -> None:
    workspace, clients = _workspace(tmp_path, pet_kit)
    reports = tmp_path / "reports"

    declined = _invoke(workspace, "--report-dir", str(reports), answer="n\n")

    assert declined.exit_code == 1
    for shown in ("documents", "source units", "input tokens", "cost", "nothing was run"):
        assert shown in declined.output, shown
    assert clients.calls == 0

    done = _invoke(workspace, "--report-dir", str(reports), "--yes")

    assert done.exit_code == 0, done.output
    assert "Total" in done.output and str(reports / REPORT_NAME) in done.output
    assert (reports / REPORT_NAME).is_file()
