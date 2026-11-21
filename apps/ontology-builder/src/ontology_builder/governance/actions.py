"""One entry point for every review and governance action on one element."""

from __future__ import annotations

from typing import Any

from ontology_builder.governance.actors import Actor, GovernanceRefusedError, require_admin
from ontology_builder.governance.changes import ChangeSet
from ontology_builder.governance.merge import merge
from ontology_builder.governance.review import correct, reassign, split
from ontology_builder.governance.status import ADMIN_ACTIONS, STATUS_ACTIONS, Handler
from ontology_builder.model import Element

ACTIONS: dict[str, Handler] = {
    **STATUS_ACTIONS,
    "correct": correct,
    "merge": merge,
    "split": split,
    "reassign": reassign,
}
"""Action name (as in the API's ``POST …/actions``) to its handler."""


def apply_action(
    changes: ChangeSet, actor: Actor, action: str, element_id: str, **payload: Any
) -> Element:
    """Apply one action to one element, whole, or raise ``GovernanceRefusedError`` and change
    nothing. The role is checked first, then the element, then the rules of the action."""
    handler = ACTIONS.get(action)
    if handler is None:
        raise GovernanceRefusedError(f"unknown action {action!r}")
    if action in ADMIN_ACTIONS:
        require_admin(actor, action)
    element = changes.get(element_id)
    with changes.atomic():
        handler(changes, actor, element, payload)
    return changes.get(element_id)
