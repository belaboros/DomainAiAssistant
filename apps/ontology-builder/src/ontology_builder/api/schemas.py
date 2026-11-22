"""Request and response bodies of the HTTP API; the OpenAPI schema (and so the generated
TypeScript client) is made from these."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ontology_builder.model import (
    ElementStatus,
    IgnorableCategory,
    IgnorableStatus,
    Level,
    Role,
    RunKind,
    RunStatus,
    UnitKind,
)

ActionName = Literal[
    "include",
    "exclude",
    "approve",
    "reject",
    "deprecate",
    "level",
    "correct",
    "merge",
    "split",
    "reassign",
]
ElementTypeName = Literal["statement", "term", "concept", "relation", "rule", "property"]


class SignIn(BaseModel):
    user: str = Field(min_length=1, max_length=64, pattern=r"\S")
    """A handle, not a real name or email address: the dataset is public (FR-2)."""
    role: Role


class SessionOut(BaseModel):
    user: str
    role: Role
    writer: bool
    """False for a second browser session: it may read but not change anything."""
    ontology: str
    """The ontology this server opened; the review routes address it by this name."""
    warning: str | None = None


class Done(BaseModel):
    ok: bool = True


class CreateOntology(BaseModel):
    name: str
    scope: dict[str, Any]


class ElementFilter(BaseModel):
    """The filters of FR-19; each is exact, but ``q`` (full text, case-insensitive)."""

    type: ElementTypeName | None = None
    status: str | None = None
    level: str | None = None
    corpus: str | None = None
    document: str | None = None
    q: str | None = None


class IndexEntryOut(BaseModel):
    """One element in the compact index the GUI filters (FR-19)."""

    id: str
    type: ElementTypeName
    label: str
    status: ElementStatus
    level: Level
    definition: str
    """The definition, or the text of a statement; empty when there is neither."""
    corpora: list[str]
    """The corpus folders of its evidence (``90_user_statements`` for user statements)."""
    documents: list[str]
    """The document IDs of its evidence."""
    search: str
    """Labels, definitions, statement text, quotes and evidence text, case-folded."""


class DocumentOut(BaseModel):
    id: str
    path: str
    title: str | None = None


class CorpusOut(BaseModel):
    folder: str
    source_path: str
    documents: list[DocumentOut]


class ElementsOut(BaseModel):
    elements: list[IndexEntryOut]
    corpora: list[CorpusOut]
    pending: int


class EvidenceOut(BaseModel):
    """One evidence passage of an element: the unit, its quote, and where the unit is."""

    unit: str
    quote: str | None = None
    text: str | None = None
    """The unit's text; ``None`` when the unit is unknown."""
    corpus: str | None = None
    document: str | None = None


class OriginOut(BaseModel):
    kind: str
    run_id: str | None = None
    author: str | None = None
    created_at: str


class MentionOut(BaseModel):
    unit: str
    concept: str


class RecordOut(BaseModel):
    """An element record: the fields every type has, typed; the type-specific ones pass through."""

    model_config = ConfigDict(extra="allow")

    label: str
    definition: str | None = None
    level: Level
    level_reason: str
    status: ElementStatus
    status_reason: str | None = None
    origin: OriginOut
    replaced_by: str | None = None
    mentions: list[MentionOut] | None = None
    """A term's mentions (unit → concept), which split and reassign act on."""


class DecisionOut(BaseModel):
    id: str
    at: str
    user: str
    role: Role
    action: str
    field: str | None = None
    old: Any = None
    new: Any = None
    reason: str | None = None


class ElementDetailOut(BaseModel):
    """One element: its evidence passages first, then the record and its decisions (FR-16)."""

    id: str
    type: ElementTypeName
    evidence: list[EvidenceOut]
    record: RecordOut
    decisions: list[DecisionOut]
    pending: bool
    """True when the element has unsaved changes."""


class VerdictOut(BaseModel):
    """The LLM's ignorable verdict on a corpus unit (FR-14)."""

    proposed: bool
    category: IgnorableCategory
    reason: str
    status: IgnorableStatus


class UnitOut(BaseModel):
    """One source unit: a corpus unit or a user statement (unsaved ones included; Q49)."""

    id: str
    kind: UnitKind
    corpus: str
    """The corpus folder, or ``90_user_statements``."""
    document: str | None = None
    text: str
    """The text; for a user statement, its latest revision."""
    ignorable: VerdictOut | None = None
    author: str | None = None
    revisions: int
    """How many revisions a user statement has; 0 for a corpus unit."""


class ActionIn(BaseModel):
    action: ActionName
    ids: list[str] = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)


class ActionResultOut(BaseModel):
    element_id: str
    ok: bool
    message: str


class ActionsOut(BaseModel):
    results: list[ActionResultOut]
    pending: int


class StatementIn(BaseModel):
    text: str = Field(min_length=1)


class AuthorIn(BaseModel):
    type: ElementTypeName
    fields: dict[str, Any]


class IdOut(BaseModel):
    id: str


class CommitOut(BaseModel):
    """``ok`` with the commit's ``sha`` (``None`` when nothing changed), or the hook output."""

    ok: bool
    sha: str | None
    output: str


class IngestIn(BaseModel):
    """A folder (under the sources root) as a new corpus, or units marked not ignorable."""

    folder: str | None = None
    units: list[str] | None = None
    confirm: bool = False


class EstimateOut(BaseModel):
    model: str
    documents: int
    units: int
    input_tokens: int
    output_tokens: int
    cost_usd: float | None


class IngestOut(BaseModel):
    run_id: str
    status: str
    commit: CommitOut


class SkippedOut(BaseModel):
    where: str
    item: str
    reason: str


class RunOut(BaseModel):
    """The record of a run: model, tokens used, start and end, skipped items (FR-6)."""

    id: str
    kind: RunKind
    user: str
    model: str
    source_path: str | None = None
    started_at: str
    ended_at: str | None = None
    status: RunStatus
    input_tokens: int
    output_tokens: int
    skipped: list[SkippedOut] = Field(default_factory=list)


class PublishIn(BaseModel):
    version: str | None = None
    """Semantic version; default: the next minor of the last governed release."""


class ReferenceOut(BaseModel):
    element_id: str
    element_label: str
    target_id: str
    target_label: str
    target_status: str


class PublishOut(BaseModel):
    version: str | None
    """``None`` when the governed build was blocked by ``offenders`` (FR-35)."""
    changelog: str | None
    offenders: list[ReferenceOut]
    warnings: list[ReferenceOut]
    commit: CommitOut
