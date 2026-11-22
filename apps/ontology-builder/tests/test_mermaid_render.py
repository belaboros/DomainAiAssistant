"""Every Mermaid diagram of ``level-N.md`` renders with the Mermaid CLI (plan 0002, T15: AC-30).

Marker ``mermaid``: needs Node, ``npm ci`` at the repo root (``@mermaid-js/mermaid-cli``) and a
headless Chromium for puppeteer. Run: ``uv run pytest -m mermaid``.
"""

from __future__ import annotations

import json
import re
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


def _taxonomies(level: str) -> list[str]:
    part = level.split("## Taxonomy", 1)[1].split("## Concepts and relations", 1)[0]
    return re.findall(r"```mermaid\n(.*?)```", part, re.S)


def _ratio(mmdc: Path, folder: Path, name: str, source: str) -> float:
    (folder / f"{name}.mmd").write_text(source, encoding="utf-8")
    config = folder / "puppeteer.json"
    config.write_text(json.dumps({"args": ["--no-sandbox"]}), encoding="utf-8")
    svg = folder / f"{name}.svg"
    command = [
        str(mmdc),
        "-q",
        "-p",
        str(config),
        "-i",
        str(folder / f"{name}.mmd"),
        "-o",
        str(svg),
    ]
    subprocess.run(command, capture_output=True, check=True, timeout=600)  # noqa: S603
    box = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', svg.read_text("utf-8"))
    assert box is not None
    return float(box.group(1)) / float(box.group(2))


@pytest.mark.parametrize("loners", [20, 60])
def test_taxonomy_is_close_to_16_9(
    mmdc: Path, tmp_path: Path, review_kit: Any, loners: int
) -> None:
    """Q65: a taxonomy with many unlinked concepts renders near 16:9, not as one wide row."""
    pet = review_kit.element("concept", label="pet")
    pets = [review_kit.element("concept", label=n, parents=[pet["id"]]) for n in ("cat", "dog")]
    rest = [review_kit.element("concept", label=f"concept number {n:02}") for n in range(loners)]
    review_kit.seed([pet, *pets, *rest])
    changes = ChangeSet.load(review_kit.store)
    scope = review_kit.store.read().scope()
    release = ReleaseInput(scope, list(changes.elements.values()), {}, "raw", "raw+0000000")
    level = build_level_files(release)["level-1.md"]
    boxed = [source for source in _taxonomies(level) if "subgraph unlinked" in source]
    assert boxed
    for n, source in enumerate(boxed):  # a small tree without a box is as wide as it is
        ratio = _ratio(mmdc, tmp_path, f"taxonomy-{loners}-{n}", source)
        assert 1.3 <= ratio <= 2.3, f"diagram {n}: {ratio:.2f}"


def test_wide_family_wraps_into_rows(mmdc: Path, tmp_path: Path, review_kit: Any) -> None:
    """Q65: a parent with many children does not draw them as one wide row."""
    dog = review_kit.element("concept", label="dog")
    kinds = [
        review_kit.element("concept", label=f"dog kind {n:02}", parents=[dog["id"]])
        for n in range(14)
    ]
    review_kit.seed([dog, *kinds])
    changes = ChangeSet.load(review_kit.store)
    scope = review_kit.store.read().scope()
    release = ReleaseInput(scope, list(changes.elements.values()), {}, "raw", "raw+0000000")
    [taxonomy] = _taxonomies(build_level_files(release)["level-1.md"])
    assert "~~~" in taxonomy
    ratio = _ratio(mmdc, tmp_path, "family", taxonomy)
    assert 1.3 <= ratio <= 2.3, f"{ratio:.2f}"
