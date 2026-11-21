"""An interrupted run leaves no partial records and can be resumed (T10: AC-8, fixture).

The LLM "fails after half of the units": the client raises ``LlmUnavailableError`` from a given
call on. Each test store mints IDs from a fixed clock and fixed bytes, so two stores that do the
same work get the same IDs; the resumed run continues with the same store, so its result can be
compared byte for byte with an uninterrupted run.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest
from ontology_builder.ingestion import (
    IngestionFailedError,
    Who,
    WriteHooks,
    plan_ingestion,
    resume_run,
    start_run,
)
from ontology_builder.model import Role

DOG = "user-manuals-pets-and-house-rules/dog-owners-manual"
ALICE = Who("alice", Role.user)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def _calls_of_full_run(kit: Any, data: Path, work: Path) -> tuple[dict[str, bytes], int]:
    store = kit.store(data)
    client = kit.client()
    plan = plan_ingestion(store, kit.manuals_root, DOG, client, ALICE)
    start_run(store, plan, client, work, confirm=True)
    return _snapshot(store.root), client.calls


def test_fail_halfway_then_resume_equals_uninterrupted(tmp_path: Path, pet_kit: Any) -> None:
    expected, calls = _calls_of_full_run(pet_kit, tmp_path / "a", tmp_path / "work-a")
    store = pet_kit.store(tmp_path / "b")
    before = _snapshot(store.root)
    failing = pet_kit.client(fail_after=calls // 2)
    plan = plan_ingestion(store, pet_kit.manuals_root, DOG, failing, ALICE)
    with pytest.raises(IngestionFailedError, match=f"--resume {plan.run_id}"):
        start_run(store, plan, failing, tmp_path / "work-b", confirm=True)
    assert _snapshot(store.root) == before, "nothing is written before the run is complete"
    client = pet_kit.client()
    resume_run(store, plan.run_id, client, tmp_path / "work-b")
    assert client.calls == calls - calls // 2, "finished batches are not asked again"
    assert _snapshot(store.root) == expected


def _git(repo: Path, *args: str) -> str:
    git = shutil.which("git")
    assert git is not None
    identity = ["-c", "user.name=test", "-c", "user.email=test@example.invalid"]
    done = subprocess.run(  # noqa: S603 - git with fixed arguments in a temp repo
        [git, "-C", str(repo), *identity, *args], check=True, capture_output=True, text=True
    )
    return done.stdout


def test_fail_halfway_without_resume_leaves_git_status_clean(tmp_path: Path, pet_kit: Any) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    store = pet_kit.store(repo / "data")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "--no-gpg-sign", "-m", "ontology")
    failing = pet_kit.client(fail_after=5)
    plan = plan_ingestion(store, pet_kit.manuals_root, DOG, failing, ALICE)
    with pytest.raises(IngestionFailedError):
        start_run(store, plan, failing, tmp_path / "work", confirm=True)
    assert _git(repo, "status", "--porcelain", "--untracked-files=all") == ""


def test_failure_after_the_swap_rolls_back_and_resumes_from_the_cache(
    tmp_path: Path, pet_kit: Any
) -> None:
    store = pet_kit.store(tmp_path / "data")
    before = _snapshot(store.root)
    client = pet_kit.client()
    plan = plan_ingestion(store, pet_kit.manuals_root, DOG, client, ALICE)

    def hook_fails() -> None:
        raise RuntimeError("pre-commit hook failed")

    with pytest.raises(IngestionFailedError, match="pre-commit hook failed"):
        start_run(
            store, plan, client, tmp_path / "work", confirm=True, hooks=WriteHooks(None, hook_fails)
        )
    assert _snapshot(store.root) == before
    again = pet_kit.client()
    run = resume_run(store, plan.run_id, again, tmp_path / "work")
    assert again.calls == 0, "every answer came from the cache"
    assert run.status == "completed"
    assert store.read().run(plan.run_id) == run


def test_before_swap_hook_writes_in_the_same_transaction(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    client = pet_kit.client()
    plan = plan_ingestion(store, pet_kit.manuals_root, DOG, client, ALICE)
    seen: list[int] = []

    def rebuild(files: Any) -> None:
        seen.append(len(files.elements()))
        files.write_release_file("raw", "marker.txt", "rebuilt\n")

    start_run(store, plan, client, tmp_path / "work", confirm=True, hooks=WriteHooks(rebuild))
    assert seen == [len(store.read().elements())] and seen[0] > 0
    assert (store.read().release_dir("raw") / "marker.txt").read_text() == "rebuilt\n"
