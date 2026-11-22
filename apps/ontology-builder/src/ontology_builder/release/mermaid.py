"""Mermaid diagrams of one level: taxonomy and concept-relation (plan 0002, ``level-N.md``).

A diagram with more than ``MAX_NODES`` nodes is split into one diagram per top-level concept (a
concept with no parent in the level). In a taxonomy, the concepts without an is-a link in the
diagram go into a "Not linked yet" box below the tree, in rows whose length aims the whole
diagram at 16:9, so a preview scaled to the page width stays readable (Q64, Q65). The
concept-relation diagram shows the is-a links too, as "is a" edges from child to parent (Q65).
Elements that are not approved get the dashed ``draft`` class (nodes) or a dotted arrow
(relations); only the raw release has any.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import NamedTuple

from markupsafe import Markup

from ontology_builder.model import Concept, Relation

MAX_NODES = 40
ASPECT = 16 / 9
"""The width-to-height ratio a taxonomy aims at."""
# Sizes of a rendered flowchart with Mermaid's defaults, in pixels, measured with the Mermaid CLI
# (2026-11-22): a box column, a row of one-line labels, the extra height of a two-line label
# (labels longer than _WRAP characters wrap), a tree rank, and the frame around a diagram.
_BOX_COLUMN = 176
_BOX_ROW = 69
_WRAPPED_ROW = 21
_WRAP = 15
_TREE_COLUMN = 176
_TREE_RANK = 100
_FRAME = 64
# A wrapped family (one parent, its children in rows), measured the same way: a column, the room
# an edge to a lower row takes when it cannot pass between the nodes of a row, and a rank.
_FAMILY_COLUMN = 192
_PASSING_EDGE = 38
_FAMILY_RANK = 100
_FAMILY_ONE_ROW = 4
"""A family of at most this many children always stays on one row."""
_IS_A = "is a"
_INDENT = Markup("    ")
_ESCAPES = (("&", "#amp;"), ('"', "#quot;"), ("<", "#lt;"), (">", "#gt;"))
_CLASS_DEF = Markup("classDef draft stroke-dasharray: 5 5")
_NODE = Markup('{}["{}"]')
_EDGE = Markup('{} -- "{}" --> {}')
_DRAFT_EDGE = Markup('{} -. "{}" .-> {}')
_NO_RELATIONS = Markup('flowchart LR\n    none["No relations at this level"]\n')


@dataclass(frozen=True)
class Diagram:
    """One Mermaid diagram; ``title`` names the top-level concept when a diagram was split.

    ``source`` is Markup: it holds only element IDs, fixed syntax and labels that went through
    ``mermaid_label``, which leaves no HTML special character in them.
    """

    title: str | None
    source: Markup


def mermaid_label(text: str) -> str:
    """Text as a quoted Mermaid node or edge label (entity codes, one line)."""
    for raw, code in _ESCAPES:
        text = text.replace(raw, code)
    return " ".join(text.split())


class _Level:
    """The concepts of one level, their is-a links inside the level, and which are drafts."""

    def __init__(self, concepts: Sequence[Concept], drafts: set[str]) -> None:
        self.by_id = {concept.id: concept for concept in concepts}
        self.drafts = drafts
        self.parents = {
            c.id: sorted(p for p in c.parents or [] if p in self.by_id) for c in concepts
        }
        self.children: dict[str, list[str]] = {concept_id: [] for concept_id in self.by_id}
        for child, parents in self.parents.items():
            for parent in parents:
                self.children[parent].append(child)

    def ordered(self, ids: Iterable[str]) -> list[str]:
        return sorted(ids, key=lambda i: (self.by_id[i].label.casefold(), i))

    def roots(self) -> list[str]:
        return self.ordered(i for i, parents in self.parents.items() if not parents)

    def subtree(self, root: str) -> set[str]:
        found, todo = {root}, [root]
        while todo:
            for child in self.children[todo.pop()]:
                if child not in found:
                    found.add(child)
                    todo.append(child)
        return found

    def top_of(self, concept_id: str) -> str:
        """The top-level concept above ``concept_id``, following the first parent."""
        seen = {concept_id}
        while self.parents[concept_id] and self.parents[concept_id][0] not in seen:
            concept_id = self.parents[concept_id][0]
            seen.add(concept_id)
        return concept_id

    def node(self, concept_id: str) -> Markup:
        return _NODE.format(concept_id, mermaid_label(self.by_id[concept_id].label))

    def depths(self, nodes: set[str]) -> dict[str, int]:
        """The rank of each node in the diagram's tree: 0 for a node without a parent in it."""
        found: dict[str, int] = {}

        def depth(node: str, seen: frozenset[str]) -> int:
            if node not in found:
                parents = [p for p in self.parents[node] if p in nodes and p not in seen]
                found[node] = 1 + max((depth(p, seen | {node}) for p in parents), default=-1)
            return found[node]

        for node in nodes:
            depth(node, frozenset())
        return found

    def render(
        self, direction: str, nodes: Iterable[str], edges: list[Markup], box: _Box | None = None
    ) -> Markup:
        ordered = self.ordered(nodes)
        boxed = set(box.nodes) if box else set()
        body = [_CLASS_DEF, *(self.node(i) for i in ordered if i not in boxed)]
        body += edges
        body += _box_lines(self, box)
        drafts = [i for i in ordered if i in self.drafts]
        if drafts:
            body.append(Markup("class {} draft").format(",".join(drafts)))
        head = Markup("flowchart {}\n").format(direction)
        return head + Markup("").join(_INDENT + line + Markup("\n") for line in body)


@dataclass(frozen=True)
class _Box:
    """The "Not linked yet" box: its concepts, row length, and the tree node it hangs below."""

    nodes: Sequence[str]
    columns: int
    below: str | None


def box_columns(
    count: int, tree_width: float, tree_height: float, wrapped_share: float = 0.0
) -> int:
    """The row length that brings a box of ``count`` concepts under a tree closest to 16:9.

    ``wrapped_share`` is the share of labels that wrap onto two lines; a row is as tall as its
    tallest label. Rows never get shorter than the tree is wide: filling that width costs nothing.
    """

    def distance(columns: int) -> float:
        row = _BOX_ROW + _WRAPPED_ROW * (1 - (1 - wrapped_share) ** columns)
        width = max(columns * _BOX_COLUMN, tree_width) + _FRAME
        height = tree_height + math.ceil(count / columns) * row + _FRAME
        return abs(math.log(width / height / ASPECT))

    fits = min(max(count, 1), max(1, int(tree_width // _BOX_COLUMN)))
    return min(range(fits, max(count, 1) + 1), key=distance)


def _box_lines(level: _Level, box: _Box | None) -> list[Markup]:
    """A left-to-right subgraph whose rows are chains of invisible links; unlinked chains stack,
    so the box is a grid (Mermaid may order the rows its own way). An invisible link from the
    deepest tree node puts the box below the tree."""
    if box is None or not box.nodes:
        return []
    lines = [Markup('subgraph unlinked["Not linked yet"]'), Markup("direction LR")]
    lines += [_INDENT + level.node(i) for i in box.nodes]
    step = box.columns
    rows = [box.nodes[start : start + step] for start in range(0, len(box.nodes), step)]
    lines += [_INDENT + Markup(" ~~~ ").join(row) for row in rows if len(row) > 1]
    lines.append(Markup("end"))
    if box.below is not None:
        lines.append(Markup("{} ~~~ unlinked").format(box.below))
    return lines


def sibling_columns(count: int) -> int:
    """How many of ``count`` children of one parent go side by side, aiming the family at 16:9.

    Edges to the lower rows run past the first row; once they outnumber its gaps they widen it.
    """
    if count <= _FAMILY_ONE_ROW:
        return max(count, 1)

    def distance(columns: int) -> float:
        width = columns * _FAMILY_COLUMN + _PASSING_EDGE * max(0, count - 2 * columns)
        height = (1 + math.ceil(count / columns)) * _FAMILY_RANK
        return abs(math.log(width / height / ASPECT))

    return min(range(2, count + 1), key=distance)


def _sibling_rows(level: _Level, nodes: set[str]) -> list[Markup]:
    """Invisible links that stack a large family's children in rows (child n above n + width)."""
    lines = []
    for parent in level.ordered(nodes):
        children = level.ordered(c for c in level.children[parent] if c in nodes)
        width = sibling_columns(len(children))
        lines += [
            Markup("{} ~~~ {}").format(children[n], children[n + width])
            for n in range(len(children) - width)
        ]
    return lines


def _taxonomy_box(level: _Level, nodes: set[str], linked: set[str]) -> _Box | None:
    boxed = level.ordered(nodes - linked)
    if not boxed:
        return None
    depths = level.depths(linked)
    per_rank: dict[int, int] = {}
    for rank in depths.values():
        per_rank[rank] = per_rank.get(rank, 0) + 1
    tree_width = max(per_rank.values(), default=0) * _TREE_COLUMN
    tree_height = len(per_rank) * _TREE_RANK
    deepest = level.ordered(n for n, rank in depths.items() if rank == max(per_rank, default=0))
    below = deepest[-1] if deepest else None
    wrapped = sum(len(level.by_id[n].label) > _WRAP for n in boxed) / len(boxed)
    return _Box(boxed, box_columns(len(boxed), tree_width, tree_height, wrapped), below)


def taxonomy_diagrams(concepts: Sequence[Concept], drafts: set[str]) -> list[Diagram]:
    """The is-a taxonomy (``flowchart TB``, parent above child), split when it is too large."""
    level = _Level(concepts, drafts)

    def diagram(title: str | None, nodes: set[str]) -> Diagram:
        links = [
            (parent, child)
            for child in level.ordered(nodes)
            for parent in level.parents[child]
            if parent in nodes
        ]
        linked = {end for link in links for end in link}
        edges = [Markup("{} --> {}").format(parent, child) for parent, child in links]
        edges += _sibling_rows(level, linked)
        box = _taxonomy_box(level, nodes, linked)
        return Diagram(title, level.render("TB", nodes, edges, box))

    if len(level.by_id) <= MAX_NODES:
        return [diagram(None, set(level.by_id))]
    found, covered = [], set()
    for root in level.roots():
        if level.children[root]:
            nodes = level.subtree(root)
            covered |= nodes
            found.append(diagram(f"Taxonomy of {level.by_id[root].label}", nodes))
    rest = level.ordered(set(level.by_id) - covered)
    for start in range(0, len(rest), MAX_NODES):
        found.append(diagram("Other concepts", set(rest[start : start + MAX_NODES])))
    return found


class _Link(NamedTuple):
    """One edge of the concept-relation diagram: a relation, or an is-a link (child → parent)."""

    subject: str
    label: str
    object: str
    draft: bool


def _edge(link: _Link) -> Markup:
    arrow = _DRAFT_EDGE if link.draft else _EDGE
    return arrow.format(link.subject, mermaid_label(link.label), link.object)


def _ends(links: Iterable[_Link]) -> set[str]:
    return {end for link in links for end in (link.subject, link.object)}


def _links(level: _Level, relations: Sequence[Relation]) -> list[_Link]:
    """The relations between concepts of the level, and the level's is-a links."""
    shown = [
        _Link(r.subject, r.predicate_label, r.object, r.id in level.drafts)
        for r in relations
        if r.subject in level.by_id and r.object in level.by_id
    ]
    shown += [
        _Link(child, _IS_A, parent, child in level.drafts)
        for child, parents in level.parents.items()
        for parent in parents
    ]
    return sorted(shown, key=lambda link: (link.subject, link.object, link.label))


def _relation_groups(level: _Level, shown: list[_Link]) -> list[tuple[str | None, list[_Link]]]:
    """One group when the diagram is small enough, else one per top-level concept of the subject."""
    if len(_ends(shown)) <= MAX_NODES:
        return [(None, shown)]
    groups: dict[str, list[_Link]] = {}
    for relation in shown:
        groups.setdefault(level.top_of(relation.subject), []).append(relation)
    return [
        (f"Relations under {level.by_id[top].label}", groups[top]) for top in level.ordered(groups)
    ]


def relation_diagrams(
    concepts: Sequence[Concept], relations: Sequence[Relation], drafts: set[str]
) -> list[Diagram]:
    """Concepts with the relations and is-a links between them (``flowchart LR``), split when
    too large."""
    level = _Level(concepts, drafts)
    shown = _links(level, relations)
    if not shown:
        return [Diagram(None, _NO_RELATIONS)]
    return [
        Diagram(title, level.render("LR", _ends(group), [_edge(link) for link in group]))
        for title, group in _relation_groups(level, shown)
    ]
