"""Which elements a level holds, and the labels terms give to concepts (FR-32, FR-33)."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from ontology_builder.model import Concept, Element, Term

LEVELS = ("level-1", "level-2", "level-3")


def level_elements(elements: Iterable[Element], level: str) -> list[Element]:
    """The elements of ``level-N.md``: levels 1..N, without terms, deprecated or ignorable ones.

    Levels are cumulative (FR-33). Terms are labels of concepts, not entries of their own.
    """
    allowed = set(LEVELS[: LEVELS.index(level) + 1])
    return [
        element
        for element in elements
        if element.level in allowed
        and element.status != "deprecated"
        and not isinstance(element, Term)
    ]


@dataclass
class ConceptLabels:
    """The labels terms give a concept: synonyms and spelling variants of its preferred label."""

    alt: list[str] = field(default_factory=list)
    hidden: list[str] = field(default_factory=list)


def term_labels(by_id: Mapping[str, Element]) -> dict[str, ConceptLabels]:
    """For each concept, the labels of the terms whose mentions point to it, sorted.

    A term with the concept's own label adds nothing; one that differs only in case is a hidden
    label (a non-preferred variant); any other is an alternative label (a synonym).
    """
    found: dict[str, ConceptLabels] = {}
    for term in by_id.values():
        if not isinstance(term, Term):
            continue
        for concept_id in {mention.concept for mention in term.mentions or []}:
            concept = by_id.get(concept_id)
            if isinstance(concept, Concept) and term.label != concept.label:
                labels = found.setdefault(concept_id, ConceptLabels())
                same_word = term.label.casefold() == concept.label.casefold()
                (labels.hidden if same_word else labels.alt).append(term.label)
    for labels in found.values():
        labels.alt = sorted(set(labels.alt))
        labels.hidden = sorted(set(labels.hidden))
    return found
