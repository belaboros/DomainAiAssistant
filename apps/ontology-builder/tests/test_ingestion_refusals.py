"""Ingestion refuses a folder already ingested, and folders it cannot take (T10: AC-7, FR-4)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from ontology_builder.ingestion import (
    IngestionFailedError,
    IngestionRefusedError,
    Who,
    discard_run,
    plan_ingestion,
    start_run,
    unfinished_runs,
)
from ontology_builder.model import Role
from ontology_builder.store import DatasetStore

MANUALS = "user-manuals-pets-and-house-rules"
RULES = f"{MANUALS}/building-and-house-rules"
DOG = f"{MANUALS}/dog-owners-manual"
ALICE = Who("alice", Role.user)


def _ingest(kit: Any, store: DatasetStore, work: Path, path: str) -> None:
    client = kit.client()
    plan = plan_ingestion(store, kit.manuals_root, path, client, ALICE)
    start_run(store, plan, client, work, confirm=True)


@pytest.mark.parametrize("again", [RULES, f"{RULES}/", f"./{RULES}"])
def test_same_folder_twice_refused_dataset_unchanged(
    tmp_path: Path, pet_kit: Any, again: str
) -> None:
    store = pet_kit.store(tmp_path / "data")
    _ingest(pet_kit, store, tmp_path / "work", RULES)
    before = store.tree_hash()
    client = pet_kit.client()
    with pytest.raises(IngestionRefusedError, match=r"already ingested .* as corpus 00_"):
        plan_ingestion(store, pet_kit.manuals_root, again, client, ALICE)
    assert client.calls == 0
    assert store.tree_hash() == before


def test_second_corpus_gets_the_next_number(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    _ingest(pet_kit, store, tmp_path / "work", DOG)
    _ingest(pet_kit, store, tmp_path / "work", RULES)
    assert list(store.read().corpora()) == ["00_dog-owners-manual", "01_building-and-house-rules"]


@pytest.mark.parametrize(
    ("path", "message"),
    [
        ("/etc", "inside the shared data folder"),
        (f"{MANUALS}/../{MANUALS}", "inside the shared data folder"),
        ("", "inside the shared data folder"),
        (f"{MANUALS}/no-such-manual", "does not exist"),
    ],
)
def test_folder_that_cannot_be_ingested_is_refused(
    tmp_path: Path, pet_kit: Any, path: str, message: str
) -> None:
    store = pet_kit.store(tmp_path / "data")
    with pytest.raises(IngestionRefusedError, match=message):
        plan_ingestion(store, pet_kit.manuals_root, path, pet_kit.client(), ALICE)


def test_folder_without_markdown_is_refused(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    (tmp_path / "sources" / "empty").mkdir(parents=True)
    with pytest.raises(IngestionRefusedError, match="no Markdown file"):
        plan_ingestion(store, tmp_path / "sources", "empty", pet_kit.client(), ALICE)


def test_unfinished_run_for_the_same_folder_must_be_resumed_or_discarded(
    tmp_path: Path, pet_kit: Any
) -> None:
    store = pet_kit.store(tmp_path / "data")
    work = tmp_path / "work"
    failing = pet_kit.client(fail_after=0)
    plan = plan_ingestion(store, pet_kit.manuals_root, DOG, failing, ALICE)
    with pytest.raises(IngestionFailedError):
        start_run(store, plan, failing, work, confirm=True)
    [unfinished] = unfinished_runs(store, work)
    assert (unfinished.id, unfinished.status) == (plan.run_id, "failed")
    client = pet_kit.client()
    again = plan_ingestion(store, pet_kit.manuals_root, DOG, client, ALICE)
    with pytest.raises(IngestionRefusedError, match=f"resume it with --resume {plan.run_id}"):
        start_run(store, again, client, work, confirm=True)
    discard_run(store, plan.run_id, work)
    assert unfinished_runs(store, work) == []
    start_run(store, again, client, work, confirm=True)
    assert list(store.read().corpora()) == ["00_dog-owners-manual"]
