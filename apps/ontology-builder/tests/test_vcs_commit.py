"""One commit of one dataset path, hooks running, never a push (plan 0002, T17: AC-25 back end).

Each test uses a temporary repository with a bare remote and a pre-commit hook that fails while
the file ``.hook-fails`` exists in the repository.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest
from ontology_builder import vcs
from ontology_builder.vcs import GitRepo, VcsRefusedError

DATASET = "data/ontology-pets-and-house-rules"
HOOK = """#!/bin/sh
if [ -f .hook-fails ]; then
  echo "detect-secrets: a secret was found in data/ontology-pets-and-house-rules/x.yaml"
  exit 1
fi
"""


def _git(repo: Path, *args: str, check: bool = True) -> str:
    git = shutil.which("git")
    assert git is not None
    done = subprocess.run(  # noqa: S603 - git with fixed arguments in a temp repo
        [git, "-C", str(repo), *args], check=check, capture_output=True, text=True
    )
    return done.stdout.strip()


@dataclass
class Repo:
    path: Path
    remote: Path

    @property
    def dataset(self) -> Path:
        return self.path / DATASET

    def head(self) -> str:
        return _git(self.path, "rev-parse", "HEAD")

    def commits(self) -> int:
        return int(_git(self.path, "rev-list", "--count", "HEAD"))

    def status(self) -> str:
        return _git(self.path, "status", "--porcelain", "--untracked-files=all")


@pytest.fixture
def repo(tmp_path: Path) -> Repo:
    remote, path = tmp_path / "remote.git", tmp_path / "work"
    _git(tmp_path, "init", "-q", "--bare", str(remote))
    _git(tmp_path, "init", "-q", "-b", "main", str(path))
    for key, value in (
        ("user.name", "test"),
        ("user.email", "test@example.invalid"),
        ("commit.gpgsign", "false"),
        ("core.hooksPath", ".git/hooks"),
    ):
        _git(path, "config", key, value)
    _git(path, "remote", "add", "origin", str(remote))
    hook = path / ".git" / "hooks" / "pre-commit"
    hook.write_text(HOOK, encoding="utf-8")
    hook.chmod(0o755)
    (path / DATASET / "01_model").mkdir(parents=True)
    (path / DATASET / "01_model" / "scope.yaml").write_text("name: x\n", encoding="utf-8")
    (path / "README.md").write_text("readme\n", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "start")
    _git(path, "push", "-q", "origin", "main")
    return Repo(path, remote)


def _change_dataset(repo: Repo) -> None:
    (repo.dataset / "01_model" / "scope.yaml").write_text("name: y\n", encoding="utf-8")
    (repo.dataset / "02_decisions").mkdir()
    (repo.dataset / "02_decisions" / "2026-11-21.jsonl").write_text("{}\n", encoding="utf-8")


def test_save_makes_one_commit_touching_only_dataset(repo: Repo) -> None:
    _change_dataset(repo)
    (repo.path / "README.md").write_text("edited elsewhere\n", encoding="utf-8")
    before = repo.commits()

    result = GitRepo(repo.dataset).commit_path(repo.dataset, "Save ontology pets-and-house-rules")

    assert result.ok, result.output
    assert repo.commits() == before + 1
    assert result.sha == repo.head()
    touched = _git(repo.path, "show", "--name-only", "--format=", "HEAD").splitlines()
    assert sorted(touched) == [
        f"{DATASET}/01_model/scope.yaml",
        f"{DATASET}/02_decisions/2026-11-21.jsonl",
    ]
    assert _git(repo.path, "log", "-1", "--format=%s") == "Save ontology pets-and-house-rules"


def test_unrelated_changes_stay_uncommitted(repo: Repo) -> None:
    _change_dataset(repo)
    (repo.path / "README.md").write_text("edited elsewhere\n", encoding="utf-8")
    (repo.path / "notes.txt").write_text("staged elsewhere\n", encoding="utf-8")
    _git(repo.path, "add", "notes.txt")

    assert GitRepo(repo.dataset).commit_path(repo.dataset, "Save").ok

    assert repo.status().splitlines() == ["M README.md", "A  notes.txt"]


def test_failing_hook_no_commit_returns_output(repo: Repo) -> None:
    _change_dataset(repo)
    (repo.path / ".hook-fails").write_text("", encoding="utf-8")
    before = repo.head()

    result = GitRepo(repo.dataset).commit_path(repo.dataset, "Save")

    assert not result.ok
    assert result.sha is None
    assert "detect-secrets: a secret was found" in result.output
    assert repo.head() == before
    staged = _git(repo.path, "diff", "--cached", "--name-only")
    assert staged == "", "the dataset is unstaged again after a failed commit"


def test_nothing_to_commit_is_ok_without_a_commit(repo: Repo) -> None:
    before = repo.head()
    result = GitRepo(repo.dataset).commit_path(repo.dataset, "Save")
    assert result.ok
    assert result.sha is None
    assert repo.head() == before


def test_never_pushes(repo: Repo) -> None:
    remote_before = _git(repo.remote, "rev-parse", "main")
    _change_dataset(repo)
    assert GitRepo(repo.dataset).commit_path(repo.dataset, "Save").ok
    assert _git(repo.remote, "rev-parse", "main") == remote_before
    source = "\n".join(
        p.read_text(encoding="utf-8") for p in Path(vcs.__file__).parent.rglob("*.py")
    )
    assert not re.search(r"\bpush\b", source), "the vcs component has no push code path"
    assert "--no-verify" not in source and '"-n"' not in source, "hooks are never bypassed"


def _detached(repo: Repo) -> None:
    _git(repo.path, "checkout", "-q", "--detach")


def _conflict(repo: Repo) -> None:
    _git(repo.path, "checkout", "-q", "-b", "other")
    (repo.path / "README.md").write_text("other\n", encoding="utf-8")
    _git(repo.path, "commit", "-q", "-am", "other")
    _git(repo.path, "checkout", "-q", "main")
    (repo.path / "README.md").write_text("main\n", encoding="utf-8")
    _git(repo.path, "commit", "-q", "-am", "main")
    _git(repo.path, "merge", "-q", "other", check=False)


@pytest.mark.parametrize(("make_state", "message"), [(_detached, "detached"), (_conflict, "merge")])
def test_refuse_on_conflicts_or_detached(repo: Repo, make_state: object, message: str) -> None:
    assert callable(make_state)
    make_state(repo)
    _change_dataset(repo)
    before = repo.head()
    with pytest.raises(VcsRefusedError, match=message):
        GitRepo(repo.dataset).commit_path(repo.dataset, "Save")
    assert repo.head() == before


def test_refuse_on_no_git(repo: Repo, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda _name: None)
    with pytest.raises(VcsRefusedError, match="git is not available"):
        GitRepo(repo.dataset)


def test_refuse_outside_a_repository(tmp_path: Path) -> None:
    with pytest.raises(VcsRefusedError, match="not inside a git working copy"):
        GitRepo(tmp_path)
