"""An open ontology: review on a pending change set, then save, publish or ingest
(plan 0002, Approach 6; ontology-builder/ADR-0004).

``open_ontology`` takes the process lock and loads the change set, re-applying a journal left by
an earlier process. Every action changes only the change set and its journal. ``save`` checks
that the dataset is as it was loaded, writes the changed records and the decisions, rebuilds the
raw release, swaps the staging copy in and commits; if anything fails the dataset is swapped
back and the change set is kept. Publishing and ingesting need a saved change set first.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Self

from ontology_builder import governance, ingestion, release
from ontology_builder.governance import ActionResult, Actor, ChangeSet
from ontology_builder.ingestion import RunPlan, Who, WriteHooks
from ontology_builder.release import PublishResult
from ontology_builder.store import DatasetFiles, DatasetStore
from ontology_builder.vcs import CommitResult, GitRepo
from ontology_builder.workflows.commit import (
    Commit,
    build_info,
    commit_transaction,
    ready_repo,
)
from ontology_builder.workflows.errors import NotFoundError, WorkflowRefusedError
from ontology_builder.workflows.journal import Journal
from ontology_builder.workflows.lock import ProcessLock
from ontology_builder.workflows.views import (
    UnitInfo,
    corpora,
    corpus_units,
    element_detail,
    element_index,
)
from ontology_builder.workflows.workspace import Workspace

_RUN_ID = re.compile(r"run_[0-9A-HJKMNP-TV-Z]{26}")


@dataclass(frozen=True)
class PublishOutcome:
    """The release result (governed, or the offenders) and the commit that holds it."""

    result: PublishResult
    commit: CommitResult


@dataclass(frozen=True)
class IngestOutcome:
    """A completed run and the commit of what it wrote."""

    run_id: str
    status: str
    commit: CommitResult


class OpenOntology:
    """One ontology opened by this process; ``close`` (or the ``with`` block) releases it."""

    def __init__(
        self, workspace: Workspace, store: DatasetStore, lock: ProcessLock, journal: Journal
    ) -> None:
        self.workspace = workspace
        self.store = store
        self._lock = lock
        self._journal = journal
        self.changes = ChangeSet.load(store)
        self._tree = store.tree_hash()
        self._units: dict[str, UnitInfo] | None = None
        self._restore()

    @property
    def name(self) -> str:
        return self.store.name

    @property
    def pending(self) -> int:
        """How many records the unsaved changes touch."""
        return self.changes.pending

    def close(self) -> None:
        """Release the lock; unsaved changes stay in the journal for the next open."""
        self._lock.release()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        trace: TracebackType | None,
    ) -> None:
        self.close()

    # ---- reading: plain data for the callers ----

    def _unit_map(self) -> dict[str, UnitInfo]:
        if self._units is None:
            self._units = corpus_units(self.store.read())
        return self._units

    def index(self) -> list[dict[str, Any]]:
        """The compact index of every element, unsaved changes included (FR-19)."""
        return element_index(self.changes, self._unit_map())

    def detail(self, element_id: str) -> dict[str, Any]:
        """One element: evidence passages, the record and its decisions (FR-16, FR-26)."""
        if element_id not in self.changes.elements:
            raise NotFoundError(f"unknown element {element_id!r}")
        return element_detail(self.changes, self._unit_map(), self.store.read(), element_id)

    def corpora(self) -> list[dict[str, Any]]:
        return corpora(self.store.read())

    def scope(self) -> dict[str, Any]:
        record = self.store.read().scope()
        return record.model_dump(mode="json", exclude_none=True) if record else {}

    def run(self, run_id: str) -> dict[str, Any]:
        """The record of a finished run (model, tokens, times, skipped items; FR-6)."""
        if not _RUN_ID.fullmatch(run_id):
            raise NotFoundError(f"unknown run {run_id!r}")
        try:
            record = self.store.read().run(run_id)
        except FileNotFoundError:
            raise NotFoundError(f"unknown run {run_id!r}") from None
        return record.model_dump(mode="json", exclude_none=True)

    # ---- review and authoring: the change set only ----

    def _restore(self) -> None:
        data = self._journal.read()
        if data is None:
            return
        if data.get("tree_hash") != self._tree:
            raise WorkflowRefusedError(
                f"the ontology {self.name!r} changed on disk since its unsaved changes were "
                "journaled; open it with discard_journal to drop them"
            )
        self.changes.restore(data["changes"])

    def _journaled[T](self, result: T) -> T:
        self._journal.write(self._tree, self.changes)
        return result

    def act(
        self, actor: Actor, action: str, element_ids: Iterable[str], payload: Mapping[str, Any]
    ) -> list[ActionResult]:
        """One review or governance action on each ID, with a result per ID (FR-17, FR-18)."""
        results = governance.apply_bulk(self.changes, actor, action, element_ids, payload)
        return self._journaled(results)

    def add_statement(self, actor: Actor, text: str) -> str:
        """A new user statement (FR-21); returns its ID."""
        return self._journaled(governance.add_user_statement(self.changes, actor, text).id)

    def revise_statement(self, actor: Actor, unit_id: str, text: str) -> str:
        unit = governance.revise_user_statement(self.changes, actor, unit_id, text)
        return self._journaled(unit.id)

    def author(self, actor: Actor, element_type: str, fields: Mapping[str, Any]) -> str:
        """An authored element (FR-22); returns its ID."""
        element = governance.author_element(self.changes, actor, element_type, fields)
        return self._journaled(element.id)

    # ---- writing: one transaction and one commit each ----

    def _ready(self) -> GitRepo:
        repo = ready_repo(self.store.root)
        if self.store.tree_hash() != self._tree:
            raise WorkflowRefusedError(
                f"the ontology {self.name!r} changed on disk since it was opened; reload it"
            )
        return repo

    def _require_saved(self, what: str) -> None:
        if self.changes.pending or self.changes.decisions:
            raise WorkflowRefusedError(f"save or discard the unsaved changes before you {what}")

    def _written(self) -> None:
        self._tree = self.store.tree_hash()
        self._units = None

    def edit_scope(self, actor: Actor, scope: Mapping[str, Any]) -> CommitResult:
        """Replace the scope record (domain admin only, FR-3) in one commit with its decision."""
        record, decision = governance.edit_scope(self.store, scope, actor)
        self._require_saved("edit the scope record")
        repo = self._ready()
        info = build_info(repo, self.store)

        def write(files: DatasetFiles) -> None:
            files.write_scope(record)
            files.append_decisions([decision])
            release.save_raw(files, info)

        commit = Commit(repo, self.store, f"Edit the scope record of ontology {self.name}")
        result = commit_transaction(self.store, commit, write)
        self._written()
        return result

    def build(self) -> str:
        """Rebuild the raw release from the saved records, without a commit; returns its folder."""
        self._require_saved("build the raw release")
        repo = self._ready()
        info = build_info(repo, self.store)
        with self.store.transaction() as files:
            release.save_raw(files, info)
        self._written()
        return str(self.store.read().release_dir("raw"))

    def save(self) -> CommitResult:
        """Write the pending changes and the raw release as one commit (FR-27, FR-28)."""
        if not self.changes.pending and not self.changes.decisions:
            return CommitResult(True, None, "nothing to save")
        repo = self._ready()
        info = build_info(repo, self.store)

        def write(files: DatasetFiles) -> None:
            self.changes.write(files)
            release.save_raw(files, info)

        decisions = len(self.changes.decisions)
        message = f"Save ontology {self.name}: {decisions} decisions"
        result = commit_transaction(self.store, Commit(repo, self.store, message), write)
        if result.ok:
            self.changes.mark_saved()
            self._journal.clear()
            self._written()
        return result

    def publish(self, actor: Actor, version: str | None = None) -> PublishOutcome:
        """Rebuild raw and, unless FR-35 finds offenders, the governed release; one commit."""
        governance.require_admin(actor, "publish a governed release")
        self._require_saved("publish")
        repo = self._ready()
        info = build_info(repo, self.store)
        commit = Commit(repo, self.store, f"Rebuild the raw release of ontology {self.name}")
        built: list[PublishResult] = []

        def write(files: DatasetFiles) -> None:
            result = release.publish(files, info, version)
            if result.governed is not None:
                number = result.governed.version
                files.append_decisions([governance.publish_decision(self.store, actor, number)])
                commit.message = f"Publish ontology {self.name} {number}"
            built.append(result)

        committed = commit_transaction(self.store, commit, write)
        self._written()
        return PublishOutcome(built[0], committed)

    # ---- ingestion ----

    def _who(self, actor: Actor) -> Who:
        return Who(actor.user, actor.role)

    def plan_ingestion(self, actor: Actor, folder: str) -> RunPlan:
        """The estimate of ingesting ``folder`` (under the sources root) as a new corpus (FR-6)."""
        sources = self.workspace.sources()
        client = self.workspace.llm()
        return ingestion.plan_ingestion(self.store, sources, folder, client, self._who(actor))

    def plan_on_demand(self, actor: Actor, unit_ids: list[str]) -> RunPlan:
        """The estimate of extracting units marked not ignorable (FR-14)."""
        client = self.workspace.llm()
        return ingestion.plan_on_demand(self.store, unit_ids, client, self._who(actor))

    def _hooks(self, repo: GitRepo, message: str) -> tuple[WriteHooks, Commit]:
        info = build_info(repo, self.store)
        commit = Commit(repo, self.store, message)

        def rebuild_raw(files: DatasetFiles) -> None:
            release.save_raw(files, info)

        return WriteHooks(before_swap=rebuild_raw, after_swap=commit), commit

    def _ran(self, commit: Commit, run_id: str, status: str) -> IngestOutcome:
        self.changes = ChangeSet.load(self.store)
        self._written()
        return IngestOutcome(run_id, status, commit.result)

    def ingest(self, plan: RunPlan, *, confirm: bool) -> IngestOutcome:
        """Run a confirmed plan; everything it writes and the raw release go into one commit."""
        self._require_saved("ingest")
        repo = self._ready()
        hooks, commit = self._hooks(repo, f"Ingest into ontology {self.name} (run {plan.run_id})")
        client = self.workspace.llm()
        work = self.workspace.work_dir
        run = ingestion.start_run(self.store, plan, client, work, confirm=confirm, hooks=hooks)
        return self._ran(commit, run.id, str(run.status))

    def resume(self, run_id: str) -> IngestOutcome:
        """Continue a failed or interrupted run from its cached answers (FR-8)."""
        self._require_saved("resume a run")
        repo = self._ready()
        hooks, commit = self._hooks(repo, f"Ingest into ontology {self.name} (run {run_id})")
        client = self.workspace.llm()
        run = ingestion.resume_run(self.store, run_id, client, self.workspace.work_dir, hooks)
        return self._ran(commit, run.id, str(run.status))


def open_ontology(
    workspace: Workspace, name: str, *, discard_journal: bool = False
) -> OpenOntology:
    """Open an ontology for this process: take the lock, finish or undo an interrupted write,
    load the records and re-apply the journal of unsaved changes."""
    store = workspace.store(name)
    if not store.exists():
        raise WorkflowRefusedError(f"the ontology {name!r} does not exist")
    folder = workspace.ontology_dir(name)
    lock = ProcessLock(folder / "server.lock")
    lock.acquire()
    try:
        store.recover()
        journal = Journal(folder / "journal.json")
        if discard_journal:
            journal.clear()
        session = OpenOntology(workspace, store, lock, journal)
    except BaseException:
        lock.release()
        raise
    return session
