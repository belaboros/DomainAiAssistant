"""Ontologies, the scope record, the element index and detail, review actions and authoring."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Query

from ontology_builder.api.deps import Ontology, Reader, Server, Writer, require_admin
from ontology_builder.api.schemas import (
    ActionIn,
    ActionResultOut,
    ActionsOut,
    AuthorIn,
    CommitOut,
    CorpusOut,
    CreateOntology,
    ElementDetailOut,
    ElementFilter,
    ElementsOut,
    IdOut,
    IndexEntryOut,
    StatementIn,
)
from ontology_builder.workflows import ADMIN_ACTIONS, create_ontology, filter_index

router = APIRouter(prefix="/api/ontologies", tags=["review"])
ONE = "/{name}"


def _commit(result: Any) -> CommitOut:
    return CommitOut(ok=result.ok, sha=result.sha, output=result.output)


@router.get("")
def ontologies(state: Server, actor: Reader) -> list[str]:
    if state.ontology is None:
        raise HTTPException(503, "no ontology is open on this server")
    return state.ontology.workspace.ontologies()


@router.post("")
def create(body: CreateOntology, state: Server, actor: Writer) -> CommitOut:
    """Create and commit a new ontology (domain admin only, FR-1)."""
    require_admin(actor, "create an ontology")
    if state.ontology is None:
        raise HTTPException(503, "no ontology is open on this server")
    with state.lock:
        return _commit(create_ontology(state.ontology.workspace, body.name, body.scope, actor))


@router.get(ONE + "/scope")
def scope(ontology: Ontology, actor: Reader) -> dict[str, Any]:
    return ontology.scope()


@router.put(ONE + "/scope")
def edit_scope(body: dict[str, Any], ontology: Ontology, actor: Writer) -> CommitOut:
    """Replace the scope record (domain admin only, FR-3), in one commit."""
    require_admin(actor, "edit the scope record")
    return _commit(ontology.edit_scope(actor, body))


@router.get(ONE + "/elements")
def elements(
    filters: Annotated[ElementFilter, Query()], ontology: Ontology, actor: Reader
) -> ElementsOut:
    """The compact index of every element; the optional filters are those of the GUI."""
    found = filter_index(ontology.index(), filters.model_dump())
    return ElementsOut(
        elements=[IndexEntryOut.model_validate(e) for e in found],
        corpora=[CorpusOut.model_validate(c) for c in ontology.corpora()],
        pending=ontology.pending,
    )


@router.get(ONE + "/elements/{element_id}")
def element(element_id: str, ontology: Ontology, actor: Reader) -> ElementDetailOut:
    """One element: its evidence passages first, then the record and its decisions (FR-16)."""
    return ElementDetailOut.model_validate(ontology.detail(element_id))


@router.post(ONE + "/actions")
def act(body: ActionIn, ontology: Ontology, actor: Writer) -> ActionsOut:
    """One action on each ID, checked for role and status per ID (FR-17, FR-18)."""
    if body.action in ADMIN_ACTIONS:
        require_admin(actor, body.action)
    results = ontology.act(actor, body.action, body.ids, body.payload)
    return ActionsOut(
        results=[
            ActionResultOut(element_id=r.element_id, ok=r.ok, message=r.message) for r in results
        ],
        pending=ontology.pending,
    )


@router.post(ONE + "/statements")
def add_statement(body: StatementIn, ontology: Ontology, actor: Writer) -> IdOut:
    return IdOut(id=ontology.add_statement(actor, body.text))


@router.put(ONE + "/statements/{unit_id}")
def revise_statement(unit_id: str, body: StatementIn, ontology: Ontology, actor: Writer) -> IdOut:
    return IdOut(id=ontology.revise_statement(actor, unit_id, body.text))


@router.post(ONE + "/elements")
def author(body: AuthorIn, ontology: Ontology, actor: Writer) -> IdOut:
    """An authored element; it must cite evidence (FR-22)."""
    return IdOut(id=ontology.author(actor, body.type, body.fields))
