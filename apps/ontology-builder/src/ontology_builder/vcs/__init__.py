"""vcs component.

Commits the changed files of one dataset path to the local git working copy.

``GitRepo(path).commit_path(path, message)`` stages and commits only ``path``, with the git hooks
running, and reports a failing hook's output instead of committing (FR-27). It never talks to a
remote.
"""

from __future__ import annotations

from ontology_builder.vcs.git import CommitResult, GitRepo, VcsRefusedError

__all__ = ["CommitResult", "GitRepo", "VcsRefusedError"]
