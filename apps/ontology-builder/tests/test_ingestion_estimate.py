"""The estimate comes before any LLM call, and the run record keeps what was used (T10: AC-6, AC-1).

The dog manual is ingested with the replayed pet fixtures (pass 1); requests no fixture covers
(pass 2 of one corpus) get a scripted answer.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from ontology_builder.extraction import pass1_requests
from ontology_builder.ingestion import (
    IngestionRefusedError,
    Who,
    plan_ingestion,
    start_run,
)
from ontology_builder.llm import Pricing, heuristic_tokens
from ontology_builder.model import Role
from ontology_builder.store import DatasetStore

DOG = "user-manuals-pets-and-house-rules/dog-owners-manual"
ALICE = Who("alice", Role.user)


def _plan(kit: Any, store: DatasetStore, client: Any, path: str = DOG) -> Any:
    return plan_ingestion(store, kit.manuals_root, path, client, ALICE)


def test_no_llm_call_before_confirm(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    client = pet_kit.client()
    before = store.tree_hash()
    plan = _plan(pet_kit, store, client)
    estimate = plan.estimate
    markdown = sorted((pet_kit.manuals / "dog-owners-manual").rglob("*.md"))
    assert estimate.documents == len(markdown)
    assert estimate.units == len(plan.units) > 0
    assert estimate.input_tokens > 0 and estimate.output_tokens > 0
    assert estimate.cost_usd is not None and estimate.cost_usd > 0
    with pytest.raises(IngestionRefusedError, match="confirmation"):
        start_run(store, plan, client, tmp_path / "work", confirm=False)
    assert client.calls == 0, "the LLM is asked nothing before the person confirms"
    assert store.tree_hash() == before
    assert not (tmp_path / "work").exists()


def test_estimate_counts_the_requests_that_are_sent(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    client = pet_kit.client()
    plan = _plan(pet_kit, store, client)
    scope = store.read().scope()
    assert scope is not None
    requests = [
        r for b in plan.batches for r in pass1_requests(b.document, b.units, scope) if b.units
    ]
    assert plan.estimate.input_tokens == sum(heuristic_tokens(r) for r in requests)
    price = Pricing.load().prices[client.model]
    assert plan.estimate.cost_usd == pytest.approx(
        price.cost(plan.estimate.input_tokens, plan.estimate.output_tokens)
    )


def test_run_record_has_model_tokens_times(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    client = pet_kit.client()
    plan = _plan(pet_kit, store, client)
    run = start_run(store, plan, client, tmp_path / "work", confirm=True)
    recorded = store.read().run(plan.run_id)
    assert recorded == run
    assert (recorded.kind, recorded.status, recorded.user) == ("ingestion", "completed", "alice")
    assert recorded.model == client.model
    assert recorded.source_path == DOG
    assert recorded.input_tokens > 0 and recorded.output_tokens > 0
    assert recorded.started_at is not None and recorded.ended_at is not None
    assert recorded.estimate == plan.estimate
    assert client.calls > 0
    assert not (tmp_path / "work" / "ontology-pets-and-house-rules" / "runs" / run.id).exists()


def test_run_writes_registry_verdicts_and_proposed_elements(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    client = pet_kit.client()
    plan = _plan(pet_kit, store, client)
    start_run(store, plan, client, tmp_path / "work", confirm=True)
    files = store.read()
    [folder] = files.corpora()
    assert folder == "00_dog-owners-manual"
    units = [u for d in files.documents(folder) for u in files.units(folder, d.id)]
    assert {u.id for u in units} == {u.id for u in plan.units}
    ignorable = [u for u in units if u.ignorable is not None]
    assert any("Bodza" in u.text for u in ignorable)
    assert all(u.ignorable.status == "proposed" for u in ignorable if u.ignorable)
    elements = files.elements().values()
    assert elements and all(e.status == "proposed" for e in elements)
    assert all(e.origin.run_id == plan.run_id for e in elements)
    known = {u.id for u in units}
    assert all({ev.unit for ev in e.evidence} <= known for e in elements)


def test_refused_while_scope_record_is_empty(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    with store.transaction() as files:
        (files.root / "01_model" / "scope.yaml").write_text("", encoding="utf-8")
    client = pet_kit.client()
    with pytest.raises(IngestionRefusedError, match="scope record is missing or empty"):
        _plan(pet_kit, store, client)
    assert client.calls == 0
