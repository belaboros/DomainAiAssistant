"""What an ingestion produced, as plain data for the scoring: units, elements, labels, text."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from typing import Any

from ontology_builder.store import DatasetFiles

_TYPES = {
    "st": "statement",
    "tm": "term",
    "cn": "concept",
    "rl": "relation",
    "ru": "rule",
    "pr": "property",
}
_TEXT_FIELDS = (
    "label",
    "definition",
    "text",
    "actor",
    "action",
    "condition",
    "predicate_label",
    "name",
    "value",
    "unit",
    "scope_note",
)
_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_SEPARATORS = re.compile(r"[\s_\-]+")


def normalise_label(label: str) -> str:
    """Case, hyphens, underscores, CamelCase and a trailing plural "s" are ignored."""
    words = _SEPARATORS.sub(" ", _CAMEL.sub(" ", label)).strip(" .,;:()\"'").casefold()
    folded = " ".join(words.split())
    return folded[:-1] if folded.endswith("s") and not folded.endswith("ss") else folded


def contains_all(text: str, groups: Iterable[Iterable[str]]) -> bool:
    """Every group has at least one keyword in ``text`` (case-insensitive)."""
    folded = text.casefold()
    return all(any(word.casefold() in folded for word in group) for group in groups)


@dataclass(frozen=True)
class Unit:
    id: str
    corpus: str
    """The source folder name of the corpus, e.g. ``dog-owners-manual``."""
    document: str
    text: str
    ignorable: bool
    category: str | None


def _number(value: Any) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def _limit_text(limit: Mapping[str, Any] | None) -> str:
    if not limit:
        return ""
    return f"{_number(limit['value'])} {limit.get('unit', '')}".strip()


@dataclass(frozen=True)
class Item:
    """One element: its type, label, searchable text and links."""

    id: str
    type: str
    label: str
    text: str
    evidence: tuple[str, ...]
    mentions: tuple[tuple[str, str], ...] = ()
    refers_to: tuple[str, ...] = ()

    @classmethod
    def of(cls, data: Mapping[str, Any]) -> Item:
        texts = [str(data[key]) for key in _TEXT_FIELDS if data.get(key) is not None]
        texts.append(_limit_text(data.get("limit")))
        texts += [str(e.get("quote", "")) for e in data.get("evidence", [])]
        return cls(
            id=str(data["id"]),
            type=_TYPES[str(data["id"]).split("_", maxsplit=1)[0]],
            label=str(data.get("label", "")),
            text=" ".join(t for t in texts if t),
            evidence=tuple(str(e["unit"]) for e in data.get("evidence", [])),
            mentions=tuple((str(m["unit"]), str(m["concept"])) for m in data.get("mentions", [])),
            refers_to=tuple(str(r) for r in data.get("refers_to", [])),
        )


@dataclass
class Findings:
    """The units by ID and the elements (not deprecated, excluded or rejected) by ID."""

    units: dict[str, Unit]
    elements: dict[str, Item]
    _labels: dict[str, set[str]] = field(default_factory=dict)

    def of_type(self, element_type: str) -> list[Item]:
        return [item for item in self.elements.values() if item.type == element_type]

    def labels(self, concept_id: str) -> set[str]:
        """The normalised labels of a concept: its own and those of the terms naming it."""
        if not self._labels:
            for concept in self.of_type("concept"):
                self._labels[concept.id] = {normalise_label(concept.label)}
            for term in self.of_type("term"):
                for _, concept_id_ in term.mentions:
                    self._labels.setdefault(concept_id_, set()).add(normalise_label(term.label))
        return self._labels.get(concept_id, set())

    def citing(self, unit_id: str) -> list[Item]:
        return [item for item in self.elements.values() if unit_id in item.evidence]

    def find_units(self, corpus: str, document: str, contains: str = "") -> list[Unit]:
        wanted = contains.casefold()
        return [
            unit
            for unit in self.units.values()
            if unit.corpus == corpus
            and unit.document == document
            and wanted in unit.text.casefold()
        ]


_GONE = {"excluded", "rejected", "deprecated"}


def _units(files: DatasetFiles) -> dict[str, Unit]:
    found: dict[str, Unit] = {}
    for folder, corpus in files.corpora().items():
        name = str(corpus.source_path).rstrip("/").rsplit("/", maxsplit=1)[-1]
        for document in files.documents(folder):
            for unit in files.units(folder, document.id):
                verdict = unit.model_dump(mode="json").get("ignorable") or {}
                ignorable = bool(verdict.get("proposed"))
                category = verdict.get("category") if ignorable else None
                found[unit.id] = Unit(unit.id, name, document.path, unit.text, ignorable, category)
    return found


def _with_properties(elements: dict[str, Item], owners: Mapping[str, str]) -> None:
    """A property's text is added to the element it belongs to, so a rule whose 60 °C is a
    property of it still reads "wash ... 60 °C"."""
    for property_id, owner in owners.items():
        if owner in elements and property_id in elements:
            item = elements[owner]
            text = f"{item.text} {elements[property_id].text}"
            elements[owner] = replace(item, text=text)


def read_findings(files: DatasetFiles) -> Findings:
    """Everything the scoring needs from the dataset of the ingestion."""
    elements: dict[str, Item] = {}
    owners: dict[str, str] = {}
    for element in files.elements().values():
        data = element.model_dump(mode="json", exclude_none=True)
        if data.get("status") not in _GONE:
            elements[data["id"]] = Item.of(data)
            if "of" in data:
                owners[data["id"]] = str(data["of"])
    _with_properties(elements, owners)
    return Findings(_units(files), elements)
