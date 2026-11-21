"""Create an ontology, and the scope-record guard of ingestion (FR-1, AC-1)."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from ontology_builder.governance.actors import (
    Actor,
    GovernanceRefusedError,
    new_decision,
    require_admin,
)
from ontology_builder.model import (
    Decision,
    DecisionAction,
    RecordInvalidError,
    ScopeRecord,
    validate_record,
)
from ontology_builder.store import DatasetExistsError, DatasetStore

_KEBAB = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


def default_base_iri(name: str) -> str:
    return f"urn:domain-ai-assistant:ontology:{name}:"


def _scope_record(name: str, scope: Mapping[str, Any]) -> ScopeRecord:
    if scope.get("name", name) != name:
        raise GovernanceRefusedError(
            f"the scope record's name {scope['name']!r} is not the ontology name {name!r}"
        )
    data = {"base_iri": default_base_iri(name), **scope, "name": name}
    try:
        return validate_record(ScopeRecord, data)
    except RecordInvalidError as error:
        raise GovernanceRefusedError(
            "the scope record is incomplete: " + "; ".join(error.problems)
        ) from None


def create_ontology(store: DatasetStore, scope: Mapping[str, Any], actor: Actor) -> ScopeRecord:
    """Create ``data/ontology-<name>/`` with the layout of FR-30 and a validated scope record.

    Only a domain admin may do this. The name must be kebab-case and not taken. The base IRI
    defaults to ``urn:domain-ai-assistant:ontology:<name>:``. A ``create`` decision is recorded.
    """
    require_admin(actor, "create an ontology")
    if not _KEBAB.fullmatch(store.name):
        raise GovernanceRefusedError(
            f"the ontology name {store.name!r} must be kebab-case, e.g. pets-and-house-rules"
        )
    record = _scope_record(store.name, scope)
    decision = new_decision(store, actor, DecisionAction.create, new=store.name)
    try:
        store.create(record, [decision])
    except DatasetExistsError:
        raise GovernanceRefusedError(f"the ontology {store.name!r} already exists") from None
    return record


def edit_scope(
    store: DatasetStore, scope: Mapping[str, Any], actor: Actor
) -> tuple[ScopeRecord, Decision]:
    """A new, validated scope record (domain admin only, FR-3) and its ``edit_scope`` decision.

    Nothing is written here: the caller writes both in one transaction.
    """
    require_admin(actor, "edit the scope record")
    old = store.read().scope()
    record = _scope_record(store.name, scope)
    decision = new_decision(
        store,
        actor,
        DecisionAction.edit_scope,
        field="scope",
        old=old.model_dump(mode="json", exclude_none=True) if old else None,
        new=record.model_dump(mode="json", exclude_none=True),
    )
    return record, decision


def require_scope(store: DatasetStore) -> ScopeRecord:
    """The ontology's scope record; refuses (as ingestion must) when it is missing or empty."""
    if not store.exists():
        raise GovernanceRefusedError(f"the ontology {store.name!r} does not exist")
    try:
        scope = store.read().scope()
    except RecordInvalidError as error:
        raise GovernanceRefusedError(
            "ingestion refused: the scope record is incomplete: " + "; ".join(error.problems)
        ) from None
    if scope is None:
        raise GovernanceRefusedError(
            "ingestion refused: the scope record is missing or empty; a domain admin must write it"
        )
    return scope
