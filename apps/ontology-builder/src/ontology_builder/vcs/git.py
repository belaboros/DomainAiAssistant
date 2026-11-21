"""Commit one dataset path to the local git working copy, with hooks (FR-27; AC-25).

Only ``git add`` and ``git commit`` limited to one path are run, so unrelated changes in the
working copy stay as they are. Hooks always run; if one fails, nothing is committed, the path
is unstaged again and the hook's output is returned. Nothing here talks to a remote.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class VcsRefusedError(RuntimeError):
    """The working copy is not in a state to commit to; nothing was changed."""


@dataclass(frozen=True)
class CommitResult:
    """``ok`` with the new commit's ``sha`` (``None`` when there was nothing to commit), or not
    ``ok`` with the output of the failed commit (a hook's message)."""

    ok: bool
    sha: str | None
    output: str


@dataclass(frozen=True)
class _Run:
    code: int
    output: str


class GitRepo:
    """The git working copy that contains ``path``."""

    def __init__(self, path: Path) -> None:
        git = shutil.which("git")
        if git is None:
            raise VcsRefusedError("git is not available: install git to save")
        self._git = git
        start = path if path.is_dir() else path.parent
        top = self._run("rev-parse", "--show-toplevel", cwd=start)
        if top.code != 0:
            raise VcsRefusedError(f"{path} is not inside a git working copy")
        self.root = Path(top.output.strip())

    def _run(self, *args: str, cwd: Path | None = None) -> _Run:
        done = subprocess.run(  # noqa: S603 - the git executable with fixed subcommands
            [self._git, *args],
            cwd=cwd or self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        return _Run(done.returncode, (done.stdout + done.stderr).strip())

    def head(self) -> str:
        """The SHA of the current commit."""
        return self._run("rev-parse", "HEAD").output

    def _git_path(self, name: str) -> Path:
        return self.root / self._run("rev-parse", "--git-path", name).output

    def check_ready(self) -> None:
        """Refuse a detached HEAD, unmerged paths, or a merge or rebase in progress."""
        if self._run("symbolic-ref", "-q", "HEAD").code != 0:
            raise VcsRefusedError("HEAD is detached: check out a branch before saving")
        unmerged = self._run("diff", "--name-only", "--diff-filter=U").output
        in_progress = any(
            self._git_path(name).exists() for name in ("MERGE_HEAD", "rebase-merge", "rebase-apply")
        )
        if unmerged or in_progress:
            raise VcsRefusedError(
                "a merge or rebase is not finished (conflicts?): resolve it before saving"
            )

    def commit_path(self, path: Path, message: str) -> CommitResult:
        """Stage every change under ``path`` and commit only that path, hooks running."""
        self.check_ready()
        relative = path.resolve().relative_to(self.root.resolve()).as_posix()
        added = self._run("add", "-A", "--", relative)
        if added.code != 0:
            return CommitResult(False, None, added.output)
        if self._run("diff", "--cached", "--quiet", "--", relative).code == 0:
            return CommitResult(True, None, "nothing to commit")
        committed = self._run("commit", "-m", message, "--", relative)
        if committed.code != 0:
            self._run("reset", "-q", "--", relative)
            return CommitResult(False, None, committed.output)
        return CommitResult(True, self.head(), committed.output)
