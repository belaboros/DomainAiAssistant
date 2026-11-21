"""The status machine of plan 0002 (T11: AC-22, AC-3 at service level)."""

from __future__ import annotations

from typing import Any

import pytest
from ontology_builder.governance import (
    Actor,
    ChangeSet,
    GovernanceRefusedError,
    apply_action,
    snapshot_of,
)
from ontology_builder.model import Role

ADMIN = Actor("bela", Role.domain_admin)
USER = Actor("sam", Role.user)

# State of the element before the action: (status, has an approved snapshot).
STATES: dict[str, tuple[str, bool]] = {
    "proposed": ("proposed", False),
    "included_new": ("included", False),
    "included_snapshot": ("included", True),
    "approved": ("approved", True),
    "excluded": ("excluded", False),
    "rejected": ("rejected", False),
    "deprecated": ("deprecated", True),
}

# The plan's table: state -> action -> resulting status; a missing action is refused.
ALLOWED: dict[str, dict[str, str]] = {
    "proposed": {
        "include": "included",
        "exclude": "excluded",
        "approve": "approved",
        "reject": "rejected",
        "level": "proposed",
    },
    "included_new": {
        "exclude": "excluded",
        "approve": "approved",
        "reject": "rejected",
        "level": "included",
    },
    "included_snapshot": {"approve": "approved", "deprecate": "deprecated", "level": "included"},
    "approved": {"deprecate": "deprecated", "level": "included"},
    "excluded": {"include": "included"},
    "rejected": {},
    "deprecated": {},
}
ACTIONS = ["include", "exclude", "approve", "reject", "deprecate", "level"]
PAYLOAD: dict[str, dict[str, Any]] = {
    "include": {},
    "exclude": {"reason": "Not about pets."},
    "approve": {},
    "reject": {"reason": "Duplicate."},
    "deprecate": {"reason": "Outdated."},
    "level": {"level": "level-3", "reason": "Special case."},
}
ALLOWED_CASES = [(s, a) for s in STATES for a in ACTIONS if a in ALLOWED[s]]
FORBIDDEN_CASES = [(s, a) for s in STATES for a in ACTIONS if a not in ALLOWED[s]]


def _seeded(review_kit: Any, state: str) -> tuple[ChangeSet, str]:
    status, snapshot = STATES[state]
    [element_id] = review_kit.seed([review_kit.concept(status, snapshot=snapshot)])
    return ChangeSet.load(review_kit.store), element_id


@pytest.mark.parametrize(("state", "action"), ALLOWED_CASES)
def test_allowed_transitions(review_kit: Any, state: str, action: str) -> None:
    changes, element_id = _seeded(review_kit, state)
    apply_action(changes, ADMIN, action, element_id, **PAYLOAD[action])
    element = changes.elements[element_id]
    assert element.status == ALLOWED[state][action]
    assert changes.decisions, "every transition records a decision"
    assert all(d.element_id == element_id and d.user == "bela" for d in changes.decisions)
    if state in {"approved", "included_snapshot"}:
        assert snapshot_of(element) is not None, "the approved snapshot is kept"


@pytest.mark.parametrize(("state", "action"), FORBIDDEN_CASES)
def test_forbidden_transition_refused(review_kit: Any, state: str, action: str) -> None:
    changes, element_id = _seeded(review_kit, state)
    before = changes.elements[element_id]
    with pytest.raises(GovernanceRefusedError):
        apply_action(changes, ADMIN, action, element_id, **PAYLOAD[action])
    assert changes.elements[element_id] == before
    assert changes.decisions == []
    assert changes.changed_ids() == []


def test_approve_from_proposed_records_include_then_approve(review_kit: Any) -> None:
    changes, element_id = _seeded(review_kit, "proposed")
    apply_action(changes, ADMIN, "approve", element_id)
    steps = [(d.action, d.field, d.old, d.new) for d in changes.decisions]
    assert steps == [
        ("include", "status", "proposed", "included"),
        ("approve", "status", "included", "approved"),
    ]
    assert [d.role for d in changes.decisions] == ["domain_admin", "domain_admin"]
    assert all(d.at == review_kit.at for d in changes.decisions)


def test_approve_stores_the_approved_snapshot(review_kit: Any) -> None:
    changes, element_id = _seeded(review_kit, "included_new")
    apply_action(changes, ADMIN, "approve", element_id)
    element = changes.elements[element_id]
    snapshot = snapshot_of(element)
    assert snapshot is not None
    assert snapshot.status == "approved"
    assert snapshot.definition == element.definition
    assert snapshot_of(snapshot) is None, "snapshots are never nested"


def test_edit_after_approval_goes_back_to_included_and_keeps_snapshot(review_kit: Any) -> None:
    changes, element_id = _seeded(review_kit, "approved")
    old_snapshot = snapshot_of(changes.elements[element_id])
    apply_action(changes, USER, "level", element_id, level="level-3", reason="Special case.")
    element = changes.elements[element_id]
    assert (element.status, element.level) == ("included", "level-3")
    assert snapshot_of(element) == old_snapshot
    fields = [(d.field, d.old, d.new) for d in changes.decisions]
    assert ("level", "level-1", "level-3") in fields
    assert ("status", "approved", "included") in fields


@pytest.mark.parametrize("action", ["exclude", "reject"])
def test_exclude_and_reject_need_a_reason(review_kit: Any, action: str) -> None:
    changes, element_id = _seeded(review_kit, "proposed")
    with pytest.raises(GovernanceRefusedError, match="reason"):
        apply_action(changes, ADMIN, action, element_id, reason="  ")
    assert changes.decisions == []


def test_reason_is_kept_on_the_record_and_the_decision(review_kit: Any) -> None:
    changes, element_id = _seeded(review_kit, "proposed")
    apply_action(changes, USER, "exclude", element_id, reason="Not about pets.")
    assert changes.elements[element_id].status_reason == "Not about pets."
    [decision] = changes.decisions
    assert (decision.action, decision.reason) == ("exclude", "Not about pets.")


@pytest.mark.parametrize("action", ["approve", "reject", "deprecate"])
@pytest.mark.parametrize("state", ["proposed", "included_new", "approved"])
def test_user_refused_admin_actions(review_kit: Any, state: str, action: str) -> None:
    changes, element_id = _seeded(review_kit, state)
    before = changes.elements[element_id]
    with pytest.raises(GovernanceRefusedError, match="domain admin"):
        apply_action(changes, USER, action, element_id, **PAYLOAD[action])
    assert changes.elements[element_id] == before
    assert changes.decisions == []


def test_unknown_action_and_element_refused(review_kit: Any) -> None:
    changes, element_id = _seeded(review_kit, "proposed")
    with pytest.raises(GovernanceRefusedError, match="unknown action"):
        apply_action(changes, ADMIN, "delete", element_id)
    with pytest.raises(GovernanceRefusedError, match="unknown element"):
        apply_action(changes, ADMIN, "include", "cn_NOPE")


def test_changes_are_written_in_one_transaction(review_kit: Any) -> None:
    changes, element_id = _seeded(review_kit, "proposed")
    apply_action(changes, USER, "include", element_id)
    with review_kit.store.transaction() as files:
        changes.write(files)
    assert changes.changed_ids() == [element_id], "kept until the save succeeded"
    changes.mark_saved()
    files = review_kit.store.read()
    assert files.elements()[element_id].status == "included"
    assert [d.action for d in files.decisions()] == ["include"]
    assert changes.changed_ids() == [] and changes.decisions == []
