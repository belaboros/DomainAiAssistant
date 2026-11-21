"""The governed change log: what changed against the previous governed ``ontology.ttl`` (FR-29).

Each element is compared by its triples (its own, its inlined blank nodes and its SHACL shape),
so any change a reader of the Turtle can see is listed. Entries are kept newest first.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from rdflib import RDFS, BNode, Graph, Literal, URIRef
from rdflib.namespace import OWL, SKOS
from rdflib.term import Node

_ELEMENT_ID = re.compile(r"^((?:st|tm|cn|rl|ru|pr)_[0-9A-HJKMNP-TV-Z]{26})(-shape)?$")
_HEADER = "# Change log of {name}\n\nGoverned releases, newest first.\n"
_SECTIONS = ("Added", "Changed", "Deprecated", "Removed")
_KINDS = ("added", "changed", "deprecated", "removed")


def _canonical(graph: Graph, node: Node) -> object:
    if isinstance(node, BNode):
        return tuple(
            sorted((str(p), _canonical(graph, o)) for p, o in graph.predicate_objects(node))
        )
    return node.n3()


@dataclass
class _Element:
    label: str = ""
    deprecated: bool = False
    triples: set[tuple[str, object]] = field(default_factory=set)


def _element_key(subject: Node, base: str) -> tuple[str, str] | None:
    """(element ID, ``"-shape"`` or ``""``) for an element's IRI or its shape's IRI."""
    if not isinstance(subject, URIRef) or not str(subject).startswith(base):
        return None
    match = _ELEMENT_ID.match(str(subject).removeprefix(base))
    return (match.group(1), match.group(2) or "") if match else None


def _add(graph: Graph, subject: Node, shape: str, element: _Element) -> None:
    for predicate, value in graph.predicate_objects(subject):
        element.triples.add((shape + str(predicate), _canonical(graph, value)))
    if shape:
        return
    label = graph.value(subject, SKOS.prefLabel) or graph.value(subject, RDFS.label)
    element.label = str(label) if label is not None else element.label
    element.deprecated = (subject, OWL.deprecated, Literal(True)) in graph


def _elements(graph: Graph, base: str) -> dict[str, _Element]:
    found: dict[str, _Element] = {}
    for subject in set(graph.subjects()):
        key = _element_key(subject, base)
        if key is not None:
            _add(graph, subject, key[1], found.setdefault(key[0], _Element()))
    return found


@dataclass(frozen=True)
class Changes:
    """Element IDs with their labels, per kind of change."""

    added: list[tuple[str, str]]
    changed: list[tuple[str, str]]
    deprecated: list[tuple[str, str]]
    removed: list[tuple[str, str]]


def _kind(old: _Element | None, new: _Element | None) -> str | None:
    if old is None:
        return "added"
    if new is None:
        return "removed"
    if new.deprecated and not old.deprecated:
        return "deprecated"
    return "changed" if new.triples != old.triples else None


def diff(previous: Graph | None, current: Graph, base: str) -> Changes:
    """The changes from ``previous`` (``None`` before the first release) to ``current``."""
    old = _elements(previous, base) if previous is not None else {}
    new = _elements(current, base)
    found: dict[str, list[tuple[str, str]]] = {kind: [] for kind in _KINDS}
    for element_id in sorted(set(old) | set(new)):
        kind = _kind(old.get(element_id), new.get(element_id))
        if kind is not None:
            label = (new.get(element_id) or old[element_id]).label
            found[kind].append((element_id, label))
    return Changes(**found)


def _entry(version: str, previous_version: str | None, changes: Changes) -> str:
    against = (
        f"Elements added, changed, deprecated and removed against {previous_version}."
        if previous_version
        else "The first governed release: every element is added."
    )
    lines = [f"## {version}", "", against, ""]
    for name, items in zip(_SECTIONS, _lists(changes), strict=True):
        lines += [f"### {name}", ""]
        lines += [f"- `{element_id}` {label}" for element_id, label in items] or ["- none"]
        lines.append("")
    return "\n".join(lines)


def _lists(changes: Changes) -> list[list[tuple[str, str]]]:
    return [changes.added, changes.changed, changes.deprecated, changes.removed]


def changelog(
    name: str, version: str, previous_version: str | None, changes: Changes, previous_text: str
) -> str:
    """``CHANGELOG.md`` with the entry for ``version`` above the earlier entries."""
    older = previous_text.split("\n## ", 1)[1] if "\n## " in previous_text else ""
    text = _HEADER.format(name=name) + "\n" + _entry(version, previous_version, changes)
    if older:
        text += "\n## " + older
    return text.rstrip("\n") + "\n"
