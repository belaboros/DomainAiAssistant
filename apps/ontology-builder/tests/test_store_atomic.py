"""The store writes deterministic files and changes a dataset in one atomic swap (plan 0002, T4)."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from ontology_builder.model import (
    Decision,
    FixedClock,
    RecordInvalidError,
    Run,
    ScopeRecord,
    SourceUnit,
    UlidMinter,
    validate_element,
    validate_record,
)
from ontology_builder.store import (
    DatasetExistsError,
    DatasetStore,
    ReadOnlyError,
    dump_yaml,
)

ElementFactory = Callable[[str], dict[str, Any]]
AT = datetime(2026, 11, 21, 10, 0, tzinfo=UTC)


@pytest.fixture
def store(tmp_path: Path, scope_record: dict[str, Any]) -> DatasetStore:
    store = DatasetStore(tmp_path, "pets-and-house-rules")
    store.create(validate_record(ScopeRecord, scope_record))
    return store


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()
    }


# ---- IDs and clock ----


def test_minter_makes_prefixed_ulids_from_the_injected_clock() -> None:
    minter = UlidMinter(FixedClock(AT), random_bytes=bytes)
    first = minter.new("concept")
    assert re.fullmatch(r"cn_[0-9A-HJKMNP-TV-Z]{26}", first)
    assert minter.new("source_unit").startswith("su_")
    assert minter.new("concept") != first, "IDs are never reused, even in the same millisecond"
    again = UlidMinter(FixedClock(AT), random_bytes=bytes)
    assert again.new("concept") == first, (
        "same clock and randomness, same IDs (deterministic tests)"
    )


def test_minter_time_part_follows_the_clock() -> None:
    early = UlidMinter(FixedClock(AT), random_bytes=bytes).new("concept")
    later_clock = FixedClock(datetime(2027, 1, 1, tzinfo=UTC))
    later = UlidMinter(later_clock, random_bytes=bytes).new("concept")
    assert early[3:13] < later[3:13]


def test_minter_refuses_unknown_kind() -> None:
    with pytest.raises(KeyError):
        UlidMinter(FixedClock(AT)).new("axiom")


def test_store_exposes_the_injected_clock_and_minter(tmp_path: Path) -> None:
    clock = FixedClock(AT)
    minter = UlidMinter(clock)
    store = DatasetStore(tmp_path, "x", clock=clock, minter=minter)
    assert store.clock.now() == AT
    assert store.minter is minter


# ---- deterministic YAML ----


def test_yaml_is_deterministic_sorted_and_keeps_unicode() -> None:
    one = dump_yaml({"b": 1, "a": {"z": "Größe 2 m für Hündchen", "y": [3, 1]}})
    two = dump_yaml({"a": {"y": [3, 1], "z": "Größe 2 m für Hündchen"}, "b": 1})
    assert one == two
    assert one == "a:\n  y:\n  - 3\n  - 1\n  z: Größe 2 m für Hündchen\nb: 1\n"


def test_yaml_does_not_wrap_long_text() -> None:
    text = "word " * 100
    assert dump_yaml({"text": text.strip()}).count("\n") == 1


def test_yaml_quotes_strings_that_look_like_other_types() -> None:
    dumped = dump_yaml({"a": "yes", "b": "2", "c": "null"})
    assert dumped == "a: 'yes'\nb: '2'\nc: 'null'\n"


# ---- records ----


@pytest.mark.parametrize(
    "element_type", ["statement", "term", "concept", "relation", "rule", "property"]
)
def test_element_round_trip_one_file_per_element(
    store: DatasetStore, element_type: str, make_element: ElementFactory
) -> None:
    element = validate_element(element_type, make_element(element_type))
    with store.transaction() as files:
        files.write_element(element)
    path = store.root / "01_model" / "elements" / element_type / f"{element.id}.yaml"
    assert path.is_file()
    assert store.read().elements() == {element.id: element}
    first = path.read_bytes()
    with store.transaction() as files:
        files.write_element(element)
    assert path.read_bytes() == first, "writing the same record again gives the same bytes"


def test_write_validates_before_writing(store: DatasetStore, make_element: ElementFactory) -> None:
    valid = validate_element("concept", make_element("concept"))
    element = valid.model_copy(update={"evidence": []})  # an invalid copy, not re-validated
    before = _snapshot(store.root)
    with pytest.raises(RecordInvalidError, match="evidence"), store.transaction() as files:
        files.write_element(element)
    assert _snapshot(store.root) == before


def test_scope_record_round_trip(store: DatasetStore, scope_record: dict[str, Any]) -> None:
    assert store.read().scope() == validate_record(ScopeRecord, scope_record)


def test_units_and_user_statements_round_trip(
    store: DatasetStore, corpus_unit: dict[str, Any]
) -> None:
    unit = validate_record(SourceUnit, corpus_unit)
    statement = validate_record(
        SourceUnit,
        corpus_unit
        | {"id": "su_01JDK7F3Q8ZX5N6M2W4R9T0BCE", "kind": "user_statement", "author": "bela",
           "created_at": "2026-11-21T10:00:00Z"},
    )  # fmt: skip
    with store.transaction() as files:
        files.write_units("00_pets", corpus_unit["document_id"], [unit])
        files.write_user_statement(statement)
    view = store.read()
    assert view.units("00_pets", corpus_unit["document_id"]) == [unit]
    assert view.user_statements() == [statement]
    assert (store.root / "00_sources" / "90_user_statements" / f"{statement.id}.yaml").is_file()


def test_decisions_are_appended_one_json_line_each_by_day(store: DatasetStore) -> None:
    def decision(n: int, day: int) -> Decision:
        return validate_record(
            Decision,
            {"id": f"dc_01JDK7F3Q8ZX5N6M2W4R9T0BC{n}", "at": f"2026-11-{day}T10:00:00Z",
             "user": "bela", "role": "domain_admin", "action": "include",
             "element_id": "cn_01JDK7F3Q8ZX5N6M2W4R9T0BCD", "old": "proposed", "new": "included"},
        )  # fmt: skip

    with store.transaction() as files:
        files.append_decisions([decision(1, 21)])
    log = store.root / "02_decisions" / "2026-11-21.jsonl"
    first = log.read_bytes()
    with store.transaction() as files:
        files.append_decisions([decision(2, 21), decision(3, 22)])
    assert log.read_bytes().startswith(first), "earlier lines are never rewritten"
    lines = log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[1])["id"].endswith("C2")
    assert (store.root / "02_decisions" / "2026-11-22.jsonl").is_file()
    assert [d.id[-2:] for d in store.read().decisions()] == ["C1", "C2", "C3"]


def test_run_record_round_trip(store: DatasetStore) -> None:
    run = validate_record(
        Run,
        {"id": "run_01JDK7F3Q8ZX5N6M2W4R9T0BCD", "kind": "ingestion", "user": "bela",
         "model": "claude-x", "started_at": "2026-11-21T10:00:00Z", "status": "completed",
         "input_tokens": 10, "output_tokens": 5},
    )  # fmt: skip
    with store.transaction() as files:
        files.write_run(run)
    assert (store.root / "02_decisions" / "runs" / f"{run.id}.yaml").is_file()
    assert store.read().run(run.id) == run


def test_release_files_are_written_as_given(store: DatasetStore) -> None:
    with store.transaction() as files:
        files.write_release_file("raw", "ontology.ttl", "@prefix dai: <x#> .\n")
    path = store.root / "03_release" / "00_raw" / "ontology.ttl"
    assert path.read_text(encoding="utf-8") == "@prefix dai: <x#> .\n"
    with pytest.raises(ValueError, match="variant"), store.transaction() as files:
        files.write_release_file("final", "ontology.ttl", "")


# ---- atomic swap ----


def test_live_view_is_read_only(store: DatasetStore, make_element: ElementFactory) -> None:
    with pytest.raises(ReadOnlyError):
        store.read().write_element(validate_element("concept", make_element("concept")))


def test_transaction_swaps_in_and_cleans_up(store: DatasetStore, tmp_path: Path) -> None:
    with store.transaction() as files:
        files.write_release_file("raw", "level-1.md", "# L1\n")
        assert not (store.root / "03_release" / "00_raw" / "level-1.md").exists()
    assert (store.root / "03_release" / "00_raw" / "level-1.md").is_file()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ontology-pets-and-house-rules"]


def test_failure_inside_transaction_leaves_dataset_unchanged(
    store: DatasetStore, tmp_path: Path, make_element: ElementFactory
) -> None:
    before = _snapshot(store.root)
    with pytest.raises(RuntimeError, match="halfway"), store.transaction() as files:
        files.write_element(validate_element("concept", make_element("concept")))
        raise RuntimeError("halfway")
    assert _snapshot(store.root) == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ontology-pets-and-house-rules"]


def test_failing_after_swap_step_rolls_back(store: DatasetStore, tmp_path: Path) -> None:
    before = _snapshot(store.root)
    seen: list[bool] = []

    def failing_commit() -> None:
        seen.append((store.root / "03_release" / "00_raw" / "level-1.md").is_file())
        raise RuntimeError("hook failed")

    with (
        pytest.raises(RuntimeError, match="hook failed"),
        store.transaction(after_swap=failing_commit) as files,
    ):
        files.write_release_file("raw", "level-1.md", "# L1\n")
    assert seen == [True], "the step after the swap sees the new files"
    assert _snapshot(store.root) == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ontology-pets-and-house-rules"]


def test_recover_restores_previous_after_crash_between_renames(
    store: DatasetStore, tmp_path: Path
) -> None:
    before = _snapshot(store.root)
    store.root.rename(store.previous_dir)
    (tmp_path / store.staging_dir.name).mkdir()
    DatasetStore(tmp_path, "pets-and-house-rules").recover()
    assert _snapshot(store.root) == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ontology-pets-and-house-rules"]


def test_recover_rolls_back_an_unconfirmed_swap(store: DatasetStore, tmp_path: Path) -> None:
    before = _snapshot(store.root)
    store.root.rename(store.previous_dir)
    store.root.mkdir()
    (store.root / "half.yaml").write_text("x: 1\n", encoding="utf-8")
    store.recover()
    assert _snapshot(store.root) == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ontology-pets-and-house-rules"]


def test_transaction_refused_while_a_stale_staging_folder_exists(store: DatasetStore) -> None:
    store.staging_dir.mkdir()
    with pytest.raises(RuntimeError, match="recover"), store.transaction():
        pass


def test_tree_hash_changes_with_any_file(store: DatasetStore) -> None:
    first = store.tree_hash()
    assert store.tree_hash() == first
    with store.transaction() as files:
        files.write_release_file("raw", "level-1.md", "# L1\n")
    assert store.tree_hash() != first


# ---- create ----


def test_create_refuses_existing_dataset(store: DatasetStore, scope_record: dict[str, Any]) -> None:
    with pytest.raises(DatasetExistsError):
        store.create(validate_record(ScopeRecord, scope_record))


def test_create_validates_scope_first(tmp_path: Path, scope_record: dict[str, Any]) -> None:
    store = DatasetStore(tmp_path, "pets")
    scope = validate_record(ScopeRecord, scope_record).model_copy(update={"purpose": " "})
    with pytest.raises(RecordInvalidError, match="purpose"):
        store.create(scope)
    assert not store.root.exists()
