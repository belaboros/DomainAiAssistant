"""One store transaction that ends in one git commit of the dataset (ontology-builder/ADR-0004).

The staging copy is written, swapped in, and then committed with the hooks running. If the
commit fails, the store swaps the previous folder back, so nothing is left outside a commit.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ontology_builder.release import BuildInfo
from ontology_builder.store import DatasetFiles, DatasetStore
from ontology_builder.vcs import CommitResult, GitRepo, VcsRefusedError
from ontology_builder.workflows.errors import WorkflowRefusedError


class CommitFailedError(RuntimeError):
    """The commit after the swap failed (a hook, most often); the swap is rolled back."""

    def __init__(self, result: CommitResult) -> None:
        self.result = result
        super().__init__(f"the commit failed: {result.output}")


def ready_repo(path: Path) -> GitRepo:
    """The git working copy of ``path``, ready to commit to, or a refusal saying why not."""
    try:
        repo = GitRepo(path)
        repo.check_ready()
    except VcsRefusedError as refused:
        raise WorkflowRefusedError(f"saving is refused: {refused}") from None
    return repo


def build_info(repo: GitRepo, store: DatasetStore) -> BuildInfo:
    return BuildInfo(source_commit=repo.head(), built_at=store.clock.now())


class Commit:
    """The ``after_swap`` step: commit only the dataset folder; raise when it fails."""

    def __init__(self, repo: GitRepo, store: DatasetStore, message: str) -> None:
        self.repo = repo
        self.path = store.root
        self.message = message
        self.result = CommitResult(False, None, "not committed")

    def __call__(self) -> None:
        try:
            self.result = self.repo.commit_path(self.path, self.message)
        except VcsRefusedError as refused:
            raise WorkflowRefusedError(f"saving is refused: {refused}") from None
        if not self.result.ok:
            raise CommitFailedError(self.result)


def commit_transaction(
    store: DatasetStore, commit: Commit, write: Callable[[DatasetFiles], None]
) -> CommitResult:
    """Run ``write`` in a staging copy, swap it in and commit; a failed commit is returned, not
    raised, after the dataset has been swapped back."""
    try:
        with store.transaction(commit) as files:
            write(files)
    except CommitFailedError as failed:
        return failed.result
    return commit.result
