"""ingestion component.

Runs one ingestion or on-demand extraction, resumable and all-or-nothing.

1. ``plan_ingestion`` (a folder as a new corpus) or ``plan_on_demand`` (units marked not
   ignorable) makes a ``RunPlan`` with its estimate: documents, units, tokens and cost (FR-6). It
   refuses a missing scope record and a folder already ingested (FR-1, FR-7). No LLM answer is
   asked for and nothing is written.
2. ``start_run(..., confirm=True)`` runs it: pass 1 per document and pass 2, each answer cached
   in the run's work folder, then one atomic write of the registry, the elements and the run record.
3. If it fails, the dataset is unchanged and ``resume_run`` continues from the cache (FR-8);
   ``discard_run`` drops it.
"""

from __future__ import annotations

from ontology_builder.ingestion.plan import (
    Batch,
    IngestionRefusedError,
    RunPlan,
    Who,
    plan_ingestion,
    plan_on_demand,
)
from ontology_builder.ingestion.run import (
    IngestionFailedError,
    WriteHooks,
    discard_run,
    resume_run,
    start_run,
    unfinished_runs,
)

__all__ = [
    "Batch",
    "IngestionFailedError",
    "IngestionRefusedError",
    "RunPlan",
    "Who",
    "WriteHooks",
    "discard_run",
    "plan_ingestion",
    "plan_on_demand",
    "resume_run",
    "start_run",
    "unfinished_runs",
]
