"""A throw-away ontology outside git, for the evaluation (FR-38; plan 0002, Evaluation).

``create_scratch`` makes the LLM client first (so a missing key stops before anything is
written), then creates the ontology in the workspace's data folder, which the caller points at a
temporary folder. ``ScratchOntology`` estimates and ingests folders like ``OpenOntology`` does,
with the same rules (scope record, estimate, confirmation, one atomic write per run), but it
takes no lock, keeps no journal and makes no commit: nothing of it is ever meant to be kept.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from ontology_builder import governance, ingestion
from ontology_builder.governance import Actor
from ontology_builder.ingestion import IngestionRefusedError, RunPlan, Who
from ontology_builder.llm import LlmClient
from ontology_builder.store import DatasetStore
from ontology_builder.workflows.workspace import Workspace


@dataclass(frozen=True)
class ScratchEstimate:
    """The summed estimate of several folders, before anything is asked of the LLM (FR-6)."""

    documents: int
    units: int
    input_tokens: int
    output_tokens: int
    cost_usd: float | None
    """``None`` when the model's price is unknown."""


@dataclass(frozen=True)
class ScratchRun:
    """One completed ingestion run: its ID, status, source folder and the tokens it used."""

    run_id: str
    status: str
    source_path: str
    input_tokens: int
    output_tokens: int


def _total(plans: Sequence[RunPlan]) -> ScratchEstimate:
    costs = [plan.estimate.cost_usd for plan in plans]
    return ScratchEstimate(
        documents=sum(plan.estimate.documents for plan in plans),
        units=sum(plan.estimate.units for plan in plans),
        input_tokens=sum(plan.estimate.input_tokens for plan in plans),
        output_tokens=sum(plan.estimate.output_tokens for plan in plans),
        cost_usd=None if any(c is None for c in costs) else sum(c or 0.0 for c in costs),
    )


class ScratchOntology:
    """An ontology in a temporary data folder that is ingested without commits."""

    def __init__(self, workspace: Workspace, store: DatasetStore, client: LlmClient) -> None:
        self.workspace = workspace
        self.store = store
        self._client = client

    @property
    def model(self) -> str:
        return self._client.model

    def _plan(self, actor: Actor, folder: str) -> RunPlan:
        who = Who(actor.user, actor.role)
        sources = self.workspace.sources()
        return ingestion.plan_ingestion(self.store, sources, folder, self._client, who)

    def estimate(self, actor: Actor, folders: Sequence[str]) -> ScratchEstimate:
        """The estimate of ingesting every folder (under the sources root) as its own corpus."""
        return _total([self._plan(actor, folder) for folder in folders])

    def ingest(self, actor: Actor, folders: Sequence[str], *, confirm: bool) -> list[ScratchRun]:
        """Ingest each folder as a new corpus, one run after another; needs the confirmation of
        the estimate. A failed run raises ``IngestionFailedError`` and stops the rest."""
        if confirm is not True:
            raise IngestionRefusedError(
                "the evaluation needs confirmation: show the estimate and ask the person first"
            )
        runs = []
        for folder in folders:
            plan = self._plan(actor, folder)
            work = self.workspace.work_dir
            run = ingestion.start_run(self.store, plan, self._client, work, confirm=True)
            runs.append(
                ScratchRun(run.id, str(run.status), folder, run.input_tokens, run.output_tokens)
            )
        return runs


def create_scratch(
    workspace: Workspace, name: str, scope: Mapping[str, Any], actor: Actor
) -> ScratchOntology:
    """Create ontology ``name`` with ``scope`` in ``workspace.data_dir``, without git."""
    client = workspace.llm()
    store = workspace.store(name)
    governance.create_ontology(store, scope, actor)
    return ScratchOntology(workspace, store, client)
