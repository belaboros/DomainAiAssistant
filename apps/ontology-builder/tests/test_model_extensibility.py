"""A new optional slot never invalidates existing records (plan 0002, T3 and T16: AC-14, FR-15).

T3 checks the records; T16 adds the release half: both releases still build from records that
went through the extended model, and they are the same as before.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml
from ontology_builder.model import ELEMENT_TYPES, SCHEMA_PATH, validate_element
from ontology_builder.release import BuildInfo, build_governed, build_raw

ElementFactory = Callable[[str], dict[str, Any]]
NEW_SLOT = "example_note"


def _schema_with_new_concept_slot(tmp_path: Path) -> Path:
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema["classes"]["Concept"]["attributes"][NEW_SLOT] = {
        "description": "A new optional slot added after records were written."
    }
    path = tmp_path / "extended.yaml"
    path.write_text(yaml.safe_dump(schema, sort_keys=False), encoding="utf-8")
    return path


def _generate_models(schema: Path, tmp_path: Path) -> ModuleType:
    generator = Path(sys.executable).parent / "gen-pydantic"
    code = subprocess.run(  # noqa: S603 - the installed LinkML generator, fixed arguments
        [str(generator), "--meta", "None", "--extra-fields", "forbid", str(schema)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    module_path = tmp_path / "extended_models.py"
    module_path.write_text(code, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("extended_models", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # needed to resolve the forward references
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def extended(tmp_path_factory: pytest.TempPathFactory) -> ModuleType:
    tmp_path = tmp_path_factory.mktemp("extended-schema")
    return _generate_models(_schema_with_new_concept_slot(tmp_path), tmp_path)


def test_new_optional_concept_slot_keeps_records_valid_and_releases_build(
    extended: ModuleType, make_element: ElementFactory, review_kit: Any
) -> None:
    for element_type, current in sorted(ELEMENT_TYPES.items()):
        record = validate_element(element_type, make_element(element_type))
        dumped = record.model_dump(mode="json", exclude_none=True)
        new_class = getattr(extended, current.__name__)
        assert new_class.model_validate(dumped).model_dump(mode="json", exclude_none=True) == dumped
    concept = make_element("concept") | {NEW_SLOT: "set by a newer version"}
    assert getattr(extended.Concept.model_validate(concept), NEW_SLOT) == "set by a newer version"
    _releases_still_build(extended, review_kit)


def _releases_still_build(extended: ModuleType, kit: Any) -> None:
    animal = kit.concept("approved", snapshot=True)
    dog = kit.element("concept", "approved", snapshot=True, parents=[animal["id"]])
    kit.seed([animal, dog, kit.element("rule", "included", refers_to=[dog["id"]])])
    info = BuildInfo("0123456789abcdef0123456789abcdef01234567", datetime(2026, 11, 21, tzinfo=UTC))
    before = (build_raw(kit.store.read(), info).files, build_governed(kit.store.read(), info))

    elements = kit.store.read().elements()
    with kit.store.transaction() as files:
        for element in elements.values():
            dumped = element.model_dump(mode="json", exclude_none=True)
            new_record = getattr(extended, type(element).__name__).model_validate(dumped)
            again = new_record.model_dump(mode="json", exclude_none=True)
            files.write_element(type(element).model_validate(again))
    raw = build_raw(kit.store.read(), info).files
    governed = build_governed(kit.store.read(), info)
    assert raw == before[0]
    assert governed.release.files == before[1].release.files
