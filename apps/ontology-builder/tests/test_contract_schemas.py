"""The shared ontology contract is machine-readable and self-consistent (plan 0002, T2)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDF

REPO = Path(__file__).resolve().parents[3]
CONTRACT = REPO / "libs" / "contracts" / "ontology"
DAI = Namespace("urn:domain-ai-assistant:vocab#")
ULID = "01JDK7F3Q8ZX5N6M2W4R9T0BCD"
HASH = "sha256:" + "a" * 64


def _schema(name: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads((CONTRACT / name).read_text(encoding="utf-8"))
    return data


@pytest.mark.parametrize("name", ["source-unit.schema.json", "manifest.schema.json"])
def test_schema_is_valid_draft_2020_12(name: str) -> None:
    schema = _schema(name)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    Draft202012Validator.check_schema(schema)


def _corpus_unit() -> dict[str, Any]:
    return {
        "id": f"su_{ULID}",
        "document_id": f"doc_{ULID}",
        "kind": "paragraph",
        "location": {"path": "dog/06.md", "heading_path": ["6 Walking"], "index_in_section": 0},
        "content_hash": HASH,
        "text": "Keep the dog on a lead of at most 2 m in the stairwell.",
    }


def test_source_unit_schema_accepts_corpus_unit_and_user_statement() -> None:
    validator = Draft202012Validator(_schema("source-unit.schema.json"))
    validator.validate(_corpus_unit())
    rev = {
        "rev": 1,
        "text": "x",
        "content_hash": HASH,
        "author": "alice",
        "at": "2026-11-21T10:00:00Z",
    }
    statement = {
        "id": f"su_{ULID}",
        "kind": "user_statement",
        "content_hash": HASH,
        "text": "x",
        "author": "alice",
        "created_at": "2026-11-21T10:00:00Z",
        "revisions": [rev],
    }
    validator.validate(statement)


@pytest.mark.parametrize(
    ("field", "value"),
    [("id", "su_dog-06-0"), ("content_hash", "md5:abc"), ("kind", "sentence")],
)
def test_source_unit_schema_rejects_bad_values(field: str, value: str) -> None:
    unit = _corpus_unit() | {field: value}
    with pytest.raises(ValidationError):
        Draft202012Validator(_schema("source-unit.schema.json")).validate(unit)


def test_corpus_unit_needs_document_and_location() -> None:
    unit = _corpus_unit()
    del unit["location"]
    with pytest.raises(ValidationError):
        Draft202012Validator(_schema("source-unit.schema.json")).validate(unit)


def _manifest(variant: str, version: str) -> dict[str, Any]:
    files = {name: HASH for name in ["ontology.ttl", "level-1.md", "level-2.md", "level-3.md"]}
    return {
        "ontology": "pets-and-house-rules",
        "variant": variant,
        "version": version,
        "built_at": "2026-11-21T10:00:00Z",
        "source_commit": "55fe603",
        "counts": {"by_type": {"concept": 3}, "by_status": {"approved": 3}, "by_level": {}},
        "files": files,
    }


def test_manifest_schema_raw_and_governed() -> None:
    validator = Draft202012Validator(_schema("manifest.schema.json"))
    validator.validate(_manifest("raw", "raw+55fe603"))
    governed = _manifest("governed", "1.0.0")
    with pytest.raises(ValidationError):  # a governed release has a change log
        validator.validate(governed)
    governed["files"]["CHANGELOG.md"] = HASH
    validator.validate(governed)
    with pytest.raises(ValidationError):  # and a semantic version
        validator.validate(governed | {"version": "raw+55fe603"})


def test_vocab_parses_and_declares_the_terms_the_contract_uses() -> None:
    graph = Graph().parse(CONTRACT / "vocab.ttl", format="turtle")
    for term in ["level", "status", "evidence", "modality", "limitValue", "refersTo"]:
        assert (DAI[term], RDF.type, OWL.AnnotationProperty) in graph, term
    for value in ["level-1", "level-2", "level-3"]:
        assert (DAI[value], RDF.type, DAI.Level) in graph
    for status in ["proposed", "included", "approved", "deprecated"]:
        assert (DAI[status], RDF.type, DAI.Status) in graph
    readme = (CONTRACT / "README.md").read_text(encoding="utf-8")
    assert "0.1.0" in readme
