"""What the reviewer reads: the element index, one element in full, and the corpora.

Everything here is plain data (dicts, lists, strings), so the callers (api, cli) never handle
model classes. The index is compact enough to be filtered in the browser (FR-19); ``filter_index``
applies the same filter on the server.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from ontology_builder.governance import ChangeSet
from ontology_builder.store import DatasetFiles

USER_STATEMENTS = "90_user_statements"
"""The corpus key of user statements in the index."""


@dataclass(frozen=True)
class UnitInfo:
    """Where a source unit is: its corpus folder and document, and its text."""

    corpus: str
    document: str | None
    text: str


def corpus_units(files: DatasetFiles) -> dict[str, UnitInfo]:
    """Every corpus unit of the dataset by ID (user statements are read from the change set)."""
    found: dict[str, UnitInfo] = {}
    for folder in files.corpora():
        for document in files.documents(folder):
            for unit in files.units(folder, document.id):
                found[unit.id] = UnitInfo(folder, document.id, unit.text)
    return found


def corpora(files: DatasetFiles) -> list[dict[str, Any]]:
    """The corpora and their documents, for the filters of the GUI."""
    return [
        {
            "folder": folder,
            "source_path": corpus.source_path,
            "documents": [
                {"id": d.id, "path": d.path, "title": d.title} for d in files.documents(folder)
            ],
        }
        for folder, corpus in files.corpora().items()
    ]


def _type_of(element_id: str) -> str:
    return {
        "st": "statement",
        "tm": "term",
        "cn": "concept",
        "rl": "relation",
        "ru": "rule",
        "pr": "property",
    }[element_id.split("_", maxsplit=1)[0]]


def _units(changes: ChangeSet, units: Mapping[str, UnitInfo]) -> dict[str, UnitInfo]:
    statements = {
        unit.id: UnitInfo(USER_STATEMENTS, None, unit.text) for unit in changes.statements.values()
    }
    return {**units, **statements}


def _search_text(data: Mapping[str, Any], cited: list[UnitInfo]) -> str:
    """Labels, definitions, statement text, quotes and evidence text, case-folded (FR-19)."""
    own = [data.get(key, "") for key in ("label", "definition", "text")]
    quotes = [e.get("quote", "") for e in data.get("evidence", [])]
    texts = [*own, *quotes, *(unit.text for unit in cited)]
    return " ".join(t for t in texts if t).casefold()


def _entry(data: Mapping[str, Any], units: Mapping[str, UnitInfo]) -> dict[str, Any]:
    cited = [units[e["unit"]] for e in data.get("evidence", []) if e["unit"] in units]
    return {
        "id": data["id"],
        "type": _type_of(data["id"]),
        "label": data.get("label", ""),
        "status": data["status"],
        "level": data["level"],
        "definition": data.get("definition") or data.get("text") or "",
        "corpora": sorted({unit.corpus for unit in cited}),
        "documents": sorted({unit.document for unit in cited if unit.document}),
        "search": _search_text(data, cited),
    }


def element_index(changes: ChangeSet, units: Mapping[str, UnitInfo]) -> list[dict[str, Any]]:
    """One compact entry per element, sorted by ID: type, label, status, level, definition,
    the corpora and documents of its evidence, and the folded text that full-text search uses."""
    every = _units(changes, units)
    return [
        _entry(changes.elements[key].model_dump(mode="json", exclude_none=True), every)
        for key in sorted(changes.elements)
    ]


_LIST_FIELDS = {"corpus": "corpora", "document": "documents"}


def _matches(entry: Mapping[str, Any], field: str, wanted: str) -> bool:
    if field == "q":
        return wanted.casefold() in entry["search"]
    if field in _LIST_FIELDS:
        return wanted in entry[_LIST_FIELDS[field]]
    return bool(entry[field] == wanted)


def filter_index(
    entries: Iterable[Mapping[str, Any]], filters: Mapping[str, str | None]
) -> list[Mapping[str, Any]]:
    """The entries that match every given filter: ``type``, ``status``, ``level``, ``corpus``,
    ``document`` (exact) and ``q`` (case-insensitive substring of labels, definitions and
    evidence text). A filter that is ``None`` or empty is ignored."""
    given = {key: value for key, value in filters.items() if value}
    return [e for e in entries if all(_matches(e, k, v) for k, v in given.items())]


def _evidence(
    data: Mapping[str, Any], changes: ChangeSet, units: Mapping[str, UnitInfo]
) -> list[dict[str, Any]]:
    every = _units(changes, units)
    found = []
    for evidence in data.get("evidence", []):
        unit = every.get(evidence["unit"])
        found.append(
            {
                "unit": evidence["unit"],
                "quote": evidence.get("quote"),
                "text": unit.text if unit else None,
                "corpus": unit.corpus if unit else None,
                "document": unit.document if unit else None,
            }
        )
    return found


def element_detail(
    changes: ChangeSet, units: Mapping[str, UnitInfo], files: DatasetFiles, element_id: str
) -> dict[str, Any]:
    """One element in full: the record, its evidence passages (first, FR-16) and every decision
    on it, saved ones first, then the unsaved ones."""
    data = changes.get(element_id).model_dump(mode="json", exclude_none=True)
    decisions = [*files.decisions(), *changes.decisions]
    return {
        "id": element_id,
        "type": _type_of(element_id),
        "evidence": _evidence(data, changes, units),
        "record": data,
        "decisions": [
            d.model_dump(mode="json", exclude_none=True)
            for d in decisions
            if d.element_id == element_id
        ],
        "pending": element_id in changes.changed_ids(),
    }
