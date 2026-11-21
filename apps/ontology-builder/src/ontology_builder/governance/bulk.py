"""One action on many elements, with a result per ID (FR-18, AC-17)."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from ontology_builder.governance.actions import apply_action
from ontology_builder.governance.actors import Actor, GovernanceRefusedError
from ontology_builder.governance.changes import ChangeSet


@dataclass(frozen=True)
class ActionResult:
    """What happened to one element of a bulk action; ``message`` says why it was refused."""

    element_id: str
    ok: bool
    message: str = ""


def apply_bulk(
    changes: ChangeSet,
    actor: Actor,
    action: str,
    element_ids: Iterable[str],
    payload: Mapping[str, Any],
) -> list[ActionResult]:
    """Apply ``action`` to each ID in turn; a refused ID changes nothing and does not stop
    the others."""
    results = []
    for element_id in element_ids:
        try:
            apply_action(changes, actor, action, element_id, **payload)
        except GovernanceRefusedError as refusal:
            results.append(ActionResult(element_id, ok=False, message=str(refusal)))
        else:
            results.append(ActionResult(element_id, ok=True))
    return results
