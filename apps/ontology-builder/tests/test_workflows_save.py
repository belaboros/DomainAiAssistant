"""The use cases across components: create, the pending change set, save, publish and ingest
(T18: AC-8 end to end, AC-25, edge cases).

Each test works in a temporary git repository whose pre-commit hook fails while the file
``.hook-fails`` exists, with a bare remote that must never receive anything.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from ontology_builder.governance import Actor, GovernanceRefusedError
from ontology_builder.ingestion import IngestionFailedError
from ontology_builder.model import Role
from ontology_builder.workflows import (
    OpenOntology,
    WorkflowRefusedError,
    Workspace,
    create_ontology,
    open_ontology,
)

NAME = "pets-and-house-rules"
DATASET = f"ontology-{NAME}"
ALICE = Actor("alice", Role.user)
ADMIN = Actor("dora", Role.domain_admin)
DOG = "user-manuals-pets-and-house-rules/dog-owners-manual"
HOOK = """#!/bin/sh
if [ -f .hook-fails ]; then
  echo "detect-secrets: a secret was found in the dataset"
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


def _init_repo(path: Path) -> Path:
    """A git repository at ``path`` with the failing-hook switch and a bare remote."""
    remote = path.parent / f"{path.name}-remote.git"
    _git(path.parent, "init", "-q", "--bare", str(remote))
    _git(path, "init", "-q", "-b", "main")
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
    (path / ".gitignore").write_text("/work/\n/.hook-fails\n", encoding="utf-8")
    (path / "README.md").write_text("readme\n", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "start")
    _git(path, "push", "-q", "origin", "main")
    return remote


@dataclass
class Repo:
    path: Path
    remote: Path
    workspace: Workspace

    @property
    def dataset(self) -> Path:
        return self.workspace.data_dir / DATASET

    def commits(self) -> int:
        return int(_git(self.path, "rev-list", "--count", "HEAD"))

    def head(self) -> str:
        return _git(self.path, "rev-parse", "HEAD")

    def touched(self) -> list[str]:
        return _git(self.path, "show", "--name-only", "--format=", "HEAD").splitlines()

    def status(self) -> str:
        return _git(self.path, "status", "--porcelain", "--untracked-files=all")

    def remote_head(self) -> str:
        return _git(self.remote, "rev-parse", "main")

    def hook_fails(self, fails: bool = True) -> None:
        switch = self.path / ".hook-fails"
        if fails:
            switch.write_text("", encoding="utf-8")
        else:
            switch.unlink()


def _no_llm() -> Any:
    pytest.fail("no LLM call expected")


@pytest.fixture
def repo(review_kit: Any, tmp_path: Path) -> Repo:
    """The review kit's dataset (in ``tmp_path``) committed in a git repository at ``tmp_path``."""
    remote = _init_repo(tmp_path)
    workspace = Workspace(
        data_dir=tmp_path,
        work_dir=tmp_path / "work",
        llm=_no_llm,
        open_store=lambda _data_dir, _name: review_kit.store,
    )
    return Repo(tmp_path, remote, workspace)


def _author_concept(session: OpenOntology) -> str:
    statement = session.add_statement(ALICE, "A dog and a cat must be introduced gradually.")
    return session.author(
        ALICE,
        "concept",
        {"label": "gradual introduction", "level": "level-2", "evidence": [{"unit": statement}]},
    )


def test_save_makes_one_commit_touching_only_dataset(repo: Repo) -> None:
    (repo.path / "README.md").write_text("edited elsewhere\n", encoding="utf-8")
    before, pushed = repo.commits(), repo.remote_head()
    with open_ontology(repo.workspace, NAME) as session:
        concept = _author_concept(session)
        assert session.pending == 2
        result = session.save()
        assert session.pending == 0

    assert result.ok, result.output
    assert repo.commits() == before + 1
    assert result.sha == repo.head()
    touched = repo.touched()
    assert all(path.startswith(f"{DATASET}/") for path in touched), touched
    assert f"{DATASET}/01_model/elements/concept/{concept}.yaml" in touched
    assert f"{DATASET}/03_release/00_raw/manifest.json" in touched
    assert any(path.startswith(f"{DATASET}/02_decisions/") for path in touched)
    assert repo.status() == "M README.md", "unrelated changes stay uncommitted"
    assert repo.remote_head() == pushed, "nothing is pushed"
    manifest = json.loads((repo.dataset / "03_release/00_raw/manifest.json").read_text())
    assert manifest["counts"]["by_type"]["concept"] == 1


def test_failing_hook_rolls_back_and_keeps_the_pending_changes(repo: Repo, review_kit: Any) -> None:
    before = repo.commits()
    with open_ontology(repo.workspace, NAME) as session:
        _author_concept(session)
        tree = review_kit.store.tree_hash()
        repo.hook_fails()
        result = session.save()

        assert not result.ok
        assert "detect-secrets: a secret was found" in result.output
        assert repo.commits() == before
        assert review_kit.store.tree_hash() == tree, "the dataset is swapped back"
        assert repo.status() == "", "nothing is left staged or written"
        assert session.pending == 2, "the change set is kept for the next try"

        repo.hook_fails(False)
        assert session.save().ok
    assert repo.commits() == before + 1


def test_save_refused_when_the_dataset_changed_on_disk(repo: Repo, review_kit: Any) -> None:
    with open_ontology(repo.workspace, NAME) as session:
        _author_concept(session)
        scope = repo.dataset / "01_model" / "scope.yaml"
        scope.write_text(scope.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        tree = review_kit.store.tree_hash()
        with pytest.raises(WorkflowRefusedError, match="reload"):
            session.save()
        assert review_kit.store.tree_hash() == tree


def test_nothing_to_save_makes_no_commit(repo: Repo) -> None:
    before = repo.commits()
    with open_ontology(repo.workspace, NAME) as session:
        result = session.save()
    assert result.ok and result.sha is None
    assert repo.commits() == before


def test_journal_keeps_pending_changes_across_a_restart(repo: Repo) -> None:
    session = open_ontology(repo.workspace, NAME)
    concept = _author_concept(session)
    session.close()  # e.g. the server stopped before Save

    with open_ontology(repo.workspace, NAME) as reopened:
        assert reopened.pending == 2
        assert reopened.changes.get(concept).label == "gradual introduction"
        assert reopened.save().ok
    with open_ontology(repo.workspace, NAME) as after:
        assert after.pending == 0, "a successful save clears the journal"
        assert concept in after.changes.elements


def test_stale_journal_refused_unless_discarded(repo: Repo) -> None:
    session = open_ontology(repo.workspace, NAME)
    _author_concept(session)
    session.close()
    scope = repo.dataset / "01_model" / "scope.yaml"
    scope.write_text(scope.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    with pytest.raises(WorkflowRefusedError, match="changed on disk"):
        open_ontology(repo.workspace, NAME)
    with open_ontology(repo.workspace, NAME, discard_journal=True) as fresh:
        assert fresh.pending == 0


def test_bulk_action_is_journaled_with_per_id_results(repo: Repo, review_kit: Any) -> None:
    ids = review_kit.seed([review_kit.concept(), review_kit.concept("excluded")])
    _git(repo.path, "add", "-A")
    _git(repo.path, "commit", "-q", "-m", "seed")
    with open_ontology(repo.workspace, NAME) as session:
        results = session.act(ALICE, "level", ids, {"level": "level-3", "reason": "detail"})
        assert [r.ok for r in results] == [True, False]
        assert session.pending == 1
    with open_ontology(repo.workspace, NAME) as reopened:
        assert reopened.changes.get(ids[0]).level == "level-3"


def test_save_refused_without_git(review_kit: Any, tmp_path: Path) -> None:
    workspace = Workspace(
        data_dir=tmp_path,
        work_dir=tmp_path / "work",
        llm=_no_llm,
        open_store=lambda _data_dir, _name: review_kit.store,
    )
    with open_ontology(workspace, NAME) as session:
        _author_concept(session)
        tree = review_kit.store.tree_hash()
        with pytest.raises(WorkflowRefusedError, match="git"):
            session.save()
        assert review_kit.store.tree_hash() == tree
        assert session.pending == 2


def test_save_refused_on_a_detached_head(repo: Repo, review_kit: Any) -> None:
    _git(repo.path, "checkout", "-q", "--detach")
    with open_ontology(repo.workspace, NAME) as session:
        _author_concept(session)
        tree = review_kit.store.tree_hash()
        with pytest.raises(WorkflowRefusedError, match="detached"):
            session.save()
        assert review_kit.store.tree_hash() == tree


def test_publish_is_admin_only_and_commits_the_governed_release(
    repo: Repo, review_kit: Any
) -> None:
    with open_ontology(repo.workspace, NAME) as session:
        concept = _author_concept(session)
        session.save()
        tree, before = review_kit.store.tree_hash(), repo.commits()
        with pytest.raises(GovernanceRefusedError, match="domain admin"):
            session.publish(ALICE)
        assert (review_kit.store.tree_hash(), repo.commits()) == (tree, before)

        assert [r.ok for r in session.act(ADMIN, "approve", [concept], {})] == [True]
        with pytest.raises(WorkflowRefusedError, match="save"):
            session.publish(ADMIN)
        session.save()
        outcome = session.publish(ADMIN)

    assert outcome.commit.ok, outcome.commit.output
    assert outcome.result.governed is not None
    assert outcome.result.governed.version == "1.0.0"
    assert repo.head() == outcome.commit.sha
    governed = repo.dataset / "03_release/01_governed"
    assert json.loads((governed / "manifest.json").read_text())["version"] == "1.0.0"
    assert (governed / "CHANGELOG.md").is_file()
    publishes = [d for d in review_kit.store.read().decisions() if d.action == "publish"]
    assert [(d.user, d.new) for d in publishes] == [("dora", "1.0.0")]


def test_create_commits_the_new_ontology(scope_record: dict[str, Any], tmp_path: Path) -> None:
    _init_repo(tmp_path)
    workspace = Workspace(data_dir=tmp_path / "data", work_dir=tmp_path / "work", llm=_no_llm)
    (tmp_path / "data").mkdir()
    before = int(_git(tmp_path, "rev-list", "--count", "HEAD"))
    with pytest.raises(GovernanceRefusedError, match="domain admin"):
        create_ontology(workspace, NAME, scope_record, ALICE)

    result = create_ontology(workspace, NAME, scope_record, ADMIN)

    assert result.ok, result.output
    assert int(_git(tmp_path, "rev-list", "--count", "HEAD")) == before + 1
    touched = _git(tmp_path, "show", "--name-only", "--format=", "HEAD").splitlines()
    assert f"data/{DATASET}/01_model/scope.yaml" in touched
    assert f"data/{DATASET}/03_release/00_raw/manifest.json" in touched
    assert _git(tmp_path, "status", "--porcelain", "--untracked-files=all") == ""


def test_create_with_a_failing_hook_leaves_nothing(
    scope_record: dict[str, Any], tmp_path: Path
) -> None:
    _init_repo(tmp_path)
    (tmp_path / ".hook-fails").write_text("", encoding="utf-8")
    workspace = Workspace(data_dir=tmp_path / "data", work_dir=tmp_path / "work", llm=_no_llm)
    (tmp_path / "data").mkdir()

    result = create_ontology(workspace, NAME, scope_record, ADMIN)

    assert not result.ok and "detect-secrets" in result.output
    assert not (tmp_path / "data" / DATASET).exists()
    assert _git(tmp_path, "status", "--porcelain", "--untracked-files=all") == ""


@pytest.fixture
def pet_repo(pet_kit: Any, tmp_path: Path) -> tuple[Repo, list[Any]]:
    """The pet dataset committed in a temp repository; the LLM factory hands out ``clients``."""
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    store = pet_kit.store(repo_path / "data")
    remote = _init_repo(repo_path)
    clients: list[Any] = []
    workspace = Workspace(
        data_dir=repo_path / "data",
        work_dir=repo_path / "work",
        llm=lambda: clients.pop(0),
        sources_root=pet_kit.manuals_root,
        open_store=lambda _data_dir, _name: store,
    )
    return Repo(repo_path, remote, workspace), clients


def test_ingest_estimates_then_commits_once(pet_repo: tuple[Repo, list[Any]], pet_kit: Any) -> None:
    repo, clients = pet_repo
    planner, runner = pet_kit.client(), pet_kit.client()
    clients.extend([planner, runner])
    before = repo.commits()
    with open_ontology(repo.workspace, NAME) as session:
        plan = session.plan_ingestion(ALICE, DOG)
        assert plan.estimate.documents > 0 and planner.calls == 0, "no LLM answer before confirm"
        outcome = session.ingest(plan, confirm=True)
        assert runner.calls > 0
        assert session.changes.elements, "the session sees the ingested elements"

    assert outcome.status == "completed"
    assert outcome.commit.ok and outcome.commit.sha == repo.head()
    assert repo.commits() == before + 1
    assert all(path.startswith(f"data/{DATASET}/") for path in repo.touched())
    assert f"data/{DATASET}/03_release/00_raw/level-1.md" in repo.touched()
    assert repo.status() == ""


def test_ingest_failing_halfway_leaves_git_clean_then_resumes(
    pet_repo: tuple[Repo, list[Any]], pet_kit: Any
) -> None:
    repo, clients = pet_repo
    clients.extend([pet_kit.client(), pet_kit.client(fail_after=3), pet_kit.client()])
    before = repo.commits()
    with open_ontology(repo.workspace, NAME) as session:
        plan = session.plan_ingestion(ALICE, DOG)
        with pytest.raises(IngestionFailedError):
            session.ingest(plan, confirm=True)
        assert repo.status() == "" and repo.commits() == before

        outcome = session.resume(plan.run_id)
    assert outcome.status == "completed"
    assert repo.commits() == before + 1
    assert repo.status() == ""


def test_ingest_refused_with_unsaved_changes(
    pet_repo: tuple[Repo, list[Any]], pet_kit: Any
) -> None:
    repo, clients = pet_repo
    clients.append(pet_kit.client())
    with open_ontology(repo.workspace, NAME) as session:
        session.add_statement(ALICE, "Dogs must be walked twice a day.")
        plan = session.plan_ingestion(ALICE, DOG)
        with pytest.raises(WorkflowRefusedError, match="save"):
            session.ingest(plan, confirm=True)
