"""``level-1.md``, ``level-2.md`` and ``level-3.md`` of a release (FR-33, FR-34; plan 0002).

Python builds the entries; the Jinja2 template ``templates/level.md.j2`` lays them out. Record
text is escaped for Markdown here (``&``, ``<`` and ``>`` as HTML entities, so no record can
inject HTML into a rendered page); the template environment also autoescapes, so a value that
is not marked as escaped can never slip through raw.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from jinja2 import Environment, PackageLoader, StrictUndefined
from markupsafe import Markup

from ontology_builder.model import (
    Concept,
    Element,
    Property,
    Relation,
    Rule,
    SourceUnit,
    Statement,
)
from ontology_builder.release.labels import LEVELS, level_elements, term_labels
from ontology_builder.release.mermaid import Diagram, relation_diagrams, taxonomy_diagrams
from ontology_builder.release.rdf import ReleaseInput

BADGES = {"proposed": "● proposed", "included": "◐ waiting for approval"}
"""Raw release: the text badge of every status that is not approved (contract: level files)."""

_COMPARATORS = {"lt": "<", "le": "≤", "eq": "=", "ge": "≥", "gt": ">"}
_MODALITIES = {"must": "must", "must_not": "must not", "may": "may"}
_ENV = Environment(
    loader=PackageLoader("ontology_builder.release", "templates"),
    autoescape=True,
    undefined=StrictUndefined,
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
)


def md(text: object) -> Markup:
    """Record text for one line of Markdown: HTML special characters as entities, one line."""
    value = str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # The one place text becomes Markup: it was escaped on the line above. markupsafe's own
    # escape would also turn quotes into entities, which makes the Markdown source hard to read.
    return Markup(" ".join(value.split()))  # noqa: S704


def _quote(text: str) -> Markup:
    """Text as a Markdown blockquote, with no trailing whitespace (pre-commit keeps files so)."""
    lines = text.splitlines() or [""]
    return Markup("\n").join(
        Markup("> ") + md(line) if line.strip() else Markup(">") for line in lines
    )


@dataclass
class Entry:
    """One catalogue entry: an anchor, a heading, an optional paragraph and bullet lines."""

    id: str
    heading: Markup
    body: Markup | None = None
    lines: list[Markup] = field(default_factory=list)


@dataclass(frozen=True)
class Cited:
    """One source unit in the Evidence appendix."""

    id: str
    number: int
    where: Markup
    quote: Markup


class _LevelFile:
    """The content of one ``level-N.md``."""

    def __init__(self, release: ReleaseInput, level: str) -> None:
        self.release = release
        self.level = level
        self.elements = sorted(
            level_elements(release.elements, level), key=lambda e: (e.label.casefold(), e.id)
        )
        self.in_level = {element.id: element for element in self.elements}
        self.all = {element.id: element for element in release.elements}
        self.labels = term_labels(self.all)
        self.evidence = _number_evidence(self.elements, release.units)

    def of_type[E: Element](self, element_type: type[E]) -> list[E]:
        return [e for e in self.elements if isinstance(e, element_type)]

    @property
    def drafts(self) -> set[str]:
        if self.release.variant != "raw":
            return set()
        return {e.id for e in self.elements if e.status != "approved"}

    def link(self, element_id: str) -> Markup:
        """A link to an element of this file, or its label (or ID) when it is not in it."""
        element = self.all.get(element_id)
        text = md(element.label if element else element_id)
        if element_id not in self.in_level:
            return text
        text = text.replace("[", "\\[").replace("]", "\\]")
        return Markup("[{}](#{})").format(text, element_id)

    def links(self, ids: Iterable[str]) -> Markup:
        return Markup(", ").join(self.link(i) for i in ids)

    def heading(self, element: Element) -> Markup:
        badge = BADGES.get(element.status) if self.release.variant == "raw" else None
        return md(element.label) + (Markup(" · ") + badge if badge else Markup(""))

    def evidence_line(self, element: Element) -> Markup:
        ids = sorted({e.unit for e in element.evidence}, key=lambda u: self.evidence[u].number)
        refs = (Markup("[§{}](#{})").format(self.evidence[u].number, u) for u in ids)
        return Markup("**Evidence:** ") + Markup(", ").join(refs)

    def common(self, element: Element, entry: Entry) -> Entry:
        entry.lines.append(Markup("**Level:** {}").format(element.level.removeprefix("level-")))
        entry.lines.append(self.evidence_line(element))
        return entry


def _concept(page: _LevelFile, concept: Concept) -> Entry:
    entry = Entry(concept.id, page.heading(concept), md(concept.definition or "") or None)
    labels = page.labels.get(concept.id)
    if labels and labels.alt:
        entry.lines.append(Markup("**Synonyms:** ") + md(", ".join(labels.alt)))
    if concept.scope_note:
        entry.lines.append(Markup("**Sense:** ") + md(concept.scope_note))
    if concept.parents:
        entry.lines.append(Markup("**Is a:** ") + page.links(sorted(concept.parents)))
    return page.common(concept, entry)


def _cardinality(minimum: int | None, maximum: int | None) -> str:
    parts = [f"at least {minimum}" if minimum is not None else "", ""]
    parts[1] = f"at most {maximum}" if maximum is not None else ""
    return ", ".join(part for part in parts if part)


def _relation(page: _LevelFile, relation: Relation) -> Entry:
    entry = Entry(relation.id, page.heading(relation), md(relation.definition or "") or None)
    arrow = Markup(" — ") + md(relation.predicate_label) + Markup(" → ")
    entry.lines.append(page.link(relation.subject) + arrow + page.link(relation.object))
    if relation.cardinality and _cardinality(relation.cardinality.min, relation.cardinality.max):
        limits = _cardinality(relation.cardinality.min, relation.cardinality.max)
        entry.lines.append(Markup("**Cardinality:** ") + md(limits))
    return page.common(relation, entry)


def _rule_lines(page: _LevelFile, rule: Rule) -> list[Markup]:
    lines = []
    if rule.condition:
        lines.append(Markup("**When:** ") + md(rule.condition))
    if rule.limit is not None:
        value = f"{rule.limit.value:g}" + (f" {rule.limit.unit}" if rule.limit.unit else "")
        lines.append(Markup("**Limit:** ") + md(f"{_COMPARATORS[rule.limit.comparator]} {value}"))
    if rule.cardinality is not None:
        limits = _cardinality(rule.cardinality.min, rule.cardinality.max)
        via = Markup(" of ") + page.link(rule.cardinality.relation)
        lines.append(Markup("**Cardinality:** ") + md(limits) + via)
    if rule.refers_to:
        lines.append(Markup("**Refers to:** ") + page.links(sorted(rule.refers_to)))
    if rule.scope:
        lines.append(Markup("**Applies to:** ") + md(", ".join(sorted(rule.scope))))
    return lines


def _rule(page: _LevelFile, rule: Rule) -> Entry:
    sentence = Markup("{} **{}** {}").format(
        md(rule.actor), _MODALITIES[rule.modality], md(rule.action)
    )
    entry = Entry(rule.id, page.heading(rule), sentence, _rule_lines(page, rule))
    return page.common(rule, entry)


def _property(page: _LevelFile, prop: Property) -> Entry:
    value = prop.value + (f" {prop.unit}" if prop.unit else "")
    entry = Entry(prop.id, page.heading(prop), md(prop.definition or "") or None)
    entry.lines.append(Markup("**Of:** ") + page.link(prop.of))
    entry.lines.append(Markup("**") + md(prop.name) + Markup(":** ") + md(value))
    return page.common(prop, entry)


def _statement(page: _LevelFile, statement: Statement) -> Entry:
    entry = Entry(statement.id, page.heading(statement), md(statement.text))
    return page.common(statement, entry)


def _location(unit: SourceUnit | None, unit_id: str) -> Markup:
    if unit is None:
        return md(f"source unit {unit_id} (not in this release's sources)")
    if unit.location is None:
        return md(f"user statement by {unit.author}" if unit.author else "user statement")
    return md(" \u203a ".join([unit.location.path, *(unit.location.heading_path or [])]))


def _unit_order(unit_id: str, unit: SourceUnit | None) -> tuple[int, str, int, int, str]:
    if unit is None or unit.location is None:
        return (1 if unit else 2, "", 0, 0, unit_id)
    where = unit.location
    return (0, where.path, where.line_start or 0, where.index_in_section, unit_id)


def _number_evidence(
    elements: Iterable[Element], units: Mapping[str, SourceUnit]
) -> dict[str, Cited]:
    """The units cited by ``elements``, numbered in document order (§1, §2, ...)."""
    cited = {evidence.unit for element in elements for evidence in element.evidence}
    ordered = sorted(cited, key=lambda u: _unit_order(u, units.get(u)))
    return {
        unit_id: Cited(
            unit_id,
            number,
            _location(units.get(unit_id), unit_id),
            _quote(units[unit_id].text) if unit_id in units else Markup("> (text not available)"),
        )
        for number, unit_id in enumerate(ordered, start=1)
    }


def _diagrams(diagrams: list[Diagram]) -> list[dict[str, Markup | None]]:
    return [{"title": md(d.title) if d.title else None, "source": d.source} for d in diagrams]


def _scope_note(level: str) -> str:
    number = LEVELS.index(level) + 1
    if number == 1:
        return "This file holds level 1, the core of the domain."
    return f"This file holds levels 1 to {number}; levels are cumulative."


def render_level(release: ReleaseInput, level: str) -> str:
    """The text of ``level-N.md`` for ``level`` (``level-1`` ... ``level-3``)."""
    page = _LevelFile(release, level)
    concepts, relations = page.of_type(Concept), page.of_type(Relation)
    text = _ENV.get_template("level.md.j2").render(
        title=md(release.scope.name),
        level_number=LEVELS.index(level) + 1,
        version=md(release.version),
        variant=release.variant,
        note=_scope_note(level),
        purpose=md(release.scope.purpose),
        raw=release.variant == "raw",
        taxonomy=_diagrams(taxonomy_diagrams(concepts, page.drafts)),
        relation_diagrams=_diagrams(relation_diagrams(concepts, relations, page.drafts)),
        sections=[
            ("Concepts", [_concept(page, c) for c in concepts]),
            ("Relations", [_relation(page, r) for r in relations]),
            ("Rules", [_rule(page, r) for r in page.of_type(Rule)]),
            ("Properties", [_property(page, p) for p in page.of_type(Property)]),
            ("Statements", [_statement(page, s) for s in page.of_type(Statement)]),
        ],
        evidence=sorted(page.evidence.values(), key=lambda c: c.number),
    )
    return text.rstrip("\n") + "\n"


def build_level_files(release: ReleaseInput) -> dict[str, str]:
    """``level-1.md``, ``level-2.md`` and ``level-3.md`` of one release, by file name."""
    return {f"{level}.md": render_level(release, level) for level in LEVELS}
