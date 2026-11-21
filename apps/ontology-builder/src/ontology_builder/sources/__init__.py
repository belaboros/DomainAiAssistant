"""sources component.

Splits Markdown documents and user statements into registered source units.

``split_markdown`` gives the block units of one document (ontology-builder/ADR-0003),
``read_corpus`` the registry of one ingested folder with minted IDs, and ``with_text`` a unit
with new text and a recomputed hash but the same ID (FR-5, AC-5).
"""

from __future__ import annotations

from ontology_builder.model import SourceUnit, content_hash, normalise, validate_record
from ontology_builder.sources.markdown import (
    Block,
    first_heading,
    split_markdown,
)
from ontology_builder.sources.registry import (
    MAX_CORPUS_NUMBER,
    CorpusLimitError,
    CorpusSource,
    DocumentSource,
    RegistryWriter,
    next_corpus_number,
    read_corpus,
    read_document,
    slugify,
)


def with_text(unit: SourceUnit, text: str) -> SourceUnit:
    """The unit with new (normalised) text and its recomputed hash; the ID never changes."""
    data = unit.model_dump(mode="json", exclude_none=True)
    data |= {"text": normalise(text), "content_hash": content_hash(text)}
    return validate_record(SourceUnit, data)


__all__ = [
    "MAX_CORPUS_NUMBER",
    "Block",
    "CorpusLimitError",
    "CorpusSource",
    "DocumentSource",
    "RegistryWriter",
    "content_hash",
    "first_heading",
    "next_corpus_number",
    "normalise",
    "read_corpus",
    "read_document",
    "slugify",
    "split_markdown",
    "with_text",
]
