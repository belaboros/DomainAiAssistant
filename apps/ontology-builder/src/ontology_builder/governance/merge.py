"""Merge a concept into another as a synonym (FR-17; plan 0002, Approach 5 and the edge cases).

The kept concept takes the merged one's evidence and parents. Every reference to the merged
concept (parents, term mentions, relations, rules, properties) is re-pointed to the kept one, in
each element that may still be edited; an approved one goes back to ``included`` and keeps its
snapshot. The merged label stays a synonym: a term with that label points to the kept concept.
The merged concept is kept with ``replaced_by``: excluded, or deprecated if it was ever approved,
which only a domain admin may do. Nothing is deleted.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from ontology_builder.governance.actors import (
    Actor,
    GovernanceRefusedError,
    new_decision,
    require_admin,
)
from ontology_builder.governance.changes import ChangeSet
from ontology_builder.governance.create import add_element
from ontology_builder.governance.status import (
    EDIT,
    INCLUDED_NEW,
    INCLUDED_SNAPSHOT,
    TRANSITIONS,
    EditRequest,
    edit,
    state_of,
    status_decision,
    updated,
)
from ontology_builder.model import Concept, DecisionAction, Element, ElementStatus, Term

_MERGEABLE: dict[str, ElementStatus] = {
    ElementStatus.proposed: ElementStatus.excluded,
    INCLUDED_NEW: ElementStatus.excluded,
    INCLUDED_SNAPSHOT: ElementStatus.deprecated,
    ElementStatus.approved: ElementStatus.deprecated,
}
"""State of the merged concept -> what it becomes; any other state is refused."""

_MERGE = DecisionAction.merge


def unique[T](items: Iterable[T]) -> list[T]:
    """The items in order, each once."""
    seen: list[T] = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def _pair(changes: ChangeSet, element: Element, into: Any) -> tuple[Concept, Concept]:
    if not isinstance(element, Concept):
        raise GovernanceRefusedError(
            f"only a concept can be merged as a synonym, and {element.id} is not a concept"
        )
    if into == element.id:
        raise GovernanceRefusedError(f"{element.id} cannot be merged into itself")
    kept = changes.get(str(into))
    if not isinstance(kept, Concept):
        raise GovernanceRefusedError(f"{kept.id} is not a concept")
    return element, kept


def _single_refs(data: Mapping[str, Any], old: str, new: str) -> dict[str, Any]:
    return {name: new for name in ("subject", "object", "of") if data.get(name) == old}


def _list_refs(data: Mapping[str, Any], old: str, new: str) -> dict[str, Any]:
    found: dict[str, Any] = {}
    for name in ("parents", "refers_to"):
        refs = data.get(name, [])
        if old in refs:
            swapped = unique(new if ref == old else ref for ref in refs)
            found[name] = [ref for ref in swapped if ref != data["id"]]
    return found


def _mention_refs(data: Mapping[str, Any], old: str, new: str) -> dict[str, Any]:
    mentions = data.get("mentions", [])
    if not any(mention["concept"] == old for mention in mentions):
        return {}
    swapped = (m | {"concept": new} if m["concept"] == old else m for m in mentions)
    return {"mentions": unique(swapped)}


def repointed(element: Element, old: str, new: str) -> dict[str, Any]:
    """The reference fields of ``element`` that change when ``old`` is replaced by ``new``."""
    data = element.model_dump(mode="json", exclude_none=True)
    return {
        **_single_refs(data, old, new),
        **_list_refs(data, old, new),
        **_mention_refs(data, old, new),
    }


def _retire(
    changes: ChangeSet, actor: Actor, pair: tuple[Concept, Concept], reason: str | None
) -> None:
    merged, kept = pair
    state = state_of(merged)
    status = _MERGEABLE.get(state)
    if status is None:
        raise GovernanceRefusedError(f"cannot merge {merged.id}: it is {state}")
    if status == ElementStatus.deprecated:
        require_admin(actor, "merge a concept that was approved (it becomes deprecated)")
    note = f"merged into {kept.id} as a synonym" + (f": {reason}" if reason else "")
    decisions = [
        status_decision(changes, actor, _MERGE, merged, status, reason),
        new_decision(
            changes.store,
            actor,
            _MERGE,
            element_id=merged.id,
            field="replaced_by",
            old=merged.replaced_by,
            new=kept.id,
            reason=reason,
        ),
    ]
    changes.put(updated(merged, status=status, status_reason=note, replaced_by=kept.id), decisions)


def _fold(
    changes: ChangeSet, actor: Actor, pair: tuple[Concept, Concept], reason: str | None
) -> None:
    merged, kept = pair
    parents = [
        ref
        for ref in unique([*(kept.parents or []), *(merged.parents or [])])
        if ref not in (merged.id, kept.id)
    ]
    fields = {
        "evidence": unique(
            [
                e.model_dump(mode="json", exclude_none=True)
                for e in [*kept.evidence, *merged.evidence]
            ]
        ),
        "parents": parents,
    }
    edit(changes, actor, kept, EditRequest(_MERGE, fields, reason))


def _follow(changes: ChangeSet, actor: Actor, pair: tuple[Concept, Concept]) -> None:
    merged, kept = pair
    reason = f"follows the merge of {merged.id} into {kept.id}"
    for element in list(changes.elements.values()):
        if element.id in (merged.id, kept.id) or EDIT not in TRANSITIONS[state_of(element)]:
            continue
        fields = repointed(element, merged.id, kept.id)
        if fields:
            edit(changes, actor, element, EditRequest(_MERGE, fields, reason))


def _keep_synonym(
    changes: ChangeSet, actor: Actor, pair: tuple[Concept, Concept], reason: str | None
) -> None:
    merged, kept = pair
    if any(_names(element, merged.label, kept.id) for element in changes.elements.values()):
        return
    evidence = [e.model_dump(mode="json", exclude_none=True) for e in merged.evidence]
    fields = {
        "label": merged.label,
        "level": merged.level,
        "level_reason": merged.level_reason,
        "evidence": evidence,
        "mentions": [{"unit": e["unit"], "concept": kept.id} for e in evidence],
    }
    add_element(changes, actor, "term", fields, _MERGE, reason)


def _names(element: Element, label: str, concept_id: str) -> bool:
    """Whether ``element`` is a term with this label and a mention of the concept."""
    return (
        isinstance(element, Term)
        and element.label.casefold() == label.casefold()
        and any(mention.concept == concept_id for mention in element.mentions or [])
    )


def merge(changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]) -> None:
    """Payload: ``into`` (the kept concept) and an optional ``reason``."""
    pair = _pair(changes, element, payload.get("into"))
    reason = payload.get("reason")
    _retire(changes, actor, pair, reason)
    _fold(changes, actor, pair, reason)
    _follow(changes, actor, pair)
    _keep_synonym(changes, actor, pair, reason)
