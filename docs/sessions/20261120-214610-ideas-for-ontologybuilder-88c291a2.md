# Session 2026-11-20 · OntologyBuilder application

- **Session:** `88c291a2-50c7-4e99-bd4e-0cd892eb1d33`
- **Saved:** 2026-11-21T13:30Z

## Summary

We captured the OntologyBuilder idea as 0002 and ran six research tracks, which produced a sourced report under `docs/research/reports/`. The main conclusion was that no existing tool covers the whole flow, and that the level tags and the evidence-linked review queue would have to be built custom. You then settled the design: custom YAML records defined with LinkML as the single source of truth, with OWL 2, SKOS and SHACL Turtle generated from them. Both a governed and a raw release are generated and version-controlled. The OntologyBuilder app holds the review GUI and is the only writer of `data/ontology-<name>/`, which has numbered folders for sources (including user statements), model, decisions and releases. Chunk IDs use a source registry with stable opaque IDs, and the domain admin can approve their own changes. Nothing is committed yet, and the next step is `/clear` then `/spec 0002`.

---

## 1 · 21:46 UTC

### Request

> Let's create an "OntologyBuilder" application that:
>  - can be used to build ontologies from text corpus (e.g.: user manuals) and human input
>  - each ontology will be stored under the data/ontology-<name> directory
>  
> Way of working #1:
> 1. user: initiates ingestion of a set of user manuals
> 2. app: processes the text corpus and creates building blocks for the ontology: statements, terms, concepts, relations, rules, ...
> 3. app: proposes higher-level/abstract/general concepts, relations and rules (using LLM)
> 4. app: assigns a (proposed) level (level-1, level-2, level-3, ignorable) for each extracted component
> 5. user: reviews/includes/excludes/corrects/overrides the proposed statements, their levels, properties 
> 6. user or domain admin: can author content: create statements for (missing) concepts (with/without definition), relations, rules (and properties of any of them)
> 7. app: shows contradictions, gaps ambiguous (extracted or authored) statements
> 8. domain-admin user: governs content, i.e.: marks it as approved/accepted or rejects them
> 9. app: build the final ontology from ingested and authored content
> 
> Levels 
>     - level-1: core components:
>           - technology agnostic core concepts, processes, actors, relations and rules which are easy and quick to understand and depict what the domain is about (without any apriory knowledge)
>            - e.g.: core components of an e-commerce business domain: product, customer, order, warehouse, delivery, payment
>            - e.g.: concepts, relations, rules about owning an dog 
>     - level-2: main components to understand the domain for those who consider using for a typical happy path case
>             - extra concepts, relations, rules explaining ecommerce for a user who want to participate
>             - e.g.: extra concept, relations and rules important for those who consider owning a dog
>     - level-3: detailed concepts
>              - peripherial concepts important for error scenarios, special cases
>     - ignorable parts which do not belong to the ontology
>               - instance-level info: personal details, stories, anecdotes about a specific dog/owner
>               - platform services user manual: leave outh specific commands to be executed when you create your landing zone or deploy your servcices
>               - e.g.: ontology shall not contain specific recepies from a cooking book

### Response

Idea 0001 also describes an ontology builder. This new idea covers that part in much more detail, so I'll capture it as a separate idea (0002) and link the two.

I saved your idea as [docs/ideas/0002-ontology-builder.md](docs/ideas/0002-ontology-builder.md) and added it to the [ideas index](docs/ideas/README.md).

- **Your text:** it's quoted word for word under `## Original idea`, typos included.
- **Status and scope:** status is `captured` and scope is `TBD`. I noted the hints: an OntologyBuilder app and `data/ontology-<name>` datasets.
- **Link to idea 0001:** idea [0001](docs/ideas/0001-manual-ontology-assistant.md) already mentions an ontology builder with review and governance. This new idea goes into that part in much more detail, so I filed it separately and linked the two below the quote. I also pointed to the pet and building manuals in [data/user-manuals-pets-and-house-rules/](data/user-manuals-pets-and-house-rules/) as a likely first set of manuals to test with. Their answer key lists the contradictions, wording changes and gaps planted in them, which step 7 should find.

Next, run `/clear` and then `/spec 0002`. That step settles the scope and asks the open questions, such as where idea 0001 ends and this one begins, and how each `data/ontology-<name>` dataset is owned and what its contract is.

## 2 · 21:53 UTC

### Request

> Research the internet:
> 
> 1. what formats/specifications are available to store ontologies or components of an ontology.
> 2. Compare the alternatives
> 3. Shall we store the ontology as one single file or multiple files or in a special storage (like a graph database)
> 4. What are the typical steps to build an ontology from text corpus?
> 5. How to decide what not to include from a text corpus into the ontology? 
> 6. What are the intermediate components until we get from text corpus, ..., to the ontology?
> 7. What is the typical process to govern an ontology?
> 8. Are there ontology builder applications for such a use-case?

### Response

I'm running six research tracks in parallel: formats, storage, the build pipeline, deciding what to leave out, governance, and existing tools.

<details>
<summary>Subagent · general-purpose · Ontology formats and specs</summary>

**Prompt:**

> Research the formats and specifications available to store ontologies or components of an ontology, and compare them.
> 
> Objective: A dense, sourced comparison of ontology/knowledge representation formats and standards, so a team building an "OntologyBuilder" app (extracts concepts, relations, rules, statements with levels/provenance/review status from user manuals with LLM help, human review and governance) can choose a storage format.
> 
> Key questions:
> - Which standards exist: RDF (and its serializations Turtle, N-Triples, N-Quads, TriG, RDF/XML, JSON-LD), RDFS, OWL 2 (profiles EL/QL/RL, functional/Manchester/OWL-XML syntaxes), SKOS (and SKOS-XL), SHACL, ShEx, SWRL, RIF, SPARQL rules, Common Logic, OBO format, LinkML, Schema.org, property-graph formats (GQL/ISO 39075, openCypher, GraphML), Topic Maps, RDF-star/RDF 1.2, PROV-O, Dublin Core, OntoLex-Lemon, nanopublications.
> - What does each represent well: terms/vocabulary vs concepts vs class axioms vs relations vs rules/constraints vs statement-level metadata (provenance, confidence, review status, level tags)? How to attach metadata to individual statements (reification, named graphs, RDF-star, OWL annotations on axioms)?
> - Comparison criteria: expressiveness, reasoning support, tooling, human readability, diff/merge friendliness in git, LLM-friendliness (can LLMs read/write it reliably), validation, adoption.
> - What do modern LLM-based ontology projects typically use (e.g., LinkML, OWL in Turtle, JSON-LD, YAML)?
> 
> Suggested sources:
> - W3C recommendations (w3.org/TR), OBO Foundry docs, LinkML docs, SHACL spec, Protégé docs, recent papers/blogs on LLMs + ontologies (2023–2026).
> 
> Constraints:
> - Prefer current state as of 2026; note RDF 1.2 / SPARQL 1.2 status.
> 
> Save your output notes to /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/formats_and_specs.md
> 
> **As a first step, you must read /Users/belaboros/.claude/skills/synced/66493f35-7dcd-4d6e-8a87-7905c6d12798_d31955f6-e258-4ffb-8085-b268b86e7658/deep-research/references/researcher.md for instructions on how to conduct research.**

**Output:**

I wrote the research notes in the required three-section format. Every finding has an inline source.

Notes file: /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/formats_and_specs.md

I checked these live in this session: the 2026 status of RDF 1.2, SPARQL 1.2 and SHACL 1.2, the RDF 1.2 Turtle spec, GQL, LinkML, nanopublications, the OBO Academy page on format variants, the ODK move to functional syntax, LLM-KG-Bench 3.0, SPIRES and DRAGON-AI. Long-stable standards (OWL 2, SKOS, PROV-O, SWRL, RIF, Common Logic, Topic Maps, OntoLex, OBO 1.4) are cited to their primary spec pages, but I did not re-open those pages.

**Status in 2026**
- RDF 1.2 is not yet a Recommendation; RDF 1.1 is still the current one.
  - Concepts and Semantics have been Candidate Recommendations since 2026-04-07.
  - The syntax specs (Turtle, TriG, N-Triples, N-Quads, XML) are still Working Drafts. The Turtle draft is dated 2026-11-11.
- SPARQL 1.2 is a set of Working Drafts and Editor's Drafts.
- SHACL 1.2 Core was still a Working Draft in August 2026. The group had hoped for Candidate Recommendation in January 2026.
- SHACL 1.2 Rules, including a compact rule language called SRL, is an active Working Draft.

**RDF-star is now part of RDF 1.2.** Turtle examples from the spec are in the notes:
- triple terms, written `<<( s p o )>>`
- reified triples, written `<< s p o ~ r >>`
- annotations, written `{| ... |}`

These can describe a triple without asserting it, which fits candidate statements that are not yet approved.

**Statement-level metadata.** The notes compare six options:
- old-style RDF reification
- named graphs (the nanopublication pattern: head, assertion, provenance and publication-info graphs, written in TriG)
- RDF 1.2 reifiers
- OWL axiom annotations
- SKOS-XL labels
- edge properties in property graphs

I found no standard vocabulary for review status or confidence.

**Git diffs and readability.**
- The OBO community (OBO Academy) calls RDF/XML ugly and unsuitable for review, while OWL Functional Syntax and OBO format "look nice" in git diffs.
- The ODK toolchain is moving its intermediate files to functional syntax.
- In my own judgement, a deterministic serialization matters more than which format you pick, and blank nodes make diffs unstable in every RDF syntax.

**LLM-friendliness.**
- LLM-KG-Bench 3.0 (30+ models) found mostly no significant preference between Turtle and JSON-LD. JSON-LD did better at fixing broken syntax; Turtle did slightly better on answering questions.
- Projects that generate OWL directly mostly choose Turtle.

**What LLM ontology projects use.**
- OntoGPT/SPIRES fills a LinkML (YAML) schema from text, links values to ontology IDs, then exports to OWL or RDF.
- DRAGON-AI exchanges JSON term objects with the LLM and keeps OWL with a reasoner for logic.
- Both stress that human curators must drive the process.

**Suggested pattern for OntologyBuilder (my inference).** A LinkML or JSON Schema model of Statement, Concept, Relation and Rule records, each with provenance, level and review-status fields. The LLM writes structured JSON/YAML that is stored in git. Approved items are exported to standard formats: SKOS for vocabulary, OWL for axioms, SHACL for constraints, PROV-O for provenance, and TriG named graphs or RDF 1.2 reifiers for statement metadata.

**Gaps**
- Status changes after August–November 2026 are unconfirmed, beyond the Turtle draft dated 2026-11-11.
- No benchmark compares how well LLMs write OWL Functional, Manchester, OBO, LinkML or SHACL.
- No study measures git merge conflicts by format.
- I did not research industry tools such as the Neo4j LLM Graph Builder, TopBraid or PoolParty.
- I did not check existing curation-status vocabularies such as IAO "has curation status" or SEPIO.

</details>

<details>
<summary>Subagent · general-purpose · Ontology storage architecture options</summary>

**Prompt:**

> Research how to physically store an ontology under development: one single file vs multiple files (modular) vs special storage (triplestore / RDF graph DB / property graph DB).
> 
> Objective: Practical, sourced guidance for an "OntologyBuilder" app in a git monorepo, which stores each ontology under data/ontology-<name>/ and needs to keep extracted candidate components (statements, terms, concepts, relations, rules), their proposed levels, provenance to source text, review/approval status, authored content and a final built ontology.
> 
> Key questions:
> - Single-file vs modular ontologies: how do OBO Foundry (ODK – Ontology Development Kit, edit file vs release files, imports, components/templates like ROBOT templates and DOSDP), Gene Ontology, SNOMED, schema.org, Wikidata organize source vs release artifacts? owl:imports and modularization best practices.
> - Git-friendliness: diffs, merge conflicts, sorted/canonical serializations (e.g., ROBOT, rdf-toolkit canonical Turtle), file-per-concept approaches, CSV/TSV templates.
> - When is a triplestore/graph DB warranted (Apache Jena Fuseki/TDB2, GraphDB, Stardog, Oxigraph, Blazegraph, RDFox, Virtuoso, Amazon Neptune; Neo4j with n10s; embedded options like Oxigraph or rdflib in-memory/SQLite)? Size thresholds, query/reasoning needs, concurrency, multi-user editing.
> - Hybrid pattern: files as source of truth in git + load into an embedded/in-memory store for querying, validation and reasoning at build time.
> - Pros/cons table and a recommendation pattern for a small-to-medium ontology (hundreds to tens of thousands of statements).
> 
> Suggested sources:
> - ODK docs, OBO Academy, ROBOT docs, W3C, vendor docs, blog posts and papers on ontology version control (e.g., git-based ontology engineering, VoCol, OntoGit), 2020–2026.
> 
> Save your output notes to /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/storage_architecture.md
> 
> **As a first step, you must read /Users/belaboros/.claude/skills/synced/66493f35-7dcd-4d6e-8a87-7905c6d12798_d31955f6-e258-4ffb-8085-b268b86e7658/deep-research/references/researcher.md for instructions on how to conduct research.**

**Output:**

I finished the storage research and saved the notes to `/Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/storage_architecture.md`. They follow the researcher.md format, with every claim linked to a source and the open questions listed as gaps.

**Findings:**
- **Source vs release:** mature projects keep a small editable source in version control and generate everything users consume.
  - In OBO's ODK this is one edit file (OWL by default, or OBO) plus imports, components and TSV/YAML templates. A Makefile and ROBOT build the releases, which are base and full by default; full merges imports and components and adds inferred axioms.
  - Gene Ontology's repo is for developers only; CI tests every pull request, and Jenkins builds snapshot and monthly releases.
  - SNOMED publishes tab-delimited Full, Snapshot and Delta release files.
  - Schema.org keeps its vocabulary in a Turtle file, `data/schema.ttl`.
  - Wikidata is a live database. Its query service outgrew Blazegraph, split its graph on 2025-05-09, and is reportedly moving to QLever.
- **Git-friendliness:**
  - Text RDF/OWL only diffs cleanly when every writer uses one deterministic serializer (ROBOT/OWLAPI, EDM Council rdf-toolkit, or rdflib's `longturtle` format with `canon=True`), enforced by a pre-commit hook.
  - Blank nodes are the main source of noisy diffs. `robot diff` compares meaning rather than text, which helps when reviewing pull requests.
  - Tab-separated files diff and merge best. OBO Academy says OBO and OWL Functional formats are chosen for editing because they read well in diffs.
- **Triplestores and graph databases:**
  - Jena TDB2 allows one writer at a time with many readers. Sharing its files across separate processes risks corruption, so shared access goes through the Fuseki server.
  - Oxigraph and pyoxigraph are embedded stores that work from Python. rdflib's in-memory store is described as impractical at millions of triples.
  - Neo4j with the n10s plugin imports only part of OWL and keeps one literal value per property by default.
  - A server store is only worth it for many people editing at once, millions of triples or more, an always-on query endpoint, or reasoning at query time. None of these applies to an ontology of hundreds to tens of thousands of statements.
- **Hybrid pattern:** files in git as the source of truth, loaded into an in-memory store at build time for SPARQL checks, SHACL validation and reasoning, is the dominant practice (ODK, VoCol).

**Recommendation in the notes:** store each ontology as modular files in git and generate the single-file release from them.
- Candidates go in one TSV per component type, with stable IDs, proposed level and provenance columns.
- Review decisions go in an append-only log, in the style of SNOMED's Delta files.
- Authored content is normalised Turtle or OWL Functional, without blank nodes.
- Template mappings follow ROBOT or DOSDP.
- A generated `build/` folder holds the release in several formats, plus a with-provenance variant (like ODK's base vs full).
- Readers rely on the dataset contract for the built files only, not on the internal TSVs.
- Use an embedded store only during build and validation. Add Fuseki or an Oxigraph server later only as a derived index loaded from git.

**Gaps and caveats:**
- I could not confirm GO's edit-file path (`src/ontology/go-edit.obo` is commonly assumed).
- I found no reliable source for "OntoGit".
- Size thresholds and the file-per-concept trade-offs are my inferences; I found no sources for either.
- I did not extract numbers from the 2026 RDF framework benchmark.
- The "rdflib in-memory doesn't scale" statement comes from the R rdflib package documentation plus an older paper, not from the Python rdflib docs.
- I did not research the commercial stores (GraphDB, Stardog, RDFox, Virtuoso, Neptune) in depth.

</details>

<details>
<summary>Subagent · general-purpose · Ontology learning pipeline from text</summary>

**Prompt:**

> Research the typical steps and intermediate artifacts for building an ontology from a text corpus (ontology learning), both classical and LLM-based.
> 
> Objective: A sourced description of the pipeline from raw text (e.g., user manuals) to a final ontology, naming every intermediate component/artifact (e.g., chunks, sentences, candidate terms, term variants/synonyms, concepts, taxonomy/is-a relations, non-taxonomic relations, axioms/rules, statements/triples, competency questions) so an "OntologyBuilder" app can define its data model.
> 
> Key questions:
> - The classical "ontology learning layer cake" (Buitelaar, Cimiano, Magnini 2005): terms → synonyms → concepts → concept hierarchy → relations → relation hierarchy → axiom schemata → general axioms. Tools like Text2Onto, OntoGen.
> - Methodologies: METHONTOLOGY, NeOn methodology, Ontology Development 101 (Noy & McGuinness), eXtreme Design / ontology design patterns, competency questions, UPON Lite.
> - LLM-era approaches (2023–2026): LLMs4OL challenge, OntoChat, Ontogenia, NeOn-GPT, OLLM, "LLM-assisted ontology engineering" papers, KG construction with LLMs (e.g., GraphRAG/Microsoft, LlamaIndex/LangChain graph extraction, iText2KG, KGGen), prompting patterns, chunking, entity resolution/canonicalization, provenance linking back to source spans.
> - Steps for abstraction/generalization: proposing higher-level concepts and rules from extracted ones (taxonomy induction, clustering).
> - Evaluation of extracted ontologies (gold standards, competency-question answering, OOPS! pitfall scanner, consistency checks with reasoners).
> - Detecting contradictions, ambiguity, terminology drift, gaps across documents.
> 
> Suggested sources:
> - Academic papers (arXiv, Semantic Web Journal, ESWC/ISWC proceedings), LLMs4OL, Microsoft GraphRAG docs, survey papers on ontology learning and LLM-based KG construction.
> 
> Save your output notes to /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/ontology_learning_pipeline.md
> 
> **As a first step, you must read /Users/belaboros/.claude/skills/synced/66493f35-7dcd-4d6e-8a87-7905c6d12798_d31955f6-e258-4ffb-8085-b268b86e7658/deep-research/references/researcher.md for instructions on how to conduct research.**

**Output:**

I've written sourced research notes on building an ontology from text, covering both the classical and the LLM-based pipeline. They answer all six key questions, with gaps flagged. The research was capped at about 15 tool calls, and some claims rest on secondary summaries rather than the primary papers.

Notes file: /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/ontology_learning_pipeline.md

Each question has a Takeaway, Cited Findings, Inferences and Gaps section, as the researcher format asks.

**Key findings:**
- **Classical layer cake (Buitelaar, Cimiano, Magnini 2005):** terms → synonyms (clustering) → concepts (definition, instances, the terms that name them) → taxonomy → relations → axioms. Text2Onto stores every learned item with a confidence score in a format-neutral model (its "Probabilistic Ontology Model"). It also updates that model incrementally when documents change, instead of reprocessing the whole corpus.
- **Manual methodologies name concrete intermediate documents:**
  - Ontology 101 has seven steps: scope, reuse, terms, classes and hierarchy, properties, constraints, instances.
  - METHONTOLOGY builds a glossary, a concept taxonomy, a binary-relations diagram, a concept dictionary and attribute tables.
  - UPON Lite goes lexicon → glossary with synonyms → taxonomy → predication → parthood.
  - eXtreme Design goes user stories → competency questions → reusable design patterns → testing.
- **LLM era (2023–2026):**
  - **LLMs4OL challenge tasks:** term typing, taxonomy discovery, non-taxonomic relations, and from 2025 a Text2Onto task (terms and types straight from documents). Non-taxonomic relations are the hardest. One 2025 participant scored only about 0.44–0.65 F1 on term extraction.
  - **OLLM (NeurIPS 2024)** generates whole taxonomy subgraphs, but only concepts and is-a links, no axioms.
  - **OntoChat, Ontogenia and NeOn-GPT** generate the ontology from competency questions and user stories.
- **KG-construction pipelines have the best-specified intermediate artifacts:**
  - **GraphRAG** goes text units of 1,200 tokens → entities (title, type, description) and relationships, merged and summarised by the LLM → optional claims with status and time bounds → Leiden communities → community reports → embeddings. Items point back to text units for provenance.
  - **LangChain and LlamaIndex** offer extraction limited to allowed entity and relation types.
  - **iText2KG** resolves entities incrementally as documents arrive. **KGGen** clusters equivalent entities and relations after extraction.
- **Evaluation:**
  - Comparison with a gold standard (precision/recall/F1).
  - Competency questions run as SPARQL queries.
  - Reasoner consistency checks (HermiT), SHACL validation, and the OOPS! pitfall catalogue (built from 693+ ontologies, three severity levels).
  - Panels of LLM judges.

  One 2025 paper found that automatic repair loops help only with conservative stopping rules; aggressive repair driven by competency questions made results worse.
- **Contradiction detection:** the MAGIC benchmark, a RAG study and Stanford's CLAIRE all show that detecting contradictions across documents remains hard for LLMs. Nothing I found covers user manuals or terminology drift specifically.

The Inferences sections propose an entity set for the OntologyBuilder data model:
- **Source text:** Document, Chunk/TextUnit, Mention/CandidateTerm, TermVariant.
- **Ontology content:** Concept, SubClassOf, Relation with domain and range, Statement/Claim, Axiom.
- **Groupings:** Cluster/Community, kept separate from Concept.
- **Requirements and testing:** CompetencyQuestion, TestQuery, TestRun, ValidationIssue.
- **Cross-cutting fields:** a confidence score and source links on everything, plus versioned snapshots.

These are my inferences, not sourced practice.

**Main gaps:**
- I didn't reach the original 2005 book chapter, so the exact eight-layer names come from your brief and secondary summaries.
- I found nothing reliable on OntoGen and no primary source on the NeOn methodology; UPON Lite's step 6 is unconfirmed.
- Two areas came up empty: classical taxonomy induction (Hearst patterns, formal concept analysis) and LLM-based induction of rules and axioms.
- None of the tools I checked documents provenance down to the character span; GraphRAG confirms only the text-unit level.
- Sources disagree on the 2025 LLMs4OL task list (three or four tasks).

</details>

<details>
<summary>Subagent · general-purpose · Ontology scoping and exclusion criteria</summary>

**Prompt:**

> Research how to decide what NOT to include from a text corpus in an ontology, and how to tier included content by importance.
> 
> Objective: Sourced criteria and techniques for scoping an ontology built from text (e.g., user manuals for dog owners, building rules, cloud platform manuals, cookbooks). The target app labels each extracted component as level-1 (core, technology-agnostic concepts that explain what the domain is about), level-2 (needed for typical happy-path participation), level-3 (peripheral, error scenarios, special cases), or ignorable (instance-level data such as personal stories and anecdotes, concrete CLI commands/procedures, specific recipes).
> 
> Key questions:
> - Scoping methods: ontology requirements specification document (ORSD, NeOn), competency questions, purpose/scope/intended users, the "ontology vs knowledge base" (TBox vs ABox, class vs instance) distinction, the universals vs particulars distinction (BFO / OBO principles), procedural vs declarative knowledge.
> - Criteria for excluding content: instance-level facts, anecdotes, procedures/how-to steps, UI/command details, ephemeral or version-specific facts, examples, opinions; how term-extraction measures (termhood, domain relevance, TF-IDF, C-value, domain-specificity vs reference corpus) help filter.
> - Techniques to rank concepts by centrality/importance: basic-level categories (Rosch), core ontology/upper-level vs domain vs application ontology layering, graph centrality, frequency, "key concepts" extraction, ontology summarization (e.g., Peroni's key concept extraction, RDF summarization), ontology modularization by abstraction level.
> - How LLM-based pipelines classify relevance/level (prompting with rubrics, few-shot examples, confidence scores) and the known failure modes.
> 
> Suggested sources:
> - NeOn methodology papers, OBO Foundry principles, BFO docs, ontology summarization papers, term extraction literature, recent LLM ontology learning papers (2023–2026).
> 
> Save your output notes to /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/scoping_and_exclusion.md
> 
> **As a first step, you must read /Users/belaboros/.claude/skills/synced/66493f35-7dcd-4d6e-8a87-7905c6d12798_d31955f6-e258-4ffb-8085-b268b86e7658/deep-research/references/researcher.md for instructions on how to conduct research.**

**Output:**

I saved the research notes, covering all four key questions, to /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/scoping_and_exclusion.md. They follow the researcher.md format: per question, a takeaway, cited findings, inferences and gaps. The research ran on about 17 web searches and fetches.

**1. Scoping**
- **NeOn ORSD** (Suárez-Figueroa et al. 2009): it records purpose, intended uses, end users and requirements. Requirements are prioritized groups of competency questions (CQs) with their answers. A "pre-glossary" lists the terms drawn from the CQs, with frequencies. That glossary is a ready seed list of what is in scope, and the CQ priorities are a coarse tiering hook.
- **Noy & McGuinness, Ontology 101**, gives the explicit exclusion rules:
  - "The ontology should not contain all the possible information about the domain."
  - In the wine example, "how to cook shrimp dishes" is left out.
  - Individual instances are the most specific level.
  - Numbers, colors and locations are usually attribute values, not classes.
- **TBox vs ABox** (Baader et al.): the TBox is schema-like knowledge about the domain's structure; the ABox is assertions about a concrete situation. BFO/OBO realism (Smith & Ceusters) says ontology terms denote universals, while particulars are data. Hoehndorf and others criticize the strict form of that rule.
- **Procedures**: step-by-step know-how is modelled as a separate kind of knowledge, with its own ontologies (PROHOW, the Procedural Knowledge Ontology). That gives sourced grounds for putting procedures in the ignorable bucket.

**2. Filtering measures**
- **C-value/NC-value** (Frantzi, Ananiadou & Mima 2000) scores how term-like a candidate is, including multi-word terms nested inside longer ones.
- **Weirdness** (Ahmad et al.), Domain-Specificity and TF-IDF compare frequency in the domain corpus against a general reference corpus.
- **OntoLearn** (Navigli & Velardi 2004) adds domain relevance plus an entropy-based "domain consensus": a term must be spread across many documents. I infer, without a source, that consensus works as an anecdote filter.

**3. Ranking by importance**
- **Rosch's basic level** (1976) is the most informative level of a taxonomy; Tanaka & Taylor show it shifts with the reader's expertise.
- **Guarino's layering** (1998) separates top-level, domain, task and application ontologies.
- **Peroni, Motta & d'Aquin's Key Concept Extraction** (2008) combines simple names (from Rosch), density, coverage and popularity, and correlated strongly with experts' choices.
- **Summarization surveys** catalogue further centrality measures, and Zhang et al.'s 2007 RDF sentence graph ranks by centrality. The notes include my proposed mapping of these to L1, L2 and L3; it is my inference.

**4. LLM pipelines and failure modes**
- LLMs4OL (2023): zero-shot term typing was the hardest task, while taxonomy discovery did better.
- 2026 preprints report errors carrying forward through pipeline stages, plausible but unsupported extractions, and failures that grow with ontology complexity rather than model size.
- Fixes in the literature: grounding in the source text, agreement across prompts, deterministic vocabulary filters, and retrieval for generating CQs.
- LLM self-reported confidence is consistently overconfident and coarse, so it should not be used as a threshold.

**Gaps**
- No source evaluates LLM importance-tier classification or anecdote/procedure exclusion directly. The failure modes listed for the app are extrapolated.
- Opinions, examples and version-specific facts have no dedicated sourced criteria.
- Several things were seen only through snippets or secondary summaries and need checking: the exact OntoLearn and weirdness formulas, KCE's weights and correlation numbers, the LLMs4OL per-model scores, and the 2026 preprints' numbers.
- Modularization by abstraction level was not found.

</details>

<details>
<summary>Subagent · general-purpose · Ontology governance processes</summary>

**Prompt:**

> Research the typical processes to govern an ontology (and enterprise knowledge graphs / controlled vocabularies).
> 
> Objective: A sourced description of governance roles, workflows, statuses and quality gates that an "OntologyBuilder" app could implement: users review/include/exclude/correct LLM-proposed components, author missing content, and a domain-admin approves or rejects; the app flags contradictions, gaps and ambiguity; a final ontology is built/released.
> 
> Key questions:
> - Roles: ontology owner/steward, domain expert, editor, curator, reviewer, consumer; RACI patterns.
> - Lifecycle/status models for terms and axioms (e.g., proposed/candidate → under review → approved/accepted → deprecated/obsolete; OBO obsoletion with replaced_by/consider; SKOS-based vocabulary status; ISO 25964 / ISO 11179 metadata registry registration statuses; Wikidata/Wikibase community processes; Gene Ontology change request process via GitHub issues and PRs).
> - Change management: versioning (owl:versionIRI, semantic versioning of ontologies), release cycles, change logs, deprecation policies, diff tools (ROBOT diff, Bubastis, ecco).
> - Quality gates: automated checks (reasoner consistency, SHACL validation, OOPS!, ROBOT report, linting), review of LLM-generated content, human-in-the-loop patterns, provenance (PROV-O) and audit trail, confidence scores.
> - Enterprise governance practices: data governance frameworks (DAMA-DMBOK), enterprise taxonomy governance (e.g., PoolParty, TopBraid EDG workflows), knowledge graph governance articles.
> - Conflict/contradiction resolution workflow and handling of multiple reviewers.
> 
> Suggested sources:
> - OBO Foundry and OBO Academy, Gene Ontology docs, ISO 11179/25964 summaries, W3C, TopBraid EDG and PoolParty docs, papers on collaborative ontology engineering (WebProtégé, Collaborative Protégé), 2018–2026.
> 
> Save your output notes to /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/governance_process.md
> 
> **As a first step, you must read /Users/belaboros/.claude/skills/synced/66493f35-7dcd-4d6e-8a87-7905c6d12798_d31955f6-e258-4ffb-8085-b268b86e7658/deep-research/references/researcher.md for instructions on how to conduct research.**

**Output:**

I wrote sourced research notes on ontology governance to `/Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/governance_process.md`. They follow the researcher.md format: one section per key question (roles; lifecycle and statuses; change management; quality gates; enterprise practice; conflict resolution), each with a takeaway, cited findings, inferences and gaps. I used about 18 searches and fetches. Some findings rest on search-result summaries rather than full page reads, and the notes mark those "(summary)". Sources run from 2008 to 2026; the voting material is the oldest (2008–2013).

**Main findings:**
- **Roles:** every tool and framework I looked at keeps proposing and editing apart from approving and publishing.
  - VocBench: Editor → Validator → Publisher.
  - TopBraid EDG: viewer, editor and manager permissions, with approval tied to a governance role such as data governor or business steward.
  - PoolParty: a user drafts and a reviewer or admin approves, rejects with a note, or reassigns.
  - DAMA-DMBOK (from secondary sources only): the owner holds approval authority, stewards do the daily curation, and stewardship is business-led.
  - I found no published RACI matrix for ontologies; the one in the notes is my own proposal.
- **Status models** share one spine: Draft/Proposed → Under review → Approved → Deprecated/Superseded/Retired.
  - OBO principle 19: never silently redefine a term. To obsolete one, set `owl:deprecated`, prefix the label with "obsolete ", remove its logical axioms, add `term replaced by` or `consider`, and announce it in advance.
  - ISO/IEC 11179-6 has the longest ladder: Candidate → Recorded → Qualified → Standard → Preferred Standard → Superseded/Retired.
  - PoolParty uses Draft, Suggested, Approved and Deprecated; any edit sends an approved concept back to Draft.
  - EDG tracks status per working copy rather than per term: Uncommitted → Under review → Approved → Committed.
  - Wikidata only creates a property after discussion, a "ready" status and at least a one-week wait.
- **Change management:**
  - Every OBO release needs a unique `owl:versionIRI`, as a date or a semantic version.
  - The ODK release pipeline builds the artifacts; the release is then reviewed, merged and tagged as a GitHub release.
  - Diff tools: ROBOT diff and Bubastis compare axioms; ecco also works at concept level. KGCL is a proposed change language for change logs at a level closer to how editors think.
  - WebProtégé keeps a revision history with author and timestamp, and revisions can be reverted.
- **Quality gates:**
  - `robot report` sorts problems into ERROR, WARN and INFO, and ERROR blocks a release by default.
  - `robot verify` runs custom SPARQL checks; any result counts as a failure.
  - Reasoners (ELK and others) check consistency.
  - EDG can force a SHACL conformance check before commit.
  - OOPS! grades pitfalls as critical, important or minor and detects 32 of them semi-automatically.
  - GitHub branch protection requires a review and passing checks before a PR can merge.
  - Papers on LLM-generated content agree that human review is needed. One pattern auto-accepts high-confidence items and sends ambiguous ones to experts. OE-Assist found that engineers got worse when the LLM was wrong (automation bias).
  - Provenance for LLM output is usually PROV-O `prov:wasGeneratedBy` pointing to a typed activity. There is no standard vocabulary for confidence, and PROV-CRED warns that raw scores need calibration before they are compared.
- **Conflict resolution:** in practice this is threaded discussion plus a decision-maker. Examples are WebProtégé entity threads, GitHub issues and PRs, PoolParty reassign or reject-with-note, EDG "request further changes", and Collaborative Protégé voting (not confirmed in current WebProtégé). A Wikidata study found that more than half of controversial discussions end without consensus, so an explicit tie-break authority is needed.

**Gaps I could not close:**
- No primary source for ISO 25964 maintenance or status rules (the standard is paywalled).
- No status model for individual axioms; OBO reviews axioms at PR level.
- No community standard for what counts as a major, minor or patch change in an ontology.
- No formal multi-reviewer quorum or tie-break policy in ontology projects.
- No way to detect ambiguity automatically, as opposed to logical contradictions.
- I did not read the full DAMA-DMBOK2 text or the W3C SHACL and PROV-O specifications.

</details>

<details>
<summary>Subagent · general-purpose · Existing ontology builder tools</summary>

**Prompt:**

> Research existing applications and tools that build ontologies (or knowledge graphs / taxonomies) from a text corpus with human review and governance.
> 
> Objective: A sourced landscape of tools relevant to an "OntologyBuilder" use case: ingest user manuals → extract terms/concepts/relations/rules (with LLM help) → propose higher-level concepts → tag importance levels → human review, authoring and approval → build final ontology. Identify which steps each tool covers, licensing (open source vs commercial), and gaps.
> 
> Key questions:
> - Ontology editors: Protégé / WebProtégé, TopBraid EDG, PoolParty (incl. its corpus analysis / concept extraction), VocBench 3, Fluent Editor, OntoStudio, Semaphore (Progress), Graphwise (GraphDB + PoolParty merger), Stardog Designer/Voicebox.
> - Text-to-ontology / KG tools: Text2Onto, OntoGen, OntoGPT (SPIRES, Monarch Initiative), DRAGON-AI, OntoChat, Microsoft GraphRAG, Neo4j LLM Knowledge Graph Builder, LlamaIndex PropertyGraphIndex, LangChain LLMGraphTransformer, iText2KG, KGGen, Cognee, Graphiti/Zep, Diffbot, WhyHow.AI, txtai, Lettria, metaphactory, others found in 2024–2026.
> - Which support human-in-the-loop review/approval workflows, provenance to source text, importance levels or modularization, contradiction detection?
> - Is there anything that covers the full use case end to end? What would need to be custom built?
> 
> Suggested sources:
> - Official product docs and GitHub repos, recent papers (OntoGPT/SPIRES, DRAGON-AI), comparison blog posts, 2023–2026.
> 
> Constraints:
> - Focus on currently maintained tools as of 2026; note discontinued ones as such.
> 
> Save your output notes to /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/existing_tools.md
> 
> **As a first step, you must read /Users/belaboros/.claude/skills/synced/66493f35-7dcd-4d6e-8a87-7905c6d12798_d31955f6-e258-4ffb-8085-b268b86e7658/deep-research/references/researcher.md for instructions on how to conduct research.**

**Output:**

I saved the research notes to `/Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/existing_tools.md`. The main finding is that no tool covers the full OntoBuilder pipeline (manuals → LLM extraction with provenance → higher-level concepts → importance tagging → review and approval → OWL/SKOS ontology).

The notes follow the researcher format: the four key questions, each with a takeaway, cited findings, inferences and gaps. They include a coverage matrix of 19 tools against 7 pipeline steps plus provenance and consistency checking, with licence for each. The work took about 16 searches and every claim cites a source.

**Closest options:**
- **Commercial:** Graphwise PoolParty is the nearest match. Its corpus analysis suggests and scores terms and relations and flags gaps in the taxonomy, and it has taxonomy governance. Graphwise formed when Semantic Web Company and Ontotext merged in October 2024. Release 10.2 (March 2026) brought a new Lucene-based concept extractor.
- **Open source:** OntoGPT/SPIRES or DRAGON-AI (CurateGPT) for schema-driven extraction grounded in existing ontologies, combined with VocBench 3 for review and authoring. VocBench 3 is BSD-3 and active (15.1.2 released 2026-07-16).

**Governance platforms with LLM assistants:**
- **TopBraid EDG:** voting workflows in 9.2, human-in-the-loop approval steps and an MCP server in 9.3, plus Copilot.
- **metaphactory:** an AI modeling agent since 5.8, term-level provenance in 5.7, modular ontology management in 5.10, and the AI assistant embedded in the editor in 6.0 (from 2026-07-14).
- **Progress Semaphore:** the AI Model Builder suggests child concepts, and a person must validate each suggestion.
- **Stardog Voicebox/Designer:** builds an ontology from descriptions and data sources, with human review of mappings. Stardog itself says its expressivity is limited.

**LLM graph-extraction frameworks** (GraphRAG, Neo4j LLM KG Builder, LangChain LLMGraphTransformer, KGGen, Graphiti, Cognee, WhyHow) produce property graphs for retrieval, not governed ontologies.
- Cognee is the only one that checks extracted entities against an OWL ontology. It cannot author ontologies itself.
- GraphRAG's entity-type discovery and community reports, and KGGen's entity clustering and de-duplication, could help in proposing higher-level concepts.
- LangChain has a reported bug where its relationship-type constraints are not enforced.

**Research prototypes:** OntoChat (user stories and competency questions), Ontogenia, OntoKGen and OLLM. Text2Onto and OntoGen are legacy: no current maintenance found.

**What no tool offers:**
- Importance levels for concepts.
- Detecting contradictions between different source documents. Existing checks (SHACL, OWL reasoners, a research "pitfall detector") only find logical inconsistencies inside the ontology.
- A review queue where each LLM-extracted candidate is linked to the passage in the manual it came from.

**What OntoBuilder would need to build:**
1. A candidate store that keeps each proposal's source evidence and confidence.
2. Extraction of rules from procedural text, such as warnings and constraints, using a custom schema.
3. Higher-level concept proposals that combine LLM generalisation, embedding clustering and community detection.
4. An annotation scheme and scoring for importance levels.
5. A review UI, or a handoff of approved candidates to VocBench, WebProtégé, EDG or metaphactory.
6. Contradiction detection across manuals.
7. OWL/SKOS export, and a loop where the approved ontology guides the next extraction round.

**Not checked (listed as gaps in the notes):**
- LlamaIndex PropertyGraphIndex, Diffbot, txtai and the status of the iText2KG repository.
- OntoStudio (no results found) and the 2025–2026 release activity of Protégé and WebProtégé.
- Pricing for the commercial platforms.
- Licences for Cognee, the Neo4j Labs app and Graphiti.
- Many vendor claims, for example Lettria's accuracy figures, come only from the vendors' own pages.

</details>

All six research tracks are running in the background. Once they finish, I'll combine the findings into one report at `docs/research/reports/Ontology formats and building process.md`, with the supporting notes in `docs/research/notes/Ontology formats and building process/`.

The storage research is finished. Five tracks are still running.

The tools research is finished as well, so four tracks are still running.

The research on building an ontology from text is finished, so three of the six tracks are done. Three are still running: formats, deciding what to leave out, and governance.

The governance research is finished, so four of the six tracks are done. The formats and leave-out tracks are still running.

Five of the six tracks are done. The formats research is the last one still running.

All six tracks are done, and none left a gap that blocks the report. I'm handing the notes to the report writer now.

<details>
<summary>Subagent · general-purpose · Write final report</summary>

**Prompt:**

> Read the notes in /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/ and synthesize into a research report that answers, for an "OntologyBuilder" app (idea 0002: /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/ideas/0002-ontology-builder.md — builds leveled ontologies (level-1/2/3, ignorable) from user manuals with LLM help plus human review, authoring and domain-admin governance; each ontology stored under data/ontology-<name>/ in a git monorepo):
> 1. What formats/specifications are available to store ontologies or components of an ontology?
> 2. Compare the alternatives.
> 3. Shall we store the ontology as one single file, multiple files, or in a special storage (like a graph database)?
> 4. What are the typical steps to build an ontology from a text corpus?
> 5. How to decide what not to include from a text corpus into the ontology?
> 6. What are the intermediate components from text corpus to the ontology?
> 7. What is the typical process to govern an ontology?
> 8. Are there ontology builder applications for such a use case?
> 
> Structure the report with one section per question (numbered as above), plus a short executive summary and a final "Implications for OntologyBuilder" section with recommendations. Note in a header that research files are evidence, not decisions (specs and ADRs take precedence), and that the date is 2026-11-20. Use relative Markdown links to the notes files (they are in ../notes/Ontology formats and building process/ relative to the report). Diagrams, if any, must be Mermaid.
> 
> Earlier research in this conversation to build on: none
> 
> Save your final report to this exact path: /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/reports/Ontology formats and building process.md
> 
> **As a first step, you must read /Users/belaboros/.claude/skills/synced/66493f35-7dcd-4d6e-8a87-7905c6d12798_d31955f6-e258-4ffb-8085-b268b86e7658/deep-research/references/report-writer.md for instructions on how to write your research report.**

**Output:**

I wrote the report from all six research notes and saved it here: /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/reports/Ontology formats and building process.md

It is about 5,500 words. The header says it is dated 2026-11-20 and that research files are evidence, not decisions (specs and ADRs take precedence). It has an executive summary, sections 1–8 answering the questions in order, and a closing "Implications for OntologyBuilder" section. It uses relative links to the notes, idea 0002 and the pet-manuals corpus notes, and I checked that every link resolves. It has three Mermaid diagrams: the storage layout and build, the building pipeline, and the component status lifecycle. Citations are inline and only claims that have a source URL in the notes are included.

**Answers:**
1. **Formats:** most options are W3C standards built on RDF: RDFS, OWL 2, SKOS/SKOS-XL, OntoLex, PROV-O, SHACL, plus SWRL, RIF and SHACL 1.2 Rules for rules. Others are OBO 1.4, LinkML, nanopublications, Common Logic, Topic Maps and property graphs (GQL). RDF 1.2 is only a Candidate Recommendation as of 2026, and its syntaxes and SHACL 1.2 are still Working Drafts. No standard vocabulary exists for review status or confidence. A table maps each kind of ontology component to the standard that fits it best.
2. **Comparison:** a table compares the formats on expressiveness, reasoning, readability, git diffs, LLM fitness and adoption. Turtle and LinkML YAML score best and RDF/XML worst. A benchmark of more than 30 LLMs found no significant preference between Turtle and JSON-LD on most tasks. Stable diffs come from a serializer that always writes the same output, not from the format chosen. Property graphs lose most of OWL.
3. **Storage:** keep the editable source as many files in git, build each release artefact as a single file, and use only an embedded store (rdflib or pyoxigraph) at build time. A graph database is not needed at hundreds to tens of thousands of statements.
4. **Steps:** the classical layer cake goes terms → synonyms → concepts → hierarchy → relations → axioms and rules. The report merges it with Ontology 101, METHONTOLOGY, UPON Lite and eXtreme Design, and with LLM-era pipelines (GraphRAG, KGGen, iText2KG) into a 10-step pipeline (scoping, then steps 1–9) that matches idea 0002's way of working.
5. **Exclusion:** leave out particulars (instance data), procedures (PROHOW/PKO) and plain attribute values such as numbers or colors. Corpus statistics (C-value, weirdness, domain consensus) help detect them. Level theory draws on Rosch's basic level, Guarino's ontology types and Key Concept Extraction. Assigning a level is the task LLMs do worst without examples (term typing), and their stated confidence runs too high.
6. **Intermediate components:** a table of artefacts (scope and competency questions, chunks, mentions, claims, concepts, clusters, axioms and rules, issues, decisions, releases), each with a precedent. It also suggests how to detect contradictions, gaps, ambiguity and terminology drift.
7. **Governance:** people who propose content are kept apart from people who approve it (VocBench, EDG, PoolParty). Statuses follow proposed → under review → approved → deprecated, with OBO-style deprecation instead of deletion. Releases carry version IRIs and quality gates (ROBOT report and verify). Two findings matter for LLM output: calibrated auto-accept worked well, but engineers performed worse when the LLM's advice was wrong.
8. **Tools:** PoolParty, TopBraid EDG, metaphactory, Semaphore, Stardog and Lettria cover parts of the flow. OntoGPT/SPIRES or DRAGON-AI plus VocBench or WebProtégé is the closest open-source combination. **No tool found offers importance levels or contradiction detection across source documents.**

**Recommendations in the Implications section:**
- **Source records:** keep LinkML-defined YAML or TSV records under `data/ontology-<name>/source/` with an append-only review log.
- **Release contract:** each release is a canonical Turtle file (SKOS + OWL) plus a manifest, and that is the dataset contract readers depend on.
- **No database in v1.**
- **Scoping record:** start each ontology with a scope record in the style of NeOn's requirements document (ORSD).
- **Level assignment:** combine fixed exclusion rules, an LLM rubric and corpus statistics. Never auto-accept on the LLM's own confidence score.
- **Governance:** the PR flow is the backbone, with a four-eyes rule (no approving your own edits).
- **Custom work:** build the evidence-linked candidate queue, the level assignment and cross-manual contradiction detection yourselves. The pet-manuals corpus can serve as the test set.

**Weak spots in the evidence:**
- Almost nothing was found on extracting rules or axioms from text.
- No study evaluates LLMs on assigning importance tiers.
- No tool documents provenance down to the exact text span.
- The storage size thresholds and the role matrix (RACI) are the researcher's judgement, not sourced.

</details>

The report writer is still running. I'll summarise the report once it's ready.

The report is in place. Next I'm linking it from idea 0002, as the research README asks.

Rule 2 says questions you ask about an idea are logged in it, so I'm adding these eight to idea 0002's Q&A log.

I've written the report: [docs/research/reports/Ontology formats and building process.md](docs/research/reports/Ontology%20formats%20and%20building%20process.md). It is about 5,500 words, with one section per question and every claim linked to a source. The notes behind it are in [docs/research/notes/Ontology formats and building process/](docs/research/notes/Ontology%20formats%20and%20building%20process/).

**Answers:**

1. **Formats:** the W3C standards built on RDF:
   - SKOS (with SKOS-XL and OntoLex) for terms, labels and synonyms.
   - OWL 2 for concepts and axioms.
   - SHACL for constraints.
   - PROV-O for where each statement came from.

   Other options are LinkML (YAML), the OBO flat-file format, nanopublications and property graphs. RDF 1.2 was a Candidate Recommendation as of April 2026, and its file syntaxes and SHACL 1.2 are still drafts.
2. **Comparison:**
   - Turtle and LinkML YAML do best on readability, git diffs and how well LLMs handle them; RDF/XML does worst.
   - Clean diffs depend more on always writing files the same way than on which format you pick.
   - Rules are the weak spot: no well-adopted standard exists.
   - No standard exists for review status or confidence either, so we will define our own fields.
3. **Storage:** neither a single file nor a graph database.
   - Keep the editable records as several files in git.
   - Generate a single release file per build.
   - Load everything into an embedded store only while building and checking.

   A graph database isn't worth it below millions of statements or many people editing at once.
4. **Steps:** the classic order is terms → synonyms → concepts → hierarchy → relations → axioms and rules. The report merges it with the newer LLM pipelines into ten steps (scoping first, then nine) that line up with your way of working.
5. **What to leave out:**
   - Instance-level facts and anecdotes about specific dogs, owners or recipes.
   - Step-by-step procedures, such as concrete commands.
   - Plain values such as numbers or colours.

   Corpus statistics can help flag these, for example by comparing word frequency against general text. Rosch's "basic level" idea and key-concept ranking give a basis for levels 1–3.
6. **Intermediate components:** scope and competency questions (the questions the ontology must answer), text chunks, term mentions, claims, concepts, clusters, axioms and rules, issues, review decisions, and releases.
7. **Governance:** the people who propose content are not the people who approve it.
   - Statuses go proposed → under review → approved → deprecated.
   - Nothing is deleted; old terms are marked obsolete.
   - Every release gets a version, and automated checks must pass first.
8. **Existing tools:** each covers only part of the flow.
   - Commercial: PoolParty comes closest; TopBraid EDG and metaphactory also cover parts.
   - Open source: OntoGPT or DRAGON-AI combined with VocBench is the nearest match.

**What no tool found offers:** importance levels, contradiction detection across different manuals, or a review queue linking each LLM proposal to the passage it came from. OntologyBuilder would have to build all three. The pet-manuals corpus, with its seeded contradictions and wording changes, can serve as the test set.

**Weak evidence:** almost nothing turned up on extracting rules from text. No study tests LLMs on assigning importance levels, and their own confidence scores run too high, so they shouldn't be used to accept proposals automatically. The size limits for "no database needed" are the researchers' judgement, not sourced.

I linked the report from [idea 0002](docs/ideas/0002-ontology-builder.md) and logged your eight questions with a summary answer in its Q&A log. Nothing is committed yet. Next, run `/clear` and then `/spec 0002`.

## 3 · 11:43 UTC

### Request

> Extra requirement for the ontology format research:
>  - it should be able to store cardinality for the relation. E.g.: an owner can have maximum 2 house pets according to building rules.
>  - store the link/evidence to store (via stable IDs) each element in the ontology
>  - ability to classify ontology elements to level-1, level-2, level-3
>  - the ontology shall be version controlled and stored in git
>  - future extendability: ability to add extra properties to ontology elements: terms, concepts, relations, rules, ...
> 
> Do you recommend adopting one of the existing standard ontology file formats or do you recommend creating a custom file format?

### Response

I'll answer from the research I already have. I'm also adding the answer as an addendum to the report and logging your question in idea 0002.

I recommend neither option on its own: use **your own data model, written in standard formats**. I'd skip a custom file format.

**My recommendation, in two layers:**

1. **What you edit (in git):** YAML records, one file per term, concept, relation or rule. Their structure is defined once in **LinkML**, a standard schema language. The YAML stays simple enough for people to review in pull requests and for the LLM to write reliably.
2. **What you release:** a single file per release, generated as **OWL 2 + SKOS + SHACL in Turtle**. This is the standard form that reasoners, Protégé, SPARQL and idea 0001's assistant can use.

**Your five requirements against this design:**

- **Cardinality:**
  - The source holds a `max: 2` field on a Rule record.
  - The release turns it into an OWL limit ("an owner has at most 2 house pets"), which reasoners use.
  - It also becomes a SHACL constraint, which is what actually catches a third pet in the data. OWL assumes there may be facts it hasn't been told, so on its own it won't flag the third pet.
- **Evidence by stable ID:**
  - Every record has an `evidence:` list pointing to the document, chunk and text span.
  - IDs are opaque (e.g. `concept:000123`) and never derived from labels, so renaming a term never breaks a link.
- **Levels:** a `level` field with fixed values level-1/2/3/ignorable. No standard format has a level property, so this part is custom whatever format you choose.
- **Git:** one YAML file per record gives clean diffs. The Turtle release is generated by a tool that always writes the same output, so it diffs cleanly too.
- **Extensibility:** adding a property means adding one field to the LinkML schema. Validation, the JSON format the LLM must follow, and the OWL export mapping are all regenerated from it.

**Why I'd skip each alternative:**

- **OWL/Turtle as the files you edit:** four of your five requirements are extra information attached to individual statements: evidence, level, review status and future properties. OWL can only attach these with verbose, nested structures that make diffs noisy and that LLMs write poorly. The level and status properties would be custom anyway.
- **A fully custom format:** you'd lose the reasoner, validation, Protégé, SPARQL and a standard format for apps that read the ontology. You'd also have to build every tool yourself, and you'd gain nothing LinkML doesn't already give you.

**One modelling point for `/spec`:** "max 2 pets *according to the building rules*" comes from one source and may be a local rule. Store it as a Rule record with its own evidence, linked to the relation, not as a bare number on the relation. If another manual gives a different limit, the app can then flag it as a contradiction instead of overwriting the first value.

I added this as an addendum to the [research report](docs/research/reports/Ontology%20formats%20and%20building%20process.md), with a table rating each option against each requirement. Your question and my answer are logged in [idea 0002](docs/ideas/0002-ontology-builder.md). The final choice belongs in an app-level decision record during `/plan`. Nothing is committed yet.

## 4 · 11:56 UTC

### Request

> Check that I understood your proposal:
>  - we are going to create a custom YAML fileformats (defined via LinkML) to store the ontology elements
>  - the custom YAML files will be the single sourcer of truth
>  - then we generate OWL 2 + SKOS + SHACL in Turtle to be able to use existing tools (e.g.: for reasoning), but not all the information will be there in the OWL 2 + SKOS + SHACL in Turtle files.

### Response

Yes, all three points are right. Two refinements:

1. **The flow is one-way.** The Turtle files are generated build output, so nobody edits them by hand. Every change, including a correction made in Protégé, goes back into the YAML, and then you regenerate. A check in the build or pre-commit can enforce this, for example by failing when the committed release doesn't match a fresh build.

2. **"Not all information" is our choice, not a limit of the format.** OWL annotations can carry almost anything. They're just verbose. A sensible split:
   - **In the release:**
     - Every *approved* element: terms, concepts, relations, cardinality and rules.
     - Each element's level, its status, and its evidence IDs (as annotations, so you can trace back to the YAML and the source text).
   - **Only in the YAML:**
     - Working state: candidates that were rejected or excluded, and the reasons.
     - The review and decision log, and the LLM's confidence scores.
     - The chunk text itself, and anything still waiting for review.
   - **Optionally**, a second "with-provenance" release that carries more, for example full PROV-O provenance and pending items, for people who need it.

`/spec 0002` should decide the exact contents of the release, because the release is the contract that other apps reading `data/ontology-<name>/` will depend on.

I logged this exchange in [idea 0002](docs/ideas/0002-ontology-builder.md#2026-11-21--idea--q3).

## 5 · 12:08 UTC

### Request

> Explain this to me: "with-provenance" release that carries more, for example full PROV-O provenance and pending items".
> 
> What is provenance and what do I need to know about the PRO-V format?

### Response

## What provenance is

Provenance is the history of a piece of information: **where it came from, how it was made, and who was involved**. For an ontology element, it answers questions like these:

- Which manual, chunk and sentence was it extracted from?
- Which run produced it, when, and with which LLM model and prompt version?
- Did a person write it instead?
- Who reviewed it, when, and what did they decide (accepted, corrected, rejected)?
- Which earlier version does it replace?

For OntologyBuilder this matters for three reasons:
- **Trust:** a reviewer can check a proposal against the source text.
- **Contradictions:** when manuals disagree (6 hours vs "depends on breed"), you need to know which manual said what.
- **Audit:** the domain admin can see why an element is in the ontology.

## PROV-O (the format is PROV, its OWL vocabulary is PROV-O)

**PROV-O** is a W3C standard (a Recommendation since 2013) for writing provenance down in RDF. What you need to know:

1. **It is a vocabulary, not a file format.** It gives you a set of agreed class and property names. You write them in Turtle or JSON-LD, like any other RDF, so they can sit in the same file as your OWL and SKOS.

2. **The core is three classes.** You rarely need more:
   - **Entity:** a thing. Examples: a manual, a chunk, a concept, a rule.
   - **Activity:** something that happened. Examples: an extraction run, a review.
   - **Agent:** someone or something responsible. Examples: a user, the domain admin, the OntologyBuilder app, the LLM.

   A handful of properties connect them:

   | Property | Meaning |
   |---|---|
   | `prov:wasGeneratedBy` | entity → the activity that created it |
   | `prov:used` | activity → the entity it read |
   | `prov:wasDerivedFrom` | entity → the entity it came from |
   | `prov:wasAssociatedWith` | activity → the agent that ran it |
   | `prov:wasAttributedTo` | entity → the agent responsible for it |
   | `prov:startedAtTime` / `prov:endedAtTime` | when an activity ran |
   | `prov:wasRevisionOf` | new version → old version |

3. **An example in OntologyBuilder terms** (IDs are illustrative):

   ```turtle
   :concept-000123  a skos:Concept ;
       skos:prefLabel "house pet"@en ;
       prov:wasDerivedFrom   :chunk-bhr-04-002 ;     # the evidence
       prov:wasGeneratedBy   :run-0007 .             # the extraction run

   :run-0007  a prov:Activity ;
       prov:used              :chunk-bhr-04-002 ;
       prov:wasAssociatedWith :ontology-builder, :llm-claude ;
       prov:startedAtTime     "2026-11-21T10:00:00Z"^^xsd:dateTime .

   :review-0042  a prov:Activity ;                   # the approval
       prov:used              :concept-000123 ;
       prov:wasAssociatedWith :domain-admin-1 .
   ```

4. **Two gaps you have to fill yourself:**
   - **No review status or confidence.** PROV-O has no "approved / pending / rejected" and no "LLM confidence 0.8". We add our own properties for these, as we already do for levels.
   - **Attaching provenance to a single statement is not PROV-O's job.** It describes *things*. To attach provenance to one axiom, such as "an owner has at most 2 house pets", you need a container around that statement: OWL axiom annotations, named graphs, or RDF 1.2 reifiers once they are final. This is the verbose part, and it is why the YAML is the editable source.

5. **It gets big.** A full provenance trail can easily be larger than the ontology itself: every run, every chunk, every review. That is why it goes in a separate release.

## What the "with-provenance" release means

The name is my proposal, not a standard. The idea is two generated release files instead of one:

| | **Standard release** | **With-provenance release** |
|---|---|---|
| For | Apps that use the ontology (e.g. idea 0001's assistant), reasoners, Protégé | Reviewers, the domain admin, auditors, debugging |
| Content | Approved elements, with level, status and evidence IDs | Everything in the standard release, plus the full PROV-O trail: runs, chunks, review activities, who did what and when |
| Pending items | Left out | Included, marked with their status (`proposed`, `under review`), so tools can show the full picture |
| Size | Small | Larger |

Pending items are candidates that nobody has approved or rejected yet. Apps that use the ontology should never see them as facts. Someone reviewing in Protégé, though, may want to see them next to the approved content.

**In the YAML nothing changes:** provenance is just plain fields on each record (`evidence`, `generated_by`, `reviewed_by`, `reviewed_at`). PROV-O is only how those fields are written in the export. If nobody needs the second release, we skip it and lose nothing, because the YAML keeps everything.

Whether to build that second release is a decision for `/spec 0002`. I logged this question in [idea 0002](docs/ideas/0002-ontology-builder.md).

## 6 · 12:25 UTC

### Request

> Let's look into the options for review/governance/approval.
> 
> I prefer review/governance/approval both
>  - "textual review" on the extracted statements
>  - "visual review" on the generated taxony diagrams and ontology diagrams
> With extra convenience options to make review, understanding and decision efficient:
>  - filter by level
>  - use special colors to highlight previously approved vs under-review and just-proposed elements
>  - ability to type and create corrected or new statements in the GUI.
> I prefer a rich GUI interface so the users could work efficiently.
> 
> Is there an existing ontology governance application with such a capability?
>  
> If I need to create a custom GUI application, 
> shall it use the editable custom YAML files
> or the generated read-only files
> or both?

### Response

I'll start by checking what the tools research already found about visual review and editing.

The earlier tools research didn't look at visual review: diagram views, filtering, colour by status. I'm starting one focused research task on that while I work out the YAML question.

<details>
<summary>Subagent · general-purpose · Research ontology review GUIs</summary>

**Prompt:**

> Research which existing ontology / taxonomy / knowledge-graph governance applications offer a rich GUI for reviewing and approving content both textually and visually, and which UI building blocks exist for a custom GUI.
> 
> Context: an "OntologyBuilder" app (idea 0002, /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/ideas/0002-ontology-builder.md) extracts statements, terms, concepts, relations (with cardinality) and rules from user manuals with an LLM. Each element has a level (level-1/2/3/ignorable), a status (proposed / under review / approved / rejected) and evidence IDs to source text. The source of truth is custom YAML records defined by a LinkML schema, kept in git. OWL 2 + SKOS + SHACL Turtle is generated from them. Earlier tool research is in /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/existing_tools.md and governance_process.md; read them first and do not repeat them. Focus only on GUI and review capabilities.
> 
> The user wants these GUI features:
> 1. Textual review of extracted statements: list or table, accept/reject/correct, with the source evidence shown.
> 2. Visual review on generated taxonomy diagrams (is-a / broader trees) and ontology diagrams (concepts + relations graph).
> 3. Filtering by a custom property (level).
> 4. Colour-coding by status: previously approved vs under review vs just proposed.
> 5. Typing and creating corrected or new statements in the GUI.
> 6. Approval workflow with roles (user vs domain admin).
> 
> Key questions:
> - For each tool, which of features 1–6 does it support, with sources? Tools: WebProtégé, Protégé desktop (+ OntoGraf, VOWL/ProtégéVOWL plugins), VocBench 3, TopBraid EDG (graph views, forms), Graphwise PoolParty (visual taxonomy, GraphViews), metaphactory (visual ontology editor, 6.0), Progress Semaphore, Stardog Designer/Explorer, Fluent Editor, gra.fo, WebVOWL, Ontodia/Reactodia, Neo4j Bloom / NeoDash, Chowlk, LinkML tooling (schemasheets, linkml-browser, any LinkML data editor), OAK, Ontotext GraphDB Workbench visual graph, others found (2024–2026).
> - Can any of them use custom properties (a level annotation, a status annotation) to filter or colour nodes? Can any edit a custom YAML/LinkML store directly, or do they all require RDF/OWL import and their own store? How hard is a round trip back to our YAML?
> - Is there one tool that covers all six features? Which is the closest, and at what licence and cost?
> - For a custom GUI: which graph and diagram libraries fit (Cytoscape.js, React Flow / xyflow, Sigma.js + graphology, Reactodia, ELK/elkjs layouts, D3, vis-network, Mermaid)? Compare them on layout of trees and graphs, size limits, interactivity (click to edit, filter, styling by data attributes) and licence.
> - Any examples of git-backed ontology or vocabulary editors with a web GUI (e.g., writing PRs or commits from a web editor; Skosmos is read-only; VocBench with git? Wikibase?).
> 
> Constraints: current state as of 2026; mark discontinued tools as such.
> 
> Save your output notes to /Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/review_gui_tools.md
> 
> **As a first step, you must read /Users/belaboros/.claude/skills/synced/66493f35-7dcd-4d6e-8a87-7905c6d12798_d31955f6-e258-4ffb-8085-b268b86e7658/deep-research/references/researcher.md for instructions on how to conduct research.**

**Output:**

I wrote the notes to `/Users/belaboros/_LOCAL_WORK/my_github/DomainAiAssistant/docs/research/notes/Ontology formats and building process/review_gui_tools.md`. No single tool covers all six GUI features. I ran about 22 searches and fetches. Many findings come from search summaries of vendor docs rather than full page reads (marked "(summary)" in the notes), and I tested nothing hands-on.

**Coverage**
- **Approval, roles and form editing (F5, F6):** VocBench 3, TopBraid EDG, PoolParty and metaphactory are strong here.
- **Diagrams (F2):** in all four, the diagrams are mostly for exploring, and nodes are coloured by type or class, not by a custom status or level.
- **The two gaps everywhere:** no tool shows the source evidence next to each extracted candidate (F1), and none colours diagram nodes by status (F4). These are the two features most specific to reviewing LLM output.
- **Tool by tool:**
  - **VocBench 3:** the graph view uses only a d3 force-directed layout (no tree diagram). Colours are fixed by resource type and property kind. The docs do not describe editing inside the graph.
  - **TopBraid EDG:** its diagram panel was read-only for data in 7.1; I could not confirm whether that is still true in 9.x.
  - **PoolParty:** GraphViews gives Tree, Overview and Detail views but is a viewer only; editing happens in the taxonomy tree or the separate GraphEditor.
  - **metaphactory:** it has a visual editor, custom metadata properties on elements (5.5), a review workflow with status and comments (5.6), and collaborative editing with the AI assistant in 6.0.
- **Closest overall:** metaphactory 6, then PoolParty Enterprise with GraphViews and GraphEditor. Neither publishes prices. The best open-source option is VocBench 3, which covers editing and approval with only a basic graph.
- **Colouring by a custom property:** only Neo4j Bloom and NeoDash document it. GraphDB's visual graph colours nodes by whatever a configurable query returns as `?type`, so it should work there too, but that is my inference, not documented. None of these has an ontology approval workflow.

**YAML and round trip**
- None of the tools edits LinkML YAML directly. Each needs an RDF or OWL import into its own store.
- A round trip back to our YAML would be lossy and laborious. Level, status and evidence IDs would have to become annotation properties. Each tool keeps its own history and workflow state, which would need mapping back. Cardinality restrictions make stable reverse mapping hard.
- The lower-friction pattern: keep YAML in git as the source of truth, use external tools read-only for visual inspection, and make decisions in a custom UI that writes YAML.
- The LinkML tools that can edit YAML have no diagrams or workflow. DataHarmonizer is a spreadsheet-style grid, and JSON-Schema forms need a conversion step. schemasheets edits schemas, not data. linkml-browser is a read-only faceted browser.

**Discontinued**
- **Gra.fo:** data.world ended it on 2026-03-13.
- **Ontodia:** archived; Reactodia is the maintained fork.
- **ProtégéVOWL:** has never had a release and lists known bugs. Protégé Desktop 5.6.9 itself is maintained.

**Libraries for a custom GUI**
- **Recommended:** Cytoscape.js (MIT) with elkjs layouts, for both is-a trees and relation graphs, with styling and filtering driven by status and level.
- **Alternative:** React Flow / xyflow with elkjs or dagre, if editable node cards with inline forms matter more than graph size.
- **Worth evaluating:** Reactodia (LGPL-2.1 or later), because it reads RDF directly.
- **Large graphs:** Sigma.js with graphology only if graphs grow beyond about 10,000 elements.
- **Mermaid:** fine for static docs and PR previews, not for interactive review.
- I confirmed licences only for Cytoscape.js and Reactodia. The others (React Flow, Sigma.js, elkjs, D3, vis-network, Mermaid) are marked unverified in the notes.

**Git-backed web editors**
- No released, maintained web editor that edits ontology files and opens PRs was found.
- **SkoHub Vocabs:** Turtle files on GitHub or GitLab, review through branches and PRs, published as a static site.
- **VoCol / Git4Voc:** validation and visualisation on top of a git repository.
- **TurtleEditor:** a research web editor for Turtle files in a repository.
- **WebProtégé:** a GitHub integration service is in development (last push reported 2025-09), but no released git-backed editing was confirmed.
- The SkoHub-style pattern (files in git, a PR as the approval step, required reviewers standing in for the domain admin) fits our design best.

**Not researched or unconfirmed**
- Progress Semaphore's visual views
- Fluent Editor's GUI
- OAK
- Wikibase
- NeoDash editable forms
- Whether EDG, PoolParty or metaphactory can colour or filter diagrams by a custom annotation

</details>

The research on review GUIs is still running. When it's back, I'll answer both questions together: whether an existing tool covers your six features, and whether a custom GUI should work on the YAML files, the generated files, or both.

No existing application covers all of your review features. You'd build a custom GUI. It should **read and write the editable YAML files, and only read the generated files**.

## Is there an existing application with these features?

| Feature | Best existing coverage |
|---|---|
| Textual review (accept, reject, correct) | VocBench 3, TopBraid EDG, PoolParty, metaphactory: good forms and workflows, but **none shows the source passage next to each candidate the LLM extracted** |
| Taxonomy and ontology diagrams | All four have diagram views, but mostly for exploring. PoolParty's diagram views can't be edited. VocBench has only a loose network layout, no tree view. |
| Filter by level | Possible only through custom properties, and not documented for diagrams |
| Colours by status | **No ontology tool does it.** Only the Neo4j viewers (Bloom, NeoDash) colour nodes by a custom property, and they have no approval workflow. |
| Type corrected or new statements | Yes, in all four, through forms |
| Approval workflow with roles | Yes: VocBench 3 (open source), EDG, PoolParty, metaphactory |

- **Closest overall:** metaphactory 6 (commercial, price not published), with a visual editor, custom metadata, a review workflow and an AI assistant. PoolParty Enterprise is second.
- **Best open-source option:** VocBench 3, which has editing and approval but only a basic graph view.
- **The deciding problem:** none of them edits our LinkML YAML. Each tool imports RDF into its own store, so level, status and evidence become annotations and the tool keeps its own workflow state. Syncing back to the YAML would lose information and take a lot of work.

## A custom GUI should use the YAML for everything it changes

- **Read and write the YAML.** It's the only place that holds the full state: candidates that are pending, excluded or rejected, their level and status, and their evidence. It's also the only thing users are allowed to change. Every approval, correction or new statement in the GUI is saved as a YAML record, checked against the LinkML schema.
- **Only read the generated files.** Show build results as overlays and never write them:
  - validation errors as warning badges;
  - parent–child links the reasoner worked out, drawn in a different line style;
  - flags for contradictions, gaps and ambiguity.

  Re-run the build after a save to refresh them.
- **Draw diagrams from the YAML model, not from the Turtle.** The release leaves out pending items, so diagrams drawn from it couldn't show your colours for "proposed" or "under review".
- **External tools stay useful as viewers.** Protégé or WebVOWL can open the release Turtle to check reasoning or to share it.

Building blocks to evaluate in `/plan`:
- **Backend:** a small service that owns reading and writing the YAML, validation and git (for example a commit per review session, and a pull request as the release gate).
- **Diagrams:** Cytoscape.js with the elkjs layout engine (both MIT-licensed) covers both trees and relation graphs, with filtering and styling by level and status. React Flow is the alternative if you want editable cards inside the diagram.
- **Precedent:** the closest published example of "files in git, pull request as approval" is SkoHub Vocabs.

## Open questions for `/spec 0002`

- One user at a time on a local machine, or several users at once on a shared server? Simultaneous edits to the YAML would need locking or merge handling.
- How do users log in, and how are the user and domain-admin roles assigned?
- Is approval a status change in the GUI, a pull-request approval in GitHub, or both?

I added this as a second addendum to the [research report](docs/research/reports/Ontology%20formats%20and%20building%20process.md), with the details in [review_gui_tools.md](docs/research/notes/Ontology%20formats%20and%20building%20process/review_gui_tools.md). Your question is logged in [idea 0002](docs/ideas/0002-ontology-builder.md). Nothing is committed yet.

## 7 · 12:41 UTC

### Request

> Let's look into the consumers of the ontology.
> The ontology will be used for multiple use-cases.
> 
> Use-case #1: education
>  - a user reads generated (human friendly) level-1.md, level-2.md or level-3.md files tu understand the domain
>  - the level*.md files contain: visual diagrams: taxonomy, ontology, ... and catalogs: concepts, relations, rules, ...
>  - there is a raw version of the files which contains all the un-approved elements and a governed version which contains only the approved elements.
> 
> 
> Use-case #2: Domain AI assistant/agent
>  - it is a chat interface to answer questions about a domain
>  - the AI assistant/agent uses traditional keyword search, RAG search, knowledge graph search, ....
>     as well as the ontology to answer the questions accurately and with consistent reliabiliy.
> 
> Use-case #3: validation
>  - validate texts against the governed ontology.
>  - find contradictions, terminology drift
> 
> Do you recommend using the custom YAML files for those 3 use-cases or the generated standard OWL 2 + SKOS + SHACL in Turtle files?

### Response

I recommend the **generated files for all three use cases, never the YAML**. The release should be built in two variants, governed and raw, each with the same set of files.

**Why the YAML stays private.** The YAML is OntologyBuilder's working state:
- Its layout changes whenever the LinkML schema changes.
- It mixes approved, pending and rejected items.

The repo's data-sharing rule (ADR-0013) is that readers rely only on the dataset contract. So the contract should describe the release, and only OntologyBuilder reads the YAML. This also guarantees that unapproved content can't reach the assistant or the validator by accident.

**What each release variant contains:**

| | Governed (approved only) | Raw (everything not rejected) |
|---|---|---|
| Turtle (OWL 2 + SKOS + SHACL) | the main machine contract | each element carries its status |
| JSON-LD | optional, for apps that prefer JSON | optional |
| `level-1.md`, `level-2.md`, `level-3.md` | Mermaid diagrams + catalogues | same, with unapproved elements marked |
| `manifest.json` | version, date, counts | same |

The raw variant replaces the "with-provenance" release I suggested earlier, so there is one extra variant, not two.

**Per use case:**

1. **Education.**
   - The `level-N.md` files come out of the same build step as the Turtle, so the two can never disagree.
   - Readers need no ontology tools.
   - A level-3 ontology diagram will probably be too big for one Mermaid chart, so split it by topic.
2. **AI assistant.** It loads the governed Turtle into an embedded store (rdflib or pyoxigraph), then:
   - answers multi-hop questions with SPARQL;
   - uses SKOS synonyms to match the user's wording;
   - uses levels to decide how deep an answer goes;
   - treats rules and cardinalities as facts it can check.

   The evidence IDs let it cite the manual passage and match ontology results with RAG results on the same chunk. That only works if chunk IDs are stable and published as part of a contract.
3. **Validation.** It uses the governed Turtle, but that release must carry more than approved terms:
   - allowed synonyms;
   - known variants that should not be used;
   - scope notes that separate meanings (*lead* the rope vs *lead* the role);
   - retired terms with their replacements.

   Contradiction checks compare claims extracted from the new text against the release's rules and limits.

**Sharing code.** The assistant and the validator will both load and query the release, so that loader belongs in a library under `libs/` (rule 6), not inside one of the apps. The step that extracts claims from text could be shared the same way.

**Open questions for `/spec 0002`:**
- Does `level-2.md` include everything in level 1, or only what level 2 adds?
- Is validation a separate app, or a feature of OntologyBuilder? A feature may read its own YAML; a separate app may not.
- Is the raw variant committed to git, or only built locally?
- Which chunk-ID scheme becomes part of the contract?

I added this as a third addendum to the [research report](docs/research/reports/Ontology%20formats%20and%20building%20process.md) and logged your question in [idea 0002](docs/ideas/0002-ontology-builder.md). Nothing is committed yet. Next, run `/clear` and then `/spec 0002` when you're ready.

## 8 · 12:47 UTC

### Request

> Level-2 contains everything from level-1 plus an extra set of concepts, relations, rules, ...
> Level-3 includes everything from level-2 and includes all the ontology elements.
> 
> RAW should be also version controlled in git.

### Response

I've logged both answers in [idea 0002](docs/ideas/0002-ontology-builder.md#2026-11-21--idea--q7).

**Levels are cumulative.** Level 1 is contained in level 2, which is contained in level 3, and level 3 is the whole ontology. The release can therefore store a single minimum level on each element and filter on it:
- `level-1.md` shows only level-1 elements.
- `level-2.md` shows level-1 and level-2 elements.
- `level-3.md` shows everything.

I made one assumption, which `/spec` should confirm: elements marked `ignorable` appear in no level at all. In the raw variant, level 3 means every element that hasn't been rejected or marked ignorable.

**The raw release goes into git**, next to the governed one. That has two consequences:
- `data/ontology-<name>/` is a dataset that gets committed (ADR-0016). Its owner records that choice when the dataset is scaffolded.
- The raw files change on every extraction run and every review. To keep diffs readable, the generator must always write the same output for the same input: sorted elements, stable IDs and no blank nodes. A pre-commit check should fail if the committed release doesn't match a fresh build, which also stops anyone editing generated files by hand.

Two questions are still open for `/spec 0002`:
- Is validation a separate app or a feature of OntologyBuilder?
- How are chunk IDs defined, so that the assistant can join ontology results with RAG results?

When you're ready, run `/clear` and then `/spec 0002`.

## 9 · 12:53 UTC

### Request

> Validation mentioned in use-case 3 will be a dedicated app stored in this monorepo.
> But I think validation will be needed in the ontology governance rich GUI application as well
> (which will be also part of this monorepo).
> 
> Can you propose alternatives to define chunk IDS?
> Criteria:
>  - stanble IDs across changes.
>  - the user manuals will be upgraded regularly
>  - the OntologyBuilder should be able to ingest the new version and identify which statements are the same and which statements have been deleted/modified and propagate the changes to the ontology elements of the those statements

### Response

## Validation in two apps

Apps in this repo never import from each other (rule 6), so the shared part goes into a **validation library** under `libs/`, which both apps call.

- **Input:** an RDF graph of the ontology, plus the text or claims to check.
- **Dedicated validation app:** passes it the governed release.
- **Governance GUI:** passes it the graph built from its in-memory model, including unapproved items, so users see contradictions while they review.

**One thing to check:** the GUI writes the YAML. If the GUI is a separate app from OntologyBuilder, two apps would write the same dataset, which the one-writer rule (ADR-0013) forbids. I recommend making the GUI **part of the OntologyBuilder app**, as a web interface next to the ingestion pipeline, not a separate app.

## Chunk IDs: the alternatives

No single ID can stay the same when the text changes and also tell you that the text changed. So each piece of source text gets three separate things:
- a **stable ID** that never changes;
- a **location** (path, heading, paragraph);
- a **content hash** of its text.

| Scheme | Stable across upgrades? | Verdict |
|---|---|---|
| A. Position (path + chunk number) | ❌ one inserted paragraph shifts every later ID | reject |
| B. Structural path (path + heading + paragraph number) | ⚠️ breaks on a heading rename or a file move | use as the *location* |
| C. Content hash | ❌ fixing a typo makes it look like delete + add | use as the *fingerprint* |
| **D. Assigned opaque ID + registry + alignment** | ✅ survives edits, moves and renames | **recommended as the identity** |
| E. IDs written into the source Markdown | ✅ stable by construction | use where we generate the manuals ourselves |
| F. W3C Web Annotation selectors (quote + surrounding text + offsets) | ✅ can be found again after small edits | use to point at an exact span inside a unit |

**How the recommended combination works:**

1. **Keep source units separate from RAG chunks.** Evidence points at *source units*: a sentence or short passage that statements are extracted from. RAG chunks only list which units they cover, so you can change the chunk size for search without breaking any evidence link.
2. **Store every unit in a registry.** The first time a unit is seen it gets a new opaque ID. The registry records:
   - the ID and the document ID;
   - the location and the content hash;
   - the text;
   - the first and last manual version it appeared in.
3. **Align each new manual version** against the registry:

   | Result | How it's recognised | What happens to the ID |
   |---|---|---|
   | Unchanged | same hash, same place | kept |
   | Moved | same hash, different place | kept |
   | Modified | similar text near the same place | kept, with a new revision |
   | Uncertain | a borderline match | a person decides in the GUI |
   | Deleted | no match in the new version | marked retired, never removed from the registry |
   | New | no match in the registry | a new ID is assigned |

4. **Propagate changes through the evidence links:**
   - **Unchanged or moved:** nothing happens, and approved elements stay approved.
   - **Modified:** the element is extracted again from the new text.
     - Same meaning: it keeps its status.
     - Different meaning: it goes back to *under review*, with an old/new text diff.
   - **Deleted:** that evidence link is removed. An element with no evidence left is flagged as orphaned, and the GUI proposes deprecating it; it is never deleted automatically.
   - **New:** normal extraction runs, and the results are *proposed*.

The full comparison and the rules for matching and propagation are in [source_ids_and_change_propagation.md](docs/research/notes/Ontology%20formats%20and%20building%20process/source_ids_and_change_propagation.md). This one is my design proposal rather than sourced research, and the note says so. I logged your question in [idea 0002](docs/ideas/0002-ontology-builder.md).

## Open questions for `/spec 0002`

- **Is the GUI part of the OntologyBuilder app?** I recommend yes.
- **Who owns the source registry?** It needs exactly one writer, otherwise two apps will assign different IDs to the same text. The options:
  - OntologyBuilder publishes it inside `data/ontology-<name>/`, and the assistant reads it from there.
  - A separate corpus dataset, `data/corpus-<name>/`, which OntologyBuilder and the assistant both read. This is the better choice if one set of manuals will feed several ontologies, or feed the assistant directly.

## 10 · 13:17 UTC

### Request

> Yes, let the OntologyBuilder app contain the rich GUI for users to review/govern the ontologies.
> 
> I prefer storing the source registry in a sub-directory under data/ontology-<name> for the sake of simplicity.

### Response

I've logged both decisions in [idea 0002](docs/ideas/0002-ontology-builder.md).

The OntologyBuilder app now holds the ingestion pipeline and the review GUI, and it is the only app that writes `data/ontology-<name>/`. Everything we've decided so far gives a layout roughly like this, as a starting point for `/spec`:

```
data/ontology-<name>/                 (committed dataset, written only by OntologyBuilder)
├── sources/      source registry: documents, source units, IDs, hashes, revisions per manual version
├── model/        editable YAML records (LinkML): terms, concepts, relations, rules, evidence, levels, status
├── decisions/    append-only review and decision log
└── release/
    ├── governed/ ontology.ttl (OWL 2 + SKOS + SHACL), level-1.md, level-2.md, level-3.md, manifest.json
    └── raw/      the same files, including unapproved elements with their status
```

The dataset contract in `libs/contracts/` covers `release/` and `sources/`. The assistant needs `sources/` to join ontology results with RAG chunks, so other apps may read it. `model/` and `decisions/` stay internal to OntologyBuilder.

The dataset contract will need a field-level schema for `sources/`. Changing the IDs or hashes later would break every app that reads them and require a root ADR, so `/spec` should fix that schema early.

All the open questions from this session are now answered and logged in the idea, so it's ready for `/clear` and then `/spec 0002`. None of today's files are committed yet; when you want them committed, `/commit-push-merge-feature-branch` does it.

## 11 · 13:24 UTC

### Request

> A. Let's use number prefixes to express processing order for the sub-directories under data/ontology-<name>
> 
> 00_sources/
> 01_model/
> 02_decisions
> 03_release/00_raw
> 03_release/01_governed
> 
> B. Let's store the statements created by the user (in the rich GUI app) under 00_sources/90_user_statements/
> 
> So statements can be ingested from source text corpus or defined by the user, and all of them are stored under 00_sources/ directory.

### Response

I've logged the layout in [idea 0002](docs/ideas/0002-ontology-builder.md). Here it is with both changes:

```
data/ontology-<name>/
├── 00_sources/
│   ├── 00_<corpus>/            ingested corpus, e.g. 00_user-manuals-pets-and-house-rules/
│   │                           (registry: documents, source units, IDs, hashes, revisions)
│   ├── 01_<another-corpus>/    room for more corpora, numbered 00–89
│   └── 90_user_statements/     statements typed by users in the GUI
├── 01_model/                   editable YAML records (LinkML)
├── 02_decisions/               append-only review and decision log
└── 03_release/
    ├── 00_raw/
    └── 01_governed/
```

Treating user statements as sources has one clear benefit: **every ontology element now has evidence**. An element a user authors cites the user's statement, just as an extracted element cites a manual passage. The pipeline, the GUI and the release then handle both kinds the same way. There are three differences to carry into the spec:

- **Provenance:** a user statement records its author and timestamp instead of a document and location.
- **No alignment step:** users edit their statements in place, and each edit becomes a new revision under the same ID.
- **Still governed:** a user statement and the elements derived from it start as *proposed* and still need domain-admin approval. One question for `/spec`: does a statement authored by the domain admin need a second approver (the four-eyes rule), or can the admin approve their own?

**Contract:** `00_sources/`, including user statements, and `03_release/` are what other apps may read. `01_model/` and `02_decisions/` stay internal to OntologyBuilder.

## 12 · 13:28 UTC

### Request

> Let's make it simple. So the domain admin can approve his/her own modifications next to the ingested/proposed elements and statements from regular (non-domain-admin) users.

### Response

I've logged it in [idea 0002](docs/ideas/0002-ontology-builder.md): there's no four-eyes rule.

- **Regular users** review and correct the proposed elements and add statements, but can't approve anything.
- **The domain admin** approves everything: what the LLM proposed, what regular users wrote, and their own changes.
- Each approval is still recorded in `02_decisions/` with who approved it and when.

The decision questions from this session are all logged, so the next step is `/clear`, then `/spec 0002`.
