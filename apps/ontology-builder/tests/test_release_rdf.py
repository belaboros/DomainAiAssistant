"""The Turtle builder: OWL 2 + SKOS + SHACL (plan 0002, T14: AC-10, AC-24 Turtle, AC-29)."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest
from ontology_builder.governance import (
    Actor,
    ChangeSet,
    add_user_statement,
    apply_action,
    author_element,
)
from ontology_builder.model import Role, Rule, ScopeRecord, Term, validate_record
from ontology_builder.release import DAI, ReleaseInput, build_graph, build_turtle
from pyshacl import validate
from rdflib import RDF, RDFS, Graph, Literal, Namespace, URIRef
from rdflib import namespace as rdf_namespace
from rdflib.compare import isomorphic
from rdflib.namespace import DCTERMS, OWL, SH, SKOS

BASE = "urn:domain-ai-assistant:ontology:pets-and-house-rules:"
ONT = Namespace(BASE)
ADMIN = Actor("bela", Role.domain_admin)
ALICE = Actor("alice", Role.user)
PETS = "A resident may keep at most 2 pets."


def _parse(text: str) -> Graph:
    return Graph().parse(data=text, format="turtle")


def _pet_release(pet_kit: Any, pet_extraction: Any, variant: str, version: str) -> ReleaseInput:
    scope = validate_record(ScopeRecord, pet_kit.scope)
    return ReleaseInput(scope, pet_extraction.elements, pet_extraction.units, variant, version)


def _kit_release(kit: Any, changes: ChangeSet, variant: str, version: str) -> ReleaseInput:
    scope = kit.store.read().scope()
    return ReleaseInput(
        scope, list(changes.elements.values()), changes.statements, variant, version
    )


# ---------- AC-10 ----------


def _lead_rule(pet_extraction: Any) -> Rule:
    for element in pet_extraction.elements:
        texts = " ".join(pet_extraction.units[e.unit].text for e in element.evidence)
        if isinstance(element, Rule) and element.limit is not None and "lead" in texts:
            return element
    raise AssertionError("the pet fixture has no lead rule with a limit")


def test_lead_limit_rule_record_and_turtle(pet_kit: Any, pet_extraction: Any) -> None:
    rule = _lead_rule(pet_extraction)
    assert rule.limit is not None
    assert (rule.limit.comparator, rule.limit.value, rule.limit.unit) == ("le", 2.0, "m")

    graph = _parse(build_turtle(_pet_release(pet_kit, pet_extraction, "raw", "raw+0000000")))
    node = ONT[rule.id]
    assert (node, RDF.type, DAI.Rule) in graph
    assert (node, RDFS.label, Literal(rule.label)) in graph
    assert (node, DAI.modality, DAI.must) in graph
    assert (node, DAI.limitComparator, Literal("<=")) in graph
    assert (
        node,
        DAI.limitValue,
        Literal(Decimal("2.0"), datatype=rdf_namespace.XSD.decimal),
    ) in graph
    assert (node, DAI.limitUnit, Literal("m")) in graph
    assert (node, DAI.actor, Literal(rule.actor)) in graph
    for evidence in rule.evidence:
        unit = ONT[evidence.unit]
        assert (node, DAI.evidence, unit) in graph
        assert (unit, RDF.type, DAI.SourceUnit) in graph
        assert (unit, RDFS.label, Literal(pet_extraction.units[evidence.unit].text)) in graph


def _max_two_pets(kit: Any) -> tuple[ChangeSet, dict[str, str]]:
    """The fixture user statement "a resident may keep at most 2 pets" and what it says."""
    changes = ChangeSet.load(kit.store)
    unit = add_user_statement(changes, ALICE, PETS).id
    evidence = [{"unit": unit}]

    def author(element_type: str, **fields: Any) -> str:
        fields = {"level": "level-1", "evidence": evidence, **fields}
        return author_element(changes, ALICE, element_type, fields).id

    resident = author("concept", label="resident")
    pet = author("concept", label="pet")
    keeps = author("relation", label="keeps", subject=resident, object=pet, predicate_label="keeps")
    rule = author(
        "rule",
        label="at most 2 pets per resident",
        modality="may",
        actor="resident",
        action="keep pets",
        cardinality={"relation": keeps, "max": 2},
        refers_to=[resident, pet, keeps],
    )
    return changes, {"resident": resident, "pet": pet, "keeps": keeps, "rule": rule, "unit": unit}


def test_max_two_pets_as_owl_and_shacl(review_kit: Any) -> None:
    changes, ids = _max_two_pets(review_kit)
    text = build_turtle(_kit_release(review_kit, changes, "raw", "raw+0000000"))
    assert "_:" not in text, "every restriction and shape is inlined"
    graph = _parse(text)
    resident, pet, keeps = ONT[ids["resident"]], ONT[ids["pet"]], ONT[ids["keeps"]]

    restrictions = [
        r
        for r in graph.objects(resident, RDFS.subClassOf)
        if (r, RDF.type, OWL.Restriction) in graph
    ]
    assert len(restrictions) == 1
    [restriction] = restrictions
    assert (restriction, OWL.onProperty, keeps) in graph
    assert (restriction, OWL.onClass, pet) in graph
    two = Literal(2, datatype=rdf_namespace.XSD.nonNegativeInteger)
    assert (restriction, OWL.maxQualifiedCardinality, two) in graph

    shape = URIRef(f"{BASE}{ids['rule']}-shape")
    assert (shape, RDF.type, SH.NodeShape) in graph
    assert (shape, SH.targetClass, resident) in graph
    [prop] = list(graph.objects(shape, SH.property))
    assert (prop, SH.path, keeps) in graph
    [value_shape] = list(graph.objects(prop, SH.qualifiedValueShape))
    assert (value_shape, SH["class"], pet) in graph
    assert (prop, SH.qualifiedMaxCount, Literal(2)) in graph
    assert (ONT[ids["rule"]], DAI.evidence, ONT[ids["unit"]]) in graph

    def data(pets: int) -> Graph:
        g = Graph()
        g.add((ONT.r1, RDF.type, resident))
        for n in range(pets):
            g.add((ONT.r1, keeps, ONT[f"p{n}"]))
            g.add((ONT[f"p{n}"], RDF.type, pet))
        return g

    assert validate(data(2), shacl_graph=graph)[0] is True
    assert validate(data(3), shacl_graph=graph)[0] is False


# ---------- AC-24 (Turtle) ----------


def test_deprecated_has_owl_deprecated_and_replacement(review_kit: Any) -> None:
    old, new = review_kit.seed(
        [
            review_kit.concept("approved", snapshot=True),
            review_kit.concept("approved", snapshot=True),
        ]
    )
    changes = ChangeSet.load(review_kit.store)
    apply_action(changes, ADMIN, "deprecate", old, replacement=new, reason="Renamed.")

    governed = _parse(build_turtle(_kit_release(review_kit, changes, "governed", "1.0.0")))
    assert (ONT[old], OWL.deprecated, Literal(True)) in governed
    assert (ONT[old], DCTERMS.isReplacedBy, ONT[new]) in governed
    assert (ONT[new], OWL.deprecated, None) not in governed
    assert not list(governed.triples((None, DAI.status, None))), "no status in the governed release"

    raw = _parse(build_turtle(_kit_release(review_kit, changes, "raw", "raw+0000000")))
    assert (ONT[old], DAI.status, DAI.deprecated) in raw
    assert (ONT[new], DAI.status, DAI.approved) in raw


# ---------- AC-29 ----------


@pytest.mark.parametrize(("variant", "version"), [("raw", "raw+0000000"), ("governed", "1.0.0")])
def test_both_variants_parse_as_turtle(
    pet_kit: Any, pet_extraction: Any, variant: str, version: str
) -> None:
    release = _pet_release(pet_kit, pet_extraction, variant, version)
    text = build_turtle(release)
    assert "_:" not in text, "no blank-node labels: every blank node is inlined"
    graph = _parse(text)
    assert isomorphic(graph, build_graph(release))
    assert build_turtle(release) == text, "the same records give the same bytes"
    ontology = URIRef(BASE.rstrip(":"))
    assert (ontology, RDF.type, OWL.Ontology) in graph
    assert (ontology, OWL.versionInfo, Literal(version)) in graph
    assert (ontology, OWL.versionIRI, None) in graph
    assert (ontology, DCTERMS.description, Literal(release.scope.purpose)) in graph
    for element in pet_extraction.elements:
        if element.level != "ignorable" and not isinstance(element, Term):
            assert (ONT[element.id], DAI.level, DAI[element.level]) in graph, element.label


def test_sample_element_triples(review_kit: Any) -> None:
    leash = review_kit.element(
        "concept",
        "included",
        label="leash",
        definition="A rope or strap to lead a dog.",
        scope_note="The rope, not the owner's role.",
    )
    animal = review_kit.concept("approved", snapshot=True)
    leash["parents"] = [animal["id"]]
    unit = leash["evidence"][0]["unit"]
    mentions = [{"unit": unit, "concept": leash["id"]}]
    terms = [
        review_kit.element("term", label=label, mentions=mentions)
        for label in ("leash", "lead", "Leash")
    ]
    review_kit.seed([animal, leash, *terms])
    changes = ChangeSet.load(review_kit.store)

    graph = _parse(build_turtle(_kit_release(review_kit, changes, "raw", "raw+0000000")))
    node = ONT[leash["id"]]
    assert (node, RDF.type, OWL.Class) in graph
    assert (node, RDF.type, SKOS.Concept) in graph
    assert (node, SKOS.prefLabel, Literal("leash")) in graph
    assert set(graph.objects(node, SKOS.altLabel)) == {Literal("lead")}
    assert set(graph.objects(node, SKOS.hiddenLabel)) == {Literal("Leash")}
    assert (node, SKOS.definition, Literal("A rope or strap to lead a dog.")) in graph
    assert (node, SKOS.scopeNote, Literal("The rope, not the owner's role.")) in graph
    assert (node, RDFS.subClassOf, ONT[animal["id"]]) in graph
    assert (node, SKOS.broader, ONT[animal["id"]]) in graph
    assert (node, DAI.level, DAI["level-1"]) in graph
    assert (node, DAI.evidence, ONT[unit]) in graph
    assert (node, DAI.status, DAI.included) in graph
    for term in terms:
        assert (ONT[term["id"]], None, None) not in graph, "terms are labels, not resources"


def test_shacl_shapes_validate_fixture_data(
    pet_kit: Any, pet_extraction: Any, review_kit: Any
) -> None:
    graph = build_graph(_pet_release(pet_kit, pet_extraction, "raw", "raw+0000000"))
    conforms, _, report = validate(graph, shacl_graph=graph)
    assert conforms, report

    changes, _ = _max_two_pets(review_kit)
    pets = build_graph(_kit_release(review_kit, changes, "raw", "raw+0000000"))
    assert list(pets.subjects(RDF.type, SH.NodeShape))
    conforms, _, report = validate(pets, shacl_graph=pets)
    assert conforms, report
