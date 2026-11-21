"""User statements: source units typed in by people (FR-21, AC-20).

A statement is a unit of kind ``user_statement`` in ``00_sources/90_user_statements/``. Editing
it adds a revision and changes its text and hash; its ID, author and creation time never change.
"""

from __future__ import annotations

from ontology_builder.governance.actors import Actor, GovernanceRefusedError, new_decision
from ontology_builder.governance.changes import ChangeSet
from ontology_builder.model import (
    DecisionAction,
    SourceUnit,
    UnitKind,
    content_hash,
    normalise,
    validate_record,
)


def _text(text: str) -> str:
    clean = normalise(text)
    if not clean:
        raise GovernanceRefusedError("a user statement cannot be empty")
    return clean


def add_user_statement(changes: ChangeSet, actor: Actor, text: str) -> SourceUnit:
    """A new statement by ``actor`` with revision 1, recorded as an ``author`` decision."""
    clean, at = _text(text), changes.store.clock.now()
    revision = {
        "rev": 1,
        "text": clean,
        "content_hash": content_hash(clean),
        "author": actor.user,
        "at": at,
    }
    unit = validate_record(
        SourceUnit,
        {
            "id": changes.store.minter.new("source_unit"),
            "kind": UnitKind.user_statement,
            "text": clean,
            "content_hash": revision["content_hash"],
            "author": actor.user,
            "created_at": at,
            "revisions": [revision],
        },
    )
    decision = new_decision(
        changes.store, actor, DecisionAction.author, element_id=unit.id, field="text", new=clean
    )
    changes.put_statement(unit, [decision])
    return unit


def revise_user_statement(changes: ChangeSet, actor: Actor, unit_id: str, text: str) -> SourceUnit:
    """The statement with a new revision by ``actor``; the ID stays (FR-21)."""
    unit = changes.statement(unit_id)
    clean = _text(text)
    if clean == unit.text:
        raise GovernanceRefusedError(f"the text of {unit_id} is unchanged")
    revisions = [r.model_dump(mode="json") for r in unit.revisions or []]
    revision = {
        "rev": len(revisions) + 1,
        "text": clean,
        "content_hash": content_hash(clean),
        "author": actor.user,
        "at": changes.store.clock.now(),
    }
    data = unit.model_dump(mode="json", exclude_none=True)
    data |= {
        "text": clean,
        "content_hash": revision["content_hash"],
        "revisions": [*revisions, revision],
    }
    revised = validate_record(SourceUnit, data)
    decision = new_decision(
        changes.store,
        actor,
        DecisionAction.correct,
        element_id=unit_id,
        field="text",
        old=unit.text,
        new=clean,
    )
    changes.put_statement(revised, [decision])
    return revised
