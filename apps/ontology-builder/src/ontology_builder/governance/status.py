"""The status machine of FR-23 to FR-25 (plan 0002, Status transitions).

``TRANSITIONS`` is the plan's table: for each state of an element, the actions allowed in it and
the status they lead to. Any action missing from a state is refused. ``edit`` stands for every
change of content (correct, level, merge, split); an edit of an approved element puts it back to
``included`` and keeps its approved snapshot (FR-24). Nothing here deletes a record (FR-25).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from ontology_builder.governance.actors import (
    Actor,
    GovernanceRefusedError,
    new_decision,
)
from ontology_builder.governance.changes import ChangeSet
from ontology_builder.model import (
    Decision,
    DecisionAction,
    Element,
    ElementStatus,
    RecordInvalidError,
    validate_record,
)

INCLUDED_NEW = "included, never approved"
INCLUDED_SNAPSHOT = "included, has approved snapshot"
EDIT = "edit"

_S = ElementStatus

Handler = Callable[[ChangeSet, Actor, Element, Mapping[str, Any]], None]
"""Applies one action to one element, or raises ``GovernanceRefusedError``."""
TRANSITIONS: dict[str, dict[str, ElementStatus]] = {
    _S.proposed: {
        "include": _S.included,
        "exclude": _S.excluded,
        "approve": _S.approved,
        "reject": _S.rejected,
        EDIT: _S.proposed,
    },
    INCLUDED_NEW: {
        "exclude": _S.excluded,
        "approve": _S.approved,
        "reject": _S.rejected,
        EDIT: _S.included,
    },
    INCLUDED_SNAPSHOT: {"approve": _S.approved, "deprecate": _S.deprecated, EDIT: _S.included},
    _S.approved: {"deprecate": _S.deprecated, EDIT: _S.included},
    _S.excluded: {"include": _S.included},
    _S.rejected: {},
    _S.deprecated: {},
}
"""State -> action -> resulting status. ``include`` / ``exclude`` / ``edit``: any role;
``approve`` / ``reject`` / ``deprecate``: domain admin only (``ADMIN_ACTIONS``)."""

ADMIN_ACTIONS = frozenset({"approve", "reject", "deprecate"})

_HINTS = {
    (INCLUDED_SNAPSHOT, "exclude"): "; it was approved before, so deprecate it instead",
    (_S.approved, "exclude"): "; deprecate it instead",
    (_S.approved, "reject"): "; deprecate it instead",
}


def snapshot_of(element: Element) -> Element | None:
    """The element's approved snapshot (FR-24), or ``None`` if it was never approved."""
    snapshot = getattr(element, "approved_snapshot", None)
    return snapshot if isinstance(snapshot, Element) else None


def state_of(element: Element) -> str:
    """The row of ``TRANSITIONS`` the element is in."""
    if element.status != _S.included:
        return str(element.status)
    return INCLUDED_SNAPSHOT if snapshot_of(element) is not None else INCLUDED_NEW


def target_status(element: Element, action: str) -> ElementStatus:
    """The status ``action`` leads to from the element's state, or a refusal saying why."""
    state = state_of(element)
    target = TRANSITIONS[state].get(action)
    if target is None:
        verb = "change" if action == EDIT else action
        raise GovernanceRefusedError(
            f"cannot {verb} {element.id}: it is {state}" + _HINTS.get((state, action), "")
        )
    return target


def updated(element: Element, **changes: Any) -> Element:
    """A validated new version of the element; a ``None`` value clears that slot."""
    data = element.model_dump(mode="json", exclude_none=True) | changes
    data = {key: value for key, value in data.items() if value is not None}
    try:
        return validate_record(type(element), data)
    except RecordInvalidError as error:
        raise GovernanceRefusedError("; ".join(error.problems)) from None


def status_decision(
    changes: ChangeSet,
    actor: Actor,
    action: DecisionAction,
    element: Element,
    new: ElementStatus,
    reason: str | None = None,
) -> Decision:
    return new_decision(
        changes.store,
        actor,
        action,
        element_id=element.id,
        field="status",
        old=str(element.status),
        new=str(new),
        reason=reason,
    )


def required_reason(payload: Mapping[str, Any], action: str) -> str:
    reason = str(payload.get("reason") or "").strip()
    if not reason:
        raise GovernanceRefusedError(f"{action} needs a reason")
    return reason


@dataclass(frozen=True)
class EditRequest:
    """A content change: the decision action, the fields with a decision each, the reason, and
    fields that change ``alongside`` without a decision of their own (the reason holds them,
    e.g. ``level_reason`` of a level override)."""

    action: DecisionAction
    fields: Mapping[str, Any]
    reason: str | None = None
    alongside: Mapping[str, Any] = field(default_factory=dict)


def edit(changes: ChangeSet, actor: Actor, element: Element, request: EditRequest) -> Element:
    """Change content under the ``edit`` rule: one decision per changed field, and a status
    decision when an approved element goes back to ``included``."""
    status = target_status(element, EDIT)
    new = updated(element, **request.fields, **request.alongside, status=status)
    decisions = [
        new_decision(
            changes.store,
            actor,
            request.action,
            element_id=element.id,
            field=name,
            old=_plain(getattr(element, name)),
            new=_plain(getattr(new, name)),
            reason=request.reason,
        )
        for name in request.fields
        if getattr(element, name) != getattr(new, name)
    ]
    if status != element.status:
        decisions.append(
            status_decision(changes, actor, request.action, element, status, request.reason)
        )
    changes.put(new, decisions)
    return new


def _plain(value: Any) -> Any:
    return value.model_dump(mode="json") if hasattr(value, "model_dump") else value


# ---- the status actions ----


def _include(
    changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]
) -> None:
    status = target_status(element, "include")
    decision = status_decision(changes, actor, DecisionAction.include, element, status)
    changes.put(updated(element, status=status, status_reason=None), [decision])


def _exclude(
    changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]
) -> None:
    status = target_status(element, "exclude")
    reason = required_reason(payload, "exclude")
    decision = status_decision(changes, actor, DecisionAction.exclude, element, status, reason)
    changes.put(updated(element, status=status, status_reason=reason), [decision])


def _reject(changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]) -> None:
    status = target_status(element, "reject")
    reason = required_reason(payload, "reject")
    decision = status_decision(changes, actor, DecisionAction.reject, element, status, reason)
    changes.put(updated(element, status=status, status_reason=reason), [decision])


def _approve(
    changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]
) -> None:
    status = target_status(element, "approve")
    decisions = []
    current = element
    if element.status == _S.proposed:  # the table: "records include + approve"
        decisions.append(
            status_decision(changes, actor, DecisionAction.include, element, _S.included)
        )
        current = updated(element, status=_S.included)
    decisions.append(status_decision(changes, actor, DecisionAction.approve, current, status))
    snapshot = updated(current, status=status, status_reason=None, approved_snapshot=None)
    approved = updated(
        snapshot, approved_snapshot=snapshot.model_dump(mode="json", exclude_none=True)
    )
    changes.put(approved, decisions)


def _deprecate(
    changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]
) -> None:
    status = target_status(element, "deprecate")
    replacement = payload.get("replacement")
    reason = payload.get("reason")
    if replacement is not None:
        if replacement == element.id:
            raise GovernanceRefusedError(f"{element.id} cannot replace itself")
        if replacement not in changes.elements:
            raise GovernanceRefusedError(f"the replacement {replacement!r} is an unknown element")
    decisions = [status_decision(changes, actor, DecisionAction.deprecate, element, status, reason)]
    if replacement is not None:
        decisions.append(
            new_decision(
                changes.store,
                actor,
                DecisionAction.deprecate,
                element_id=element.id,
                field="replaced_by",
                old=element.replaced_by,
                new=replacement,
                reason=reason,
            )
        )
    new = updated(element, status=status, status_reason=reason, replaced_by=replacement)
    changes.put(new, decisions)


def _level(changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]) -> None:
    reason = payload.get("reason")
    alongside = {"level_reason": reason} if reason else {}
    request = EditRequest(DecisionAction.level, {"level": payload.get("level")}, reason, alongside)
    edit(changes, actor, element, request)


STATUS_ACTIONS: dict[str, Handler] = {
    "include": _include,
    "exclude": _exclude,
    "approve": _approve,
    "reject": _reject,
    "deprecate": _deprecate,
    "level": _level,
}
