# Generated from schema/ontology_builder.yaml by apps/ontology-builder/tools/gen_model.py.
# Do not edit by hand; test_model_validation.py fails when this file drifts from the schema.
from __future__ import annotations

import re
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

metamodel_version = "1.12.0"
version = "0.1.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias=True,
        validate_by_name=True,
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )


class Level(StrEnum):
    """
    How important an element is for a reader of the domain (FR-13).
    """

    level_1 = "level-1"
    """
    Core knowledge every newcomer needs first.
    """
    level_2 = "level-2"
    """
    Everyday knowledge that builds on level-1.
    """
    level_3 = "level-3"
    """
    Full detail, special cases and error scenarios.
    """
    ignorable = "ignorable"
    """
    Not domain knowledge; left out of every level.
    """


class ElementStatus(StrEnum):
    """
    Review status of an element (FR-23).
    """

    proposed = "proposed"
    """
    Proposed by the LLM, not yet reviewed.
    """
    included = "included"
    """
    Accepted by a user or authored; waiting for approval.
    """
    excluded = "excluded"
    """
    Excluded by a user, with a reason.
    """
    approved = "approved"
    """
    Approved by a domain admin.
    """
    rejected = "rejected"
    """
    Rejected by a domain admin, with a reason.
    """
    deprecated = "deprecated"
    """
    Formerly approved; kept, optionally with a replacement.
    """


class ElementType(StrEnum):
    statement = "statement"
    term = "term"
    concept = "concept"
    relation = "relation"
    rule = "rule"
    property = "property"


class OriginKind(StrEnum):
    llm = "llm"
    """
    Proposed by the LLM during an ingestion run.
    """
    user = "user"
    """
    Authored by a person.
    """


class UnitKind(StrEnum):
    paragraph = "paragraph"
    list_item = "list_item"
    blockquote = "blockquote"
    table_row = "table_row"
    user_statement = "user_statement"


class IgnorableCategory(StrEnum):
    """
    Why a whole source unit is proposed as ignorable (FR-14).
    """

    instance_or_anecdote = "instance_or_anecdote"
    generic_or_historical_story = "generic_or_historical_story"
    quote_or_motivational = "quote_or_motivational"
    procedure = "procedure"
    other = "other"


class IgnorableStatus(StrEnum):
    proposed = "proposed"
    """
    Proposed by the LLM.
    """
    confirmed = "confirmed"
    """
    Confirmed by a person.
    """
    rejected = "rejected"
    """
    A person marked the unit not ignorable.
    """


class Modality(StrEnum):
    must = "must"
    must_not = "must_not"
    may = "may"


class Comparator(StrEnum):
    lt = "lt"
    """
    less than
    """
    le = "le"
    """
    at most
    """
    eq = "eq"
    """
    exactly
    """
    ge = "ge"
    """
    at least
    """
    gt = "gt"
    """
    more than
    """


class Role(StrEnum):
    user = "user"
    """
    Reviews, corrects and authors.
    """
    domain_admin = "domain_admin"
    """
    Also approves, rejects, deprecates and publishes.
    """


class DecisionAction(StrEnum):
    create = "create"
    include = "include"
    exclude = "exclude"
    correct = "correct"
    level = "level"
    merge = "merge"
    split_ = "split"
    reassign = "reassign"
    approve = "approve"
    reject = "reject"
    deprecate = "deprecate"
    author = "author"
    confirm_ignorable = "confirm_ignorable"
    not_ignorable = "not_ignorable"
    edit_scope = "edit_scope"
    publish = "publish"


class RunKind(StrEnum):
    ingestion = "ingestion"
    on_demand = "on_demand"


class RunStatus(StrEnum):
    running = "running"
    completed = "completed"
    failed = "failed"


class LevelGuidance(ConfiguredBaseModel):
    """
    What counts as level-1, level-2 and level-3 in this ontology (the rubric).
    """

    level_1: str = Field(default=...)
    level_2: str = Field(default=...)
    level_3: str = Field(default=...)

    @field_validator("level_1")
    @classmethod
    def pattern_level_1(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_1 format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_1 format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_2")
    @classmethod
    def pattern_level_2(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_2 format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_2 format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_3")
    @classmethod
    def pattern_level_3(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_3 format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_3 format: {v}"
            raise ValueError(err_msg)
        return v


class ScopeRecord(ConfiguredBaseModel):
    """
    The scope record of one ontology (FR-1); 01_model/scope.yaml.
    """

    name: str = Field(default=...)
    purpose: str = Field(default=...)
    readers: str = Field(default=..., description="""The intended readers.""")
    level_guidance: LevelGuidance = Field(default=...)
    ignorable_examples: list[str] = Field(default=..., min_length=1)
    base_iri: str = Field(default=...)

    @field_validator("name")
    @classmethod
    def pattern_name(cls, v: Any) -> Any:
        pattern = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("purpose")
    @classmethod
    def pattern_purpose(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid purpose format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid purpose format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("readers")
    @classmethod
    def pattern_readers(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid readers format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid readers format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("base_iri")
    @classmethod
    def pattern_base_iri(cls, v: Any) -> Any:
        pattern = re.compile(r"^\S+[:/#]$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid base_iri format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid base_iri format: {v}"
            raise ValueError(err_msg)
        return v


class Corpus(ConfiguredBaseModel):
    """
    One ingested folder; 00_sources/<NN>_<slug>/corpus.yaml.
    """

    id: str = Field(default=...)
    number: int = Field(default=..., ge=0, le=89)
    slug: str = Field(default=...)
    source_path: str = Field(
        default=..., description="""The ingested folder, relative to SHARED_DATA_DIR."""
    )
    ingest_run: str = Field(default=...)

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^co_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("slug")
    @classmethod
    def pattern_slug(cls, v: Any) -> Any:
        pattern = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid slug format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid slug format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("ingest_run")
    @classmethod
    def pattern_ingest_run(cls, v: Any) -> Any:
        pattern = re.compile(r"^run_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid ingest_run format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid ingest_run format: {v}"
            raise ValueError(err_msg)
        return v


class Document(ConfiguredBaseModel):
    """
    One Markdown file of a corpus; 00_sources/<NN>_<slug>/documents/<doc-id>.yaml.
    """

    id: str = Field(default=...)
    corpus_id: str = Field(default=...)
    path: str = Field(default=...)
    title: str = Field(default=...)
    content_hash: str = Field(default=...)

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^doc_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("corpus_id")
    @classmethod
    def pattern_corpus_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^co_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid corpus_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid corpus_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("content_hash")
    @classmethod
    def pattern_content_hash(cls, v: Any) -> Any:
        pattern = re.compile(r"^sha256:[0-9a-f]{64}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid content_hash format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid content_hash format: {v}"
            raise ValueError(err_msg)
        return v


class Location(ConfiguredBaseModel):
    path: str = Field(default=...)
    heading_path: list[str] | None = Field(default=None)
    index_in_section: int = Field(default=..., ge=0)
    line_start: int | None = Field(default=None, ge=1)
    line_end: int | None = Field(default=None, ge=1)


class IgnorableVerdict(ConfiguredBaseModel):
    proposed: bool = Field(default=...)
    category: IgnorableCategory = Field(default=...)
    reason: str = Field(default=...)
    status: IgnorableStatus = Field(default=...)


class Revision(ConfiguredBaseModel):
    rev: int = Field(default=..., ge=1)
    text: str = Field(default=...)
    content_hash: str = Field(default=...)
    author: str = Field(default=...)
    at: datetime = Field(default=...)

    @field_validator("content_hash")
    @classmethod
    def pattern_content_hash(cls, v: Any) -> Any:
        pattern = re.compile(r"^sha256:[0-9a-f]{64}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid content_hash format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid content_hash format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("author")
    @classmethod
    def pattern_author(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid author format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid author format: {v}"
            raise ValueError(err_msg)
        return v


class SourceUnit(ConfiguredBaseModel):
    """
    One Markdown block or user statement (contract libs/contracts/ontology/source-unit.schema.json).
    """

    id: str = Field(default=...)
    content_hash: str = Field(default=...)
    text: str = Field(default=...)
    author: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    document_id: str | None = Field(default=None)
    kind: UnitKind = Field(default=...)
    location: Location | None = Field(default=None)
    ignorable: IgnorableVerdict | None = Field(default=None)
    revisions: list[Revision] | None = Field(default=None)

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^su_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("content_hash")
    @classmethod
    def pattern_content_hash(cls, v: Any) -> Any:
        pattern = re.compile(r"^sha256:[0-9a-f]{64}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid content_hash format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid content_hash format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("author")
    @classmethod
    def pattern_author(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid author format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid author format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("document_id")
    @classmethod
    def pattern_document_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^doc_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid document_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid document_id format: {v}"
            raise ValueError(err_msg)
        return v


class Evidence(ConfiguredBaseModel):
    unit: str = Field(default=...)
    quote: str | None = Field(default=None)

    @field_validator("unit")
    @classmethod
    def pattern_unit(cls, v: Any) -> Any:
        pattern = re.compile(r"^su_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid unit format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid unit format: {v}"
            raise ValueError(err_msg)
        return v


class Origin(ConfiguredBaseModel):
    kind: OriginKind = Field(default=...)
    run_id: str | None = Field(default=None)
    author: str | None = Field(default=None)
    created_at: datetime = Field(default=...)

    @field_validator("run_id")
    @classmethod
    def pattern_run_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^run_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid run_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid run_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("author")
    @classmethod
    def pattern_author(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid author format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid author format: {v}"
            raise ValueError(err_msg)
        return v


class Cardinality(ConfiguredBaseModel):
    min: int | None = Field(default=None, ge=0)
    max: int | None = Field(default=None, ge=0)


class RuleCardinality(Cardinality):
    relation: str = Field(default=...)
    min: int | None = Field(default=None, ge=0)
    max: int | None = Field(default=None, ge=0)

    @field_validator("relation")
    @classmethod
    def pattern_relation(cls, v: Any) -> Any:
        pattern = re.compile(r"^rl_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid relation format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid relation format: {v}"
            raise ValueError(err_msg)
        return v


class Limit(ConfiguredBaseModel):
    comparator: Comparator = Field(default=...)
    value: float = Field(default=...)
    unit: str | None = Field(default=None)


class Mention(ConfiguredBaseModel):
    unit: str = Field(default=...)
    concept: str = Field(default=...)

    @field_validator("unit")
    @classmethod
    def pattern_unit(cls, v: Any) -> Any:
        pattern = re.compile(r"^su_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid unit format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid unit format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("concept")
    @classmethod
    def pattern_concept(cls, v: Any) -> Any:
        pattern = re.compile(r"^cn_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid concept format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid concept format: {v}"
            raise ValueError(err_msg)
        return v


class Element(ConfiguredBaseModel):
    """
    Slots every element type shares (01_model/elements/<type>/<id>.yaml).
    """

    id: str = Field(default=...)
    label: str = Field(default=...)
    definition: str | None = Field(default=None)
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)
    status: ElementStatus = Field(default=...)
    status_reason: str | None = Field(default=None)
    evidence: list[Evidence] = Field(
        default=...,
        description="""The source units this element comes from (FR-10, FR-22). At least one.""",
        min_length=1,
    )
    origin: Origin = Field(default=...)
    replaced_by: str | None = Field(default=None)

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("replaced_by")
    @classmethod
    def pattern_replaced_by(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid replaced_by format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid replaced_by format: {v}"
            raise ValueError(err_msg)
        return v


class Statement(Element):
    """
    An atomic claim taken from a source unit.
    """

    text: str = Field(default=...)
    approved_snapshot: Statement | None = Field(default=None)
    id: str = Field(default=...)
    label: str = Field(default=...)
    definition: str | None = Field(default=None)
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)
    status: ElementStatus = Field(default=...)
    status_reason: str | None = Field(default=None)
    evidence: list[Evidence] = Field(
        default=...,
        description="""The source units this element comes from (FR-10, FR-22). At least one.""",
        min_length=1,
    )
    origin: Origin = Field(default=...)
    replaced_by: str | None = Field(default=None)

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^st_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("replaced_by")
    @classmethod
    def pattern_replaced_by(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid replaced_by format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid replaced_by format: {v}"
            raise ValueError(err_msg)
        return v


class Term(Element):
    """
    A word; each mention resolves it to one concept (synonyms and senses, FR-11, FR-12).
    """

    mentions: list[Mention] | None = Field(default=None)
    approved_snapshot: Term | None = Field(default=None)
    id: str = Field(default=...)
    label: str = Field(default=...)
    definition: str | None = Field(default=None)
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)
    status: ElementStatus = Field(default=...)
    status_reason: str | None = Field(default=None)
    evidence: list[Evidence] = Field(
        default=...,
        description="""The source units this element comes from (FR-10, FR-22). At least one.""",
        min_length=1,
    )
    origin: Origin = Field(default=...)
    replaced_by: str | None = Field(default=None)

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^tm_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("replaced_by")
    @classmethod
    def pattern_replaced_by(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid replaced_by format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid replaced_by format: {v}"
            raise ValueError(err_msg)
        return v


class Concept(Element):
    parents: list[str] | None = Field(
        default=None, description="""Is-a links to broader concepts."""
    )
    scope_note: str | None = Field(
        default=None, description="""Separates this sense from other senses of the same term."""
    )
    approved_snapshot: Concept | None = Field(default=None)
    id: str = Field(default=...)
    label: str = Field(default=...)
    definition: str | None = Field(default=None)
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)
    status: ElementStatus = Field(default=...)
    status_reason: str | None = Field(default=None)
    evidence: list[Evidence] = Field(
        default=...,
        description="""The source units this element comes from (FR-10, FR-22). At least one.""",
        min_length=1,
    )
    origin: Origin = Field(default=...)
    replaced_by: str | None = Field(default=None)

    @field_validator("parents")
    @classmethod
    def pattern_parents(cls, v: Any) -> Any:
        pattern = re.compile(r"^cn_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid parents format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid parents format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^cn_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("replaced_by")
    @classmethod
    def pattern_replaced_by(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid replaced_by format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid replaced_by format: {v}"
            raise ValueError(err_msg)
        return v


class Relation(Element):
    subject: str = Field(default=...)
    object: str = Field(default=...)
    predicate_label: str = Field(default=...)
    cardinality: Cardinality | None = Field(default=None)
    approved_snapshot: Relation | None = Field(default=None)
    id: str = Field(default=...)
    label: str = Field(default=...)
    definition: str | None = Field(default=None)
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)
    status: ElementStatus = Field(default=...)
    status_reason: str | None = Field(default=None)
    evidence: list[Evidence] = Field(
        default=...,
        description="""The source units this element comes from (FR-10, FR-22). At least one.""",
        min_length=1,
    )
    origin: Origin = Field(default=...)
    replaced_by: str | None = Field(default=None)

    @field_validator("subject")
    @classmethod
    def pattern_subject(cls, v: Any) -> Any:
        pattern = re.compile(r"^cn_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid subject format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid subject format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("object")
    @classmethod
    def pattern_object(cls, v: Any) -> Any:
        pattern = re.compile(r"^cn_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid object format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid object format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("predicate_label")
    @classmethod
    def pattern_predicate_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid predicate_label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid predicate_label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^rl_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("replaced_by")
    @classmethod
    def pattern_replaced_by(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid replaced_by format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid replaced_by format: {v}"
            raise ValueError(err_msg)
        return v


class Rule(Element):
    """
    Who must or must not do what, under which condition, with any limit.
    """

    modality: Modality = Field(default=...)
    actor: str = Field(default=...)
    action: str = Field(default=...)
    condition: str | None = Field(default=None)
    limit: Limit | None = Field(default=None)
    cardinality: RuleCardinality | None = Field(default=None)
    scope: list[str] | None = Field(
        default=None,
        description="""The corpora or documents the rule applies to; empty means everywhere.""",
    )
    refers_to: list[str] | None = Field(default=None)
    approved_snapshot: Rule | None = Field(default=None)
    id: str = Field(default=...)
    label: str = Field(default=...)
    definition: str | None = Field(default=None)
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)
    status: ElementStatus = Field(default=...)
    status_reason: str | None = Field(default=None)
    evidence: list[Evidence] = Field(
        default=...,
        description="""The source units this element comes from (FR-10, FR-22). At least one.""",
        min_length=1,
    )
    origin: Origin = Field(default=...)
    replaced_by: str | None = Field(default=None)

    @field_validator("actor")
    @classmethod
    def pattern_actor(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid actor format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid actor format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("action")
    @classmethod
    def pattern_action(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid action format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid action format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("scope")
    @classmethod
    def pattern_scope(cls, v: Any) -> Any:
        pattern = re.compile(r"^(co|doc)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid scope format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid scope format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("refers_to")
    @classmethod
    def pattern_refers_to(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid refers_to format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid refers_to format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^ru_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("replaced_by")
    @classmethod
    def pattern_replaced_by(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid replaced_by format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid replaced_by format: {v}"
            raise ValueError(err_msg)
        return v


class Property(Element):
    """
    A property of another element (e.g. a lifespan of a concept).
    """

    of: str = Field(default=...)
    name: str = Field(default=...)
    value: str = Field(default=...)
    unit: str | None = Field(default=None)
    approved_snapshot: Property | None = Field(default=None)
    id: str = Field(default=...)
    label: str = Field(default=...)
    definition: str | None = Field(default=None)
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)
    status: ElementStatus = Field(default=...)
    status_reason: str | None = Field(default=None)
    evidence: list[Evidence] = Field(
        default=...,
        description="""The source units this element comes from (FR-10, FR-22). At least one.""",
        min_length=1,
    )
    origin: Origin = Field(default=...)
    replaced_by: str | None = Field(default=None)

    @field_validator("of")
    @classmethod
    def pattern_of(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid of format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid of format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("name")
    @classmethod
    def pattern_name(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^pr_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("replaced_by")
    @classmethod
    def pattern_replaced_by(cls, v: Any) -> Any:
        pattern = re.compile(r"^(st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid replaced_by format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid replaced_by format: {v}"
            raise ValueError(err_msg)
        return v


class Decision(ConfiguredBaseModel):
    """
    One recorded decision; a line of 02_decisions/YYYY-MM-DD.jsonl (FR-26).
    """

    id: str = Field(default=...)
    at: datetime = Field(default=...)
    user: str = Field(default=...)
    role: Role = Field(default=...)
    action: DecisionAction = Field(default=...)
    element_id: str | None = Field(default=None)
    field: str | None = Field(default=None)
    old: Any | None = Field(default=None)
    new: Any | None = Field(default=None)
    reason: str | None = Field(default=None)

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^dc_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("user")
    @classmethod
    def pattern_user(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid user format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid user format: {v}"
            raise ValueError(err_msg)
        return v


class Estimate(ConfiguredBaseModel):
    documents: int = Field(default=..., ge=0)
    units: int = Field(default=..., ge=0)
    input_tokens: int = Field(default=..., ge=0)
    output_tokens: int = Field(default=..., ge=0)
    cost_usd: float | None = Field(default=None, ge=0)


class SkippedItem(ConfiguredBaseModel):
    where: str = Field(default=..., description="""The batch or document the item came from.""")
    item: str = Field(default=..., description="""The item as returned, shortened.""")
    reason: str = Field(default=...)


class Run(ConfiguredBaseModel):
    """
    One ingestion or on-demand extraction; 02_decisions/runs/<run-id>.yaml (FR-6).
    """

    id: str = Field(default=...)
    kind: RunKind = Field(default=...)
    user: str = Field(default=...)
    model: str = Field(default=...)
    source_path: str | None = Field(default=None)
    started_at: datetime = Field(default=...)
    ended_at: datetime | None = Field(default=None)
    status: RunStatus = Field(default=...)
    estimate: Estimate | None = Field(default=None)
    input_tokens: int = Field(default=..., ge=0)
    output_tokens: int = Field(default=..., ge=0)
    skipped: list[SkippedItem] | None = Field(default=None)

    @field_validator("id")
    @classmethod
    def pattern_id(cls, v: Any) -> Any:
        pattern = re.compile(r"^run_[0-9A-HJKMNP-TV-Z]{26}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("user")
    @classmethod
    def pattern_user(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid user format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid user format: {v}"
            raise ValueError(err_msg)
        return v


class Candidate(ConfiguredBaseModel):
    key: str = Field(default=..., description="""Local key, unique in one response.""")
    label: str = Field(default=...)
    evidence: list[str] = Field(
        default=...,
        description="""Aliases (U1, U2, ...) of the source units the candidate comes from.""",
        min_length=1,
    )
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)

    @field_validator("key")
    @classmethod
    def pattern_key(cls, v: Any) -> Any:
        pattern = re.compile(r"^[A-Za-z0-9_.:-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid key format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid key format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("evidence")
    @classmethod
    def pattern_evidence(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid evidence format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid evidence format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v


class UnitVerdict(ConfiguredBaseModel):
    unit: str = Field(default=...)
    ignorable: bool = Field(default=...)
    category: IgnorableCategory | None = Field(
        default=None, description="""Required when ignorable is true."""
    )
    reason: str | None = Field(default=None)

    @field_validator("unit")
    @classmethod
    def pattern_unit(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid unit format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid unit format: {v}"
            raise ValueError(err_msg)
        return v


class CandidateStatement(Candidate):
    text: str = Field(default=...)
    key: str = Field(default=..., description="""Local key, unique in one response.""")
    label: str = Field(default=...)
    evidence: list[str] = Field(
        default=...,
        description="""Aliases (U1, U2, ...) of the source units the candidate comes from.""",
        min_length=1,
    )
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)

    @field_validator("key")
    @classmethod
    def pattern_key(cls, v: Any) -> Any:
        pattern = re.compile(r"^[A-Za-z0-9_.:-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid key format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid key format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("evidence")
    @classmethod
    def pattern_evidence(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid evidence format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid evidence format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v


class CandidateMention(ConfiguredBaseModel):
    unit: str = Field(default=...)
    concept: str = Field(
        default=..., description="""Key of the candidate concept this mention names."""
    )

    @field_validator("unit")
    @classmethod
    def pattern_unit(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid unit format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid unit format: {v}"
            raise ValueError(err_msg)
        return v


class CandidateTerm(Candidate):
    mentions: list[CandidateMention] | None = Field(default=None)
    key: str = Field(default=..., description="""Local key, unique in one response.""")
    label: str = Field(default=...)
    evidence: list[str] = Field(
        default=...,
        description="""Aliases (U1, U2, ...) of the source units the candidate comes from.""",
        min_length=1,
    )
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)

    @field_validator("key")
    @classmethod
    def pattern_key(cls, v: Any) -> Any:
        pattern = re.compile(r"^[A-Za-z0-9_.:-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid key format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid key format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("evidence")
    @classmethod
    def pattern_evidence(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid evidence format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid evidence format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v


class CandidateConcept(Candidate):
    definition: str | None = Field(default=None)
    parents: list[str] | None = Field(
        default=None, description="""Keys of broader candidate concepts."""
    )
    key: str = Field(default=..., description="""Local key, unique in one response.""")
    label: str = Field(default=...)
    evidence: list[str] = Field(
        default=...,
        description="""Aliases (U1, U2, ...) of the source units the candidate comes from.""",
        min_length=1,
    )
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)

    @field_validator("key")
    @classmethod
    def pattern_key(cls, v: Any) -> Any:
        pattern = re.compile(r"^[A-Za-z0-9_.:-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid key format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid key format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("evidence")
    @classmethod
    def pattern_evidence(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid evidence format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid evidence format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v


class CandidateRelation(Candidate):
    subject: str = Field(default=..., description="""Key of a candidate concept.""")
    object: str = Field(default=..., description="""Key of a candidate concept.""")
    cardinality: Cardinality | None = Field(default=None)
    key: str = Field(default=..., description="""Local key, unique in one response.""")
    label: str = Field(default=...)
    evidence: list[str] = Field(
        default=...,
        description="""Aliases (U1, U2, ...) of the source units the candidate comes from.""",
        min_length=1,
    )
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)

    @field_validator("key")
    @classmethod
    def pattern_key(cls, v: Any) -> Any:
        pattern = re.compile(r"^[A-Za-z0-9_.:-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid key format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid key format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("evidence")
    @classmethod
    def pattern_evidence(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid evidence format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid evidence format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v


class CandidateRuleCardinality(Cardinality):
    relation: str = Field(default=..., description="""Key of a candidate relation.""")
    min: int | None = Field(default=None, ge=0)
    max: int | None = Field(default=None, ge=0)


class CandidateRule(Candidate):
    modality: Modality = Field(default=...)
    actor: str = Field(default=...)
    action: str = Field(default=...)
    condition: str | None = Field(default=None)
    limit: Limit | None = Field(default=None)
    cardinality: CandidateRuleCardinality | None = Field(default=None)
    refers_to: list[str] | None = Field(
        default=None, description="""Keys of the candidates the rule refers to."""
    )
    key: str = Field(default=..., description="""Local key, unique in one response.""")
    label: str = Field(default=...)
    evidence: list[str] = Field(
        default=...,
        description="""Aliases (U1, U2, ...) of the source units the candidate comes from.""",
        min_length=1,
    )
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)

    @field_validator("key")
    @classmethod
    def pattern_key(cls, v: Any) -> Any:
        pattern = re.compile(r"^[A-Za-z0-9_.:-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid key format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid key format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("evidence")
    @classmethod
    def pattern_evidence(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid evidence format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid evidence format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v


class CandidateProperty(Candidate):
    of: str = Field(default=..., description="""Key of the candidate the property belongs to.""")
    name: str = Field(default=...)
    value: str = Field(default=...)
    unit: str | None = Field(default=None)
    key: str = Field(default=..., description="""Local key, unique in one response.""")
    label: str = Field(default=...)
    evidence: list[str] = Field(
        default=...,
        description="""Aliases (U1, U2, ...) of the source units the candidate comes from.""",
        min_length=1,
    )
    level: Level = Field(default=...)
    level_reason: str = Field(default=...)

    @field_validator("key")
    @classmethod
    def pattern_key(cls, v: Any) -> Any:
        pattern = re.compile(r"^[A-Za-z0-9_.:-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid key format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid key format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("label")
    @classmethod
    def pattern_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("evidence")
    @classmethod
    def pattern_evidence(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid evidence format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid evidence format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("level_reason")
    @classmethod
    def pattern_level_reason(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid level_reason format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid level_reason format: {v}"
            raise ValueError(err_msg)
        return v


class ExtractionOutput(ConfiguredBaseModel):
    """
    The whole pass 1 answer for one document (calls A and B merged).
    """

    unit_verdicts: list[UnitVerdict] = Field(default=...)
    statements: list[CandidateStatement] | None = Field(default=None)
    terms: list[CandidateTerm] | None = Field(default=None)
    concepts: list[CandidateConcept] | None = Field(default=None)
    relations: list[CandidateRelation] | None = Field(default=None)
    rules: list[CandidateRule] | None = Field(default=None)
    properties: list[CandidateProperty] | None = Field(default=None)


class SynonymGroup(ConfiguredBaseModel):
    """
    Several terms that name one concept (FR-11).
    """

    concept: str = Field(
        default=...,
        description="""Alias (C1, C2, ...) of the concept, as shown in the pass 2 prompt.""",
    )
    preferred_label: str = Field(default=...)
    terms: list[str] = Field(default=..., description="""Term labels.""", min_length=1)
    merge: list[str] | None = Field(
        default=None,
        description="""Aliases of new concepts that are the same thing; merged into concept.""",
    )

    @field_validator("concept")
    @classmethod
    def pattern_concept(cls, v: Any) -> Any:
        pattern = re.compile(r"^C[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid concept format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid concept format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("preferred_label")
    @classmethod
    def pattern_preferred_label(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid preferred_label format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid preferred_label format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("merge")
    @classmethod
    def pattern_merge(cls, v: Any) -> Any:
        pattern = re.compile(r"^C[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid merge format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid merge format: {v}"
            raise ValueError(err_msg)
        return v


class Sense(ConfiguredBaseModel):
    concept: str = Field(
        default=..., description="""Alias (C1, C2, ...) of the concept this sense names."""
    )
    scope_note: str = Field(default=...)
    mentions: list[str] = Field(
        default=...,
        description="""Aliases of the units where the term has this sense.""",
        min_length=1,
    )

    @field_validator("concept")
    @classmethod
    def pattern_concept(cls, v: Any) -> Any:
        pattern = re.compile(r"^C[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid concept format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid concept format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("scope_note")
    @classmethod
    def pattern_scope_note(cls, v: Any) -> Any:
        pattern = re.compile(r"\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid scope_note format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid scope_note format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator("mentions")
    @classmethod
    def pattern_mentions(cls, v: Any) -> Any:
        pattern = re.compile(r"^U[1-9][0-9]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid mentions format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid mentions format: {v}"
            raise ValueError(err_msg)
        return v


class SenseSplit(ConfiguredBaseModel):
    """
    One term that names different concepts in different places (FR-12).
    """

    term: str = Field(default=..., description="""The term label.""")
    senses: list[Sense] = Field(default=..., min_length=2)


class TermResolutionOutput(ConfiguredBaseModel):
    """
    Pass 2 output for one ingestion (its JSON schema is the structured-output format).
    """

    synonym_groups: list[SynonymGroup] | None = Field(default=None)
    sense_splits: list[SenseSplit] | None = Field(default=None)


class ConceptsOutput(ConfiguredBaseModel):
    """
    Pass 1, call A for one document; unit verdicts and the concept-side candidates.
    """

    unit_verdicts: list[UnitVerdict] = Field(default=...)
    statements: list[CandidateStatement] | None = Field(default=None)
    terms: list[CandidateTerm] | None = Field(default=None)
    concepts: list[CandidateConcept] | None = Field(default=None)
    relations: list[CandidateRelation] | None = Field(default=None)


class RulesOutput(ConfiguredBaseModel):
    """
    Pass 1, call B for one document; rules and properties.
    """

    rules: list[CandidateRule] | None = Field(default=None)
    properties: list[CandidateProperty] | None = Field(default=None)


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
LevelGuidance.model_rebuild()
ScopeRecord.model_rebuild()
Corpus.model_rebuild()
Document.model_rebuild()
Location.model_rebuild()
IgnorableVerdict.model_rebuild()
Revision.model_rebuild()
SourceUnit.model_rebuild()
Evidence.model_rebuild()
Origin.model_rebuild()
Cardinality.model_rebuild()
RuleCardinality.model_rebuild()
Limit.model_rebuild()
Mention.model_rebuild()
Element.model_rebuild()
Statement.model_rebuild()
Term.model_rebuild()
Concept.model_rebuild()
Relation.model_rebuild()
Rule.model_rebuild()
Property.model_rebuild()
Decision.model_rebuild()
Estimate.model_rebuild()
SkippedItem.model_rebuild()
Run.model_rebuild()
Candidate.model_rebuild()
UnitVerdict.model_rebuild()
CandidateStatement.model_rebuild()
CandidateMention.model_rebuild()
CandidateTerm.model_rebuild()
CandidateConcept.model_rebuild()
CandidateRelation.model_rebuild()
CandidateRuleCardinality.model_rebuild()
CandidateRule.model_rebuild()
CandidateProperty.model_rebuild()
ExtractionOutput.model_rebuild()
SynonymGroup.model_rebuild()
Sense.model_rebuild()
SenseSplit.model_rebuild()
TermResolutionOutput.model_rebuild()
ConceptsOutput.model_rebuild()
RulesOutput.model_rebuild()
