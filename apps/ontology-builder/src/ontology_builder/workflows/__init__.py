"""workflows component.

Runs the app's use cases (create, ingest, review, save, publish) across the components below it.

``Workspace`` (or ``workspace_from_env``) says where the datasets and the work folder are and how
to make an LLM client. ``create_ontology`` creates and commits a new ontology. ``open_ontology``
takes the process lock and gives an ``OpenOntology``: review actions and authoring change its
pending change set (journaled in the work folder); ``save``, ``publish`` and ``ingest`` each write
in one atomic swap followed by one git commit of the dataset, and roll back when it fails.
``index``, ``detail``, ``corpora``, ``scope`` and ``run`` return plain data for the callers, and
the role, refusal and error types they need are re-exported here. ``create_scratch`` makes a
throw-away ontology that is ingested without any commit, for the evaluation (FR-38).
"""

from __future__ import annotations

from ontology_builder.governance import ADMIN_ACTIONS, Actor, GovernanceRefusedError, actor_of
from ontology_builder.ingestion import IngestionFailedError, IngestionRefusedError
from ontology_builder.llm import LlmError
from ontology_builder.workflows.create import create_ontology
from ontology_builder.workflows.errors import NotFoundError, WorkflowRefusedError
from ontology_builder.workflows.lock import ProcessLock
from ontology_builder.workflows.scratch import (
    ScratchEstimate,
    ScratchOntology,
    ScratchRun,
    create_scratch,
)
from ontology_builder.workflows.session import (
    IngestOutcome,
    OpenOntology,
    PublishOutcome,
    open_ontology,
)
from ontology_builder.workflows.views import USER_STATEMENTS, filter_index
from ontology_builder.workflows.workspace import FIXTURES_DIR, Workspace, workspace_from_env

__all__ = [
    "ADMIN_ACTIONS",
    "FIXTURES_DIR",
    "USER_STATEMENTS",
    "Actor",
    "GovernanceRefusedError",
    "IngestOutcome",
    "IngestionFailedError",
    "IngestionRefusedError",
    "LlmError",
    "NotFoundError",
    "OpenOntology",
    "ProcessLock",
    "PublishOutcome",
    "ScratchEstimate",
    "ScratchOntology",
    "ScratchRun",
    "WorkflowRefusedError",
    "Workspace",
    "actor_of",
    "create_ontology",
    "create_scratch",
    "filter_index",
    "open_ontology",
    "workspace_from_env",
]
