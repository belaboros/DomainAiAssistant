"""User statements: a source unit in ``90_user_statements/`` with revisions (T13: AC-20)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest
import yaml
from ontology_builder.governance import (
    Actor,
    ChangeSet,
    GovernanceRefusedError,
    add_user_statement,
    revise_user_statement,
)
from ontology_builder.model import FixedClock, Role, content_hash

ALICE = Actor("alice", Role.user)
SAM = Actor("sam", Role.user)
SCHEMA = Path(__file__).parents[3] / "libs/contracts/ontology/source-unit.schema.json"
TEXT = "A dog and a cat must be introduced gradually."


def _save(kit: Any, changes: ChangeSet) -> None:
    with kit.store.transaction() as files:
        changes.write(files)
    changes.mark_saved()


def _file(kit: Any, unit_id: str) -> Path:
    path: Path = kit.store.root / "00_sources" / "90_user_statements" / f"{unit_id}.yaml"
    return path


def test_statement_unit_fields(review_kit: Any) -> None:
    changes = ChangeSet.load(review_kit.store)
    unit = add_user_statement(changes, ALICE, "  A dog and a cat\nmust be introduced gradually. ")
    _save(review_kit, changes)

    data = yaml.safe_load(_file(review_kit, unit.id).read_text(encoding="utf-8"))
    jsonschema.validate(data, json.loads(SCHEMA.read_text(encoding="utf-8")))
    assert data["id"].startswith("su_")
    assert data["kind"] == "user_statement"
    assert (data["text"], data["content_hash"]) == (TEXT, content_hash(TEXT))
    assert data["author"] == "alice"
    assert data["created_at"] == "2026-11-21T10:00:00Z"
    assert [(r["rev"], r["text"], r["author"]) for r in data["revisions"]] == [(1, TEXT, "alice")]
    [decision] = review_kit.store.read().decisions()
    assert (decision.action, decision.element_id, decision.new) == ("author", unit.id, TEXT)


def test_edit_keeps_id_adds_revision_changes_hash(review_kit: Any) -> None:
    changes = ChangeSet.load(review_kit.store)
    unit = add_user_statement(changes, ALICE, TEXT)
    _save(review_kit, changes)

    changes = ChangeSet.load(review_kit.store)
    changes.store.clock = FixedClock(review_kit.at.replace(hour=11))
    revised = revise_user_statement(changes, SAM, unit.id, "A dog and a cat meet gradually.")
    _save(review_kit, changes)

    [stored] = review_kit.store.read().user_statements()
    assert stored.id == unit.id == revised.id
    assert stored.content_hash != unit.content_hash
    assert stored.content_hash == content_hash("A dog and a cat meet gradually.")
    assert stored.author == "alice", "the statement keeps its first author"
    assert [(r.rev, r.author, r.at.hour) for r in stored.revisions or []] == [
        (1, "alice", 10),
        (2, "sam", 11),
    ]
    decisions = review_kit.store.read().decisions()
    assert [(d.action, d.old, d.new) for d in decisions][-1] == (
        "correct",
        TEXT,
        "A dog and a cat meet gradually.",
    )


def test_empty_statement_refused(review_kit: Any) -> None:
    changes = ChangeSet.load(review_kit.store)
    with pytest.raises(GovernanceRefusedError, match="empty"):
        add_user_statement(changes, ALICE, " \n ")
    assert changes.statements == {} and changes.decisions == []


def test_revision_refusals(review_kit: Any) -> None:
    changes = ChangeSet.load(review_kit.store)
    unit = add_user_statement(changes, ALICE, TEXT)
    with pytest.raises(GovernanceRefusedError, match="unknown user statement"):
        revise_user_statement(changes, ALICE, "su_00000000000000000000000000", "x")
    with pytest.raises(GovernanceRefusedError, match="unchanged"):
        revise_user_statement(changes, ALICE, unit.id, f" {TEXT}\n")
    assert len(changes.decisions) == 1
