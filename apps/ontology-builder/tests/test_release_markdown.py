"""The ``level-N.md`` builder: diagrams, catalogues, evidence (plan 0002, T15: AC-30)."""

from __future__ import annotations

import re
from typing import Any

from ontology_builder.governance import ChangeSet
from ontology_builder.model import Concept, Element, ScopeRecord, validate_record
from ontology_builder.release import ReleaseInput, build_level_files, level_elements
from ontology_builder.release.mermaid import box_columns

LEVEL_FILES = ["level-1.md", "level-2.md", "level-3.md"]
_LINK = re.compile(r"\]\(#([a-z]+_[0-9A-Z]+)\)")
_ANCHOR = re.compile(r'<a id="([a-z]+_[0-9A-Z]+)"></a>')
_MERMAID = re.compile(r"```mermaid\n(.*?)```", re.S)
_NODE = re.compile(r"^\s+(cn_[0-9A-Z]+)\[", re.M)


def pet_release(pet_kit: Any, pet_extraction: Any, variant: str = "raw") -> ReleaseInput:
    scope = validate_record(ScopeRecord, pet_kit.scope)
    version = "raw+0000000" if variant == "raw" else "1.0.0"
    return ReleaseInput(scope, pet_extraction.elements, pet_extraction.units, variant, version)


def kit_release(kit: Any, variant: str = "raw", version: str = "raw+0000000") -> ReleaseInput:
    changes = ChangeSet.load(kit.store)
    scope = kit.store.read().scope()
    return ReleaseInput(
        scope, list(changes.elements.values()), changes.statements, variant, version
    )


def diagrams(text: str, kind: str) -> list[str]:
    return [d for d in _MERMAID.findall(text) if d.startswith(f"flowchart {kind}")]


def test_each_level_has_taxonomy_and_relation_diagrams_and_catalogues(
    pet_kit: Any, pet_extraction: Any
) -> None:
    files = build_level_files(pet_release(pet_kit, pet_extraction))
    assert sorted(files) == LEVEL_FILES
    for name, text in files.items():
        assert text.startswith("# pets-and-house-rules"), name
        assert "raw+0000000" in text.splitlines()[2], name
        assert diagrams(text, "TB"), f"{name}: no taxonomy diagram"
        assert diagrams(text, "LR"), f"{name}: no concept-relation diagram"
        sections = re.findall(r"^## (.+)$", text, re.M)
        assert sections[:2] == ["Taxonomy", "Concepts and relations"], name
        assert {"Concepts", "Relations", "Rules", "Evidence"} <= set(sections), name
        assert sections[-1] == "Evidence", name
    concepts = [e for e in level_elements(pet_extraction.elements, "level-3") if _concept(e)]
    for concept in concepts:
        assert f'<a id="{concept.id}"></a>' in files["level-3.md"], concept.label


def _concept(element: Element) -> bool:
    return isinstance(element, Concept)


def test_evidence_links_resolve_to_unit_ids(pet_kit: Any, pet_extraction: Any) -> None:
    release = pet_release(pet_kit, pet_extraction)
    for name, text in build_level_files(release).items():
        anchors = set(_ANCHOR.findall(text))
        links = set(_LINK.findall(text))
        assert links <= anchors, f"{name}: links without an anchor: {sorted(links - anchors)[:3]}"
        unit_anchors = {a for a in anchors if a.startswith("su_")}
        level = name.removesuffix(".md")
        cited = {e.unit for x in level_elements(release.elements, level) for e in x.evidence}
        assert unit_anchors == cited, name
        assert unit_anchors <= set(release.units), name
        assert {link for link in links if link.startswith("su_")} == cited, name


def test_raw_marks_non_approved(review_kit: Any) -> None:
    approved = review_kit.concept("approved", snapshot=True) | {"label": "dog"}
    included = review_kit.element("concept", "included", label="lead")
    proposed = review_kit.element("concept", "proposed", label="stairwell")
    relation = review_kit.element(
        "relation", "approved", subject=approved["id"], object=included["id"], label="walks on"
    )
    review_kit.seed([approved, included, proposed, relation])

    level = build_level_files(kit_release(review_kit))["level-1.md"]
    assert re.search(r"^### stairwell · ● proposed$", level, re.M)
    assert re.search(r"^### lead · ◐ waiting for approval$", level, re.M)
    assert re.search(r"^### dog$", level, re.M)
    for diagram in diagrams(level, "TB") + diagrams(level, "LR"):
        assert "classDef draft stroke-dasharray: 5 5" in diagram
        drafts = set(re.findall(r"^\s+class (.+) draft$", diagram, re.M))
        flat = {node for line in drafts for node in line.split(",")}
        assert approved["id"] not in flat
        assert included["id"] in flat or included["id"] not in diagram
    [taxonomy] = diagrams(level, "TB")
    assert {included["id"], proposed["id"]} <= {
        n for line in re.findall(r"^\s+class (.+) draft$", taxonomy, re.M) for n in line.split(",")
    }

    governed = build_level_files(kit_release(review_kit, "governed", "1.0.0"))["level-1.md"]
    assert "●" not in governed and "◐" not in governed
    assert not re.search(r"^\s+class .+ draft$", governed, re.M)


def test_large_diagram_split_by_top_level_concept(review_kit: Any) -> None:
    roots = [review_kit.element("concept", label=label) for label in ("animal", "building")]
    children = [
        review_kit.element("concept", label=f"{root['label']} {n:02}", parents=[root["id"]])
        for root in roots
        for n in range(25)
    ]
    loner = review_kit.element("concept", label="rule book")
    review_kit.seed([*roots, *children, loner])

    level = build_level_files(kit_release(review_kit))["level-1.md"]
    taxonomies = diagrams(level, "TB")
    assert len(taxonomies) == 3, "one per top-level concept with children, one for the rest"
    nodes = [set(_NODE.findall(d)) for d in taxonomies]
    assert all(len(n) <= 40 for n in nodes)
    assert {roots[0]["id"], *(c["id"] for c in children[:25])} in nodes
    assert {loner["id"]} in nodes
    assert "### Taxonomy of animal" in level, "a split diagram is named after its top concept"


def test_small_diagram_not_split(review_kit: Any) -> None:
    root = review_kit.element("concept", label="animal")
    child = review_kit.element("concept", label="dog", parents=[root["id"]])
    review_kit.seed([root, child])
    level = build_level_files(kit_release(review_kit))["level-1.md"]
    [taxonomy] = diagrams(level, "TB")
    assert f"{root['id']} --> {child['id']}" in taxonomy


def test_mermaid_labels_are_escaped(review_kit: Any) -> None:
    concept = review_kit.element("concept", label='the "lead" <2 m> & co')
    review_kit.seed([concept])
    level = build_level_files(kit_release(review_kit))["level-1.md"]
    [taxonomy] = diagrams(level, "TB")
    assert f'{concept["id"]}["the #quot;lead#quot; #lt;2 m#gt; #amp; co"]' in taxonomy
    assert "### the &quot;lead&quot; &lt;2 m&gt; &amp; co" not in level
    assert '### the "lead" &lt;2 m&gt; &amp; co' in level, "HTML is escaped, quotes are kept"


def test_large_relation_diagram_split_by_top_level_concept(review_kit: Any) -> None:
    roots = [review_kit.element("concept", label=label) for label in ("animal", "building")]
    children = [
        review_kit.element("concept", label=f"{root['label']} {n:02}", parents=[root["id"]])
        for root in roots
        for n in range(21)
    ]
    relations = [
        review_kit.element("relation", subject=child["parents"][0], object=child["id"])
        for child in children
    ]
    review_kit.seed([*roots, *children, *relations])

    level = build_level_files(kit_release(review_kit))["level-1.md"]
    split = diagrams(level, "LR")
    assert len(split) == 2
    assert all(len(set(_NODE.findall(d))) == 22 for d in split)
    assert "### Relations under animal" in level
    assert "### Relations under building" in level


def _rows(taxonomy: str) -> list[list[str]]:
    """The rows of the "Not linked yet" box: its chains of invisible ``a ~~~ b`` links."""
    box = taxonomy.split('subgraph unlinked["Not linked yet"]', 1)[1].split("    end", 1)[0]
    assert "direction LR" in box
    chains = [line for line in box.splitlines() if "~~~" in line]
    return [re.findall(r"cn_[0-9A-Z]+", line) for line in chains]


def test_unlinked_concepts_are_wrapped_in_rows(review_kit: Any) -> None:
    """Q64, Q65: concepts without an is-a link in the level go into a box of rows below the tree."""
    pet = review_kit.element("concept", label="pet")
    dog = review_kit.element("concept", label="dog", parents=[pet["id"]])
    loners = [review_kit.element("concept", label=f"loner {n:02}") for n in range(20)]
    review_kit.seed([pet, dog, *loners])
    level = build_level_files(kit_release(review_kit))["level-1.md"]
    [taxonomy] = diagrams(level, "TB")
    assert f"{pet['id']} --> {dog['id']}" in taxonomy
    rows = _rows(taxonomy)
    assert len(rows) > 1, "never one single wide row"
    width = len(rows[0])
    assert all(len(row) == width for row in rows[:-1]) and 0 < len(rows[-1]) <= width
    assert [node for row in rows for node in row] == [loner["id"] for loner in loners]
    box = taxonomy.split("subgraph", 1)[1].split("    end", 1)[0]
    assert pet["id"] not in box and dog["id"] not in box, "linked concepts stay outside the box"
    assert f"{dog['id']} ~~~ unlinked" in taxonomy, "the box sits below the tree"


def test_box_columns_aim_at_16_9() -> None:
    """More concepts give more columns; a wide tree lets the box use its width."""
    assert box_columns(6, 0, 0) < box_columns(20, 0, 0) < box_columns(60, 0, 0)
    for count in (6, 20, 40, 80):
        assert -(-count // box_columns(count, 0, 0)) > 1, f"{count}: more than one row"
    assert box_columns(20, 0, 0, wrapped_share=1.0) >= box_columns(20, 0, 0)  # taller rows
    assert box_columns(20, 2000, 300) >= box_columns(20, 0, 0)  # fills a wide tree


def test_linked_only_taxonomy_has_no_box(review_kit: Any) -> None:
    root = review_kit.element("concept", label="animal")
    child = review_kit.element("concept", label="dog", parents=[root["id"]])
    review_kit.seed([root, child])
    [taxonomy] = diagrams(build_level_files(kit_release(review_kit))["level-1.md"], "TB")
    assert "subgraph" not in taxonomy and "~~~" not in taxonomy


def _relation_diagram(level: str) -> str:
    [relations] = diagrams(level, "LR")
    return relations


def test_relation_diagram_shows_is_a_edges(review_kit: Any) -> None:
    """Q65: is-a links between concepts of the level also appear in the concept-relation diagram."""
    pet = review_kit.element("concept", label="pet")
    dog = review_kit.element("concept", label="dog", parents=[pet["id"]])
    owner = review_kit.element("concept", label="owner")
    owns = review_kit.element("relation", subject=owner["id"], object=pet["id"]) | {
        "predicate_label": "owns"
    }
    review_kit.seed([pet, dog, owner, owns])
    relations = _relation_diagram(build_level_files(kit_release(review_kit))["level-1.md"])
    assert f'{dog["id"]} -. "is a" .-> {pet["id"]}' in relations  # a proposed child: dotted
    assert f'{owner["id"]} -. "owns" .-> {pet["id"]}' in relations


def test_is_a_alone_makes_a_relation_diagram(review_kit: Any) -> None:
    pet = review_kit.element("concept", "approved", snapshot=True, label="pet")
    cat = review_kit.element("concept", "approved", snapshot=True, label="cat", parents=[pet["id"]])
    review_kit.seed([pet, cat])
    relations = _relation_diagram(build_level_files(kit_release(review_kit))["level-1.md"])
    assert f'{cat["id"]} -- "is a" --> {pet["id"]}' in relations
    assert "No relations at this level" not in relations


def test_siblings_wrap_into_rows(review_kit: Any) -> None:
    """Q65: many children of one parent are stacked in rows by invisible links."""
    dog = review_kit.element("concept", label="dog")
    kinds = [
        review_kit.element("concept", label=f"kind {n:02}", parents=[dog["id"]]) for n in range(12)
    ]
    review_kit.seed([dog, *kinds])
    [taxonomy] = diagrams(build_level_files(kit_release(review_kit))["level-1.md"], "TB")
    for kind in kinds:
        assert f"{dog['id']} --> {kind['id']}" in taxonomy
    stacked = re.findall(r"(cn_[0-9A-Z]+) ~~~ (cn_[0-9A-Z]+)", taxonomy)
    ids = [kind["id"] for kind in kinds]
    width = ids.index(stacked[0][1]) - ids.index(stacked[0][0])
    assert 1 < width < 12
    assert stacked == [(ids[n], ids[n + width]) for n in range(12 - width)]
