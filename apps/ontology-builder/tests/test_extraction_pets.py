"""Pass 1 on the pet manuals, replayed from the curated fixtures (T8: AC-9, fixture half)."""

from __future__ import annotations

from typing import Any

from ontology_builder.model import (
    Concept,
    Element,
    Property,
    Relation,
    Rule,
    Statement,
    Term,
)


def _references(element: Element) -> set[str]:
    if isinstance(element, Concept):
        return set(element.parents or [])
    if isinstance(element, Term):
        return {mention.concept for mention in element.mentions or []}
    if isinstance(element, Relation):
        return {element.subject, element.object}
    if isinstance(element, Rule):
        cardinality = {element.cardinality.relation} if element.cardinality else set()
        return set(element.refers_to or []) | cardinality
    if isinstance(element, Property):
        return {element.of}
    return set()


def test_all_element_types_cite_existing_units(pet_extraction: Any) -> None:
    elements = pet_extraction.elements
    assert {type(e) for e in elements} == {Statement, Term, Concept, Relation, Rule, Property}
    units = pet_extraction.units
    for element in elements:
        assert element.evidence, element.label
        assert all(evidence.unit in units for evidence in element.evidence), element.label
        if isinstance(element, Term):
            assert all(mention.unit in units for mention in element.mentions or [])


def test_every_document_is_answered_and_nothing_skipped(pet_extraction: Any) -> None:
    assert len(pet_extraction.documents) == 37
    assert [s for d in pet_extraction.documents for s in d.skipped] == []
    assert all(d.elements for d in pet_extraction.documents)


def test_references_point_to_elements_of_the_same_run(pet_extraction: Any) -> None:
    ids = {element.id for element in pet_extraction.elements}
    assert len(ids) == len(pet_extraction.elements)
    for element in pet_extraction.elements:
        assert _references(element) <= ids, element.label


def test_all_records_are_proposed_by_the_llm(pet_extraction: Any) -> None:
    for element in pet_extraction.elements:
        assert element.status == "proposed"
        assert element.origin.kind == "llm"


def _texts(pet_extraction: Any, element: Element) -> str:
    return " ".join(pet_extraction.units[e.unit].text for e in element.evidence)


def test_content_next_to_ignorable_passages_is_extracted(pet_extraction: Any) -> None:
    """dog 1: lifespan and registration; rules 1: resident and house management."""
    labels = {e.label.lower() for e in pet_extraction.elements if isinstance(e, Concept)}
    assert {"resident", "house management"} <= labels
    lifespans = [
        e
        for e in pet_extraction.elements
        if isinstance(e, Property) and "lifespan" in e.name.lower()
    ]
    assert any("A dog lives 10 to 15 years." in _texts(pet_extraction, p) for p in lifespans)
    rules = [e for e in pet_extraction.elements if isinstance(e, Rule)]
    assert any("older than 4 months" in _texts(pet_extraction, r) for r in rules)


def test_lead_limit_rule_has_its_limit(pet_extraction: Any) -> None:
    """rules 4.2: the lead may not be longer than 2 metres (feeds AC-10 in T14)."""
    rules = [
        e
        for e in pet_extraction.elements
        if isinstance(e, Rule) and e.limit is not None and "lead" in _texts(pet_extraction, e)
    ]
    assert any(
        rule.modality == "must"  # an obligation with an upper bound, not "must not exceed"
        and rule.limit is not None
        and (rule.limit.comparator, rule.limit.value, rule.limit.unit) == ("le", 2.0, "m")
        for rule in rules
    )
