# Ontology and knowledge representation formats and specifications: comparison for OntologyBuilder

> Research notes, 2026-11-20. Scope: formats and standards for storing ontologies or parts of them (terms, concepts, axioms, relations, rules, constraints, statement-level metadata). Context: an "OntologyBuilder" app that extracts concepts, relations, rules and statements from user manuals with LLM help and puts them through human review and governance (levels, provenance, review status).
>
> Source note: facts about long-stable standards (OWL 2, SKOS, PROV-O, etc.) are cited to their primary specification URLs. Most of these were not re-fetched in this session; they are listed as stable references. Status facts for 2026 (RDF 1.2, SPARQL 1.2, SHACL 1.2) and LLM evidence were checked live.

## Which standards exist, and what is their status in 2026?

### Takeaway
Most of the stack is a family of W3C standards built on one data model, RDF. On top of RDF sit vocabularies: RDFS, OWL 2, SKOS, PROV-O, DCTERMS and OntoLex. Beside them sit shape languages (SHACL, ShEx) and rule languages (SWRL, RIF, SHACL Rules). Outside that family are ISO standards (Common Logic, Topic Maps, GQL), community formats (OBO, LinkML, Schema.org) and property-graph formats. As of late 2026, RDF 1.2 is **not yet a Recommendation**: Concepts and Semantics are Candidate Recommendations, and the syntaxes are still Working Drafts. SPARQL 1.2 and SHACL 1.2 are Working Drafts.

### Cited Findings

**RDF 1.1 and RDF 1.2 (incorporating RDF-star)**
- The latest RDF **Recommendation** is still RDF 1.1. RDF 1.2 Concepts and RDF 1.2 Semantics are W3C Candidate Recommendations dated 2026-04-07. — [What's New in RDF 1.2 (Group Note Draft, 2026-07-14)](https://www.w3.org/TR/rdf12-new/); [RDF 1.2 Concepts CR](https://www.w3.org/TR/2026/CR-rdf12-concepts-20260407/); [W3C news: invites implementations](https://www.w3.org/news/2026/w3c-invites-implementations-of-rdf-1-2-concepts-and-abstract-data-model-and-rdf-1-2-semantics)
- To exit CR, at least two independent implementations must pass each test in the RDF 1.2 test suite. — [CR call for wide review](https://lists.w3.org/Archives/Public/public-review-announce/2026Apr/0003.html)
- As of mid-2026, RDF 1.2 N-Triples, N-Quads, TriG, Turtle and XML Syntax were Working Drafts (June 2026); RDF 1.2 Schema was a WD (2026-03-28); the Primer is a Note draft; and SPARQL 1.2 documents were WDs or Editor's Drafts with no Recommendation dates. — [What's New in RDF 1.2](https://www.w3.org/TR/rdf12-new/)
- The RDF 1.2 Turtle WD is dated 2026-11-11, so it is still a work in progress. — [RDF 1.2 Turtle](https://www.w3.org/TR/rdf12-turtle/)
- RDF 1.2 Turtle syntax for statements about statements:
  - triple term: `_:anno rdf:reifies <<( _:e38 :jobTitle "Designer" )>> .`
  - reified triple: `<< :employee38 :jobTitle "Assistant Designer" ~ _:id >> :accordingTo :employee22 .` (the `~ reifier` is optional; if left out, a fresh blank node is used)
  - annotation, which asserts the triple and also describes it: `:alice :name "Alice" ~ :t {| :statedBy :bob ; :recorded "2021-07-07"^^xsd:date |} .`
  - `rdf:reifies` links a reifier (an IRI or blank node) to a triple term. A triple term on its own is **not asserted**. — [RDF 1.2 Turtle WD](https://www.w3.org/TR/rdf12-turtle/)
- The working group that produces RDF 1.2 and SPARQL 1.2 is the former RDF-star WG (mailing list `public-rdf-star-wg`). RDF-star has been folded into RDF 1.2 through triple terms and reifiers. — [What's New in RDF 1.2](https://www.w3.org/TR/rdf12-new/)
- RDF 1.1 serializations, all Recommendations: Turtle, N-Triples, N-Quads, TriG, RDF/XML and JSON-LD 1.1. — [RDF 1.1 Primer](https://www.w3.org/TR/rdf11-primer/); [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/)

**SHACL 1.2 and SHACL Rules**
- SHACL 1.0 (2017) is a Recommendation. In November 2025 the Data Shapes WG hoped to take SHACL 1.2 Core and SHACL 1.2 SPARQL to CR in January 2026. W3C snapshots from August 2026 still list both as Working Drafts. — [WG announcement Nov 2025](https://lists.w3.org/Archives/Public/public-review-announce/2025Nov/0001.html); [SHACL 1.2 Core WD 2026-08-28](https://www.w3.org/TR/2026/WD-shacl12-core-20260828/)
- SHACL 1.2 Rules (WD, with many 2026 snapshots up to at least 2026-08-10) **generates new RDF data** from rules plus a data graph. Rules can be written in RDF or in a new compact **SHACL Rules Language (SRL)**. Evaluation runs to a fixed point and uses stratification so the result does not depend on rule order. Open issues include how rules relate to shapes and to SPARQL CONSTRUCT. — [SHACL 1.2 Rules WD](https://www.w3.org/TR/2026/WD-shacl12-rules-20260810/); [history](https://www.w3.org/standards/history/shacl12-rules/)

**Other W3C standards (stable references)**
- **RDFS 1.1**: classes, subClassOf, subPropertyOf, domain, range. — [RDF Schema 1.1](https://www.w3.org/TR/rdf-schema/)
- **OWL 2** (2nd edition, 2012): DL-based ontologies. Three profiles: **EL** (polynomial reasoning; large terminologies such as SNOMED), **QL** (query rewriting to SQL), **RL** (rule-based implementation). Five syntaxes: RDF/XML (the only one tools must support), Turtle (any RDF syntax), Functional-Style, Manchester and OWL/XML. — [OWL 2 Overview](https://www.w3.org/TR/owl2-overview/); [OWL 2 Profiles](https://www.w3.org/TR/owl2-profiles/); [Manchester Syntax](https://www.w3.org/TR/owl2-manchester-syntax/)
- **SKOS** (2009): concept schemes, prefLabel/altLabel/hiddenLabel, broader/narrower/related, exactMatch/closeMatch, notes. **SKOS-XL** turns labels into resources (`skosxl:Label`), so a label can carry its own metadata (source, status). — [SKOS Reference](https://www.w3.org/TR/skos-reference/); [SKOS-XL appendix](https://www.w3.org/TR/skos-reference/skos-xl.html)
- **ShEx 2**: a shape language, a W3C Community Group report rather than a Recommendation. It has a compact syntax (ShExC) and a JSON form. — [ShEx 2.1](https://shex.io/shex-semantics/)
- **SWRL** (W3C Member Submission 2004, never a Recommendation): Horn rules over OWL, supported in Protégé/Pellet. — [SWRL submission](https://www.w3.org/submissions/SWRL/)
- **RIF** (Recommendation 2010; Core, BLD, PRD dialects): a rule interchange format with little adoption. — [RIF Overview](https://www.w3.org/TR/rif-overview/)
- **SPARQL 1.1** (Recommendation 2013): CONSTRUCT queries are often used as de-facto rules (as are SPIN and SHACL-AF SPARQL rules). — [SPARQL 1.1 Query](https://www.w3.org/TR/sparql11-query/); [SHACL Advanced Features Note](https://www.w3.org/TR/shacl-af/)
- **PROV-O** (Recommendation 2013): Entity, Activity, Agent, wasGeneratedBy, wasDerivedFrom, wasAttributedTo, and qualified forms. — [PROV-O](https://www.w3.org/TR/prov-o/)
- **Dublin Core Terms**: creator, created, modified, source, license, etc. — [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- **OntoLex-Lemon** (W3C Community Group report 2016): links lexical entries (forms, senses, morphology) to ontology concepts. — [OntoLex-Lemon](https://www.w3.org/2016/05/ontolex/)
- **Schema.org**: a general-purpose web vocabulary, used mostly as JSON-LD in web pages. — [schema.org](https://schema.org/docs/datamodel.html)

**Non-W3C standards**
- **Common Logic** (ISO/IEC 24707): full first-order logic; dialects CLIF, CGIF, XCL. — [ISO/IEC 24707](https://www.iso.org/standard/66249.html)
- **Topic Maps** (ISO/IEC 13250, XTM syntax): topics, associations, occurrences. Now largely legacy. — [ISO/IEC 13250](https://www.iso.org/standard/38068.html)
- **GQL** (ISO/IEC 39075:2024, published 2024-04-12, 610 pp.): the first ISO query language for **property graphs**. Cypher influenced it. A 2nd edition is in development. — [IEC webstore](https://webstore.iec.ch/publication/94107); [ISO committee draft page](https://www.iso.org/standard/89917.html); [Wikipedia](https://en.wikipedia.org/wiki/Graph_Query_Language)
- openCypher (a query language, not a storage format) and **GraphML** (an XML exchange format for graphs with typed key/value attributes) — [GraphML](http://graphml.graphdrawing.org/)
- **OBO flat file format 1.4**: a stanza-based format (`[Term] id: name: def: is_a: relationship:`) that maps to a subset of OWL 2. — [OBO 1.4 spec](https://owlcollab.github.io/oboformat/doc/obo-syntax.html)
- **LinkML**: YAML schemas with generators for JSON-LD/contexts, RDF, SHACL, ShEx, OWL, SPARQL, JSON Schema, Pydantic, SQL DDL, TypeDB, GraphQL, ER diagrams, SSSOM and more. It also has `linkml validate`. Apache-2.0. — [LinkML docs](https://linkml.io/linkml/)
- **Nanopublications**: the smallest publishable claim, as **four named graphs**: head, assertion, provenance and publication info. The provenance graph MUST link to the assertion graph. The guidelines recommend TriG. Servers expose TriG, N-Quads, TriX and JSON-LD. — [Nanopub guidelines](https://raw.githubusercontent.com/Nanopublication/Guidelines/8388dd90795b264f4b01c64d0f7218babcae4871/index.html); [Kuhn et al., arXiv 1809.06532](https://arxiv.org/pdf/1809.06532); [DCMI page](https://msi.dublincore.org/standards/nanopublication)

### Inferences
- If you build on RDF in 2026, write RDF 1.1 Turtle/TriG for portability. Use RDF 1.2 reifier/annotation syntax only when the stores and parsers you need support it, because the syntax specs are still drafts. Triple-term semantics could still change in detail before Recommendation, though CR suggests the abstract model is stable.
- SHACL 1.0 is the safe choice for validation now. SHACL 1.2 Rules (SRL) is a promising future home for "rules" extracted from manuals, but it is not stable yet.

### Gaps
- I found no confirmation of whether any RDF 1.2 or SPARQL 1.2 document reached Proposed Recommendation or Recommendation after August 2026. Check https://www.w3.org/standards/.
- I did not verify SHACL 1.2 Core's status for September–November 2026.

## What does each format represent well (terms, concepts, axioms, relations, rules, statement metadata)?

### Takeaway
No single format covers every layer. A practical split:
- **Vocabulary/terms**: SKOS (+SKOS-XL, OntoLex for linguistic detail)
- **Class axioms/logic**: OWL 2
- **Relations/facts**: RDF triples or property graphs
- **Constraints**: SHACL
- **Rules**: SWRL, SHACL Rules or SPARQL CONSTRUCT, none of them perfect
- **Statement metadata** (provenance, confidence, review status, level): named graphs, nanopublication-style; RDF 1.2 reifiers; OWL axiom annotations; or edge properties in a property graph

### Cited Findings
- SKOS is designed for **concept schemes** (thesauri, taxonomies) with *informal* semantics. broader/narrower are deliberately not subclass relations. — [SKOS Reference](https://www.w3.org/TR/skos-reference/)
- SKOS-XL makes each label a resource, so per-label provenance and status are possible. — [SKOS-XL](https://www.w3.org/TR/skos-reference/skos-xl.html)
- OWL 2 provides class expressions, property characteristics, disjointness and cardinalities, and supports **annotations on axioms** (`Annotation(...)` inside an axiom in Functional Syntax; `owl:Axiom` with `owl:annotatedSource/Property/Target` in RDF). Axiom annotations carry no logical meaning. — [OWL 2 Structural Spec §10](https://www.w3.org/TR/owl2-syntax/#Annotations); [OWL 2 RDF mapping](https://www.w3.org/TR/owl2-mapping-to-rdf/)
- SHACL validates data graphs against shapes (cardinality, datatype, value sets, SPARQL constraints) under a closed-world reading. OWL uses the open-world assumption and inference. — [SHACL](https://www.w3.org/TR/shacl/)
- SHACL 1.2 Rules derives new triples (rules expressed in RDF or SRL). — [SHACL 1.2 Rules WD](https://www.w3.org/TR/2026/WD-shacl12-rules-20260810/)
- RDF 1.2 reifiers plus annotation syntax let you attach `:statedBy`, `:recorded`, etc. to an individual triple, with or without asserting it. That suits "proposed but not yet approved" statements, which can stay as unasserted triple terms. — [RDF 1.2 Turtle](https://www.w3.org/TR/rdf12-turtle/)
- Nanopublications put metadata at the level of a **group of triples** (the assertion graph), with separate provenance and publication-info graphs. — [Nanopub guidelines](https://raw.githubusercontent.com/Nanopublication/Guidelines/8388dd90795b264f4b01c64d0f7218babcae4871/index.html)
- PROV-O provides the vocabulary for "generated by an extraction activity, using a source document, attributed to an LLM or a reviewer". — [PROV-O](https://www.w3.org/TR/prov-o/)
- OntoLex-Lemon separates the lexicon (words and senses in the manuals) from the ontology concept. — [OntoLex-Lemon](https://www.w3.org/2016/05/ontolex/)
- OBO format covers terms, definitions with xrefs, synonyms with scope (EXACT, NARROW, BROAD, RELATED), is_a and relationship, but **"does not cover all of OWL"**. Use it only with ontologies that stay within the OBO limits. — [OBO Academy: OWL format variants](https://oboacademy.github.io/obook/explanation/owl-format-variants)
- LinkML models classes, slots, enums (including ontology-backed enums) and constraints, and compiles to OWL, SHACL and JSON Schema. It is a **schema/data-modeling language** rather than a DL ontology language. — [LinkML docs](https://linkml.io/linkml/); [OntoGPT/SPIRES, arXiv 2304.02711](https://arxiv.org/html/2304.02711v2)
- Property graphs (GQL) let nodes **and edges** carry key/value properties natively, which makes per-relation metadata trivial. GQL standardizes querying, not a file format. — [ISO/IEC 39075](https://webstore.iec.ch/publication/94107)

**Ways to attach metadata to one statement (summary)**

| Mechanism | Granularity | Asserted? | Status / support |
|---|---|---|---|
| RDF reification (`rdf:Statement`, RDF 1.0) | triple | no (separate) | standard, verbose (4+ triples), widely supported |
| Named graphs (TriG/N-Quads) | set of triples | yes | RDF 1.1 Rec; every quad store supports them; nanopub pattern |
| RDF 1.2 triple terms + `rdf:reifies` / `{| |}` | triple (many reifiers per triple) | optional | CR (concepts) / WD (syntax); support growing |
| OWL 2 axiom annotations | axiom | yes | Rec; Protégé/OWL API support; no logical effect |
| SKOS-XL labels | label | n/a | Rec appendix |
| Property-graph edge properties | edge | yes | native in Neo4j etc.; GQL ISO 2024 |
| LinkML slots on a reified "Statement" class | any you model | n/a (app-level) | via generated JSON Schema/SHACL |

### Inferences
- For OntologyBuilder's "statement with level, provenance and review status", the closest *standard* pattern is nanopub-style named graphs, or a per-statement reifier in RDF 1.2. Both can use PROV-O and DCTERMS for the metadata. A LinkML schema can define the same "Statement" record and generate JSON Schema for LLM output plus SHACL for validation.
- Keep candidate and rejected statements out of the asserted ontology graph, using separate named graphs or unasserted triple terms, so reasoners only see approved knowledge.

### Gaps
- I found no standard vocabulary for "review status" or "confidence". Projects typically define their own properties, or reuse PROV-O plus custom ones. I did not verify existing vocabularies such as `oboInOwl`, `IAO:0000114` (has curation status) or SEPIO for this.

## Comparison: expressiveness, reasoning, tooling, readability, git diff/merge, LLM-friendliness, validation, adoption

### Takeaway
Turtle (and TriG) is the best general RDF text format for git and LLMs. OWL Functional Syntax and OBO format are the ontology-community favourites for diffs. RDF/XML is the worst for humans and diffs. LinkML YAML is the most approachable for developers and LLMs, but it is a schema language rather than a reasoning language. JSON-LD suits APIs and LLM structured output, but diffs and reads less well as an editing master.

### Cited Findings
- RDF/XML is "a pretty ugly format, really hard to understand by most users" and "not suitable for manual review". It is still the default serialisation of OWL-flavoured OBO ontologies, and RDF and OWL tools understand it widely. — [OBO Academy](https://oboacademy.github.io/obook/explanation/owl-format-variants)
- OWL Functional Syntax is a "very common syntax for editing ontologies in OWL, because they look nice in diff tools such as `git diff`". — [OBO Academy](https://oboacademy.github.io/obook/explanation/owl-format-variants)
- OBO format is "the most easy to read of all the serialisations" and "looks clear and beautiful in diffs". Mondo and Uberon edit in OBO. — [OBO Academy](https://oboacademy.github.io/obook/explanation/owl-format-variants)
- Manchester Syntax is the default for OWL tutorials and for writing class expressions in Protégé. — [OBO Academy](https://oboacademy.github.io/obook/explanation/owl-format-variants)
- OBO Graphs JSON is for tools that do not need reasoners; it covers what is "relevant in 99% of the use cases". — [OBO Academy](https://oboacademy.github.io/obook/explanation/owl-format-variants)
- The ODK community moved intermediate files from RDF/XML to `.ofn` for smaller files and cleaner diffs. ODK 1.5 added `import_component_format: ofn`. The ODK editor workflow uses `git diff` as the first sanity check on edits. — [C-Path ODK issue](https://gitlab.c-path.org/c-pathontology/critical-path-ontology/-/issues/79); [ODK releases](https://www.github.com/INCATools/ontology-development-kit/releases); [AIO editors workflow](https://berkeleybop.org/artificial-intelligence-ontology/odk-workflows/EditorsWorkflow/)
- ODK/ROBOT are the standard OBO toolchain for building, reasoning, QC and releasing ontologies. — [ODK paper, arXiv 2207.02056](https://arxiv.org/pdf/2207.02056)
- **LLM-friendliness evidence (LLM-KG-Bench 3.0, 30+ LLMs)**: in Turtle vs JSON-LD t-tests, most models showed **no significant format preference** on most tasks.
  - The syntax-repair task (RdfSyntaxFixList) favoured JSON-LD: 16 of 36 models preferred JSON-LD, 1 preferred Turtle.
  - The text-to-answer and SPARQL-answer tasks leaned to Turtle: 8 and 5 models preferred Turtle, 0 and 1 preferred JSON-LD.
  - The paper does not name an overall best format. — [LLM-KG-Bench 3.0, arXiv 2505.13098](https://arxiv.org/html/2505.13098v1)
- An ESWC 2024 OWL-generation study chose Turtle because LLMs have likely seen it often in training. — [ESWC 2024 paper](https://2024.eswc-conferences.org/wp-content/uploads/2024/04/146640137.pdf)
- A 2025 study compares schema representations, from simple triples to DL axioms in Manchester Syntax, as LLM *input* for generation quality. — [arXiv 2507.09389](https://arxiv.org/html/2507.09389v1)
- A systematic review of LLMs for ontology engineering (30 papers, 2018 to May 2025) finds LLMs used as engineer, domain expert and evaluator. Inputs include OWL, text and competency questions; outputs include axioms and documentation. Task definitions, datasets and metrics vary widely between papers. — [Li, Garijo, Poveda-Villalón, SWJ](https://semantic-web-journal.net/content/large-language-models-ontology-engineering-systematic-literature-review-0)
- GQL is an ISO standard query language, but the property-graph *file* interchange story (GraphML, CSV imports, vendor JSON) is not standardized the same way. — [ISO/IEC 39075](https://webstore.iec.ch/publication/94107); [GraphML](http://graphml.graphdrawing.org/)

**Comparison matrix** (synthesis; ratings are this researcher's judgement based on the findings above and the specs)

| Format | Expressiveness | Reasoning | Validation | Human read | Git diff/merge | LLM read/write | Adoption |
|---|---|---|---|---|---|---|---|
| RDF Turtle / TriG | data model only; carries OWL/SKOS/SHACL | via OWL/RDFS reasoners | SHACL/ShEx | good | good if sorted/canonical (blank nodes and prefix order can churn) | good; most-used in LLM papers | very high |
| N-Triples / N-Quads | same | same | same | poor (verbose) | excellent line-based diffs when sorted | ok (verbose, easy to parse) | high |
| JSON-LD | same | same | SHACL, JSON Schema | ok | ok-poor (nesting) | good; JSON tooling, structured outputs | very high (web) |
| RDF/XML | same | same | same | poor | poor | poor | legacy default |
| OWL Functional | full OWL 2 | DL reasoners (HermiT, ELK, Pellet) | reasoner consistency checks | ok | very good | moderate (less training data) | OBO/ODK |
| Manchester | full OWL 2 (class expressions) | same | same | best for logic | ok | good for single axioms | Protégé |
| OBO 1.4 | OWL subset | via conversion to OWL | ROBOT report | very good | very good | good (simple stanzas) | biomedical |
| SKOS (in Turtle) | thesaurus-level | minimal | SHACL / qSKOS | good | good | good | libraries, EU vocabularies |
| SHACL | closed-world constraints (+rules in 1.2) | n/a (validation) | itself | ok | good (Turtle) | moderate | growing |
| SWRL / RIF | Horn rules | Pellet / rule engines | — | ok / poor | ok / poor | low | low |
| Common Logic | full FOL | FOL provers | — | ok (CLIF) | ok | low | niche |
| LinkML YAML | schema/classes/enums/constraints; not full DL | via generated OWL | `linkml validate`, JSON Schema, SHACL | very good | very good | very good (YAML/JSON, schema-to-JSON-Schema) | growing (biomedical, data coordination) |
| Property graph (GQL/Cypher, GraphML) | nodes and edges with properties; no standard semantics | none standard | DB schema constraints | ok | poor as DB; GraphML ok | good for Cypher | high in industry |
| Topic Maps (XTM) | topics/associations | none | — | poor | poor | low | legacy |

### Inferences
- **Diff/merge**: line-oriented, deterministic serializations matter more than format choice. Sorted N-Triples, a canonical Turtle writer, OFN from the OWL API, and one-file-per-concept YAML all give stable diffs. Blank nodes (e.g., OWL restrictions, RDF reification) produce unstable diffs in any RDF syntax.
- **LLM-friendliness**: the evidence does not show a big gap between Turtle and JSON-LD. JSON(-LD) or YAML fits constrained/structured-output decoding (JSON Schema) best, which is a practical reliability advantage for extraction. Turtle is most natural when the LLM must read existing ontologies.

### Gaps
- I found no rigorous benchmark of LLM accuracy writing OWL Functional, Manchester, OBO, LinkML or SHACL versus Turtle.
- I found no quantitative study of git merge-conflict rates per format.

## What do modern LLM-based ontology projects use?

### Takeaway
The LLM is usually given and asked for **JSON/YAML objects that follow a schema** (LinkML in OntoGPT/SPIRES; JSON term objects in DRAGON-AI). Results are then converted to OWL/RDF (Turtle, OFN, OBO) for reasoning, QC and release. Research prototypes that generate OWL directly mostly use **Turtle**. Human experts in the loop are a consistent recommendation.

### Cited Findings
- **OntoGPT / SPIRES**: the user provides a **LinkML schema**. SPIRES recursively prompts the LLM to fill the schema from text with zero-shot extraction, then **grounds** values to ontology identifiers. This gives far more consistent IDs than LLM output alone. Outputs are JSON/YAML/RDF/OWL that conform to the schema (OWL through linkml-owl). The current version uses LiteLLM for model access. — [SPIRES, arXiv 2304.02711](https://arxiv.org/html/2304.02711v2); [PMC version](https://pmc.ncbi.nlm.nih.gov/articles/PMC10924283); [OntoGPT PyPI](https://pypi.org/project/ontogpt/0.3.2)
- **DRAGON-AI** (J. Biomed. Semantics 2024): "Each term is represented as a structured object which is serialized using JSON" (id, label, definition, relationships, logical_definitions). Numeric IDs are replaced by CamelCase label symbols before embedding and prompting. Output is JSON, parsed with a standard parser. YAML appears only in figures. OBO appears only as a comparison. The source ontologies are OWL, reasoned with ELK. LinkML, ROBOT templates, DOSDP and OTTR are mentioned as template workflows. — [DRAGON-AI, PMC11484368](https://pmc.ncbi.nlm.nih.gov/articles/PMC11484368/)
- DRAGON-AI evaluation: high precision on relationship generation; definitions were acceptable but worse than human-written ones. The authors stress that curators must drive the process, and the tool can take instructions from GitHub issues. — [arXiv 2312.10904](https://arxiv.org/abs/2312.10904v2); [eScholarship](https://escholarship.org/uc/item/10x4r512)
- The ESWC 2024 OWL-generation work emits Turtle, and NeOn-GPT-style pipelines validate syntax, consistency and modeling pitfalls (OOPS!) after generation. — [ESWC 2024](https://2024.eswc-conferences.org/wp-content/uploads/2024/04/146640137.pdf); [NeOn-GPT](https://eprints.soton.ac.uk/511839/1/neon_gpt_2_final.pdf)
- LinkML lists a "How to Generate AI prompts" guide and generators to JSON Schema and Pydantic, which LLM structured-output APIs consume. — [LinkML docs](https://linkml.io/linkml/)

### Inferences
- A pattern that fits OntologyBuilder:
  1. A LinkML (or JSON Schema) model of `Concept`, `Relation`, `Rule` and `Statement` records with provenance, level and review-status slots.
  2. LLMs emit JSON/YAML that conforms to it.
  3. Records are stored as git-friendly YAML or JSON, one file per item or per source section.
  4. Approved items are exported to RDF: SKOS for vocabulary, OWL for axioms, SHACL for constraints, PROV-O for provenance, and TriG named graphs or RDF 1.2 reifiers for statement metadata.

  This mirrors OntoGPT and DRAGON-AI practice and keeps an interoperable standards output.
- Property graphs are attractive when per-edge metadata and querying matter more than formal semantics. They give up OWL reasoning and SHACL validation unless the data is mapped to RDF.

### Gaps
- I did not research industry tools in this session: Neo4j LLM Graph Builder, the TopBraid/PoolParty LLM features, or Protégé LLM plugins. I have no sourced claims on their formats.
- I found no 2026-specific survey of the formats LLM ontology tools use. The evidence above is from 2023–2025 papers.
