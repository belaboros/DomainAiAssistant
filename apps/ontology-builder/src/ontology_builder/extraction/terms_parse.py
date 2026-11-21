"""Validate the pass 2 answer item by item, and merge the answer of the retry into it.

A synonym group is known by its concept alias, a sense split by its term label: a retry item with
the same name replaces the invalid one. An answer whose lists are not lists is unusable as a whole.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel

from ontology_builder.extraction.parse import UnusableOutputError
from ontology_builder.model import (
    RecordInvalidError,
    SenseSplit,
    SkippedItem,
    SynonymGroup,
    validate_record,
)

WHERE = "term resolution"
_NAME_SLOT = {"synonym_groups": "concept", "sense_splits": "term"}
_SHORT = 200


@dataclass(frozen=True)
class InvalidTermItem:
    list_name: str
    item: Any
    problems: list[str]

    @property
    def name(self) -> Any:
        slot = _NAME_SLOT[self.list_name]
        return self.item.get(slot) if isinstance(self.item, Mapping) else None

    def for_retry(self) -> dict[str, Any]:
        return {"list": self.list_name, "item": self.item, "problems": self.problems}


@dataclass
class TermAnswer:
    groups: list[SynonymGroup] = field(default_factory=list)
    splits: list[SenseSplit] = field(default_factory=list)
    invalid: list[InvalidTermItem] = field(default_factory=list)

    def names(self) -> set[Any]:
        return (
            {g.concept for g in self.groups}
            | {s.term for s in self.splits}
            | {i.name for i in self.invalid}
        )


def _list(data: Mapping[str, Any], name: str) -> list[Any]:
    value = data.get(name)
    if value is None:
        return []
    if not isinstance(value, list):
        raise UnusableOutputError(f"{name} must be a list")
    return value


def _valid[M: BaseModel](
    answer: TermAnswer, data: Mapping[str, Any], list_name: str, model: type[M]
) -> list[M]:
    valid = []
    for item in _list(data, list_name):
        try:
            valid.append(validate_record(model, item if isinstance(item, Mapping) else {}))
        except RecordInvalidError as error:
            answer.invalid.append(InvalidTermItem(list_name, item, error.problems))
    return valid


def parse_terms(data: Mapping[str, Any]) -> TermAnswer:
    """Split one answer into valid groups and splits and invalid items."""
    answer = TermAnswer()
    answer.groups = _valid(answer, data, "synonym_groups", SynonymGroup)
    answer.splits = _valid(answer, data, "sense_splits", SenseSplit)
    return answer


def merge_retry(first: TermAnswer, retry: TermAnswer) -> TermAnswer:
    """The first answer plus the retry; first-answer invalid items the retry left out stay."""
    answered = retry.names()
    return TermAnswer(
        groups=first.groups + retry.groups,
        splits=first.splits + retry.splits,
        invalid=[i for i in first.invalid if i.name not in answered] + retry.invalid,
    )


def describe(item: Any) -> str:
    """A short text of a group or split for the run record."""
    if hasattr(item, "model_dump"):
        item = item.model_dump(mode="json", exclude_none=True)
    return json.dumps(item, ensure_ascii=False, sort_keys=True)[:_SHORT]


def skipped(item: Any, reason: str) -> SkippedItem:
    return SkippedItem(where=WHERE, item=describe(item), reason=reason)


def report_invalid(answer: TermAnswer, note: str) -> list[SkippedItem]:
    """The still-invalid items as skipped items."""
    return [skipped(i.item, f"invalid {note}: " + "; ".join(i.problems)) for i in answer.invalid]
