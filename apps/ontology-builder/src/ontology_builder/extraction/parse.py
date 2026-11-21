"""Validate one pass 1 answer item by item, and merge the answer of the retry into it.

An answer that lacks ``unit_verdicts`` or whose lists are not lists is unusable as a whole. Every
other problem belongs to one item: that item is invalid and goes into the retry, the rest is kept.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel

from ontology_builder.model import (
    Candidate,
    CandidateConcept,
    CandidateProperty,
    CandidateRelation,
    CandidateRule,
    CandidateStatement,
    CandidateTerm,
    RecordInvalidError,
    SkippedItem,
    UnitVerdict,
    validate_record,
)

CANDIDATE_LISTS: dict[str, type[Candidate]] = {
    "statements": CandidateStatement,
    "terms": CandidateTerm,
    "concepts": CandidateConcept,
    "relations": CandidateRelation,
    "rules": CandidateRule,
    "properties": CandidateProperty,
}
"""Output list name to its candidate class, in the order records are minted."""

CALL_A_LISTS = ("statements", "terms", "concepts", "relations")
"""The candidate lists of call A (``ConceptsOutput``, with the unit verdicts; ADR-0007)."""
CALL_B_LISTS = ("rules", "properties")
"""The candidate lists of call B (``RulesOutput``)."""

KIND_OF_LIST: dict[str, str] = {
    "unit_verdicts": "verdict",
    "statements": "statement",
    "terms": "term",
    "concepts": "concept",
    "relations": "relation",
    "rules": "rule",
    "properties": "property",
}
_SHORT = 200


class UnusableOutputError(ValueError):
    """The answer as a whole does not have the required shape."""


@dataclass(frozen=True)
class InvalidItem:
    """One item that failed validation, with what was wrong."""

    list_name: str
    item: Any
    problems: list[str]

    @property
    def name(self) -> Any:
        """The key of a candidate or the unit of a verdict, as far as it is readable."""
        return (
            self.item.get("key") or self.item.get("unit")
            if isinstance(self.item, Mapping)
            else None
        )

    def for_retry(self) -> dict[str, Any]:
        return {"list": self.list_name, "item": self.item, "problems": self.problems}


@dataclass
class Parsed:
    """The valid verdicts and candidates of one or more answers, and what was left out."""

    verdicts: dict[str, UnitVerdict] = field(default_factory=dict)
    candidates: dict[str, list[Candidate]] = field(
        default_factory=lambda: {name: [] for name in CANDIDATE_LISTS}
    )
    invalid: list[InvalidItem] = field(default_factory=list)
    skipped: list[SkippedItem] = field(default_factory=list)

    def keys(self) -> set[str]:
        return {c.key for items in self.candidates.values() for c in items}


def describe(list_name: str, item: Any) -> str:
    """A short text of an item for the run record: its kind, key and label."""
    if isinstance(item, BaseModel):
        item = item.model_dump(mode="json")
    if isinstance(item, Mapping):
        kind = KIND_OF_LIST.get(list_name, list_name)
        text = f"{kind} {item.get('key') or item.get('unit', '?')} {item.get('label', '')!r}"
    else:
        text = f"{list_name}: {item!r}"
    return text[:_SHORT]


def _verdict(item: Any) -> UnitVerdict:
    verdict = validate_record(UnitVerdict, item if isinstance(item, Mapping) else {})
    if verdict.ignorable and verdict.category is None:
        raise RecordInvalidError("UnitVerdict", ["category: required when ignorable is true"])
    return verdict


def _list(data: Mapping[str, Any], name: str, required: bool) -> list[Any]:
    value = data.get(name)
    if value is None and not required:
        return []
    if not isinstance(value, list):
        raise UnusableOutputError(f"{name} must be a list")
    return value


def parse_answer(data: Mapping[str, Any], lists: Sequence[str], verdicts: bool) -> Parsed:
    """Split one answer into valid verdicts and candidates and invalid items.

    ``lists`` names the candidate lists the answer may hold; ``verdicts`` says whether it must
    hold ``unit_verdicts`` (call A) or holds none (call B).
    """
    parsed = Parsed()
    for item in _list(data, "unit_verdicts", required=True) if verdicts else []:
        try:
            verdict = _verdict(item)
        except RecordInvalidError as error:
            parsed.invalid.append(InvalidItem("unit_verdicts", item, error.problems))
            continue
        parsed.verdicts[verdict.unit] = verdict
    for name in lists:
        candidate_class = CANDIDATE_LISTS[name]
        for item in _list(data, name, required=False):
            try:
                parsed.candidates[name].append(
                    validate_record(candidate_class, item if isinstance(item, Mapping) else {})
                )
            except RecordInvalidError as error:
                parsed.invalid.append(InvalidItem(name, item, error.problems))
    return parsed


def _retried(retry: Parsed) -> set[Any]:
    """Keys and units the retry answered, validly or not."""
    return retry.keys() | set(retry.verdicts) | {item.name for item in retry.invalid}


def merge_answers(first: Parsed, retry: Parsed, where: str) -> Parsed:
    """The first answer plus the items of a later one (a retry, or call B); a reused key is skipped.

    The result's ``invalid`` holds what is still invalid: the later answer's invalid items and the
    first answer's invalid items the later one did not answer at all.
    """
    answered = _retried(retry)
    merged = Parsed(
        verdicts=first.verdicts | retry.verdicts,
        candidates={name: list(items) for name, items in first.candidates.items()},
        invalid=[item for item in first.invalid if item.name not in answered] + retry.invalid,
        skipped=first.skipped + retry.skipped,
    )
    keys = first.keys()
    for name, items in retry.candidates.items():
        for candidate in items:
            if candidate.key in keys:
                merged.skipped.append(
                    skip(where, name, candidate, f"duplicate key {candidate.key}")
                )
                continue
            keys.add(candidate.key)
            merged.candidates[name].append(candidate)
    return merged


def skip(where: str, list_name: str, item: Any, reason: str) -> SkippedItem:
    return SkippedItem(where=where, item=describe(list_name, item), reason=reason)


def report_invalid(parsed: Parsed, where: str, note: str) -> None:
    """Move every still-invalid item into the skipped list."""
    for invalid in parsed.invalid:
        reason = f"invalid {note}: " + "; ".join(invalid.problems)
        parsed.skipped.append(skip(where, invalid.list_name, invalid.item, reason))
    parsed.invalid = []
