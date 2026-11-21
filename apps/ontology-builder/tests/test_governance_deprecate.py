"""Deprecation with a replacement, and no delete path (plan 0002, T11: AC-24 records)."""

from __future__ import annotations

import contextlib
import inspect
import re
from pathlib import Path
from typing import Any

import pytest
from ontology_builder import governance
from ontology_builder.governance import Actor, ChangeSet, GovernanceRefusedError, apply_action
from ontology_builder.model import Role
from ontology_builder.store import DatasetFiles, DatasetStore

ADMIN = Actor("bela", Role.domain_admin)
USER = Actor("sam", Role.user)
ACTIONS: dict[str, dict[str, Any]] = {
    "include": {},
    "exclude": {"reason": "r"},
    "approve": {},
    "reject": {"reason": "r"},
    "deprecate": {"reason": "r"},
    "level": {"level": "level-2", "reason": "r"},
}
_DELETE_CALL = r"\.(unlink|rmdir)\(|rmtree|os\.remove|\bdel\s+\w+\.elements"
GOVERNANCE_DIR = Path(governance.__file__).parent


def test_deprecate_with_replacement(review_kit: Any) -> None:
    old, new = review_kit.seed(
        [review_kit.concept("approved", snapshot=True), review_kit.concept()]
    )
    changes = ChangeSet.load(review_kit.store)
    apply_action(changes, ADMIN, "deprecate", old, replacement=new, reason="Renamed.")
    with review_kit.store.transaction() as files:
        changes.write(files)
    record = review_kit.store.read().elements()[old]
    assert (record.status, record.replaced_by, record.status_reason) == (
        "deprecated",
        new,
        "Renamed.",
    )
    assert record.approved_snapshot is not None
    steps = [(d.action, d.field, d.old, d.new) for d in review_kit.store.read().decisions()]
    assert steps == [
        ("deprecate", "status", "approved", "deprecated"),
        ("deprecate", "replaced_by", None, new),
    ]


def test_deprecate_without_replacement(review_kit: Any) -> None:
    [old] = review_kit.seed([review_kit.concept("approved", snapshot=True)])
    changes = ChangeSet.load(review_kit.store)
    apply_action(changes, ADMIN, "deprecate", old)
    assert changes.elements[old].status == "deprecated"
    assert changes.elements[old].replaced_by is None
    assert len(changes.decisions) == 1


@pytest.mark.parametrize("replacement", ["self", "cn_NOPE"])
def test_deprecate_refuses_a_bad_replacement(review_kit: Any, replacement: str) -> None:
    [old] = review_kit.seed([review_kit.concept("approved", snapshot=True)])
    changes = ChangeSet.load(review_kit.store)
    with pytest.raises(GovernanceRefusedError, match="replace"):
        apply_action(
            changes,
            ADMIN,
            "deprecate",
            old,
            replacement=old if replacement == "self" else replacement,
        )
    assert changes.elements[old].status == "approved"
    assert changes.decisions == []


@pytest.mark.parametrize("actor", [ADMIN, USER], ids=["admin", "user"])
def test_no_operation_deletes_approved_excluded_rejected(review_kit: Any, actor: Actor) -> None:
    ids = review_kit.seed(
        [
            review_kit.concept("approved", snapshot=True),
            review_kit.concept("excluded"),
            review_kit.concept("rejected"),
        ]
    )
    changes = ChangeSet.load(review_kit.store)
    for element_id in ids:
        for action, payload in ACTIONS.items():
            with contextlib.suppress(GovernanceRefusedError):
                apply_action(changes, actor, action, element_id, **payload)
    with review_kit.store.transaction() as files:
        changes.write(files)
    assert set(ids) <= set(review_kit.store.read().elements())
    for element_id in ids:
        assert (_element_file(review_kit.store, element_id)).is_file()


def test_there_is_no_delete_path() -> None:
    delete_like = re.compile(r"delete|remove|unlink|rmtree|drop", re.IGNORECASE)
    for name in governance.__all__:
        assert not delete_like.search(name), name
    for name, _ in inspect.getmembers(ChangeSet) + inspect.getmembers(DatasetFiles):
        assert not delete_like.search(name), name
    for path in GOVERNANCE_DIR.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert not re.search(_DELETE_CALL, source), path


def _element_file(store: DatasetStore, element_id: str) -> Path:
    return store.root / "01_model" / "elements" / "concept" / f"{element_id}.yaml"
