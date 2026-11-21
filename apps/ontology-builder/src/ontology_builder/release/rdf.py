"""The RDF graph of a release: OWL 2 + SKOS + SHACL in Turtle (plan 0002, RDF mapping; FR-32).

The mapping is the one of the shared contract ``libs/contracts/ontology/README.md``. Which
elements go into a release, and in which version, is decided by the caller (raw or governed
build); this module maps the elements it is given. Every blank node is inlined and gets a label
derived from the element ID, so the Turtle carries no blank-node labels and its order is the same
on every build (FR-36).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal

from rdflib import RDF, RDFS, XSD, BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, SH, SKOS

from ontology_builder.model import (
    Cardinality,
    Concept,
    Element,
    Property,
    Relation,
    Rule,
    ScopeRecord,
    SourceUnit,
    Statement,
    Term,
)
from ontology_builder.release.labels import LEVELS, term_labels

DAI = Namespace("urn:domain-ai-assistant:vocab#")
"""The ``dai:`` vocabulary of the shared contract (``libs/contracts/ontology/vocab.ttl``)."""

VARIANTS = ("raw", "governed")
_COMPARATORS = {"lt": "<", "le": "<=", "eq": "=", "ge": ">=", "gt": ">"}
_PREFIXES = {
    "dai": DAI,
    "dcterms": DCTERMS,
    "owl": OWL,
    "rdf": RDF,
    "rdfs": RDFS,
    "sh": SH,
    "skos": SKOS,
    "xsd": XSD,
}


@dataclass(frozen=True)
class ReleaseInput:
    """What one release graph is built from.

    ``elements`` are the elements of the release, in the version to publish; ``units`` are the
    source units they may cite (corpus units and user statements, by ID).
    """

    scope: ScopeRecord
    elements: Sequence[Element]
    units: Mapping[str, SourceUnit]
    variant: str
    version: str


def ontology_iri(scope: ScopeRecord) -> URIRef:
    """The ontology's IRI: the base IRI without its trailing ``:``, ``/`` or ``#``."""
    return URIRef(scope.base_iri.rstrip(":/#"))


class _GraphBuilder:
    def __init__(self, release: ReleaseInput) -> None:
        if release.variant not in VARIANTS:
            raise ValueError(f"unknown release variant {release.variant!r}; use raw or governed")
        self.release = release
        self.graph = Graph()
        self.base = Namespace(release.scope.base_iri)
        self.by_id = {element.id: element for element in release.elements}

    def iri(self, element_id: str) -> URIRef:
        return self.base[element_id]

    def add(self, subject: URIRef | BNode, predicate: URIRef, value: object) -> None:
        """Add a triple; ``None`` and empty strings are left out (only parts that apply)."""
        if value is None or value == "":
            return
        node = value if isinstance(value, URIRef | BNode | Literal) else Literal(value)
        self.graph.add((subject, predicate, node))

    def build(self) -> Graph:
        for prefix, namespace in _PREFIXES.items():
            self.graph.bind(prefix, namespace)
        self.graph.bind("", self.base)
        self._header()
        for element_id in sorted(self.by_id):
            element = self.by_id[element_id]
            if isinstance(element, Term):
                continue  # a term is a label of the concepts it names (contract: terms)
            self._common(element)
            _write(self, element)
        self._labels_from_terms()
        self._cited_units()
        return self.graph

    def _header(self) -> None:
        scope, version = self.release.scope, self.release.version
        node = ontology_iri(scope)
        self.add(node, RDF.type, OWL.Ontology)
        self.add(node, OWL.versionIRI, URIRef(f"{scope.base_iri}version-{version}"))
        self.add(node, OWL.versionInfo, version)
        self.add(node, DCTERMS.description, scope.purpose)

    def _common(self, element: Element) -> None:
        node = self.iri(element.id)
        if element.level in LEVELS:
            self.add(node, DAI.level, DAI[element.level])
        for evidence in element.evidence:
            self.add(node, DAI.evidence, self.iri(evidence.unit))
        if self.release.variant == "raw":
            self.add(node, DAI.status, DAI[element.status])
        if element.status == "deprecated":
            self.add(node, OWL.deprecated, Literal(True))
            if element.replaced_by:
                self.add(node, DCTERMS.isReplacedBy, self.iri(element.replaced_by))
        if not isinstance(element, Concept):
            self.add(node, SKOS.definition, element.definition)

    def _labels_from_terms(self) -> None:
        for concept_id, labels in term_labels(self.by_id).items():
            for label in labels.alt:
                self.add(self.iri(concept_id), SKOS.altLabel, label)
            for label in labels.hidden:
                self.add(self.iri(concept_id), SKOS.hiddenLabel, label)

    def _cited_units(self) -> None:
        cited = {evidence.unit for element in self.by_id.values() for evidence in element.evidence}
        for unit_id in sorted(cited):
            unit = self.release.units.get(unit_id)
            if unit is not None:
                node = self.iri(unit_id)
                self.add(node, RDF.type, DAI.SourceUnit)
                self.add(node, RDFS.label, unit.text)

    def cardinality(self, owner_id: str, relation: Relation, limits: Cardinality) -> None:
        """A cardinality as an OWL qualified restriction and as a SHACL node shape."""
        if limits.min is None and limits.max is None:
            return
        domain, prop, range_ = (
            self.iri(relation.subject),
            self.iri(relation.id),
            self.iri(relation.object),
        )
        restriction = BNode(f"{owner_id}-restriction")
        self.add(domain, RDFS.subClassOf, restriction)
        self.add(restriction, RDF.type, OWL.Restriction)
        self.add(restriction, OWL.onProperty, prop)
        self.add(restriction, OWL.onClass, range_)
        shape = URIRef(f"{self.iri(owner_id)}-shape")
        property_shape, value_shape = BNode(f"{owner_id}-property"), BNode(f"{owner_id}-value")
        self.add(shape, RDF.type, SH.NodeShape)
        self.add(shape, SH.targetClass, domain)
        self.add(shape, SH.property, property_shape)
        self.add(property_shape, SH.path, prop)
        self.add(property_shape, SH.qualifiedValueShape, value_shape)
        self.add(value_shape, SH["class"], range_)
        for count, owl_term, sh_term in (
            (limits.min, OWL.minQualifiedCardinality, SH.qualifiedMinCount),
            (limits.max, OWL.maxQualifiedCardinality, SH.qualifiedMaxCount),
        ):
            if count is not None:
                self.add(restriction, owl_term, Literal(count, datatype=XSD.nonNegativeInteger))
                self.add(property_shape, sh_term, Literal(count))


def _concept(builder: _GraphBuilder, concept: Concept) -> None:
    node = builder.iri(concept.id)
    builder.add(node, RDF.type, OWL.Class)
    builder.add(node, RDF.type, SKOS.Concept)
    builder.add(node, SKOS.prefLabel, concept.label)
    builder.add(node, SKOS.definition, concept.definition)
    builder.add(node, SKOS.scopeNote, concept.scope_note)
    for parent in sorted(concept.parents or []):
        builder.add(node, RDFS.subClassOf, builder.iri(parent))
        builder.add(node, SKOS.broader, builder.iri(parent))


def _relation(builder: _GraphBuilder, relation: Relation) -> None:
    node = builder.iri(relation.id)
    builder.add(node, RDF.type, OWL.ObjectProperty)
    builder.add(node, RDFS.label, relation.label)
    builder.add(node, RDFS.domain, builder.iri(relation.subject))
    builder.add(node, RDFS.range, builder.iri(relation.object))
    if relation.cardinality is not None:
        builder.cardinality(relation.id, relation, relation.cardinality)


def _rule(builder: _GraphBuilder, rule: Rule) -> None:
    node = builder.iri(rule.id)
    builder.add(node, RDF.type, DAI.Rule)
    builder.add(node, RDFS.label, rule.label)
    builder.add(node, DAI.modality, DAI[rule.modality])
    builder.add(node, DAI.actor, rule.actor)
    builder.add(node, DAI.action, rule.action)
    builder.add(node, DAI.condition, rule.condition)
    if rule.limit is not None:
        builder.add(node, DAI.limitComparator, _COMPARATORS[rule.limit.comparator])
        value = Literal(Decimal(str(rule.limit.value)), datatype=XSD.decimal)
        builder.add(node, DAI.limitValue, value)
        builder.add(node, DAI.limitUnit, rule.limit.unit)
    for scope_id in sorted(rule.scope or []):
        builder.add(node, DAI.scope, builder.iri(scope_id))
    for ref in sorted(rule.refers_to or []):
        builder.add(node, DAI.refersTo, builder.iri(ref))
    if rule.cardinality is not None:
        relation = builder.by_id.get(rule.cardinality.relation)
        if isinstance(relation, Relation):
            builder.cardinality(rule.id, relation, rule.cardinality)


def _statement(builder: _GraphBuilder, statement: Statement) -> None:
    node = builder.iri(statement.id)
    builder.add(node, RDF.type, DAI.Statement)
    builder.add(node, RDFS.label, statement.text)


def _property(builder: _GraphBuilder, prop: Property) -> None:
    node = builder.iri(prop.id)
    builder.add(node, RDF.type, DAI.Property)
    builder.add(node, RDFS.label, prop.label)
    builder.add(node, DAI.propertyOf, builder.iri(prop.of))
    builder.add(node, DAI.propertyName, prop.name)
    builder.add(node, DAI.propertyValue, prop.value)
    builder.add(node, DAI.propertyUnit, prop.unit)


def _write(builder: _GraphBuilder, element: Element) -> None:
    match element:
        case Concept():
            _concept(builder, element)
        case Relation():
            _relation(builder, element)
        case Rule():
            _rule(builder, element)
        case Statement():
            _statement(builder, element)
        case Property():
            _property(builder, element)


def build_graph(release: ReleaseInput) -> Graph:
    """The RDF graph of one release (OWL 2 + SKOS + SHACL + ``dai:``)."""
    return _GraphBuilder(release).build()


def build_turtle(release: ReleaseInput) -> str:
    """``ontology.ttl`` of one release: RDF 1.1 Turtle, the same bytes for the same input."""
    text = build_graph(release).serialize(format="turtle")
    return text if text.endswith("\n") else text + "\n"
