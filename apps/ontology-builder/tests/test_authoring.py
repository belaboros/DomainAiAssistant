"""Authored elements: evidence required, status ``included`` (plan 0002, T13: AC-21)."""

from __future__ import annotations

from typing import Any

import pytest
from ontology_builder.governance import (
    Actor,
    ChangeSet,
    GovernanceRefusedError,
    add_user_statement,
    author_element,
)
from ontology_builder.model import Corpus, Document, Role, SourceUnit, validate_record

ALICE = Actor("alice", Role.user)


def _save(kit: Any, changes: ChangeSet) -> None:
    with kit.store.transaction() as files:
        changes.write(files)
    changes.mark_saved()


def test_concept_without_definition_from_statement_is_included(review_kit: Any) -> None:
    changes = ChangeSet.load(review_kit.store)
    statement = add_user_statement(changes, ALICE, "A dog and a cat must be introduced gradually.")
    concept = author_element(
        changes,
        ALICE,
        "concept",
        {"label": "gradual introduction", "level": "level-2", "evidence": [{"unit": statement.id}]},
    )
    _save(review_kit, changes)

    stored = review_kit.store.read().elements()[concept.id]
    assert stored.status == "included"
    assert stored.definition is None
    assert [e.unit for e in stored.evidence] == [statement.id]
    assert (stored.origin.kind, stored.origin.author) == ("user", "alice")
    assert stored.level_reason, "an authored element gets a level reason"
    decisions = [d for d in review_kit.store.read().decisions() if d.element_id == concept.id]
    assert [(d.action, d.user, d.new) for d in decisions] == [("author", "alice", "included")]


@pytest.mark.parametrize("evidence", [None, []])
def test_authoring_without_evidence_refused(review_kit: Any, evidence: Any) -> None:
    changes = ChangeSet.load(review_kit.store)
    fields = {"label": "pet", "level": "level-1"}
    if evidence is not None:
        fields["evidence"] = evidence
    with pytest.raises(GovernanceRefusedError, match="evidence"):
        author_element(changes, ALICE, "concept", fields)
    assert changes.changed_ids() == [] and changes.decisions == []


def test_authoring_refuses_an_unknown_unit(review_kit: Any) -> None:
    changes = ChangeSet.load(review_kit.store)
    with pytest.raises(GovernanceRefusedError, match="unknown source unit"):
        author_element(
            changes,
            ALICE,
            "concept",
            {"label": "pet", "level": "level-1", "evidence": [{"unit": review_kit.unit()}]},
        )


def test_authoring_may_cite_a_corpus_unit(review_kit: Any, corpus_unit: dict[str, Any]) -> None:
    unit = validate_record(SourceUnit, corpus_unit)
    corpus_id, document_id = review_kit.store.minter.new("corpus"), str(unit.document_id)
    corpus = {
        "id": corpus_id,
        "number": 0,
        "slug": "dog",
        "source_path": "manuals/dog",
        "ingest_run": review_kit.store.minter.new("run"),
    }
    document = {
        "id": document_id,
        "corpus_id": corpus_id,
        "path": "dog.md",
        "title": "Dog",
        "content_hash": unit.content_hash,
    }
    with review_kit.store.transaction() as files:
        files.write_corpus("00_dog", validate_record(Corpus, corpus))
        files.write_document("00_dog", validate_record(Document, document))
        files.write_units("00_dog", document_id, [unit])
    changes = ChangeSet.load(review_kit.store)
    rule = author_element(
        changes,
        ALICE,
        "concept",
        {"label": "leash", "level": "level-1", "evidence": [{"unit": unit.id}]},
    )
    assert rule.status == "included"


def test_authoring_refuses_unknown_references(review_kit: Any) -> None:
    changes = ChangeSet.load(review_kit.store)
    statement = add_user_statement(changes, ALICE, "A resident may keep at most 2 pets.")
    with pytest.raises(GovernanceRefusedError, match="unknown element"):
        author_element(
            changes,
            ALICE,
            "relation",
            {
                "label": "keeps",
                "level": "level-1",
                "evidence": [{"unit": statement.id}],
                "subject": "cn_00000000000000000000000000",
                "object": "cn_00000000000000000000000001",
                "predicate_label": "keeps",
            },
        )


@pytest.mark.parametrize("field", ["status", "origin", "id", "approved_snapshot"])
def test_authoring_sets_status_and_origin_itself(review_kit: Any, field: str) -> None:
    changes = ChangeSet.load(review_kit.store)
    statement = add_user_statement(changes, ALICE, "Cats need a scratching post.")
    with pytest.raises(GovernanceRefusedError, match=field):
        author_element(
            changes,
            ALICE,
            "concept",
            {"label": "x", "level": "level-1", "evidence": [{"unit": statement.id}], field: "x"},
        )
