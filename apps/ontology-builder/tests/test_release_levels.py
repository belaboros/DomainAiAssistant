"""What each ``level-N.md`` holds (plan 0002: T15 cumulative levels; T16 raw selection; AC-26)."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from ontology_builder.governance import ChangeSet
from ontology_builder.model import ScopeRecord, Term, validate_record
from ontology_builder.release import DAI, BuildInfo, ReleaseInput, build_level_files, save_raw
from rdflib import Graph, Namespace

_ELEMENT_ANCHOR = re.compile(r'<a id="((?:st|cn|rl|ru|pr)_[0-9A-Z]+)"></a>')


def _ids(text: str) -> set[str]:
    return set(_ELEMENT_ANCHOR.findall(text))


def test_levels_cumulative_by_id(pet_kit: Any, pet_extraction: Any) -> None:
    scope = validate_record(ScopeRecord, pet_kit.scope)
    elements = pet_extraction.elements
    release = ReleaseInput(scope, elements, pet_extraction.units, "raw", "raw+0000000")
    files = build_level_files(release)
    one, two, three = (_ids(files[f"level-{n}.md"]) for n in (1, 2, 3))
    assert one < two < three, "each level holds the one before it and more"
    expected = {
        e.id
        for e in elements
        if not isinstance(e, Term) and e.level != "ignorable" and e.status != "deprecated"
    }
    assert three == expected
    assert one == {e.id for e in elements if e.id in expected and e.level == "level-1"}


def test_no_ignorable_or_deprecated_in_levels(review_kit: Any) -> None:
    kept = review_kit.element("concept", label="dog", level="level-3")
    ignorable = review_kit.element("concept", label="Bodza", level="ignorable")
    deprecated = review_kit.element("concept", "deprecated", snapshot=True, label="hound")
    review_kit.seed([kept, ignorable, deprecated])
    changes = ChangeSet.load(review_kit.store)
    scope = review_kit.store.read().scope()
    elements = list(changes.elements.values())
    files = build_level_files(ReleaseInput(scope, elements, {}, "raw", "raw+0000000"))
    assert kept["id"] in files["level-3.md"]
    for text in files.values():
        for left_out in (ignorable, deprecated):
            assert left_out["id"] not in text
            assert left_out["label"] not in text


def test_raw_excludes_excluded_rejected_ignorable_with_status(review_kit: Any) -> None:
    """AC-26 (raw): everything except excluded, rejected and ignorable, each with its status."""
    kept = {
        status: review_kit.concept(status, snapshot=status in {"approved", "deprecated"})
        for status in ("proposed", "included", "approved", "deprecated")
    }
    left_out = [
        review_kit.concept("excluded"),
        review_kit.concept("rejected"),
        review_kit.element("concept", level="ignorable"),
    ]
    review_kit.seed([*kept.values(), *left_out])
    info = BuildInfo("0123456789abcdef0123456789abcdef01234567", datetime(2026, 11, 21, tzinfo=UTC))
    with review_kit.store.transaction() as files:
        save_raw(files, info)

    folder = review_kit.store.read().release_files("raw")
    graph = Graph().parse(data=folder["ontology.ttl"].decode("utf-8"), format="turtle")
    base = Namespace(review_kit.store.read().scope().base_iri)
    for status, record in kept.items():
        assert (base[record["id"]], DAI.status, DAI[status]) in graph, status
    for record in left_out:
        assert (base[record["id"]], None, None) not in graph, record["status"]
        for name, data in folder.items():
            assert record["id"] not in data.decode("utf-8"), name
