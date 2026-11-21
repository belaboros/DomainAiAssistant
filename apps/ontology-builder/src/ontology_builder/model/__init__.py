"""model component.

Defines the LinkML schema of every record and validates records against it.

The schema is ``schema/ontology_builder.yaml``; the Pydantic classes are generated from it into
``_generated.py`` (never edited by hand). Every record is validated with ``validate_record`` or
``validate_element`` before it is written (plan 0002, NFR validity).
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from ontology_builder.model._generated import (
    Candidate,
    CandidateConcept,
    CandidateMention,
    CandidateProperty,
    CandidateRelation,
    CandidateRule,
    CandidateRuleCardinality,
    CandidateStatement,
    CandidateTerm,
    Cardinality,
    Comparator,
    Concept,
    ConceptsOutput,
    Corpus,
    Decision,
    DecisionAction,
    Document,
    Element,
    ElementStatus,
    ElementType,
    Estimate,
    Evidence,
    ExtractionOutput,
    IgnorableCategory,
    IgnorableStatus,
    IgnorableVerdict,
    Level,
    LevelGuidance,
    Limit,
    Location,
    Mention,
    Modality,
    Origin,
    OriginKind,
    Property,
    Relation,
    Revision,
    Role,
    Rule,
    RuleCardinality,
    RulesOutput,
    Run,
    RunKind,
    RunStatus,
    ScopeRecord,
    Sense,
    SenseSplit,
    SkippedItem,
    SourceUnit,
    Statement,
    SynonymGroup,
    Term,
    TermResolutionOutput,
    UnitKind,
    UnitVerdict,
)
from ontology_builder.model.ids import ID_PREFIXES, Clock, FixedClock, SystemClock, UlidMinter
from ontology_builder.model.text import content_hash, normalise

SCHEMA_PATH = Path(__file__).parent / "schema" / "ontology_builder.yaml"

ELEMENT_TYPES: dict[str, type[Element]] = {
    "statement": Statement,
    "term": Term,
    "concept": Concept,
    "relation": Relation,
    "rule": Rule,
    "property": Property,
}
"""Element type name (as in ``01_model/elements/<type>/``) to its record class."""


class RecordInvalidError(ValueError):
    """A record does not conform to the schema; ``problems`` lists each finding."""

    def __init__(self, record_class: str, problems: list[str]) -> None:
        self.record_class = record_class
        self.problems = problems
        super().__init__(f"invalid {record_class} record: " + "; ".join(problems))


def _problems(error: ValidationError) -> list[str]:
    found = []
    for item in error.errors():
        where = ".".join(str(part) for part in item["loc"]) or "(record)"
        found.append(f"{where}: {item['msg']}")
    return found


def validate_record[M: BaseModel](record_class: type[M], data: Mapping[str, Any]) -> M:
    """Validate ``data`` against ``record_class`` and return the record, or raise."""
    try:
        return record_class.model_validate(dict(data))
    except ValidationError as error:
        raise RecordInvalidError(record_class.__name__, _problems(error)) from None


def validate_element(element_type: str, data: Mapping[str, Any]) -> Element:
    """Validate an element record of the given type (``concept``, ``rule``, ...)."""
    record_class = ELEMENT_TYPES.get(element_type)
    if record_class is None:
        raise RecordInvalidError("Element", [f"unknown element type {element_type!r}"])
    return validate_record(record_class, data)


def tool_input_schema(output_class: type[BaseModel]) -> dict[str, Any]:
    """The JSON Schema of an LLM output class, sent as the structured-output schema (ADR-0006)."""
    return output_class.model_json_schema(mode="validation")


__all__ = [
    "ELEMENT_TYPES",
    "ID_PREFIXES",
    "SCHEMA_PATH",
    "Candidate",
    "CandidateConcept",
    "CandidateMention",
    "CandidateProperty",
    "CandidateRelation",
    "CandidateRule",
    "CandidateRuleCardinality",
    "CandidateStatement",
    "CandidateTerm",
    "Cardinality",
    "Clock",
    "Comparator",
    "Concept",
    "ConceptsOutput",
    "Corpus",
    "Decision",
    "DecisionAction",
    "Document",
    "Element",
    "ElementStatus",
    "ElementType",
    "Estimate",
    "Evidence",
    "ExtractionOutput",
    "FixedClock",
    "IgnorableCategory",
    "IgnorableStatus",
    "IgnorableVerdict",
    "Level",
    "LevelGuidance",
    "Limit",
    "Location",
    "Mention",
    "Modality",
    "Origin",
    "OriginKind",
    "Property",
    "RecordInvalidError",
    "Relation",
    "Revision",
    "Role",
    "Rule",
    "RuleCardinality",
    "RulesOutput",
    "Run",
    "RunKind",
    "RunStatus",
    "ScopeRecord",
    "Sense",
    "SenseSplit",
    "SkippedItem",
    "SourceUnit",
    "Statement",
    "SynonymGroup",
    "SystemClock",
    "Term",
    "TermResolutionOutput",
    "UlidMinter",
    "UnitKind",
    "UnitVerdict",
    "content_hash",
    "normalise",
    "tool_input_schema",
    "validate_element",
    "validate_record",
]
