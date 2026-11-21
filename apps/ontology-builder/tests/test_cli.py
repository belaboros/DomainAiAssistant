"""The ``ontology-builder`` commands (T20: AC-6 through the CLI)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from ontology_builder.cli import make_app
from ontology_builder.workflows import Workspace
from typer.testing import CliRunner

NAME = "pets-and-house-rules"
DOG = "user-manuals-pets-and-house-rules/dog-owners-manual"


class Calls:
    """The LLM clients the workspace made, so a test can count the calls."""

    def __init__(self, pet_kit: Any) -> None:
        self.pet_kit = pet_kit
        self.clients: list[Any] = []

    def __call__(self) -> Any:
        self.clients.append(self.pet_kit.client())
        return self.clients[-1]

    @property
    def total(self) -> int:
        return sum(client.calls for client in self.clients)


@pytest.fixture
def served(review_kit: Any, tmp_path: Path, pet_kit: Any, git_init: Any) -> Any:
    """The review kit's dataset in a git repository, with the pet manuals as sources."""
    git_init(tmp_path)
    calls = Calls(pet_kit)
    workspace = Workspace(
        data_dir=tmp_path,
        work_dir=tmp_path / "work",
        llm=calls,
        sources_root=pet_kit.manuals_root,
        open_store=lambda _data_dir, _name: review_kit.store,
    )
    return workspace, calls


def _invoke(workspace: Workspace, *args: str, answer: str | None = None) -> Any:
    return CliRunner().invoke(make_app(lambda: workspace), list(args), input=answer)


def test_create_makes_and_commits_the_ontology(
    scope_record: dict[str, Any], tmp_path: Path, git_init: Any
) -> None:
    git_init(tmp_path)
    scope = tmp_path / "scope.yaml"
    scope.write_text(yaml.safe_dump({k: v for k, v in scope_record.items() if k != "name"}))
    workspace = Workspace(data_dir=tmp_path / "data", work_dir=tmp_path / "work", llm=_no_llm)

    done = _invoke(workspace, "create", "house-rules", "--scope", str(scope), "--user", "dora")

    assert done.exit_code == 0, done.output
    assert "committed" in done.output
    assert (tmp_path / "data" / "ontology-house-rules" / "01_model" / "scope.yaml").is_file()


def _no_llm() -> Any:
    pytest.fail("no LLM call expected")


def test_ingest_shows_the_estimate_and_asks_first(served: Any, review_kit: Any) -> None:
    workspace, calls = served
    tree = review_kit.store.tree_hash()

    declined = _invoke(workspace, "ingest", NAME, DOG, "--user", "alice", answer="n\n")

    assert declined.exit_code == 1
    for shown in ("documents", "source units", "input tokens", "cost"):
        assert shown in declined.output, shown
    assert "nothing was run" in declined.output
    assert calls.total == 0, "no LLM call before the confirmation"
    assert review_kit.store.tree_hash() == tree

    ran = _invoke(workspace, "ingest", NAME, DOG, "--user", "alice", answer="y\n")
    assert ran.exit_code == 0, ran.output
    assert "completed" in ran.output and "committed" in ran.output
    assert calls.total > 0


def test_ingest_yes_skips_the_question(served: Any, review_kit: Any) -> None:
    workspace, _calls = served
    ran = _invoke(workspace, "ingest", NAME, DOG, "--user", "alice", "--yes")
    assert ran.exit_code == 0, ran.output
    assert "Run it?" not in ran.output
    runs = list((review_kit.store.root / "02_decisions" / "runs").glob("run_*.yaml"))
    assert len(runs) == 1


def test_refusals_exit_1_with_the_message(served: Any, tmp_path: Path) -> None:
    workspace, _calls = served
    _invoke(workspace, "ingest", NAME, DOG, "--user", "alice", "--yes")
    again = _invoke(workspace, "ingest", NAME, DOG, "--user", "alice", "--yes")
    assert again.exit_code == 1
    assert "already" in again.output
    plain = Workspace(data_dir=tmp_path, work_dir=tmp_path / "work", llm=_no_llm)
    missing = _invoke(plain, "build", "no-such-ontology")
    assert missing.exit_code == 1 and "does not exist" in missing.output


def test_build_rebuilds_the_raw_release_without_a_commit(
    served: Any, review_kit: Any, tmp_path: Path
) -> None:
    workspace, _calls = served
    review_kit.seed([review_kit.concept()])
    done = _invoke(workspace, "build", NAME)
    assert done.exit_code == 0, done.output
    raw = review_kit.store.root / "03_release" / "00_raw"
    assert (raw / "ontology.ttl").is_file() and (raw / "manifest.json").is_file()
    assert str(raw) in done.output


def test_serve_opens_the_ontology_and_runs_the_api(
    served: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace, _calls = served
    seen: list[tuple[str, int]] = []

    def fake_serve(ontology: Any, port: int) -> None:
        seen.append((ontology.name, port))

    monkeypatch.setattr("ontology_builder.api.serve", fake_serve)
    done = _invoke(workspace, "serve", NAME, "--port", "9876")
    assert done.exit_code == 0, done.output
    assert seen == [(NAME, 9876)]
    assert "http://127.0.0.1:9876" in done.output
    assert not (workspace.ontology_dir(NAME) / "server.lock").exists(), "the lock is released"
