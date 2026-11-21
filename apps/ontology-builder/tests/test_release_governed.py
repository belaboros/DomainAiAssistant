"""Governed builds: snapshots, versions, change log, the FR-35 check (plan 0002, T16).

Covers AC-23, AC-27 and AC-31, and the edge case "deprecating an element that others refer to".
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from ontology_builder.governance import Actor, ChangeSet, apply_action
from ontology_builder.model import Role
from ontology_builder.release import (
    BuildInfo,
    PublishResult,
    ReleaseVersionError,
    publish,
)
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import SKOS

ADMIN = Actor("bela", Role.domain_admin)
ALICE = Actor("alice", Role.user)
INFO = BuildInfo(
    source_commit="0123456789abcdef0123456789abcdef01234567",
    built_at=datetime(2026, 11, 21, 12, 0, tzinfo=UTC),
)
ONT = Namespace("urn:domain-ai-assistant:ontology:pets-and-house-rules:")


def _publish(kit: Any, version: str | None = None) -> PublishResult:
    with kit.store.transaction() as files:
        return publish(files, INFO, version)


def _act(kit: Any, actor: Actor, action: str, element_id: str, **payload: Any) -> None:
    changes = ChangeSet.load(kit.store)
    apply_action(changes, actor, action, element_id, **payload)
    with kit.store.transaction() as files:
        changes.write(files)
    changes.mark_saved()


def _governed(kit: Any) -> dict[str, str]:
    files = kit.store.read().release_files("governed")
    return {name: data.decode("utf-8") for name, data in files.items()}


def _graph(text: str) -> Graph:
    return Graph().parse(data=text, format="turtle")


def test_edit_after_approval_governed_keeps_old_definition(review_kit: Any) -> None:
    """AC-23: an edit puts the concept back to included; governed keeps the approved version."""
    [concept] = review_kit.seed([review_kit.concept("approved", snapshot=True)])
    old = "A rope or strap to lead a dog."
    assert _publish(review_kit, "1.0.0").governed is not None

    _act(review_kit, ALICE, "correct", concept, field="definition", value="A strap.")
    assert review_kit.store.read().elements()[concept].status == "included"
    result = _publish(review_kit)
    assert result.governed is not None
    governed = _graph(_governed(review_kit)["ontology.ttl"])
    assert (ONT[concept], SKOS.definition, Literal(old)) in governed
    assert (ONT[concept], SKOS.definition, Literal("A strap.")) not in governed
    raw = review_kit.store.read().release_files("raw")["ontology.ttl"].decode("utf-8")
    assert (ONT[concept], SKOS.definition, Literal("A strap.")) in _graph(raw)


def test_publish_defaults_to_next_minor_with_changelog(review_kit: Any) -> None:
    """AC-27: 1.0.0, then approvals; the next publish is 1.1.0 with a change log."""
    kept, edited, to_deprecate, to_remove = review_kit.seed(
        [review_kit.concept("approved", snapshot=True) for _ in range(4)]
    )
    [waiting] = review_kit.seed([review_kit.concept("included")])
    first = _publish(review_kit)
    assert first.governed is not None
    assert first.governed.version == "1.0.0", "the first governed version"

    _act(review_kit, ALICE, "correct", edited, field="definition", value="Changed.")
    _act(review_kit, ADMIN, "approve", edited)
    _act(review_kit, ADMIN, "approve", waiting)
    _act(review_kit, ADMIN, "deprecate", to_deprecate, replacement=kept, reason="Same thing.")
    _act(review_kit, ALICE, "level", to_remove, level="ignorable", reason="Not domain knowledge.")
    _act(review_kit, ADMIN, "approve", to_remove)
    [proposed] = review_kit.seed([review_kit.concept("proposed")])

    second = _publish(review_kit)
    assert second.governed is not None
    assert second.governed.version == "1.1.0"
    files = _governed(review_kit)
    graph = _graph(files["ontology.ttl"])
    in_release = {
        s.removeprefix(str(ONT)) for s in map(str, graph.subjects()) if s.startswith(str(ONT))
    }
    assert {kept, edited, waiting, to_deprecate} <= in_release
    assert proposed not in in_release
    assert to_remove not in in_release

    changelog = files["CHANGELOG.md"]
    newest, older = changelog.split("\n## 1.0.0", 1)
    assert "## 1.1.0" in newest
    assert "against 1.0.0" in newest
    sections = dict(re_sections(newest))
    assert waiting in sections["Added"]
    assert edited in sections["Changed"]
    assert to_deprecate in sections["Deprecated"]
    assert to_remove in sections["Removed"]
    assert kept not in newest, "an unchanged element is not listed"
    assert kept in older, "the 1.0.0 entry is kept below the newest one"


def re_sections(text: str) -> list[tuple[str, str]]:
    parts = text.split("\n### ")[1:]
    return [(part.split("\n", 1)[0], part.split("\n", 1)[1]) for part in parts]


def test_explicit_version_must_be_semver_and_newer(review_kit: Any) -> None:
    review_kit.seed([review_kit.concept("approved", snapshot=True)])
    assert _publish(review_kit, "2.0.0").governed is not None
    for version in ("2.0.0", "1.9.0", "2.1", "v2.1.0"):
        with pytest.raises(ReleaseVersionError):
            _publish(review_kit, version)
    assert _governed(review_kit)["manifest.json"].count('"2.0.0"') == 1


def test_approved_rule_on_proposed_concept_blocks_publish(review_kit: Any) -> None:
    """AC-31: offenders listed, governed folder unchanged, raw rebuilt."""
    review_kit.seed([review_kit.concept("approved", snapshot=True)])
    assert _publish(review_kit, "1.0.0").governed is not None
    before = review_kit.store.read().release_files("governed")

    concept = review_kit.concept("proposed")
    rule = review_kit.element("rule", "approved", snapshot=True, refers_to=[concept["id"]])
    review_kit.seed([concept, rule])
    result = _publish(review_kit)

    assert result.governed is None
    assert [(o.element_id, o.target_id, o.target_status) for o in result.offenders] == [
        (rule["id"], concept["id"], "proposed")
    ]
    assert review_kit.store.read().release_files("governed") == before
    raw = review_kit.store.read().release_files("raw")["ontology.ttl"].decode("utf-8")
    assert rule["id"] in raw and concept["id"] in raw


def test_deprecated_reference_warns(review_kit: Any) -> None:
    subject, target = review_kit.seed(
        [
            review_kit.concept("approved", snapshot=True),
            review_kit.concept("approved", snapshot=True),
        ]
    )
    relation = review_kit.element(
        "relation", "approved", snapshot=True, subject=subject, object=target
    )
    review_kit.seed([relation])
    _act(review_kit, ADMIN, "deprecate", target, reason="Outdated.")

    result = _publish(review_kit)
    assert result.governed is not None
    assert result.offenders == []
    assert [(w.element_id, w.target_id, w.target_status) for w in result.warnings] == [
        (relation["id"], target, "deprecated")
    ]
