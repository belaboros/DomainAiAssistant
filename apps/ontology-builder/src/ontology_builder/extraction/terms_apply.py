"""Apply a pass 2 answer to the new elements of a run (FR-11, FR-12; plan 0002, Approach 5).

1. Terms with the same label (ignoring case) become one term record.
2. Synonym groups merge new concepts into the group's concept: the evidence and parents of a
   merged concept go to the one kept, the merged record is left out, and every reference to it
   (parents, mentions, relations, rules, properties) points to the kept concept. A concept already
   in the ontology is never merged away and never changed; new concepts may merge into it.
3. A group's preferred label becomes the kept concept's label; the mentions of its terms point to
   the kept concept.
4. A sense split points the term's mention in each listed unit to that sense's concept, and the
   sense's scope note goes on the concept.
An item that cites an unknown alias is reported and left out. Every record is validated again.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from ontology_builder.extraction.terms_parse import TermAnswer, skipped
from ontology_builder.extraction.terms_prompt import TermPrompt, label_key
from ontology_builder.model import (
    ELEMENT_TYPES,
    Element,
    SenseSplit,
    SkippedItem,
    SynonymGroup,
    validate_element,
)

_TYPE_NAME = {record_class: name for name, record_class in ELEMENT_TYPES.items()}
_LEVEL_RANK = {"level-1": 1, "level-2": 2, "level-3": 3, "ignorable": 4}

Record = dict[str, Any]


class _Refused(ValueError):
    """An item that cannot be applied; the message is the reason in the run record."""


@dataclass
class _Workspace:
    """The records of a run as plain data while the answer is applied."""

    prompt: TermPrompt
    records: dict[str, Record]
    types: dict[str, str]
    new_concepts: set[str]
    existing: set[str]
    into: dict[str, str] = field(default_factory=dict)
    skipped: list[SkippedItem] = field(default_factory=list)

    def find(self, concept_id: str) -> str:
        while concept_id in self.into:
            concept_id = self.into[concept_id]
        return concept_id

    def concept(self, alias: str) -> str:
        concept_id = self.prompt.concepts.get(alias)
        if concept_id is None:
            raise _Refused(f"cites unknown concept {alias}")
        return concept_id

    def unit(self, alias: str) -> str:
        unit_id = self.prompt.units.get(alias)
        if unit_id is None:
            raise _Refused(f"cites unknown unit {alias}")
        return unit_id

    def term(self, label: str) -> Record:
        for element_id, name in self.types.items():
            record = self.records.get(element_id)
            if name == "term" and record and label_key(record["label"]) == label_key(label):
                return record
        raise _Refused(f"no term with the label {label!r}")


def _unique(items: Iterable[Any]) -> list[Any]:
    seen: list[Any] = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


# ---------- 1. one term per label ----------


def _merge_terms(space: _Workspace) -> None:
    kept: dict[str, Record] = {}
    for element_id, name in list(space.types.items()):
        if name != "term":
            continue
        record = space.records[element_id]
        first = kept.setdefault(label_key(record["label"]), record)
        if first is record:
            continue
        first["evidence"] = _unique(first["evidence"] + record["evidence"])
        first["mentions"] = _unique(first.get("mentions", []) + record.get("mentions", []))
        del space.records[element_id]


# ---------- 2. merging concepts ----------


def _merge_one(space: _Workspace, source: str, target: str) -> None:
    root, into = space.find(source), space.find(target)
    if root == into:
        return
    if root in space.existing:
        raise _Refused(
            f"concept {source} is already in the ontology; merging it is a review action"
        )
    space.into[root] = into


def _apply_merges(space: _Workspace, group: SynonymGroup) -> None:
    target = space.concept(group.concept)
    sources = [space.concept(alias) for alias in group.merge or []]
    for source in sources:
        _merge_one(space, source, target)


def _fold(kept: Record, merged: Record) -> None:
    """Move the evidence, parents and a better level or a definition of ``merged`` into ``kept``."""
    kept["evidence"] = _unique(kept["evidence"] + merged["evidence"])
    kept["parents"] = _unique(kept.get("parents", []) + merged.get("parents", []))
    if _LEVEL_RANK[merged["level"]] < _LEVEL_RANK[kept["level"]]:
        kept["level"], kept["level_reason"] = merged["level"], merged["level_reason"]
    if not kept.get("definition") and merged.get("definition"):
        kept["definition"] = merged["definition"]


def _fold_merged(space: _Workspace) -> None:
    for source in space.into:
        merged = space.records.pop(source)
        kept = space.records.get(space.find(source))
        if kept is not None:
            _fold(kept, merged)


def _concept_ref(space: _Workspace) -> Callable[[str], str]:
    return lambda ref: space.find(ref) if ref.startswith("cn_") else ref


def _rewire(record: Record, kind: str, ref: Callable[[str], str]) -> None:
    """Point every concept reference of one record to the concept kept after the merges."""
    if kind == "concept":
        record["parents"] = [
            p for p in _unique(map(ref, record.get("parents", []))) if p != record["id"]
        ]
    elif kind == "term":
        for mention in record.get("mentions", []):
            mention["concept"] = ref(mention["concept"])
    elif kind == "relation":
        record["subject"], record["object"] = ref(record["subject"]), ref(record["object"])
    elif kind == "rule":
        record["refers_to"] = _unique(map(ref, record.get("refers_to", [])))
    elif kind == "property":
        record["of"] = ref(record["of"])


# ---------- 3. and 4. labels, mentions, senses ----------


def _apply_group(space: _Workspace, group: SynonymGroup) -> None:
    kept = space.find(space.concept(group.concept))
    if kept in space.records:
        space.records[kept]["label"] = group.preferred_label
    missing = []
    for label in group.terms:
        try:
            term = space.term(label)
        except _Refused as refused:
            missing.append(str(refused))
            continue
        for mention in term.get("mentions", []):
            mention["concept"] = kept
    if missing:
        raise _Refused("; ".join(missing))


def _apply_split(space: _Workspace, split: SenseSplit) -> None:
    term = space.term(split.term)
    senses = [
        (space.find(space.concept(sense.concept)), sense, [space.unit(u) for u in sense.mentions])
        for sense in split.senses
    ]
    for concept_id, sense, units in senses:
        for mention in term.get("mentions", []):
            if mention["unit"] in units:
                mention["concept"] = concept_id
        if concept_id in space.records:
            space.records[concept_id]["scope_note"] = sense.scope_note


def _each(
    space: _Workspace, items: Sequence[Any], apply: Callable[[_Workspace, Any], None]
) -> list[Any]:
    """Apply each item; report a refused one and return the items that were applied."""
    applied = []
    for item in items:
        try:
            apply(space, item)
        except _Refused as refused:
            space.skipped.append(skipped(item, str(refused)))
        else:
            applied.append(item)
    return applied


# ---------- the whole answer ----------


@dataclass
class Applied:
    elements: list[Element]
    merged: dict[str, str]
    skipped: list[SkippedItem]


def _workspace(prompt: TermPrompt, elements: Sequence[Element], existing: set[str]) -> _Workspace:
    records = {e.id: e.model_dump(mode="json", exclude_none=True) for e in elements}
    types = {e.id: _TYPE_NAME[type(e)] for e in elements}
    new = {element_id for element_id, name in types.items() if name == "concept"}
    return _Workspace(prompt, records, types, new, existing)


def _finish(space: _Workspace) -> list[Element]:
    ref = _concept_ref(space)
    elements = []
    for element_id, record in space.records.items():
        kind = space.types[element_id]
        _rewire(record, kind, ref)
        if kind == "term":
            record["mentions"] = _unique(record.get("mentions", []))
        clean = {name: value for name, value in record.items() if value not in (None, [])}
        elements.append(validate_element(kind, clean))
    return elements


def apply_answer(
    prompt: TermPrompt,
    elements: Sequence[Element],
    existing: Mapping[str, Element],
    answer: TermAnswer,
) -> Applied:
    """The run's elements after the answer, the merged concept IDs and what was left out."""
    space = _workspace(prompt, elements, set(existing))
    _merge_terms(space)
    groups = _each(space, answer.groups, _apply_merges)
    _fold_merged(space)
    _each(space, groups, _apply_group)
    _each(space, answer.splits, _apply_split)
    merged = {source: space.find(source) for source in space.into}
    return Applied(_finish(space), merged, space.skipped)
