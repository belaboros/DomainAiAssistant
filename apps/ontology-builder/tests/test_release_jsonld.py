"""The JSON-LD twin of ``ontology.ttl`` (plan 0002, T30: FR-37, with FR-36 determinism)."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

import pytest
from ontology_builder.model import ScopeRecord, validate_record
from ontology_builder.release import (
    BuildInfo,
    ReleaseInput,
    build_jsonld,
    build_raw,
    build_turtle,
    publish,
)
from rdflib import Graph
from rdflib.compare import isomorphic

COMMIT = "0123456789abcdef0123456789abcdef01234567"


def _seed(kit: Any) -> None:
    animal = kit.concept("approved", snapshot=True)
    dog = kit.element("concept", "approved", snapshot=True, parents=[animal["id"]], label="dog")
    relation = kit.element(
        "relation", "approved", snapshot=True, subject=dog["id"], object=animal["id"]
    ) | {"cardinality": {"min": 1, "max": 2}}
    relation["approved_snapshot"]["cardinality"] = {"min": 1, "max": 2}
    rule = kit.element("rule", "approved", snapshot=True, refers_to=[dog["id"]])
    kit.seed([animal, dog, kit.concept("proposed"), relation, rule])


def _publish(kit: Any) -> dict[str, dict[str, bytes]]:
    info = BuildInfo(COMMIT, datetime(2026, 11, 22, 12, 0, tzinfo=UTC))
    with kit.store.transaction() as files:
        publish(files, info, "1.0.0")
    folders = kit.store.read()
    return {variant: folders.release_files(variant) for variant in ("raw", "governed")}


def _same_graph(turtle: str, jsonld: str) -> bool:
    return isomorphic(
        Graph().parse(data=turtle, format="turtle"), Graph().parse(data=jsonld, format="json-ld")
    )


@pytest.mark.parametrize("variant", ["raw", "governed"])
def test_both_releases_have_jsonld_in_manifest(review_kit: Any, variant: str) -> None:
    """FR-37: each release holds ``ontology.jsonld`` with the graph of ``ontology.ttl``."""
    _seed(review_kit)
    folder = _publish(review_kit)[variant]
    jsonld = folder["ontology.jsonld"]
    assert _same_graph(folder["ontology.ttl"].decode("utf-8"), jsonld.decode("utf-8"))
    manifest = json.loads(folder["manifest.json"])
    assert manifest["files"]["ontology.jsonld"] == "sha256:" + hashlib.sha256(jsonld).hexdigest()


def test_pet_graph_is_the_same_in_both_formats(pet_kit: Any, pet_extraction: Any) -> None:
    """FR-37 on the whole pet extraction: terms, rules, cardinalities and SHACL shapes."""
    scope = validate_record(ScopeRecord, pet_kit.scope)
    release = ReleaseInput(scope, pet_extraction.elements, pet_extraction.units, "raw", "raw+0")
    jsonld = build_jsonld(release)
    assert _same_graph(build_turtle(release), jsonld)
    assert jsonld == build_jsonld(release)


def test_jsonld_is_canonical(pet_kit: Any, pet_extraction: Any) -> None:
    """FR-36: the order of the file comes from the data, not from the graph's set order."""
    scope = validate_record(ScopeRecord, pet_kit.scope)
    release = ReleaseInput(scope, pet_extraction.elements, pet_extraction.units, "raw", "raw+0")
    text = build_jsonld(release)
    assert text.endswith("}\n")
    document = json.loads(text)
    lines = text.splitlines()
    nodes = [json.loads(line.strip().rstrip(",")) for line in lines if line.startswith("    {")]
    assert nodes == document["@graph"]  # one node per line, in the order of @graph
    for line, node in zip((x for x in lines if x.startswith("    {")), nodes, strict=True):
        assert line.strip().rstrip(",") == json.dumps(node, sort_keys=True, ensure_ascii=False)
    assert document["@context"]["dai"] == "urn:domain-ai-assistant:vocab#"
    ids = [node["@id"] for node in document["@graph"]]
    assert ids == sorted(ids)
    for node in document["@graph"]:
        for value in node.values():
            if isinstance(value, list):
                keys = [json.dumps(item, sort_keys=True) for item in value]
                assert keys == sorted(keys), node["@id"]


def test_two_builds_give_the_same_jsonld(review_kit: Any) -> None:
    """FR-36: two builds of the same records give the same JSON-LD bytes."""
    _seed(review_kit)
    builds = [
        build_raw(
            review_kit.store.read(), BuildInfo(COMMIT, datetime(2026, 11, 22, hour, 0, tzinfo=UTC))
        )
        for hour in (9, 17)
    ]
    first, second = (build.files["ontology.jsonld"] for build in builds)
    assert first == second
