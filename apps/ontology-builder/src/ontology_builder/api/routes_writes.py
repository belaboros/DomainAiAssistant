"""Save, publish and ingest: each writes one atomic change and one git commit; and run records."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from ontology_builder.api.deps import Ontology, Reader, Writer, require_admin
from ontology_builder.api.schemas import (
    CommitOut,
    EstimateOut,
    IngestIn,
    IngestOut,
    PublishIn,
    PublishOut,
    ReferenceOut,
    RunOut,
)
from ontology_builder.workflows import Actor, OpenOntology

router = APIRouter(prefix="/api/ontologies/{name}", tags=["writes"])


def _commit(result: Any) -> CommitOut:
    return CommitOut(ok=result.ok, sha=result.sha, output=result.output)


def _references(found: list[Any]) -> list[ReferenceOut]:
    return [
        ReferenceOut(
            element_id=r.element_id,
            element_label=r.element_label,
            target_id=r.target_id,
            target_label=r.target_label,
            target_status=r.target_status,
        )
        for r in found
    ]


@router.post("/save")
def save(ontology: Ontology, actor: Writer) -> CommitOut:
    """Write the pending changes and the raw release as one commit, or return the hook output
    (FR-27); nothing is pushed."""
    return _commit(ontology.save())


@router.post("/publish")
def publish(body: PublishIn, ontology: Ontology, actor: Writer) -> PublishOut:
    """Build the governed release (domain admin only), or list the offenders (FR-29, FR-35)."""
    require_admin(actor, "publish a governed release")
    outcome = ontology.publish(actor, body.version)
    governed = outcome.result.governed
    return PublishOut(
        version=governed.version if governed else None,
        changelog=governed.files.get("CHANGELOG.md") if governed else None,
        offenders=_references(outcome.result.offenders),
        warnings=_references(outcome.result.warnings),
        commit=_commit(outcome.commit),
    )


def _plan(ontology: OpenOntology, actor: Actor, body: IngestIn) -> Any:
    if body.folder and not body.units:
        return ontology.plan_ingestion(actor, body.folder)
    if body.units and not body.folder:
        return ontology.plan_on_demand(actor, body.units)
    raise HTTPException(422, "give either a folder or the units marked not ignorable")


@router.post("/ingestions/estimate")
def estimate(body: IngestIn, ontology: Ontology, actor: Writer) -> EstimateOut:
    """What a run would cost, before any LLM call (FR-6)."""
    plan = _plan(ontology, actor, body)
    shown = plan.estimate
    return EstimateOut(
        model=plan.model,
        documents=shown.documents,
        units=shown.units,
        input_tokens=shown.input_tokens,
        output_tokens=shown.output_tokens,
        cost_usd=shown.cost_usd,
    )


@router.post("/ingestions")
def ingest(body: IngestIn, ontology: Ontology, actor: Writer) -> IngestOut:
    """Run an ingestion or on-demand extraction, only once its estimate is confirmed (FR-6)."""
    if not body.confirm:
        raise HTTPException(409, "confirm the estimate first: nothing was run")
    outcome = ontology.ingest(_plan(ontology, actor, body), confirm=True)
    return IngestOut(run_id=outcome.run_id, status=outcome.status, commit=_commit(outcome.commit))


@router.get("/runs/{run_id}")
def run(run_id: str, ontology: Ontology, actor: Reader) -> RunOut:
    """The record of a run: model, tokens used, start and end (FR-6)."""
    return RunOut.model_validate(ontology.run(run_id))
