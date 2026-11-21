"""Elements authored by people (FR-22, AC-21): evidence required, status ``included``."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any

from ontology_builder.governance.actors import Actor, GovernanceRefusedError
from ontology_builder.governance.changes import ChangeSet
from ontology_builder.governance.create import add_element
from ontology_builder.governance.review import PROTECTED_FIELDS
from ontology_builder.model import DecisionAction, Element


def _references(fields: Mapping[str, Any]) -> Iterator[str]:
    """Every element ID the fields point to."""
    for name in ("subject", "object", "of"):
        if fields.get(name):
            yield str(fields[name])
    for name in ("parents", "refers_to"):
        yield from (str(ref) for ref in fields.get(name) or [])
    yield from (str(m.get("concept")) for m in fields.get("mentions") or [])


def _check(changes: ChangeSet, fields: Mapping[str, Any]) -> None:
    given = sorted(PROTECTED_FIELDS & set(fields))
    if given:
        raise GovernanceRefusedError(f"an authored element cannot set {', '.join(given)}")
    evidence = fields.get("evidence") or []
    if not evidence:
        raise GovernanceRefusedError(
            "an authored element needs evidence: a user statement or a corpus source unit"
        )
    for item in evidence:
        if not changes.has_unit(str(item.get("unit"))):
            raise GovernanceRefusedError(
                f"the evidence cites unknown source unit {item.get('unit')!r}"
            )
    for ref in _references(fields):
        changes.get(ref)


def author_element(
    changes: ChangeSet,
    actor: Actor,
    element_type: str,
    fields: Mapping[str, Any],
    reason: str | None = None,
) -> Element:
    """A new ``included`` element of ``element_type`` by ``actor``, with an ``author`` decision.

    It must cite at least one existing source unit and refer only to existing elements. Its
    status, origin and ID are set here; a missing level reason says who set the level.
    """
    _check(changes, fields)
    data = {"level_reason": f"Set by {actor.user} when authoring.", **fields}
    return add_element(changes, actor, element_type, data, DecisionAction.author, reason)
