"""Elements already in the ontology that a run extended (ADR-0012, FR-11, FR-24, FR-26).

Pass 2 adds evidence and parents (concepts) or mentions and evidence (terms) to existing
elements. Here each one gets an ``extend`` decision with the run's user and role, and an approved
one goes back to ``included``: it keeps its approved snapshot, so the governed release keeps the
approved version until a domain admin approves it again.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from ontology_builder.ingestion.plan import RunPlan
from ontology_builder.model import (
    Decision,
    DecisionAction,
    Element,
    ElementStatus,
    Term,
    validate_record,
)
from ontology_builder.store import DatasetStore


def _fields(element: Element) -> tuple[str, ...]:
    return ("evidence", "mentions") if isinstance(element, Term) else ("evidence", "parents")


def _values(element: Element, names: Sequence[str]) -> dict[str, Any]:
    data = element.model_dump(mode="json", exclude_none=True)
    return {name: data.get(name, []) for name in names}


def _decision(
    store: DatasetStore, plan: RunPlan, element_id: str, field: str, old: Any, new: Any
) -> Decision:
    return validate_record(
        Decision,
        {
            "id": store.minter.new("decision"),
            "at": store.clock.now(),
            "user": plan.user,
            "role": plan.role,
            "action": DecisionAction.extend,
            "element_id": element_id,
            "field": field,
            "old": old,
            "new": new,
            "reason": f"extended by run {plan.run_id}",
        },
    )


def extend_existing(
    store: DatasetStore,
    plan: RunPlan,
    extended: Sequence[Element],
    previous: Mapping[str, Element],
) -> tuple[list[Element], list[Decision]]:
    """The records to write for the extended elements, and their decisions."""
    records: list[Element] = []
    decisions: list[Decision] = []
    for element in extended:
        record, made = _extend_one(store, plan, element, previous[element.id])
        records.append(record)
        decisions.extend(made)
    return records, decisions


def _extend_one(
    store: DatasetStore, plan: RunPlan, after: Element, before: Element
) -> tuple[Element, list[Decision]]:
    names = _fields(after)
    old, new = _values(before, names), _values(after, names)
    decisions = [_decision(store, plan, after.id, ", ".join(names), old, new)]
    if before.status != ElementStatus.approved:
        return after, decisions
    reason = f"extended by run {plan.run_id}; approve again"
    reopened = after.model_copy(update={"status": ElementStatus.included, "status_reason": reason})
    decisions.append(_decision(store, plan, after.id, "status", "approved", "included"))
    return reopened, decisions
