"""Run a planned ingestion or on-demand extraction: confirmed, cached, resumable, all-or-nothing.

``start_run`` needs ``confirm=True``: the LLM is asked nothing before the person has seen the
estimate (FR-6). Pass 1 runs per batch (one document) and pass 2 once; each answer is cached in
the run's work folder as soon as it arrives. Only when everything is answered is the dataset
written, in one transaction: the corpus registry (or the marked units), the proposed elements and
the run record. If anything fails, the dataset is as it was and the run can be resumed with
``resume_run``, which asks only for the batches still missing (FR-8, AC-8).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from ontology_builder.extraction import (
    DocumentExtraction,
    ExtractionContext,
    TermInput,
    TermResolution,
    extract_document,
    resolve_terms,
)
from ontology_builder.ingestion.plan import (
    Batch,
    IngestionRefusedError,
    RunPlan,
    corpus_number,
    normalise_source_path,
    require_scope,
)
from ontology_builder.ingestion.work import RunFolder
from ontology_builder.llm import LlmClient
from ontology_builder.model import (
    Concept,
    Corpus,
    Decision,
    DecisionAction,
    ElementStatus,
    IgnorableStatus,
    IgnorableVerdict,
    Run,
    RunStatus,
    SourceUnit,
    validate_record,
)
from ontology_builder.store import DatasetFiles, DatasetStore

_NOT_IN_PLAY = {ElementStatus.excluded, ElementStatus.rejected, ElementStatus.deprecated}


class IngestionFailedError(RuntimeError):
    """A run stopped before it wrote anything; it can be resumed by its ID."""

    def __init__(self, run_id: str, reason: str) -> None:
        self.run_id = run_id
        super().__init__(
            f"run {run_id} stopped and nothing was written: {reason}. "
            f"Resume it with --resume {run_id}"
        )


@dataclass(frozen=True)
class WriteHooks:
    """What the caller adds to the final write (workflows: rebuild raw inside, commit after)."""

    before_swap: Callable[[DatasetFiles], None] | None = None
    after_swap: Callable[[], None] | None = None


def _dump(record: Any) -> Any:
    return record.model_dump(mode="json", exclude_none=True)


def _with[M: BaseModel](record_class: type[M], record: BaseModel, **changes: Any) -> M:
    return validate_record(record_class, _dump(record) | changes)


def _refuse_parallel_run(work_dir: Path, plan: RunPlan) -> None:
    """One unfinished run per source folder; another one must be resumed or discarded first."""
    for other in RunFolder.unfinished(work_dir, plan.ontology):
        known = other.plan()
        if plan.source_path is not None and known.source_path == plan.source_path:
            raise IngestionRefusedError(
                f"run {known.run_id} for {plan.source_path} is unfinished; "
                f"resume it with --resume {known.run_id} or discard it"
            )


def start_run(
    store: DatasetStore,
    plan: RunPlan,
    client: LlmClient,
    work_dir: Path,
    *,
    confirm: bool,
    hooks: WriteHooks | None = None,
) -> Run:
    """Run a plan once the person has confirmed its estimate; returns the completed run record."""
    if confirm is not True:
        raise IngestionRefusedError(
            "the run needs confirmation: show the estimate and ask the person first"
        )
    if client.model != plan.model:
        raise IngestionRefusedError(f"the run was estimated for {plan.model}, not {client.model}")
    _refuse_parallel_run(work_dir, plan)
    run = validate_record(
        Run,
        {
            "id": plan.run_id,
            "kind": plan.kind,
            "user": plan.user,
            "model": plan.model,
            "source_path": plan.source_path,
            "started_at": store.clock.now(),
            "status": RunStatus.running,
            "estimate": _dump(plan.estimate),
            "input_tokens": 0,
            "output_tokens": 0,
        },
    )
    folder = RunFolder.of(work_dir, plan.ontology, plan.run_id)
    folder.start(plan, run)
    return _execute(store, folder, client, hooks or WriteHooks())


def resume_run(
    store: DatasetStore,
    run_id: str,
    client: LlmClient,
    work_dir: Path,
    hooks: WriteHooks | None = None,
) -> Run:
    """Continue an interrupted or failed run; finished batches are not asked again."""
    folder = RunFolder.of(work_dir, store.name, run_id)
    plan = folder.plan()
    if client.model != plan.model:
        raise IngestionRefusedError(f"run {run_id} was made with {plan.model}, not {client.model}")
    store.recover()  # undo a write that was interrupted half-way
    folder.write_run(_with(Run, folder.run(), status=RunStatus.running))
    return _execute(store, folder, client, hooks or WriteHooks())


def discard_run(store: DatasetStore, run_id: str, work_dir: Path) -> None:
    """Drop an unfinished run and its cached answers; the dataset is not touched."""
    folder = RunFolder.of(work_dir, store.name, run_id)
    folder.plan()  # refuses an unknown run
    folder.remove()


def unfinished_runs(store: DatasetStore, work_dir: Path) -> list[Run]:
    """The run records of every unfinished run of the ontology."""
    return [folder.run() for folder in RunFolder.unfinished(work_dir, store.name)]


def _execute(store: DatasetStore, folder: RunFolder, client: LlmClient, hooks: WriteHooks) -> Run:
    plan = folder.plan()
    try:
        documents = _pass1(store, folder, plan, client)
        terms = _pass2(store, folder, plan, client, documents)
        run = _completed(store, folder.run(), documents, terms)
        _write(store, plan, documents, terms, run, hooks)
    except Exception as error:
        failed = _with(Run, folder.run(), status=RunStatus.failed, ended_at=store.clock.now())
        folder.write_run(failed)
        raise IngestionFailedError(plan.run_id, str(error)) from error
    folder.remove()
    return run


def _context(store: DatasetStore, plan: RunPlan) -> ExtractionContext:
    return ExtractionContext(
        scope=require_scope(store.read(), store.name),
        run_id=plan.run_id,
        clock=store.clock,
        minter=store.minter,
        not_ignorable=frozenset(plan.not_ignorable),
    )


def _pass1(
    store: DatasetStore, folder: RunFolder, plan: RunPlan, client: LlmClient
) -> list[DocumentExtraction]:
    """Pass 1 for every batch, from the cache where it already ran."""
    context = _context(store, plan)
    results = []
    for batch in plan.batches:
        result = folder.pass1(batch.document.id)
        if result is None:
            result = _extract(client, batch, context)
            folder.save_pass1(result)
        results.append(result)
    return results


def _extract(client: LlmClient, batch: Batch, context: ExtractionContext) -> DocumentExtraction:
    if not batch.units:  # an empty document: nothing to ask
        return DocumentExtraction(batch.document.id)
    return extract_document(client, batch.document, batch.units, context)


def _existing_concepts(store: DatasetStore) -> list[Concept]:
    return [
        element
        for element in store.read().elements().values()
        if isinstance(element, Concept) and element.status not in _NOT_IN_PLAY
    ]


def _pass2(
    store: DatasetStore,
    folder: RunFolder,
    plan: RunPlan,
    client: LlmClient,
    documents: list[DocumentExtraction],
) -> TermResolution:
    """Pass 2 over the new elements of every batch and the concepts already in the ontology."""
    cached = folder.pass2()
    if cached is not None:
        return cached
    found = TermInput(
        elements=[element for document in documents for element in document.elements],
        units={unit.id: unit for unit in plan.units},
        existing=_existing_concepts(store),
    )
    result = resolve_terms(client, found)
    folder.save_pass2(result)
    return result


def _completed(
    store: DatasetStore, run: Run, documents: list[DocumentExtraction], terms: TermResolution
) -> Run:
    skipped = [item for document in documents for item in document.skipped] + terms.skipped
    return _with(
        Run,
        run,
        status=RunStatus.completed,
        ended_at=store.clock.now(),
        input_tokens=sum(d.input_tokens for d in documents) + terms.input_tokens,
        output_tokens=sum(d.output_tokens for d in documents) + terms.output_tokens,
        skipped=[_dump(item) for item in skipped],
    )


def _write(
    store: DatasetStore,
    plan: RunPlan,
    documents: list[DocumentExtraction],
    terms: TermResolution,
    run: Run,
    hooks: WriteHooks,
) -> None:
    """Write everything of the run in one transaction (one atomic swap)."""
    verdicts = {unit: verdict for d in documents for unit, verdict in d.verdicts.items()}
    with store.transaction(hooks.after_swap) as files:
        if plan.corpus is not None:
            _write_corpus(files, plan, plan.corpus, verdicts)
        else:
            _write_kept(store, files, plan)
        for element in terms.elements:
            files.write_element(element)
        files.write_run(run)
        if hooks.before_swap is not None:
            hooks.before_swap(files)


def _with_verdict(unit: SourceUnit, verdict: IgnorableVerdict | None) -> SourceUnit:
    return unit if verdict is None else _with(SourceUnit, unit, ignorable=_dump(verdict))


def _write_corpus(
    files: DatasetFiles, plan: RunPlan, new: Corpus, verdicts: dict[str, IgnorableVerdict]
) -> None:
    """The new corpus registry, with each unit's ignorable verdict; numbered at write time."""
    for folder, corpus in files.corpora().items():
        if normalise_source_path(corpus.source_path) == plan.source_path:
            raise IngestionRefusedError(
                f"{plan.source_path} was ingested as corpus {folder} while this run was going on"
            )
    corpus = _with(Corpus, new, number=corpus_number(files))
    folder = f"{corpus.number:02d}_{corpus.slug}"
    files.write_corpus(folder, corpus)
    for batch in plan.batches:
        files.write_document(folder, batch.document)
        units = [_with_verdict(unit, verdicts.get(unit.id)) for unit in batch.units]
        files.write_units(folder, batch.document.id, units)


def _write_kept(store: DatasetStore, files: DatasetFiles, plan: RunPlan) -> None:
    """Mark the units of an on-demand run not ignorable, with one decision each (FR-14, FR-26)."""
    kept = set(plan.not_ignorable)
    decisions = []
    for batch in plan.batches:
        units = files.units(batch.folder, batch.document.id)
        changed = []
        for unit in units:
            if unit.id in kept and unit.ignorable is not None:
                verdict = _with(IgnorableVerdict, unit.ignorable, status=IgnorableStatus.rejected)
                changed.append(_with(SourceUnit, unit, ignorable=_dump(verdict)))
                decisions.append(_kept_decision(store, plan, unit.id))
            else:
                changed.append(unit)
        files.write_units(batch.folder, batch.document.id, changed)
    files.append_decisions(decisions)


def _kept_decision(store: DatasetStore, plan: RunPlan, unit_id: str) -> Decision:
    return validate_record(
        Decision,
        {
            "id": store.minter.new("decision"),
            "at": store.clock.now(),
            "user": plan.user,
            "role": plan.role,
            "action": DecisionAction.not_ignorable,
            "element_id": unit_id,
            "field": "ignorable.status",
            "old": str(IgnorableStatus.proposed),
            "new": str(IgnorableStatus.rejected),
            "reason": f"marked not ignorable; extracted in run {plan.run_id}",
        },
    )
