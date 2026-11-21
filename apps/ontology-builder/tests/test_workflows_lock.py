"""One process per dataset: a lock in the work folder (T18: edge case "two GUI windows")."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest
from ontology_builder.workflows import ProcessLock, WorkflowRefusedError, Workspace, open_ontology


def _workspace(kit: Any, tmp_path: Path) -> Workspace:
    return Workspace(
        data_dir=kit.store.root.parent,
        work_dir=tmp_path / "work",
        llm=lambda: pytest.fail("no LLM call expected"),
        open_store=lambda _data_dir, _name: kit.store,
    )


def test_second_server_refused(review_kit: Any, tmp_path: Path) -> None:
    workspace = _workspace(review_kit, tmp_path)
    first = open_ontology(workspace, "pets-and-house-rules")
    with pytest.raises(WorkflowRefusedError, match="already open"):
        open_ontology(workspace, "pets-and-house-rules")
    first.close()
    again = open_ontology(workspace, "pets-and-house-rules")
    again.close()


def test_lock_names_the_holder_and_is_released(tmp_path: Path) -> None:
    lock = ProcessLock(tmp_path / "server.lock")
    lock.acquire()
    assert (tmp_path / "server.lock").read_text(encoding="utf-8").strip() == str(os.getpid())
    with pytest.raises(WorkflowRefusedError, match=f"process {os.getpid()}"):
        ProcessLock(tmp_path / "server.lock").acquire()
    lock.release()
    assert not (tmp_path / "server.lock").exists()


def test_stale_lock_of_a_dead_process_is_taken_over(tmp_path: Path) -> None:
    path = tmp_path / "server.lock"
    path.write_text("999999999\n", encoding="utf-8")  # no such process
    lock = ProcessLock(path)
    lock.acquire()
    assert path.read_text(encoding="utf-8").strip() == str(os.getpid())
    lock.release()


def test_unknown_ontology_refused_and_no_lock_left(review_kit: Any, tmp_path: Path) -> None:
    workspace = Workspace(
        data_dir=tmp_path, work_dir=tmp_path / "work", llm=lambda: pytest.fail("no LLM")
    )
    with pytest.raises(WorkflowRefusedError, match="does not exist"):
        open_ontology(workspace, "no-such-ontology")
    assert not list((tmp_path / "work").rglob("*.lock"))
