"""A later run extends the concepts and terms already in the ontology (T36, ADR-0012, Q61).

Two corpora, ingested in two runs: the first names the dog, the second says that every pet is a
dog or a cat. Pass 2 of the second run merges its "dog" into the first run's "dog"; the parent
"pet" and the new evidence must reach the existing dog, with an ``extend`` decision.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
from ontology_builder.ingestion import (
    IngestionFailedError,
    Who,
    WriteHooks,
    plan_ingestion,
    resume_run,
    start_run,
)
from ontology_builder.llm import LlmRequest, LlmResponse, heuristic_tokens
from ontology_builder.model import Concept, Role, ScopeRecord, Term, validate_record
from ontology_builder.store import DatasetStore

MODEL = "claude-test"
WHO = Who("alice", Role.user)
_UNIT = re.compile(r"^\[U(\d+)\]", re.MULTILINE)
_CONCEPT = re.compile(r"^\[(C\d+)\] (\w+).*?(already in the ontology)?\)?$", re.MULTILINE)


def _candidate(key: str, label: str, unit: str, **extra: Any) -> dict[str, Any]:
    return {
        "key": key,
        "label": label,
        "evidence": [unit],
        "level": "level-1",
        "level_reason": "core",
    } | extra


def _concepts_answer(prompt: str) -> dict[str, Any]:
    units = [f"U{n}" for n in _UNIT.findall(prompt)]
    first = units[0]
    concepts = [_candidate("c.dog", "dog", first)]
    terms = [{"label": "dog", "mentions": [{"unit": first, "concept": "c.dog"}]}]
    if "Every pet" in prompt:
        concepts = [
            _candidate("c.dog", "dog", first, parents=["c.pet"]),
            _candidate("c.pet", "pet", first),
        ]
    return {
        "unit_verdicts": [{"unit": unit, "ignorable": False} for unit in units],
        "concepts": concepts,
        "terms": [t | _candidate("t.dog", "dog", first) for t in terms],
    }


def _terms_answer(prompt: str) -> dict[str, Any]:
    dogs = {
        alias: bool(existing)
        for alias, label, existing in _CONCEPT.findall(prompt)
        if label == "dog"
    }
    old = [alias for alias, existing in dogs.items() if existing]
    new = [alias for alias, existing in dogs.items() if not existing]
    if not old:
        return {"synonym_groups": [], "sense_splits": []}
    group = {"concept": old[0], "preferred_label": "dog", "terms": ["dog"], "merge": new}
    return {"synonym_groups": [group], "sense_splits": []}


class DogClient:
    model = MODEL

    def complete(self, request: LlmRequest) -> LlmResponse:
        title = request.schema.get("title")
        if title == "TermResolutionOutput":
            data = _terms_answer(request.prompt)
        elif title == "RulesOutput":
            data = {"rules": [], "properties": []}
        else:
            data = _concepts_answer(request.prompt)
        return LlmResponse(data, 100, 50, MODEL)

    def count_tokens(self, request: LlmRequest) -> int:
        return heuristic_tokens(request)


@pytest.fixture
def kit(tmp_path: Path, scope_record: dict[str, Any]) -> tuple[DatasetStore, Path, Path]:
    sources = tmp_path / "sources"
    for folder, text in {
        "dogs": "# Dogs\n\nA dog needs a daily walk.\n",
        "rules": "# Pets\n\nEvery pet (dog or cat) must be registered.\n",
    }.items():
        (sources / folder).mkdir(parents=True)
        (sources / folder / "01.md").write_text(text, encoding="utf-8")
    store = DatasetStore(tmp_path / "data", "pets-and-house-rules")
    store.create(validate_record(ScopeRecord, scope_record))
    return store, sources, tmp_path / "work"


def _ingest(kit: tuple[DatasetStore, Path, Path], folder: str) -> None:
    store, sources, work = kit
    client = DogClient()
    plan = plan_ingestion(store, sources, folder, client, WHO)
    start_run(store, plan, client, work, confirm=True)


def _by_label(store: DatasetStore, kind: type[Any], label: str) -> list[Any]:
    elements = store.read().elements().values()
    return [e for e in elements if isinstance(e, kind) and e.label.lower() == label]


def _extend_decisions(store: DatasetStore, element_id: str) -> list[Any]:
    decisions = store.read().decisions()
    return [d for d in decisions if d.action == "extend" and d.element_id == element_id]


def _approve(store: DatasetStore, concept: Concept) -> Concept:
    snapshot = concept.model_dump(mode="json", exclude_none=True) | {"status": "approved"}
    approved = concept.model_copy(update={"status": "approved"})
    approved = validate_record(
        Concept, approved.model_dump(mode="json") | {"approved_snapshot": snapshot}
    )
    with store.transaction() as files:
        files.write_element(approved)
    return approved


def test_later_run_adds_parent_and_evidence_to_the_existing_concept(kit: Any) -> None:
    store = kit[0]
    _ingest(kit, "dogs")
    [dog] = _by_label(store, Concept, "dog")
    _ingest(kit, "rules")
    [after] = _by_label(store, Concept, "dog")
    [pet] = _by_label(store, Concept, "pet")
    assert after.id == dog.id
    assert after.parents == [pet.id]
    assert len(after.evidence) == len(dog.evidence) + 1
    assert after.status == dog.status == "proposed"
    [decision] = _extend_decisions(store, dog.id)
    assert (decision.field, decision.user, decision.role) == ("evidence, parents", "alice", "user")
    assert decision.old["parents"] == [] and decision.new["parents"] == [pet.id]


def test_extended_approved_concept_goes_back_to_included_with_its_snapshot(kit: Any) -> None:
    store = kit[0]
    _ingest(kit, "dogs")
    [dog] = _by_label(store, Concept, "dog")
    approved = _approve(store, dog)
    _ingest(kit, "rules")
    [after] = _by_label(store, Concept, "dog")
    assert after.status == "included"
    assert after.approved_snapshot == approved.approved_snapshot
    assert after.parents
    fields = [d.field for d in _extend_decisions(store, dog.id)]
    assert fields == ["evidence, parents", "status"]


def test_later_run_keeps_one_term_record_per_label(kit: Any) -> None:
    store = kit[0]
    _ingest(kit, "dogs")
    _ingest(kit, "rules")
    [term] = _by_label(store, Term, "dog")
    [dog] = _by_label(store, Concept, "dog")
    assert len(term.mentions) == 2
    assert {m.concept for m in term.mentions} == {dog.id}
    [decision] = _extend_decisions(store, term.id)
    assert decision.field == "evidence, mentions"


class NoCallClient(DogClient):
    def complete(self, request: LlmRequest) -> LlmResponse:
        raise AssertionError("the resumed run must use the cached answers")


def _fail(files: Any) -> None:
    raise OSError("disk full")


def test_resumed_run_extends_from_the_pass_2_cache(kit: Any) -> None:
    """The extended elements are part of the cached pass 2 result (resume, FR-8)."""
    store, sources, work = kit
    _ingest(kit, "dogs")
    client = DogClient()
    plan = plan_ingestion(store, sources, "rules", client, WHO)
    with pytest.raises(IngestionFailedError):
        start_run(store, plan, client, work, confirm=True, hooks=WriteHooks(before_swap=_fail))
    resume_run(store, plan.run_id, NoCallClient(), work)
    [dog] = _by_label(store, Concept, "dog")
    [pet] = _by_label(store, Concept, "pet")
    assert dog.parents == [pet.id]
