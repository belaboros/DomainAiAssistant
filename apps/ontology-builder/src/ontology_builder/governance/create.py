"""New elements made by a review action (a sense of a split, the synonym term of a merge)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ontology_builder.governance.actors import Actor, GovernanceRefusedError, new_decision
from ontology_builder.governance.changes import ChangeSet
from ontology_builder.model import (
    DecisionAction,
    Element,
    ElementStatus,
    OriginKind,
    RecordInvalidError,
    validate_element,
)


def add_element(
    changes: ChangeSet,
    actor: Actor,
    element_type: str,
    fields: Mapping[str, Any],
    action: DecisionAction,
    reason: str | None = None,
) -> Element:
    """Mint, validate and add an ``included`` element authored by ``actor``; one decision
    records it (field ``status``, from nothing to ``included``)."""
    data = {
        **fields,
        "id": changes.store.minter.new(element_type),
        "status": ElementStatus.included,
        "origin": {
            "kind": OriginKind.user,
            "author": actor.user,
            "created_at": changes.store.clock.now(),
        },
    }
    try:
        element = validate_element(element_type, data)
    except RecordInvalidError as error:
        raise GovernanceRefusedError("; ".join(error.problems)) from None
    decision = new_decision(
        changes.store,
        actor,
        action,
        element_id=element.id,
        field="status",
        new=str(ElementStatus.included),
        reason=reason,
    )
    changes.put(element, [decision])
    return element
