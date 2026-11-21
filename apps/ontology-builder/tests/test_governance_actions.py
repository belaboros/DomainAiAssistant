"""Review actions: correct, level, merge, split, reassign (plan 0002, T12: AC-16)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import pytest
from ontology_builder.governance import (
    Actor,
    ChangeSet,
    GovernanceRefusedError,
    apply_action,
    snapshot_of,
)
from ontology_builder.model import Concept, Element, Property, Relation, Role, Rule, Term
from ontology_builder.store import DatasetStore

ALICE = Actor("alice", Role.user)
ADMIN = Actor("bela", Role.domain_admin)


@dataclass
class World:
    """Three concepts, the terms "lead" and "leash", a relation and a rule (all ``proposed``)."""

    kit: Any
    ids: dict[str, str]
    units: dict[str, str]

    def changes(self) -> ChangeSet:
        return ChangeSet.load(self.kit.store)

    def save(self, changes: ChangeSet) -> None:
        with self.kit.store.transaction() as files:
            changes.write(files)
        changes.mark_saved()

    def stored(self, key: str) -> Element:
        store: DatasetStore = self.kit.store
        return store.read().elements()[self.ids[key]]


def _world(kit: Any, approved: frozenset[str] = frozenset()) -> World:
    units = {name: kit.unit() for name in ["dog", "rule", "role"]}

    def ev(*names: str) -> list[dict[str, str]]:
        return [{"unit": units[n]} for n in names]

    def status(key: str) -> dict[str, Any]:
        return {"status": "approved", "snapshot": True} if key in approved else {}

    leash = kit.element("concept", label="leash", evidence=ev("dog"), **status("leash"))
    lead = kit.element("concept", label="lead", evidence=ev("rule", "role"), **status("lead"))
    dog = kit.element("concept", label="dog", evidence=ev("dog"), definition=None)
    records = {"leash": leash, "lead": lead, "dog": dog}
    records["term_lead"] = kit.element(
        "term",
        label="lead",
        evidence=ev("rule", "role"),
        mentions=[
            {"unit": units["rule"], "concept": lead["id"]},
            {"unit": units["role"], "concept": lead["id"]},
        ],
        **status("term_lead"),
    )
    records["term_leash"] = kit.element(
        "term",
        label="leash",
        evidence=ev("dog"),
        mentions=[{"unit": units["dog"], "concept": leash["id"]}],
    )
    records["relation"] = kit.element(
        "relation", subject=dog["id"], object=lead["id"], evidence=ev("dog"), **status("relation")
    )
    records["rule"] = kit.element(
        "rule", refers_to=[lead["id"]], evidence=ev("rule"), **status("rule")
    )
    records["property"] = kit.element("property", of=lead["id"], evidence=ev("rule"))
    kit.seed(list(records.values()))
    return World(kit, {key: record["id"] for key, record in records.items()}, units)


@pytest.fixture
def world(review_kit: Any) -> World:
    return _world(review_kit)


def _as[E: Element](record_class: type[E], element: Element) -> E:
    assert isinstance(element, record_class)
    return element


def _mentions(element: Element) -> dict[str, str]:
    return {m.unit: m.concept for m in _as(Term, element).mentions or []}


# ---- AC-16: every action records the record change and a full decision ----

Check = Callable[[World], None]


def _payload(world: World, action: str) -> tuple[str, dict[str, Any], str]:
    """(element key, payload, the field the action changes) for each action."""
    cases: dict[str, tuple[str, dict[str, Any], str]] = {
        "include": ("lead", {}, "status"),
        "exclude": ("lead", {"reason": "Not a pet concept."}, "status"),
        "correct": (
            "lead",
            {"field": "definition", "value": "A rope to walk a dog.", "reason": "Typo."},
            "definition",
        ),
        "level": ("lead", {"level": "level-2", "reason": "Everyday care."}, "level"),
        "merge": ("lead", {"into": world.ids["leash"], "reason": "Same thing."}, "status"),
        "split": (
            "term_lead",
            {
                "units": [world.units["role"]],
                "label": "leading role",
                "scope_note": "The owner leads the dog.",
                "reason": "Two senses.",
            },
            "mentions",
        ),
        "reassign": (
            "term_lead",
            {"unit": world.units["role"], "concept": world.ids["dog"], "reason": "Wrong sense."},
            "mentions",
        ),
    }
    return cases[action]


EXPECTED: dict[str, Check] = {
    "include": lambda w: _assert(w.stored("lead").status == "included"),
    "exclude": lambda w: _assert(w.stored("lead").status_reason == "Not a pet concept."),
    "correct": lambda w: _assert(w.stored("lead").definition == "A rope to walk a dog."),
    "level": lambda w: _assert(w.stored("lead").level == "level-2"),
    "merge": lambda w: _assert(w.stored("lead").replaced_by == w.ids["leash"]),
    "split": lambda w: _assert(len(set(_mentions(w.stored("term_lead")).values())) == 2),
    "reassign": lambda w: _assert(w.ids["dog"] in _mentions(w.stored("term_lead")).values()),
}


def _assert(condition: bool) -> None:
    assert condition


@pytest.mark.parametrize("action", list(EXPECTED))
def test_action_records_decision(world: World, action: str) -> None:
    key, payload, field = _payload(world, action)
    changes = world.changes()
    apply_action(changes, ALICE, action, world.ids[key], **payload)
    world.save(changes)

    EXPECTED[action](world)
    decisions = world.kit.store.read().decisions()
    assert decisions, "the action is recorded"
    assert {(d.user, d.role, d.at) for d in decisions} == {("alice", "user", world.kit.at)}
    assert {d.action for d in decisions} == {action}
    mine = [d for d in decisions if d.element_id == world.ids[key] and d.field == field]
    assert mine, f"a decision on {key}.{field}"
    assert mine[0].old != mine[0].new
    assert mine[0].reason == payload.get("reason")


# ---- correct ----


@pytest.mark.parametrize("field", ["id", "status", "origin", "approved_snapshot", "replaced_by"])
def test_correct_refuses_protected_fields(world: World, field: str) -> None:
    changes = world.changes()
    with pytest.raises(GovernanceRefusedError, match=field):
        apply_action(changes, ALICE, "correct", world.ids["lead"], field=field, value="x")
    assert changes.decisions == []


def test_correct_refuses_an_invalid_value(world: World) -> None:
    changes = world.changes()
    with pytest.raises(GovernanceRefusedError, match="level"):
        apply_action(changes, ALICE, "correct", world.ids["lead"], field="level", value="level-9")
    assert changes.changed_ids() == [] and changes.decisions == []


def test_correct_after_approval_goes_back_to_included(review_kit: Any) -> None:
    world = _world(review_kit, frozenset({"lead"}))
    changes = world.changes()
    apply_action(changes, ALICE, "correct", world.ids["lead"], field="definition", value="New.")
    lead = changes.elements[world.ids["lead"]]
    assert lead.status == "included"
    snapshot = snapshot_of(lead)
    assert snapshot is not None and snapshot.definition != "New."


# ---- merge ----


def test_merge_moves_evidence_and_references_and_approved_go_back_to_included(
    review_kit: Any,
) -> None:
    world = _world(review_kit, frozenset({"rule", "relation"}))
    changes = world.changes()
    apply_action(changes, ALICE, "merge", world.ids["lead"], into=world.ids["leash"])
    world.save(changes)

    leash, lead = world.stored("leash"), world.stored("lead")
    assert {e.unit for e in leash.evidence} == set(world.units.values())
    assert (lead.status, lead.replaced_by) == ("excluded", world.ids["leash"])
    assert "merged into" in (lead.status_reason or "")
    rule, relation = world.stored("rule"), world.stored("relation")
    assert _as(Rule, rule).refers_to == [world.ids["leash"]]
    assert _as(Relation, relation).object == world.ids["leash"]
    assert _as(Property, world.stored("property")).of == world.ids["leash"]
    assert (rule.status, relation.status) == ("included", "included")
    assert snapshot_of(rule) is not None, "the governed release keeps the approved version"
    assert set(_mentions(world.stored("term_lead")).values()) == {world.ids["leash"]}, (
        "lead is a synonym of leash"
    )


def test_merge_without_a_term_adds_the_label_as_synonym_term(review_kit: Any) -> None:
    unit = review_kit.unit()
    kept = review_kit.element("concept", label="leash")
    merged = review_kit.element("concept", label="lead", evidence=[{"unit": unit}])
    review_kit.seed([kept, merged])
    changes = ChangeSet.load(review_kit.store)
    apply_action(changes, ALICE, "merge", merged["id"], into=kept["id"])
    terms = [e for e in changes.elements.values() if e.id.startswith("tm_")]
    [term] = terms
    assert (term.label, term.status) == ("lead", "included")
    assert [(m.unit, m.concept) for m in _as(Term, term).mentions or []] == [(unit, kept["id"])]
    assert term.origin.kind == "user" and term.origin.author == "alice"


def test_merging_an_approved_concept_needs_an_admin(review_kit: Any) -> None:
    world = _world(review_kit, frozenset({"lead"}))
    changes = world.changes()
    with pytest.raises(GovernanceRefusedError, match="domain admin"):
        apply_action(changes, ALICE, "merge", world.ids["lead"], into=world.ids["leash"])
    assert changes.changed_ids() == [] and changes.decisions == []

    apply_action(changes, ADMIN, "merge", world.ids["lead"], into=world.ids["leash"])
    lead = changes.elements[world.ids["lead"]]
    assert (lead.status, lead.replaced_by) == ("deprecated", world.ids["leash"])


@pytest.mark.parametrize(
    ("source", "target", "message"),
    [
        ("lead", "lead", "itself"),
        ("lead", "rule", "concept"),
        ("term_lead", "term_leash", "concept"),
        ("lead", "missing", "unknown element"),
    ],
)
def test_merge_refusals(world: World, source: str, target: str, message: str) -> None:
    changes = world.changes()
    into = world.ids.get(target, "cn_00000000000000000000000000")
    with pytest.raises(GovernanceRefusedError, match=message):
        apply_action(changes, ALICE, "merge", world.ids[source], into=into)
    assert changes.changed_ids() == [] and changes.decisions == []


def test_merge_of_an_excluded_concept_is_refused(review_kit: Any) -> None:
    kept, gone = review_kit.concept(), review_kit.concept("excluded")
    review_kit.seed([kept, gone])
    changes = ChangeSet.load(review_kit.store)
    with pytest.raises(GovernanceRefusedError, match="excluded"):
        apply_action(changes, ALICE, "merge", gone["id"], into=kept["id"])


# ---- split ----


def test_split_creates_an_included_sense_and_both_concepts_are_included(
    review_kit: Any,
) -> None:
    world = _world(review_kit, frozenset({"lead", "term_lead"}))
    changes = world.changes()
    apply_action(
        changes,
        ALICE,
        "split",
        world.ids["term_lead"],
        units=[world.units["role"]],
        label="leading role",
        scope_note="The owner leads the dog.",
        original_scope_note="The rope or strap.",
    )
    world.save(changes)

    mentions = _mentions(world.stored("term_lead"))
    new_id = mentions[world.units["role"]]
    assert mentions[world.units["rule"]] == world.ids["lead"]
    sense = world.kit.store.read().elements()[new_id]
    assert (sense.label, sense.status, _as(Concept, sense).scope_note) == (
        "leading role",
        "included",
        "The owner leads the dog.",
    )
    assert [e.unit for e in sense.evidence] == [world.units["role"]]
    lead = world.stored("lead")
    assert lead.status == "included"
    assert _as(Concept, lead).scope_note == "The rope or strap."
    assert [e.unit for e in lead.evidence] == [world.units["rule"]]
    assert world.stored("term_lead").status == "included"


@pytest.mark.parametrize(
    ("units", "message"),
    [([], "at least one"), (["other"], "no mention"), (["rule", "role"], "keeps")],
)
def test_split_refusals(world: World, units: list[str], message: str) -> None:
    changes = world.changes()
    chosen = [world.units.get(u, "su_00000000000000000000000000") for u in units]
    with pytest.raises(GovernanceRefusedError, match=message):
        apply_action(
            changes,
            ALICE,
            "split",
            world.ids["term_lead"],
            units=chosen,
            label="x",
            scope_note="y",
        )
    assert changes.changed_ids() == [] and changes.decisions == []


def test_split_needs_a_term(world: World) -> None:
    with pytest.raises(GovernanceRefusedError, match="term"):
        apply_action(
            world.changes(), ALICE, "split", world.ids["lead"], units=[], label="x", scope_note="y"
        )


# ---- reassign ----


def test_reassign_points_one_mention_to_another_concept(world: World) -> None:
    changes = world.changes()
    apply_action(
        changes,
        ALICE,
        "reassign",
        world.ids["term_lead"],
        unit=world.units["rule"],
        concept=world.ids["leash"],
    )
    mentions = _mentions(changes.elements[world.ids["term_lead"]])
    assert mentions == {
        world.units["rule"]: world.ids["leash"],
        world.units["role"]: world.ids["lead"],
    }


@pytest.mark.parametrize(
    ("unit", "target", "message"),
    [("other", "leash", "no mention"), ("rule", "rule", "concept"), ("rule", "gone", "excluded")],
)
def test_reassign_refusals(review_kit: Any, unit: str, target: str, message: str) -> None:
    world = _world(review_kit)
    gone = review_kit.concept("excluded")
    review_kit.seed([gone])
    world.ids["gone"] = gone["id"]
    changes = world.changes()
    with pytest.raises(GovernanceRefusedError, match=message):
        apply_action(
            changes,
            ALICE,
            "reassign",
            world.ids["term_lead"],
            unit=world.units.get(unit, "su_00000000000000000000000000"),
            concept=world.ids[target],
        )
    assert changes.changed_ids() == [] and changes.decisions == []


# ---- atomicity ----


def test_a_refused_action_leaves_no_partial_change(world: World) -> None:
    changes = world.changes()

    def half_then_refuse() -> None:
        apply_action(changes, ALICE, "include", world.ids["lead"])
        raise GovernanceRefusedError("refused halfway")

    with pytest.raises(GovernanceRefusedError), changes.atomic():
        half_then_refuse()
    assert changes.elements[world.ids["lead"]].status == "proposed"
    assert changes.changed_ids() == [] and changes.decisions == []
