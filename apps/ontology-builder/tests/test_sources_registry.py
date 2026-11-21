"""Source units and the source registry (plan 0002, T6: AC-4, AC-5 and the edge cases)."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

import pytest
from ontology_builder.model import FixedClock, SourceUnit, UlidMinter, validate_record
from ontology_builder.sources import (
    CorpusLimitError,
    content_hash,
    next_corpus_number,
    normalise,
    read_corpus,
    split_markdown,
    with_text,
)
from ontology_builder.store import DatasetStore

AT = datetime(2026, 11, 21, 10, 0, tzinfo=UTC)
RUN = "run_01JDK7F3Q8ZX5N6M2W4R9T0BCD"
MANUALS = Path(__file__).resolve().parents[3] / "data" / "user-manuals-pets-and-house-rules"
ULID_ID = re.compile(r"^(su|doc|co)_[0-9A-HJKMNP-TV-Z]{26}$")


def _minter() -> UlidMinter:
    return UlidMinter(FixedClock(AT))


def _store(tmp_path: Path) -> DatasetStore:
    store = DatasetStore(tmp_path, "pets", clock=FixedClock(AT), minter=_minter())
    store.root.mkdir()
    return store


def _ingest(store: DatasetStore, manual: str) -> None:
    """Register one manual folder as the next corpus, as ingestion will (T10)."""
    with store.transaction() as files:
        number = next_corpus_number(files.corpora())
        corpus = read_corpus(
            MANUALS / manual,
            source_path=f"user-manuals-pets-and-house-rules/{manual}",
            number=number,
            run_id=RUN,
            minter=store.minter,
        )
        corpus.write_to(files)


def test_two_corpora_get_00_and_01(tmp_path: Path) -> None:
    store = _store(tmp_path)
    _ingest(store, "dog-owners-manual")
    _ingest(store, "building-and-house-rules")
    corpora = store.read().corpora()
    assert list(corpora) == ["00_dog-owners-manual", "01_building-and-house-rules"]
    assert [c.number for c in corpora.values()] == [0, 1]
    dogs = store.read().documents("00_dog-owners-manual")
    assert len(dogs) == len(list((MANUALS / "dog-owners-manual").rglob("*.md")))
    assert all(store.read().units("00_dog-owners-manual", d.id) for d in dogs)


def test_unit_fields_present(tmp_path: Path) -> None:
    store = _store(tmp_path)
    _ingest(store, "building-and-house-rules")
    files = store.read()
    [document] = [
        d for d in files.documents("00_building-and-house-rules") if d.path == "04-pets/02-dogs.md"
    ]
    assert document.title == "4. Pets — 4.2 Dogs"
    units = files.units("00_building-and-house-rules", document.id)
    lead = units[0]
    assert ULID_ID.match(lead.id) and lead.document_id == document.id
    assert lead.kind == "list_item"
    assert lead.location is not None
    assert lead.location.path == "04-pets/02-dogs.md"
    assert lead.location.heading_path == ["4. Pets — 4.2 Dogs"]
    assert [u.location.index_in_section for u in units if u.location] == list(range(len(units)))
    assert lead.text.startswith("Dogs must be kept on a lead at all times")
    assert lead.content_hash == content_hash(lead.text)
    assert lead.location.line_start == 3


def test_ids_contain_no_text_or_position(tmp_path: Path) -> None:
    first = read_corpus(
        MANUALS / "dog-owners-manual", source_path="dogs", number=0, run_id=RUN, minter=_minter()
    )
    again = read_corpus(
        MANUALS / "dog-owners-manual",
        source_path="dogs",
        number=0,
        run_id=RUN,
        minter=UlidMinter(FixedClock(AT), random_bytes=lambda n: b"\x07" * n),
    )
    units = [u for d in first.documents for u in d.units]
    units_again = [u for d in again.documents for u in d.units]
    assert all(ULID_ID.match(u.id) for u in units)
    assert all(ULID_ID.match(d.document.id) for d in first.documents)
    assert len({u.id for u in units}) == len(units)
    # Same text and same position, different minter: same hashes, entirely different IDs.
    assert [u.content_hash for u in units] == [u.content_hash for u in units_again]
    assert not {u.id for u in units} & {u.id for u in units_again}


def test_text_edit_changes_hash_not_id(corpus_unit: dict[str, object]) -> None:
    unit = validate_record(SourceUnit, corpus_unit)
    edited = with_text(unit, "Keep the dog on a lead of at most 3 m in the stairwell.")
    assert edited.id == unit.id
    assert edited.content_hash != unit.content_hash
    assert edited.content_hash == content_hash(edited.text)


def test_normalisation_is_nfc_and_whitespace() -> None:
    assert normalise("  Café\n  and\tcats  ") == "Café and cats"
    assert content_hash("Café  cats") == content_hash("Café cats")
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", content_hash("x"))


def test_block_kinds_headings_and_sections() -> None:
    markdown = (
        "Intro before any heading.\n\n"
        "# Pets\n\nA paragraph.\n\n- item one\n- item two\n  - nested\n\n"
        "## Dogs\n\n> A quote\n>\n> over two paragraphs.\n\n"
        "| Pet | Max |\n|---|---|\n| dog | 2 |\n| cat | 3 |\n\n"
        "```\ncode is skipped\n```\n"
    )
    blocks = split_markdown(markdown)
    summary = [(b.kind, b.text, b.heading_path, b.index_in_section) for b in blocks]
    assert summary == [
        ("paragraph", "Intro before any heading.", (), 0),
        ("paragraph", "A paragraph.", ("Pets",), 0),
        ("list_item", "item one", ("Pets",), 1),
        ("list_item", "item two", ("Pets",), 2),
        ("list_item", "nested", ("Pets",), 3),
        ("blockquote", "A quote over two paragraphs.", ("Pets", "Dogs"), 0),
        ("table_row", "Pet: dog | Max: 2", ("Pets", "Dogs"), 1),
        ("table_row", "Pet: cat | Max: 3", ("Pets", "Dogs"), 2),
    ]
    assert (blocks[5].line_start, blocks[5].line_end) == (13, 15)


def test_empty_and_headingless_files(tmp_path: Path) -> None:
    folder = tmp_path / "notes"
    folder.mkdir()
    (folder / "empty.md").write_text("", encoding="utf-8")
    (folder / "plain.md").write_text("Just text.\n\nMore text.\n", encoding="utf-8")
    corpus = read_corpus(folder, source_path="notes", number=3, run_id=RUN, minter=_minter())
    assert corpus.folder == "03_notes"
    empty, plain = corpus.documents
    assert (empty.document.path, empty.document.title, empty.units) == ("empty.md", "empty", [])
    assert plain.document.title == "plain"
    assert [u.location.heading_path for u in plain.units if u.location] == [[], []]


def test_identical_text_separate_ids_same_hash() -> None:
    blocks = split_markdown("# A\n\nSame text.\n\n# B\n\nSame text.\n")
    assert blocks[0].text == blocks[1].text
    folder_units = [b.to_unit("doc_01JDK7F3Q8ZX5N6M2W4R9T0BCD", "a.md", _minter()) for b in blocks]
    assert folder_units[0].id != folder_units[1].id
    assert folder_units[0].content_hash == folder_units[1].content_hash


def test_corpus_numbers_run_from_00_to_89() -> None:
    assert next_corpus_number([]) == 0
    assert next_corpus_number(["00_a", "01_b", "90_user_statements"]) == 2
    with pytest.raises(CorpusLimitError):
        next_corpus_number([f"{n:02d}_c" for n in range(90)])
