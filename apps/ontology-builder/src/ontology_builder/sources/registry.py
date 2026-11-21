"""The source registry of one corpus: corpus, documents and units (FR-4, FR-5; plan 0002).

``read_corpus`` reads a folder of Markdown files (sub-folders included) and mints every ID.
``CorpusSource.write_to`` writes the registry through any writer with the store's methods, so
this component does not depend on the store.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ontology_builder.model import (
    Corpus,
    Document,
    SourceUnit,
    UlidMinter,
    normalise,
    validate_record,
)
from ontology_builder.sources.markdown import first_heading, split_markdown

MAX_CORPUS_NUMBER = 89
_NUMBERED = re.compile(r"^(\d{2})_")
_NOT_SLUG = re.compile(r"[^a-z0-9]+")


class CorpusLimitError(ValueError):
    """All corpus numbers 00-89 of an ontology are taken."""


class RegistryWriter(Protocol):
    """What the registry needs to be written (``store.DatasetFiles`` in a transaction)."""

    def write_corpus(self, folder: str, corpus: Corpus) -> None: ...

    def write_document(self, folder: str, document: Document) -> None: ...

    def write_units(self, folder: str, document_id: str, units: list[SourceUnit]) -> None: ...


@dataclass(frozen=True)
class DocumentSource:
    document: Document
    units: list[SourceUnit]


@dataclass(frozen=True)
class CorpusSource:
    """One corpus with its documents and units, ready to be written."""

    corpus: Corpus
    documents: list[DocumentSource]

    @property
    def folder(self) -> str:
        """The corpus folder under ``00_sources/``: ``NN_<slug>``."""
        return f"{self.corpus.number:02d}_{self.corpus.slug}"

    @property
    def units(self) -> list[SourceUnit]:
        return [unit for document in self.documents for unit in document.units]

    def write_to(self, writer: RegistryWriter) -> None:
        writer.write_corpus(self.folder, self.corpus)
        for item in self.documents:
            writer.write_document(self.folder, item.document)
            writer.write_units(self.folder, item.document.id, item.units)


def next_corpus_number(existing_folders: Iterable[str]) -> int:
    """The next free corpus number after the numbered folders 00-89 already present."""
    numbers = [
        int(match.group(1))
        for name in existing_folders
        if (match := _NUMBERED.match(name)) and int(match.group(1)) <= MAX_CORPUS_NUMBER
    ]
    number = max(numbers, default=-1) + 1
    if number > MAX_CORPUS_NUMBER:
        raise CorpusLimitError("this ontology already holds 90 corpora (00-89)")
    return number


def slugify(name: str) -> str:
    """A kebab-case slug of a folder name (``Dog Owners_Manual`` → ``dog-owners-manual``)."""
    return _NOT_SLUG.sub("-", normalise(name).lower()).strip("-") or "corpus"


def _markdown_files(folder: Path) -> list[Path]:
    return sorted(
        path
        for path in folder.rglob("*.md")
        if path.is_file()
        and not any(part.startswith(".") for part in path.relative_to(folder).parts)
    )


def read_document(folder: Path, path: Path, corpus_id: str, minter: UlidMinter) -> DocumentSource:
    """One Markdown file as a document and its units; the title is its first heading or name."""
    raw = path.read_bytes()
    markdown = raw.decode("utf-8")
    relative = path.relative_to(folder).as_posix()
    document = validate_record(
        Document,
        {
            "id": minter.new("document"),
            "corpus_id": corpus_id,
            "path": relative,
            "title": first_heading(markdown) or path.stem,
            "content_hash": "sha256:" + hashlib.sha256(raw).hexdigest(),
        },
    )
    units = [block.to_unit(document.id, relative, minter) for block in split_markdown(markdown)]
    return DocumentSource(document, units)


def read_corpus(
    folder: Path, *, source_path: str, number: int, run_id: str, minter: UlidMinter
) -> CorpusSource:
    """Every Markdown file under ``folder`` as one corpus with number ``number``.

    ``source_path`` is the folder as recorded in ``corpus.yaml`` (relative to ``SHARED_DATA_DIR``).
    """
    corpus = validate_record(
        Corpus,
        {
            "id": minter.new("corpus"),
            "number": number,
            "slug": slugify(folder.name),
            "source_path": source_path,
            "ingest_run": run_id,
        },
    )
    documents = [read_document(folder, path, corpus.id, minter) for path in _markdown_files(folder)]
    return CorpusSource(corpus, documents)
