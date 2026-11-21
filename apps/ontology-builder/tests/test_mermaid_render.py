"""Every Mermaid diagram of ``level-N.md`` renders with the Mermaid CLI (plan 0002, T15: AC-30).

Marker ``mermaid``: needs Node, ``npm ci`` at the repo root (``@mermaid-js/mermaid-cli``) and a
headless Chromium for puppeteer. Run: ``uv run pytest -m mermaid``.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest
from ontology_builder.governance import ChangeSet
from ontology_builder.model import ScopeRecord, validate_record
from ontology_builder.release import ReleaseInput, build_level_files

pytestmark = pytest.mark.mermaid

REPO = Path(__file__).resolve().parents[3]
MMDC = REPO / "node_modules" / ".bin" / "mmdc"


def _render(folder: Path, name: str, text: str) -> None:
    source = folder / name
    source.write_text(text, encoding="utf-8")
    config = folder / "puppeteer.json"
    config.write_text(json.dumps({"args": ["--no-sandbox"]}), encoding="utf-8")
    out = folder / "out"
    out.mkdir(exist_ok=True)
    command = [str(MMDC), "-q", "-p", str(config), "-i", str(source), "-o", str(out / name)]
    result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=600)  # noqa: S603
    assert result.returncode == 0, f"{name}: {result.stderr[-2000:]}"
    svgs = list(out.glob(f"{source.stem}-*.svg"))
    assert len(svgs) == text.count("```mermaid"), name


@pytest.fixture(scope="module")
def mmdc() -> Path:
    if not MMDC.exists():
        pytest.fail("the Mermaid CLI is missing: run `npm ci` at the repository root")
    return MMDC


@pytest.mark.parametrize("variant", ["raw", "governed"])
def test_pet_level_diagrams_render(
    mmdc: Path, tmp_path: Path, pet_kit: Any, pet_extraction: Any, variant: str
) -> None:
    scope = validate_record(ScopeRecord, pet_kit.scope)
    version = "raw+0000000" if variant == "raw" else "1.0.0"
    release = ReleaseInput(scope, pet_extraction.elements, pet_extraction.units, variant, version)
    for name, text in build_level_files(release).items():
        _render(tmp_path, f"{variant}-{name}", text)


def test_escaped_labels_and_draft_edges_render(mmdc: Path, tmp_path: Path, review_kit: Any) -> None:
    odd = review_kit.element("concept", "approved", label='the "lead" <2 m> & co')
    plain = review_kit.element("concept", label="dog # 1; end", parents=[odd["id"]])
    relations = [
        review_kit.element("relation", status, subject=odd["id"], object=plain["id"])
        | {"predicate_label": 'is "tied" to'}
        for status in ("approved", "proposed")
    ]
    review_kit.seed([odd, plain, *relations])
    changes = ChangeSet.load(review_kit.store)
    scope = review_kit.store.read().scope()
    release = ReleaseInput(scope, list(changes.elements.values()), {}, "raw", "raw+0000000")
    _render(tmp_path, "odd.md", build_level_files(release)["level-1.md"])
