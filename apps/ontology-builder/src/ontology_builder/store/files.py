"""The files of one ontology dataset folder, in the layout of FR-30 (plan 0002, Dataset layout)."""

from __future__ import annotations

import json
import shutil
from collections.abc import Mapping
from datetime import UTC
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from ontology_builder.model import (
    ELEMENT_TYPES,
    Corpus,
    Decision,
    Document,
    Element,
    Run,
    ScopeRecord,
    SourceUnit,
    validate_element,
    validate_record,
)
from ontology_builder.store.yaml_io import dump_json_line, dump_yaml, load_yaml, to_data

SOURCES = "00_sources"
USER_STATEMENTS = f"{SOURCES}/90_user_statements"
MODEL = "01_model"
ELEMENTS = f"{MODEL}/elements"
DECISIONS = "02_decisions"
RUNS = f"{DECISIONS}/runs"
RELEASE = "03_release"
RELEASE_VARIANTS = {"raw": f"{RELEASE}/00_raw", "governed": f"{RELEASE}/01_governed"}

LAYOUT_FOLDERS = [
    USER_STATEMENTS,
    *(f"{ELEMENTS}/{element_type}" for element_type in sorted(ELEMENT_TYPES)),
    RUNS,
    *RELEASE_VARIANTS.values(),
]
"""The leaf folders of a new dataset; each gets a ``.gitkeep`` so git keeps the layout."""

_TYPE_OF_CLASS = {record_class: name for name, record_class in ELEMENT_TYPES.items()}


class ReadOnlyError(RuntimeError):
    """A write to the live dataset folder; writes go through ``DatasetStore.transaction``."""


class DatasetFiles:
    """Reads and, inside a transaction, writes the records of one dataset folder."""

    def __init__(self, root: Path, *, writable: bool) -> None:
        self.root = root
        self._writable = writable

    # ---- low level ----

    def _write_text(self, relative: str, text: str) -> None:
        if not self._writable:
            raise ReadOnlyError(f"{self.root} is read-only; write inside a transaction")
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))

    def _write_record(self, relative: str, record: BaseModel) -> None:
        data = to_data(record)
        self._write_text(relative, dump_yaml(data))

    def _read_data(self, relative: str) -> Any:
        return load_yaml((self.root / relative).read_text(encoding="utf-8"))

    def _yaml_files(self, relative: str) -> list[Path]:
        folder = self.root / relative
        return sorted(folder.glob("*.yaml")) if folder.is_dir() else []

    def make_layout(self) -> None:
        for folder in LAYOUT_FOLDERS:
            self._write_text(f"{folder}/.gitkeep", "")

    # ---- scope and elements ----

    def write_scope(self, scope: ScopeRecord) -> None:
        self._write_record(f"{MODEL}/scope.yaml", scope)

    def scope(self) -> ScopeRecord | None:
        """The scope record; ``None`` when the file is missing or empty, raises when invalid."""
        if not (self.root / MODEL / "scope.yaml").is_file():
            return None
        data = self._read_data(f"{MODEL}/scope.yaml")
        if data is None:
            return None
        return validate_record(ScopeRecord, data)

    def write_element(self, element: Element) -> None:
        element_type = _TYPE_OF_CLASS[type(element)]
        self._write_record(f"{ELEMENTS}/{element_type}/{element.id}.yaml", element)

    def elements(self) -> dict[str, Element]:
        found: dict[str, Element] = {}
        for element_type in sorted(ELEMENT_TYPES):
            for path in self._yaml_files(f"{ELEMENTS}/{element_type}"):
                data = load_yaml(path.read_text(encoding="utf-8"))
                element = validate_element(element_type, data)
                found[element.id] = element
        return found

    # ---- sources ----

    def write_corpus(self, folder: str, corpus: Corpus) -> None:
        self._write_record(f"{SOURCES}/{folder}/corpus.yaml", corpus)

    def corpora(self) -> dict[str, Corpus]:
        """Corpus records by folder name (``00_<slug>`` ...), in folder order."""
        found: dict[str, Corpus] = {}
        for path in sorted((self.root / SOURCES).glob("*/corpus.yaml")):
            found[path.parent.name] = validate_record(Corpus, self._read_data(_rel(self, path)))
        return found

    def write_document(self, folder: str, document: Document) -> None:
        self._write_record(f"{SOURCES}/{folder}/documents/{document.id}.yaml", document)

    def documents(self, folder: str) -> list[Document]:
        return [
            validate_record(Document, self._read_data(_rel(self, path)))
            for path in self._yaml_files(f"{SOURCES}/{folder}/documents")
        ]

    def write_units(self, folder: str, document_id: str, units: list[SourceUnit]) -> None:
        data = [to_data(unit) for unit in units]
        self._write_text(f"{SOURCES}/{folder}/units/{document_id}.yaml", dump_yaml(data))

    def units(self, folder: str, document_id: str) -> list[SourceUnit]:
        data = self._read_data(f"{SOURCES}/{folder}/units/{document_id}.yaml") or []
        return [validate_record(SourceUnit, item) for item in data]

    def write_user_statement(self, unit: SourceUnit) -> None:
        self._write_record(f"{USER_STATEMENTS}/{unit.id}.yaml", unit)

    def user_statements(self) -> list[SourceUnit]:
        return [
            validate_record(SourceUnit, self._read_data(_rel(self, path)))
            for path in self._yaml_files(USER_STATEMENTS)
        ]

    # ---- decisions and runs ----

    def append_decisions(self, decisions: list[Decision]) -> None:
        """Append each decision as one JSON line to the file of its UTC day."""
        for decision in decisions:
            line = dump_json_line(to_data(decision))
            relative = f"{DECISIONS}/{decision.at.astimezone(UTC).date().isoformat()}.jsonl"
            path = self.root / relative
            existing = path.read_text(encoding="utf-8") if path.is_file() else ""
            self._write_text(relative, existing + line)

    def decisions(self) -> list[Decision]:
        found: list[Decision] = []
        for path in sorted((self.root / DECISIONS).glob("*.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                found.append(validate_record(Decision, json.loads(line)))
        return found

    def write_run(self, run: Run) -> None:
        self._write_record(f"{RUNS}/{run.id}.yaml", run)

    def run(self, run_id: str) -> Run:
        return validate_record(Run, self._read_data(f"{RUNS}/{run_id}.yaml"))

    # ---- releases ----

    def write_release_file(self, variant: str, name: str, text: str) -> None:
        if variant not in RELEASE_VARIANTS:
            raise ValueError(f"unknown release variant {variant!r}; use raw or governed")
        self._write_text(f"{RELEASE_VARIANTS[variant]}/{name}", text)

    def release_dir(self, variant: str) -> Path:
        return self.root / RELEASE_VARIANTS[variant]

    def release_files(self, variant: str) -> dict[str, bytes]:
        """The files of a release folder by name (no ``.gitkeep``); empty before the first build."""
        folder = self.release_dir(variant)
        if not folder.is_dir():
            return {}
        return {
            path.name: path.read_bytes()
            for path in sorted(folder.iterdir())
            if path.is_file() and path.name != ".gitkeep"
        }

    def replace_release(self, variant: str, files: Mapping[str, str]) -> None:
        """Replace a release folder as a whole: write a sibling folder, then swap it in.

        Inside a transaction this happens in the staging copy, so a failure leaves the live
        dataset as it was; the swap also means no file of an older build is left behind.
        """
        if not self._writable:
            raise ReadOnlyError(f"{self.root} is read-only; write inside a transaction")
        target = self.release_dir(variant)
        fresh = target.with_name(f".{target.name}.new")
        stale = target.with_name(f".{target.name}.old")
        for leftover in (fresh, stale):
            if leftover.exists():
                shutil.rmtree(leftover)
        fresh.mkdir(parents=True)
        for name, text in sorted(files.items()):
            (fresh / name).write_bytes(text.encode("utf-8"))
        if target.exists():
            target.rename(stale)
        fresh.rename(target)
        if stale.exists():
            shutil.rmtree(stale)


def _rel(files: DatasetFiles, path: Path) -> str:
    return path.relative_to(files.root).as_posix()
