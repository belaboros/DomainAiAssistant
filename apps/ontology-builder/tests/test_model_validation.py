"""Every record is validated against the LinkML-generated model (plan 0002, T3: AC-9, AC-12)."""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from ontology_builder.model import (
    ELEMENT_TYPES,
    Concept,
    ConceptsOutput,
    ExtractionOutput,
    RecordInvalidError,
    RulesOutput,
    ScopeRecord,
    SourceUnit,
    TermResolutionOutput,
    tool_input_schema,
    validate_element,
    validate_record,
)

APP = Path(__file__).resolve().parents[1]
CONTRACT = APP.parents[1] / "libs" / "contracts" / "ontology"
ElementFactory = Callable[[str], dict[str, Any]]
UNIT = "su_01JDK7F3Q8ZX5N6M2W4R9T0BCD"
ALIAS = "U1"  # the LLM cites units by their prompt alias (Q38)


def test_generated_models_match_the_schema() -> None:
    """The committed _generated.py is exactly what the generator makes from the schema."""
    result = subprocess.run(  # noqa: S603 - the app's own generator, fixed arguments
        [sys.executable, str(APP / "tools" / "gen_model.py"), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_element_types_are_the_six_of_the_spec() -> None:
    assert sorted(ELEMENT_TYPES) == [
        "concept", "property", "relation", "rule", "statement", "term",
    ]  # fmt: skip


@pytest.mark.parametrize("element_type", sorted(ELEMENT_TYPES))
def test_valid_record_of_each_type_validates(
    element_type: str, make_element: ElementFactory
) -> None:
    element = validate_element(element_type, make_element(element_type))
    assert isinstance(element, ELEMENT_TYPES[element_type])
    assert element.evidence[0].unit == UNIT


@pytest.mark.parametrize("element_type", sorted(ELEMENT_TYPES))
@pytest.mark.parametrize("evidence", [None, []])
def test_record_without_evidence_is_invalid(
    element_type: str, evidence: list[Any] | None, make_element: ElementFactory
) -> None:
    record = make_element(element_type)
    if evidence is None:
        del record["evidence"]
    else:
        record["evidence"] = evidence
    with pytest.raises(RecordInvalidError, match="evidence"):
        validate_element(element_type, record)


@pytest.mark.parametrize("element_type", sorted(ELEMENT_TYPES))
@pytest.mark.parametrize("field", ["level", "level_reason"])
def test_every_element_has_level_and_reason(
    element_type: str, field: str, make_element: ElementFactory
) -> None:
    record = make_element(element_type)
    del record[field]
    with pytest.raises(RecordInvalidError, match=field):
        validate_element(element_type, record)
    record[field] = "   " if field == "level_reason" else None
    with pytest.raises(RecordInvalidError, match=field):
        validate_element(element_type, record)


@pytest.mark.parametrize("level", ["level-1", "level-2", "level-3", "ignorable"])
def test_the_four_levels_are_valid(level: str, make_element: ElementFactory) -> None:
    assert validate_element("concept", make_element("concept") | {"level": level}).level == level


@pytest.mark.parametrize("level", ["level-4", "important", "Level-1", ""])
def test_unknown_level_is_invalid(level: str, make_element: ElementFactory) -> None:
    with pytest.raises(RecordInvalidError, match="level"):
        validate_element("concept", make_element("concept") | {"level": level})


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", "cn_leash"),  # not a ULID
        ("id", "tm_01JDK7F3Q8ZX5N6M2W4R9T0BCD"),  # a term ID on a concept
        ("status", "accepted"),
        ("parents", ["leash"]),
        ("evidence", [{"unit": "su_dog-06-0"}]),
        ("origin", {"kind": "magic", "created_at": "2026-11-21T10:00:00Z"}),
        ("unknown_field", "x"),  # typos never pass silently
    ],
)
def test_bad_values_are_invalid(field: str, value: Any, make_element: ElementFactory) -> None:
    with pytest.raises(RecordInvalidError):
        validate_element("concept", make_element("concept") | {field: value})


def test_error_names_the_record_and_every_problem(make_element: ElementFactory) -> None:
    record = make_element("concept") | {"level": "level-9", "evidence": []}
    with pytest.raises(RecordInvalidError) as caught:
        validate_element("concept", record)
    assert "Concept" in str(caught.value)
    assert {p.split(":")[0] for p in caught.value.problems} >= {"level", "evidence"}


def test_unknown_element_type_is_refused(make_element: ElementFactory) -> None:
    with pytest.raises(RecordInvalidError, match="element type"):
        validate_element("axiom", make_element("concept"))


def test_approved_snapshot_is_validated_as_the_same_type(make_element: ElementFactory) -> None:
    snapshot = make_element("concept") | {"status": "approved"}
    record = make_element("concept") | {"status": "included", "approved_snapshot": snapshot}
    concept = validate_record(Concept, record)
    assert isinstance(concept.approved_snapshot, Concept)
    snapshot["evidence"] = []
    with pytest.raises(RecordInvalidError, match="evidence"):
        validate_record(Concept, record)


def test_scope_record_validates_and_refuses_empty_fields(scope_record: dict[str, Any]) -> None:
    assert validate_record(ScopeRecord, scope_record).name == "pets-and-house-rules"
    with pytest.raises(RecordInvalidError, match="purpose"):
        validate_record(ScopeRecord, scope_record | {"purpose": " "})
    with pytest.raises(RecordInvalidError, match="name"):
        validate_record(ScopeRecord, scope_record | {"name": "Pets_And_Rules"})


def test_source_unit_model_agrees_with_the_contract_schema(corpus_unit: dict[str, Any]) -> None:
    """What the model accepts and dumps, the shared contract accepts too."""
    unit = validate_record(SourceUnit, corpus_unit)
    contract = json.loads((CONTRACT / "source-unit.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(contract).validate(unit.model_dump(mode="json", exclude_none=True))
    with pytest.raises(RecordInvalidError):
        validate_record(SourceUnit, corpus_unit | {"kind": "sentence"})


def _extraction_output() -> dict[str, Any]:
    candidate = {"evidence": [ALIAS], "level": "level-1", "level_reason": "core"}
    return {
        "unit_verdicts": [{"unit": ALIAS, "ignorable": False}],
        "statements": [{"key": "s1", "label": "lead rule", "text": "x", **candidate}],
        "terms": [
            {"key": "t1", "label": "lead", "mentions": [{"unit": ALIAS, "concept": "c1"}]}
            | candidate
        ],
        "concepts": [{"key": "c1", "label": "leash", **candidate}],
        "relations": [{"key": "r1", "label": "keeps", "subject": "c1", "object": "c1"} | candidate],
        "rules": [
            {
                "key": "u1",
                "label": "lead in stairwell",
                "modality": "must",
                "actor": "owner",
                "action": "use a lead",
                "limit": {"comparator": "le", "value": 2, "unit": "m"},
                "refers_to": ["c1"],
            }
            | candidate
        ],
        "properties": [
            {"key": "p1", "label": "length", "of": "c1", "name": "n", "value": "2"} | candidate
        ],
    }


@pytest.mark.parametrize(
    "output", [ExtractionOutput, ConceptsOutput, RulesOutput, TermResolutionOutput]
)
def test_tool_input_schema_is_a_json_object_schema(output: type[Any]) -> None:
    schema = tool_input_schema(output)
    Draft202012Validator.check_schema(schema)
    assert schema["type"] == "object"
    again = tool_input_schema(output)
    assert json.dumps(schema, sort_keys=True) == json.dumps(again, sort_keys=True)


def test_llm_output_validates_against_model_and_tool_schema() -> None:
    output = _extraction_output()
    Draft202012Validator(tool_input_schema(ExtractionOutput)).validate(output)
    parsed = validate_record(ExtractionOutput, output)
    assert parsed.rules is not None
    assert parsed.rules[0].limit is not None
    assert parsed.rules[0].limit.value == 2.0
    output["concepts"][0]["evidence"] = []
    with pytest.raises(RecordInvalidError, match="evidence"):
        validate_record(ExtractionOutput, output)
    output["concepts"][0]["evidence"] = [UNIT]
    with pytest.raises(RecordInvalidError, match="evidence"):
        validate_record(ExtractionOutput, output)


def test_every_element_has_level_and_reason_on_pet_fixtures(pet_extraction: Any) -> None:
    """AC-12 on the curated pet fixtures: one of the four levels and a reason, and valid records."""
    assert pet_extraction.elements
    for element in pet_extraction.elements:
        assert element.level in {"level-1", "level-2", "level-3", "ignorable"}
        assert element.level_reason.strip()
        element_type = type(element).__name__.lower()
        validate_element(element_type, element.model_dump(mode="json", exclude_none=True))
