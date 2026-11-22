"""Mermaid diagrams of one level: taxonomy and concept-relation (plan 0002, ``level-N.md``).

A diagram with more than ``MAX_NODES`` nodes is split into one diagram per top-level concept (a
concept with no parent in the level). In a taxonomy, the concepts without an is-a link in the
diagram go into a "Not linked yet" box, ``BOX_COLUMNS`` per row, so they don't stretch the diagram
into one long row (Q64). Elements that are not approved get the dashed ``draft``
class (nodes) or a dotted arrow (relations); only the raw release has any.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from markupsafe import Markup

from ontology_builder.model import Concept, Relation

MAX_NODES = 40
BOX_COLUMNS = 5
"""Concepts per row in the "Not linked yet" box of a taxonomy."""
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

    def render(
        self, direction: str, nodes: Iterable[str], edges: list[Markup], boxed: Sequence[str] = ()
    ) -> Markup:
        ordered = self.ordered(nodes)
        body = [_CLASS_DEF, *(self.node(i) for i in ordered if i not in boxed)]
        body += edges
        body += _box_lines(self, boxed)
        drafts = [i for i in ordered if i in self.drafts]
        if drafts:
            body.append(Markup("class {} draft").format(",".join(drafts)))
        head = Markup("flowchart {}\n").format(direction)
        return head + Markup("").join(_INDENT + line + Markup("\n") for line in body)


def _box_lines(level: _Level, boxed: Sequence[str]) -> list[Markup]:
    """A left-to-right subgraph whose rows are chains of invisible links, ``BOX_COLUMNS`` long;
    unlinked chains stack, so the box is a grid (Mermaid may order the rows its own way)."""
    if not boxed:
        return []
    lines = [Markup('subgraph unlinked["Not linked yet"]'), Markup("direction LR")]
    lines += [_INDENT + level.node(i) for i in boxed]
    rows = [boxed[start : start + BOX_COLUMNS] for start in range(0, len(boxed), BOX_COLUMNS)]
    lines += [_INDENT + Markup(" ~~~ ").join(row) for row in rows if len(row) > 1]
    return [*lines, Markup("end")]


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
        boxed = level.ordered(nodes - linked)
        edges = [Markup("{} --> {}").format(parent, child) for parent, child in links]
        return Diagram(title, level.render("TB", nodes, edges, boxed))

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


def _edge(relation: Relation, drafts: set[str]) -> Markup:
    arrow = _DRAFT_EDGE if relation.id in drafts else _EDGE
    return arrow.format(relation.subject, mermaid_label(relation.predicate_label), relation.object)


def _ends(relations: Iterable[Relation]) -> set[str]:
    return {end for relation in relations for end in (relation.subject, relation.object)}


def _relation_groups(
    level: _Level, shown: list[Relation]
) -> list[tuple[str | None, list[Relation]]]:
    """One group when the diagram is small enough, else one per top-level concept of the subject."""
    if len(_ends(shown)) <= MAX_NODES:
        return [(None, shown)]
    groups: dict[str, list[Relation]] = {}
    for relation in shown:
        groups.setdefault(level.top_of(relation.subject), []).append(relation)
    return [
        (f"Relations under {level.by_id[top].label}", groups[top]) for top in level.ordered(groups)
    ]


def relation_diagrams(
    concepts: Sequence[Concept], relations: Sequence[Relation], drafts: set[str]
) -> list[Diagram]:
    """Concepts and the relations between them (``flowchart LR``), split when too large."""
    level = _Level(concepts, drafts)
    shown = [r for r in relations if r.subject in level.by_id and r.object in level.by_id]
    shown.sort(key=lambda r: (r.subject, r.object, r.id))
    if not shown:
        return [Diagram(None, _NO_RELATIONS)]
    return [
        Diagram(title, level.render("LR", _ends(group), [_edge(r, drafts) for r in group]))
        for title, group in _relation_groups(level, shown)
    ]
