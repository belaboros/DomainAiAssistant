"""The dataset and release layout of FR-30 / FR-31 (plan 0002: T4 dataset layout; T16 releases)."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import jsonschema
from ontology_builder.model import ELEMENT_TYPES, ScopeRecord, validate_record
from ontology_builder.release import BuildInfo, publish
from ontology_builder.store import DatasetStore

FR30_FOLDERS = [
    "00_sources",
    "00_sources/90_user_statements",
    "01_model",
    *(f"01_model/elements/{t}" for t in sorted(ELEMENT_TYPES)),
    "02_decisions",
    "02_decisions/runs",
    "03_release",
    "03_release/00_raw",
    "03_release/01_governed",
]


def test_dataset_layout(tmp_path: Path, scope_record: dict[str, Any]) -> None:
    """AC-28 (layout): a new dataset has every folder of FR-30 and its scope record."""
    store = DatasetStore(tmp_path, "pets-and-house-rules")
    store.create(validate_record(ScopeRecord, scope_record))
    root = tmp_path / "ontology-pets-and-house-rules"
    assert store.root == root
    for folder in FR30_FOLDERS:
        assert (root / folder).is_dir(), folder
    assert (root / "01_model" / "scope.yaml").is_file()
    top = sorted(p.name for p in root.iterdir())
    assert top == ["00_sources", "01_model", "02_decisions", "03_release"]
    empty_leaves = [p for p in root.rglob("*") if p.is_dir() and not any(p.iterdir())]
    assert empty_leaves == [], "every empty folder keeps a .gitkeep so git keeps the layout"


RELEASE_FILES = ["level-1.md", "level-2.md", "level-3.md", "manifest.json", "ontology.ttl"]
MANIFEST_SCHEMA = Path(__file__).parents[3] / "libs/contracts/ontology/manifest.schema.json"


def test_release_files_and_manifest_checksums(review_kit: Any) -> None:
    """AC-28: both release folders hold the files of FR-31 and a manifest that matches them."""
    concept = review_kit.concept("approved", snapshot=True)
    review_kit.seed([concept, review_kit.concept("proposed"), review_kit.element("rule")])
    built_at = datetime(2026, 11, 21, 12, 0, tzinfo=UTC)
    info = BuildInfo(source_commit="89abcdef0123456789abcdef0123456789abcdef", built_at=built_at)
    with review_kit.store.transaction() as files:
        result = publish(files, info, "1.0.0")
    assert result.governed is not None

    schema = json.loads(MANIFEST_SCHEMA.read_text(encoding="utf-8"))
    for variant, extra in (("raw", []), ("governed", ["CHANGELOG.md"])):
        folder = review_kit.store.read().release_files(variant)
        assert sorted(folder) == sorted([*RELEASE_FILES, *extra]), variant
        manifest = json.loads(folder["manifest.json"])
        jsonschema.validate(manifest, schema, format_checker=jsonschema.FormatChecker())
        assert manifest["ontology"] == "pets-and-house-rules"
        assert manifest["variant"] == variant
        assert manifest["source_commit"] == info.source_commit
        assert manifest["built_at"] == "2026-11-21T12:00:00Z"
        expected = {
            name: "sha256:" + hashlib.sha256(data).hexdigest()
            for name, data in folder.items()
            if name != "manifest.json"
        }
        assert manifest["files"] == expected, variant
    raw = json.loads(review_kit.store.read().release_files("raw")["manifest.json"])
    governed = json.loads(review_kit.store.read().release_files("governed")["manifest.json"])
    assert raw["version"] == "raw+89abcde"
    assert governed["version"] == "1.0.0"
    assert raw["counts"]["by_status"] == {
        "approved": 1,
        "deprecated": 0,
        "included": 0,
        "proposed": 2,
    }
    assert governed["counts"]["by_type"]["concept"] == 1
    assert governed["counts"]["by_status"] == {"approved": 1, "deprecated": 0}
