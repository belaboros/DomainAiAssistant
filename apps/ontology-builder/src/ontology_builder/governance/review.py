"""Review actions on content: correct a field, split a term into senses, reassign a mention
(FR-17). Each one is an edit under the status machine and records a decision per changed field.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ontology_builder.governance.actors import Actor, GovernanceRefusedError
from ontology_builder.governance.changes import ChangeSet
from ontology_builder.governance.create import add_element
from ontology_builder.governance.status import EditRequest, edit
from ontology_builder.model import Concept, DecisionAction, Element, ElementStatus, Term

PROTECTED_FIELDS = frozenset(
    {"id", "status", "status_reason", "origin", "approved_snapshot", "replaced_by"}
)
"""Fields that only the status actions change; ``correct`` refuses them."""

_CLOSED = {ElementStatus.excluded, ElementStatus.rejected, ElementStatus.deprecated}


def correct(changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]) -> None:
    """Payload: ``field``, ``value`` and an optional ``reason``."""
    name = str(payload.get("field"))
    if name in PROTECTED_FIELDS:
        raise GovernanceRefusedError(f"the field {name!r} cannot be corrected")
    if name not in type(element).model_fields:
        raise GovernanceRefusedError(f"{element.id} has no field {name!r}")
    request = EditRequest(
        DecisionAction.correct, {name: payload.get("value")}, payload.get("reason")
    )
    edit(changes, actor, element, request)


def _term(element: Element, action: str) -> Term:
    if not isinstance(element, Term):
        raise GovernanceRefusedError(f"{action} needs a term, and {element.id} is not a term")
    return element


def _mention_data(term: Term) -> list[dict[str, str]]:
    return [{"unit": m.unit, "concept": m.concept} for m in term.mentions or []]


def _open_concept(changes: ChangeSet, concept_id: str) -> Concept:
    concept = changes.get(concept_id)
    if not isinstance(concept, Concept):
        raise GovernanceRefusedError(f"{concept_id} is not a concept")
    if concept.status in _CLOSED:
        raise GovernanceRefusedError(
            f"cannot point a mention to {concept_id}: it is {concept.status}"
        )
    return concept


def reassign(
    changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]
) -> None:
    """Payload: ``unit`` (the mention), ``concept`` (where it points now), optional ``reason``."""
    term = _term(element, "reassign")
    unit, target = str(payload.get("unit")), str(payload.get("concept"))
    mentions = _mention_data(term)
    if unit not in {m["unit"] for m in mentions}:
        raise GovernanceRefusedError(f"{term.id} has no mention in {unit}")
    _open_concept(changes, target)
    moved = [m | {"concept": target} if m["unit"] == unit else m for m in mentions]
    edit(
        changes,
        actor,
        term,
        EditRequest(DecisionAction.reassign, {"mentions": moved}, payload.get("reason")),
    )


def _split_units(term: Term, units: list[str]) -> str:
    """Check the units to move and return the one concept their mentions point to now."""
    if not units:
        raise GovernanceRefusedError("a split needs at least one mention to move")
    mentions = {m.unit: m.concept for m in term.mentions or []}
    missing = [unit for unit in units if unit not in mentions]
    if missing:
        raise GovernanceRefusedError(f"{term.id} has no mention in {', '.join(missing)}")
    if set(mentions) <= set(units):
        raise GovernanceRefusedError("a split keeps at least one mention with the current sense")
    origins = {mentions[unit] for unit in units}
    if len(origins) != 1:
        raise GovernanceRefusedError("the mentions to move point to different concepts")
    return origins.pop()


def _narrow_original(
    changes: ChangeSet, actor: Actor, original_id: str, units: list[str], payload: Mapping[str, Any]
) -> None:
    """The original sense loses the moved evidence (if any is left) and gets its scope note."""
    original = changes.get(original_id)
    fields: dict[str, Any] = {}
    kept = [
        e.model_dump(mode="json", exclude_none=True)
        for e in original.evidence
        if e.unit not in units
    ]
    if kept and len(kept) != len(original.evidence):
        fields["evidence"] = kept
    if payload.get("original_scope_note"):
        fields["scope_note"] = payload["original_scope_note"]
    if fields:
        edit(
            changes,
            actor,
            original,
            EditRequest(DecisionAction.split_, fields, payload.get("reason")),
        )


def split(changes: ChangeSet, actor: Actor, element: Element, payload: Mapping[str, Any]) -> None:
    """Payload: ``units`` (mentions that name the new sense), its ``label`` and ``scope_note``,
    an optional ``definition``, ``original_scope_note`` and ``reason``."""
    term = _term(element, "split")
    units = [str(unit) for unit in payload.get("units") or []]
    original_id = _split_units(term, units)
    reason = payload.get("reason")
    fields = {
        "label": payload.get("label"),
        "definition": payload.get("definition"),
        "scope_note": payload.get("scope_note"),
        "level": term.level,
        "level_reason": term.level_reason,
        "evidence": [{"unit": unit} for unit in units],
    }
    sense = add_element(
        changes,
        actor,
        "concept",
        {k: v for k, v in fields.items() if v is not None},
        DecisionAction.split_,
        reason,
    )
    moved = [m | {"concept": sense.id} if m["unit"] in units else m for m in _mention_data(term)]
    edit(changes, actor, term, EditRequest(DecisionAction.split_, {"mentions": moved}, reason))
    _narrow_original(changes, actor, original_id, units, payload)
