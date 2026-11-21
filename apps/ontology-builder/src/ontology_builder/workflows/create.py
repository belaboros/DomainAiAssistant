"""Create an ontology and commit it with its first raw release (FR-1, FR-27)."""

from __future__ import annotations

import shutil
from collections.abc import Mapping
from typing import Any

from ontology_builder import governance, release
from ontology_builder.governance import Actor
from ontology_builder.store import DatasetFiles
from ontology_builder.vcs import CommitResult
from ontology_builder.workflows.commit import Commit, build_info, commit_transaction, ready_repo
from ontology_builder.workflows.workspace import Workspace


def create_ontology(
    workspace: Workspace, name: str, scope: Mapping[str, Any], actor: Actor
) -> CommitResult:
    """Create ``data/ontology-<name>/`` (domain admin only) and commit it. If the commit fails,
    the new folder is removed again, so nothing is left outside a commit."""
    governance.require_admin(actor, "create an ontology")
    repo = ready_repo(workspace.data_dir)
    store = workspace.store(name)
    governance.create_ontology(store, scope, actor)
    info = build_info(repo, store)

    def write(files: DatasetFiles) -> None:
        release.save_raw(files, info)

    commit = Commit(repo, store, f"Create ontology {name}")
    try:
        result = commit_transaction(store, commit, write)
    except BaseException:
        shutil.rmtree(store.root, ignore_errors=True)
        raise
    if not result.ok:
        shutil.rmtree(store.root, ignore_errors=True)
    return result
