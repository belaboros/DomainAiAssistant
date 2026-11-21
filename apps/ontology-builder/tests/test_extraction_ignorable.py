"""Ignorable passages of the pet manuals, replayed from the curated fixtures (T8: AC-13, fixture).

The on-demand extraction of a unit marked not ignorable is T10; its LLM requests have no recorded
fixture, so they get the scripted answer of ``PetClient`` (one statement and concept per unit).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from ontology_builder.ingestion import (
    IngestionRefusedError,
    Who,
    plan_ingestion,
    plan_on_demand,
    start_run,
)
from ontology_builder.model import Concept, Role, Rule, Term

SEEDED = [
    ("dog-owners-manual", "01-before-you-get-a-dog.md", "Bodza", "instance_or_anecdote"),
    ("cat-owners-manual", "01-before-you-get-a-cat.md", "Egyptians", "generic_or_historical_story"),
    ("building-and-house-rules", "01-scope-and-definitions.md", "Salus", "quote_or_motivational"),
    (
        "building-and-house-rules",
        "01-scope-and-definitions.md",
        "shared interest",
        "quote_or_motivational",
    ),
]


def _unit(pet_extraction: Any, manual: str, path: str, contains: str) -> str:
    [corpus] = [c for c in pet_extraction.corpora if c.folder.endswith(manual)]
    [unit] = [
        u for u in corpus.units if u.location and u.location.path == path and contains in u.text
    ]
    return str(unit.id)


@pytest.mark.parametrize(("manual", "path", "contains", "category"), SEEDED)
def test_bodza_egypt_cicero_ignorable_with_categories(
    pet_extraction: Any, manual: str, path: str, contains: str, category: str
) -> None:
    verdict = pet_extraction.verdicts[_unit(pet_extraction, manual, path, contains)]
    assert verdict.proposed is True and verdict.status == "proposed"
    assert verdict.category == category
    assert verdict.reason.strip()


def test_only_the_seeded_passages_are_ignorable(pet_extraction: Any) -> None:
    seeded = {_unit(pet_extraction, m, p, c) for m, p, c, _ in SEEDED}
    assert set(pet_extraction.verdicts) == seeded


def test_no_element_cites_ignorable_units(pet_extraction: Any) -> None:
    ignorable = set(pet_extraction.verdicts)
    for element in pet_extraction.elements:
        assert not {e.unit for e in element.evidence} & ignorable, element.label
        if isinstance(element, Term):
            assert not {m.unit for m in element.mentions or []} & ignorable, element.label


def test_traps_are_not_extracted(pet_extraction: Any) -> None:
    """No Bodza, Bastet or Egypt concept; no "shared interest" rule; 13 years is no evidence."""
    for element in pet_extraction.elements:
        if isinstance(element, Concept):
            assert not any(w in element.label for w in ("Bodza", "Bastet", "Egypt")), element.label
        if isinstance(element, Rule):
            assert "shared interest" not in f"{element.label} {element.action}".lower()
        texts = " ".join(pet_extraction.units[e.unit].text for e in element.evidence)
        assert "thirteen years" not in texts, element.label


def test_not_ignorable_runs_extraction_after_confirm(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    work = tmp_path / "work"
    client = pet_kit.client()
    dog = "user-manuals-pets-and-house-rules/dog-owners-manual"
    plan = plan_ingestion(store, pet_kit.manuals_root, dog, client, Who("bela", Role.user))
    start_run(store, plan, client, work, confirm=True)
    files = store.read()
    [folder] = files.corpora()
    units = [u for d in files.documents(folder) for u in files.units(folder, d.id)]
    [bodza] = [u for u in units if "Bodza" in u.text]
    assert bodza.ignorable is not None and bodza.ignorable.status == "proposed"
    before = set(files.elements())

    alice = Who("alice", Role.user)
    asking = pet_kit.client()
    on_demand = plan_on_demand(store, [bodza.id], asking, alice)
    assert (on_demand.estimate.documents, on_demand.estimate.units) == (1, 1)
    assert on_demand.estimate.input_tokens > 0 and on_demand.estimate.cost_usd
    with pytest.raises(IngestionRefusedError, match="confirmation"):
        start_run(store, on_demand, asking, work, confirm=False)
    assert asking.calls == 0, "no extraction before the cost is confirmed"

    run = start_run(store, on_demand, asking, work, confirm=True)
    assert asking.calls > 0
    assert any("marked these units as not ignorable: U1." in r.prompt for r in asking.scripted)
    files = store.read()
    [unit] = [
        u for d in files.documents(folder) for u in files.units(folder, d.id) if u.id == bodza.id
    ]
    assert unit.ignorable is not None and unit.ignorable.status == "rejected"
    new = [e for e in files.elements().values() if e.id not in before]
    assert new and all({ev.unit for ev in e.evidence} == {bodza.id} for e in new)
    assert all(e.origin.run_id == run.id and e.status == "proposed" for e in new)
    [decision] = [d for d in files.decisions() if d.action == "not_ignorable"]
    assert (decision.user, decision.role, decision.element_id) == ("alice", "user", bodza.id)
    assert (decision.old, decision.new) == ("proposed", "rejected")
    assert (run.kind, run.status, run.user) == ("on_demand", "completed", "alice")

    with pytest.raises(IngestionRefusedError, match="already rejected"):
        plan_on_demand(store, [bodza.id], pet_kit.client(), alice)


def test_on_demand_refuses_a_unit_not_proposed_ignorable(tmp_path: Path, pet_kit: Any) -> None:
    store = pet_kit.store(tmp_path / "data")
    client = pet_kit.client()
    dog = "user-manuals-pets-and-house-rules/dog-owners-manual"
    plan = plan_ingestion(store, pet_kit.manuals_root, dog, client, Who("bela", Role.user))
    start_run(store, plan, client, tmp_path / "work", confirm=True)
    plain = next(u for u in plan.units if "Bodza" not in u.text)
    with pytest.raises(IngestionRefusedError, match="not proposed ignorable"):
        plan_on_demand(store, [plain.id], client, Who("alice", Role.user))
    with pytest.raises(IngestionRefusedError, match="unknown source unit"):
        plan_on_demand(store, ["su_01JDK7F3Q8ZX5N6M2W4R9T0BCD"], client, Who("alice", Role.user))
