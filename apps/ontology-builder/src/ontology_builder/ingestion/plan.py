"""What a run will do, and what it is estimated to cost, before the LLM is called (FR-6).

A ``RunPlan`` is made by ``plan_ingestion`` (a new corpus, FR-4) or ``plan_on_demand`` (units a
person marked not ignorable, FR-14). It holds the minted IDs of everything it will write, so a run
that is resumed writes exactly what an uninterrupted run would (FR-8). Making a plan reads the
dataset and counts tokens; it never asks the LLM for an answer and never writes anything.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from ontology_builder import llm
from ontology_builder.extraction import pass1_requests
from ontology_builder.llm import LlmClient, Pricing
from ontology_builder.model import (
    Corpus,
    Document,
    Estimate,
    IgnorableStatus,
    RecordInvalidError,
    Role,
    RunKind,
    ScopeRecord,
    SourceUnit,
    validate_record,
)
from ontology_builder.sources import CorpusLimitError, next_corpus_number, read_corpus
from ontology_builder.store import DatasetFiles, DatasetStore


class IngestionRefusedError(ValueError):
    """A run is refused before anything is asked or written; the message says why."""


@dataclass(frozen=True)
class Batch:
    """One document of a run: pass 1 runs on its units, and its answer is cached on its own."""

    folder: str
    """The corpus folder under ``00_sources/`` (``NN_<slug>``)."""
    document: Document
    units: list[SourceUnit]


@dataclass(frozen=True)
class RunPlan:
    """Everything a run needs, fixed before it starts."""

    ontology: str
    run_id: str
    kind: RunKind
    user: str
    role: Role
    model: str
    estimate: Estimate
    batches: list[Batch]
    corpus: Corpus | None = None
    """The new corpus of an ingestion; ``None`` for an on-demand extraction."""
    source_path: str | None = None
    not_ignorable: list[str] = field(default_factory=list)
    """Units a person marked not ignorable (on-demand extraction)."""

    @property
    def units(self) -> list[SourceUnit]:
        return [unit for batch in self.batches for unit in batch.units]


def require_scope(files: DatasetFiles, name: str) -> ScopeRecord:
    """The scope record; a run is refused while it is missing, empty or incomplete (FR-1, AC-1)."""
    try:
        scope = files.scope()
    except RecordInvalidError as error:
        raise IngestionRefusedError(
            f"ingestion into {name!r} refused: the scope record is incomplete: "
            + "; ".join(error.problems)
        ) from None
    if scope is None:
        raise IngestionRefusedError(
            f"ingestion into {name!r} refused: the scope record is missing or empty; "
            "a domain admin must write it first"
        )
    return scope


def _estimate(
    batches: list[Batch],
    scope: ScopeRecord,
    client: LlmClient,
    pricing: Pricing,
    not_ignorable: list[str],
) -> Estimate:
    """Counts and tokens of pass 1 for every batch with units (the requests that will be sent)."""
    requests = [
        request
        for batch in batches
        if batch.units
        for request in pass1_requests(batch.document, batch.units, scope, not_ignorable)
    ]
    tokens = llm.estimate(requests, client.model, client.count_tokens, pricing)
    return validate_record(
        Estimate,
        {
            "documents": len(batches),
            "units": sum(len(batch.units) for batch in batches),
            "input_tokens": tokens.input_tokens,
            "output_tokens": tokens.output_tokens,
            "cost_usd": tokens.cost_usd,
        },
    )


def normalise_source_path(source_path: str) -> str:
    """The source folder relative to the shared data folder, as ``corpus.yaml`` records it."""
    path = PurePosixPath(source_path.strip().replace("\\", "/"))
    if not source_path.strip() or path.is_absolute() or ".." in path.parts:
        raise IngestionRefusedError(
            f"the source folder {source_path!r} must be a path inside the shared data folder"
        )
    return path.as_posix()


def _refuse_already_ingested(files: DatasetFiles, name: str, source_path: str) -> None:
    for folder, corpus in files.corpora().items():
        if normalise_source_path(corpus.source_path) == source_path:
            raise IngestionRefusedError(
                f"{source_path} was already ingested into {name!r} as corpus {folder}; "
                "re-ingesting a corpus is not supported yet"
            )


def corpus_number(files: DatasetFiles) -> int:
    """The next free corpus number 00-89 of the dataset."""
    try:
        return next_corpus_number(files.corpora())
    except CorpusLimitError as error:
        raise IngestionRefusedError(str(error)) from None


@dataclass(frozen=True)
class Who:
    """Who starts a run: a handle and a role."""

    user: str
    role: Role


def plan_ingestion(
    store: DatasetStore,
    sources_root: Path,
    source_path: str,
    client: LlmClient,
    who: Who,
    pricing: Pricing | None = None,
) -> RunPlan:
    """Plan the ingestion of ``sources_root / source_path`` as a new corpus (FR-4 to FR-7).

    Refused when the scope record is missing, the folder is missing, holds no Markdown file or
    was already ingested into this ontology. The estimate counts pass 1 of every document.
    """
    if not store.exists():
        raise IngestionRefusedError(f"the ontology {store.name!r} does not exist")
    files = store.read()
    scope = require_scope(files, store.name)
    path = normalise_source_path(source_path)
    folder = sources_root / path
    if not folder.is_dir():
        raise IngestionRefusedError(f"the source folder {path} does not exist")
    _refuse_already_ingested(files, store.name, path)
    run_id = store.minter.new("run")
    corpus = read_corpus(
        folder, source_path=path, number=corpus_number(files), run_id=run_id, minter=store.minter
    )
    if not corpus.documents:
        raise IngestionRefusedError(f"the source folder {path} holds no Markdown file")
    batches = [Batch(corpus.folder, item.document, item.units) for item in corpus.documents]
    return RunPlan(
        ontology=store.name,
        run_id=run_id,
        kind=RunKind.ingestion,
        user=who.user,
        role=who.role,
        model=client.model,
        estimate=_estimate(batches, scope, client, pricing or Pricing.load(), []),
        batches=batches,
        corpus=corpus.corpus,
        source_path=path,
    )


def _find_units(files: DatasetFiles, unit_ids: list[str]) -> dict[str, tuple[str, Document]]:
    """Where each wanted unit is: its corpus folder and document."""
    found: dict[str, tuple[str, Document]] = {}
    wanted = set(unit_ids)
    for folder in files.corpora():
        for document in files.documents(folder):
            for unit in files.units(folder, document.id):
                if unit.id in wanted:
                    found[unit.id] = (folder, document)
    return found


def _check_ignorable(unit: SourceUnit) -> None:
    verdict = unit.ignorable
    if verdict is None or verdict.status != IgnorableStatus.proposed:
        state = "not proposed ignorable" if verdict is None else f"already {verdict.status}"
        raise IngestionRefusedError(
            f"unit {unit.id} is {state}; only a unit proposed ignorable can be marked not ignorable"
        )


def _on_demand_batches(files: DatasetFiles, unit_ids: list[str]) -> list[Batch]:
    """One batch per document, holding only the wanted units of it, in document order."""
    where = _find_units(files, unit_ids)
    missing = [unit_id for unit_id in unit_ids if unit_id not in where]
    if missing:
        raise IngestionRefusedError(f"unknown source unit {', '.join(missing)}")
    batches: dict[str, Batch] = {}
    for folder, document in where.values():
        if document.id in batches:
            continue
        units = [u for u in files.units(folder, document.id) if u.id in where]
        for unit in units:
            _check_ignorable(unit)
        batches[document.id] = Batch(folder, document, units)
    return list(batches.values())


def plan_on_demand(
    store: DatasetStore,
    unit_ids: list[str],
    client: LlmClient,
    who: Who,
    pricing: Pricing | None = None,
) -> RunPlan:
    """Plan the extraction of units a person marks not ignorable (FR-14, AC-13).

    Each unit must be proposed ignorable and not yet confirmed or rejected. Pass 1 runs on the
    marked units only, with the note that a person kept them.
    """
    if not unit_ids:
        raise IngestionRefusedError("no source unit was given")
    if not store.exists():
        raise IngestionRefusedError(f"the ontology {store.name!r} does not exist")
    files = store.read()
    scope = require_scope(files, store.name)
    batches = _on_demand_batches(files, list(dict.fromkeys(unit_ids)))
    kept = [unit.id for batch in batches for unit in batch.units]
    return RunPlan(
        ontology=store.name,
        run_id=store.minter.new("run"),
        kind=RunKind.on_demand,
        user=who.user,
        role=who.role,
        model=client.model,
        estimate=_estimate(batches, scope, client, pricing or Pricing.load(), kept),
        batches=batches,
        not_ignorable=kept,
    )
