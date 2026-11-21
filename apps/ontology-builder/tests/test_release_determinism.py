"""Two builds from the same records give the same bytes (plan 0002, T16: AC-32, FR-36)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import pytest
from ontology_builder.release import BuildInfo, build_governed, build_raw

COMMIT = "0123456789abcdef0123456789abcdef01234567"


def _seed(kit: Any) -> None:
    animal = kit.concept("approved", snapshot=True)
    dog = kit.element("concept", "approved", snapshot=True, parents=[animal["id"]], label="dog")
    lead = kit.element("concept", "included", label="lead")
    relation = kit.element(
        "relation", "approved", snapshot=True, subject=dog["id"], object=animal["id"]
    ) | {"cardinality": {"min": 1, "max": 2}}
    relation["approved_snapshot"]["cardinality"] = {"min": 1, "max": 2}
    rule = kit.element("rule", "approved", snapshot=True, refers_to=[dog["id"]])
    kit.seed([animal, dog, lead, relation, rule])


@pytest.mark.parametrize("variant", ["raw", "governed"])
def test_two_builds_identical_except_built_at(review_kit: Any, variant: str) -> None:
    _seed(review_kit)
    builds = []
    for hour in (9, 17):
        info = BuildInfo(COMMIT, datetime(2026, 11, 21, hour, 0, tzinfo=UTC))
        files = review_kit.store.read()
        release = (
            build_raw(files, info) if variant == "raw" else build_governed(files, info).release
        )
        builds.append(release.files)
    first, second = builds
    assert sorted(first) == sorted(second)
    for name in first:
        if name != "manifest.json":
            assert first[name] == second[name], name
    one, two = (json.loads(build["manifest.json"]) for build in builds)
    assert one.pop("built_at") != two.pop("built_at")
    assert one == two
    assert first["manifest.json"].endswith("}\n")
