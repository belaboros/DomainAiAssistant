"""Bulk actions with per-ID results (plan 0002, T11: AC-17)."""

from __future__ import annotations

from typing import Any

from ontology_builder.governance import Actor, ChangeSet, apply_bulk
from ontology_builder.model import Role

ADMIN = Actor("bela", Role.domain_admin)
USER = Actor("sam", Role.user)


def test_bulk_level3_on_20_records_20_decisions(review_kit: Any) -> None:
    ids = review_kit.seed([review_kit.concept() for _ in range(20)])
    changes = ChangeSet.load(review_kit.store)
    results = apply_bulk(changes, USER, "level", ids, {"level": "level-3", "reason": "Details."})
    assert [r.element_id for r in results] == ids
    assert all(r.ok for r in results)
    assert all(changes.elements[i].level == "level-3" for i in ids)
    assert len(changes.decisions) == 20
    assert {(d.action, d.user, d.role, d.old, d.new) for d in changes.decisions} == {
        ("level", "sam", "user", "level-1", "level-3")
    }
    assert sorted(changes.changed_ids()) == sorted(ids)


def test_bulk_approve_admin_only(review_kit: Any) -> None:
    ids = review_kit.seed([review_kit.concept("included") for _ in range(3)])
    changes = ChangeSet.load(review_kit.store)

    refused = apply_bulk(changes, USER, "approve", ids, {})
    assert [r.ok for r in refused] == [False, False, False]
    assert all("domain admin" in r.message for r in refused)
    assert changes.decisions == [] and changes.changed_ids() == []

    approved = apply_bulk(changes, ADMIN, "approve", ids, {})
    assert all(r.ok for r in approved)
    assert all(changes.elements[i].status == "approved" for i in ids)


def test_bulk_reports_each_refusal_and_applies_the_rest(review_kit: Any) -> None:
    ids = review_kit.seed(
        [review_kit.concept("proposed"), review_kit.concept("rejected"), review_kit.concept()]
    )
    changes = ChangeSet.load(review_kit.store)
    results = apply_bulk(changes, USER, "include", [*ids, "cn_NOPE"], {})
    assert [r.ok for r in results] == [True, False, True, False]
    assert "rejected" in results[1].message
    assert "unknown element" in results[3].message
    assert changes.elements[ids[1]].status == "rejected"
    assert len(changes.decisions) == 2


def test_bulk_reject_needs_reason_per_id(review_kit: Any) -> None:
    ids = review_kit.seed([review_kit.concept() for _ in range(2)])
    changes = ChangeSet.load(review_kit.store)
    results = apply_bulk(changes, ADMIN, "reject", ids, {"reason": "Out of scope."})
    assert all(r.ok for r in results)
    assert {d.reason for d in changes.decisions} == {"Out of scope."}
