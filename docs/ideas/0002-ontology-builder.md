# 0002 · OntologyBuilder: build leveled ontologies from text corpora and human input

- **Status:** captured
- **Scope:** TBD (decided by `/spec`: `system`, or the name of one app) (mentions: OntologyBuilder app, `data/ontology-<name>` datasets)
- **Captured:** 2026-11-20
- **Spec:** _none yet_

## Original idea

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

Related: this idea expands the "ontology builder" and "governance process" parts of [idea 0001](0001-manual-ontology-assistant.md). A likely first corpus is [data/user-manuals-pets-and-house-rules/](../../data/user-manuals-pets-and-house-rules/), with its answer key (seeded contradictions, terminology drift, gaps) in [docs/research/notes/pet-manuals-corpus/](../research/notes/pet-manuals-corpus/README.md).

Research: [Ontology formats and building process](../research/reports/Ontology%20formats%20and%20building%20process.md) (2026-11-20). It covers storage formats, single vs multiple files vs a graph DB, the text-to-ontology pipeline and its intermediate artefacts, exclusion criteria, governance and existing tools.

## Q&A log

<!--
Append one entry per question, oldest first. Never delete entries.

### YYYY-MM-DD · <stage: idea | spec | plan | implement | review | architecture | scaffold> · Q<n>
**Asked by:** Claude | user
**Q:** [<skill · stage>] <question exactly as asked>
**Options offered:** <list, or "free text">
**A:** <the answer, verbatim if it is the user's; a summary if it is Claude's>
**Effect:** <what changed because of it, e.g. "added FR-4 to spec">
-->

### 2026-11-20 · idea · Q1
**Asked by:** user
**Q:** Research the internet: 1. what formats/specifications are available to store ontologies or components of an ontology. 2. Compare the alternatives 3. Shall we store the ontology as one single file or multiple files or in a special storage (like a graph database) 4. What are the typical steps to build an ontology from text corpus? 5. How to decide what not to include from a text corpus into the ontology? 6. What are the intermediate components until we get from text corpus, ..., to the ontology? 7. What is the typical process to govern an ontology? 8. Are there ontology builder applications for such a use-case?
**Options offered:** free text
**A:** (Claude, summary) Research report [Ontology formats and building process](../research/reports/Ontology%20formats%20and%20building%20process.md). Formats: the W3C RDF stack (SKOS for vocabulary, OWL 2 for axioms, SHACL for constraints, PROV-O for provenance) plus LinkML. No standard exists for review status or confidence. Storage: modular files in git as the source of truth, a generated single-file Turtle release, an embedded store only at build time, and no graph database at this size. Pipeline: the "layer cake" from terms to axioms, plus LLM-era chunking, entity resolution and clustering. Exclusion: particulars and anecdotes (ABox) and procedures. Governance: proposer and approver are different people, statuses run proposed → under review → approved → deprecated, nothing is deleted, releases are versioned. Tools: PoolParty, TopBraid EDG, metaphactory, OntoGPT/DRAGON-AI and VocBench each cover parts. None offers importance levels or contradiction detection across documents.
**Effect:** Report linked from this idea; input for `/spec 0002`.

### 2026-11-21 · idea · Q2
**Asked by:** user
**Q:** Extra requirement for the ontology format research: - it should be able to store cardinality for the relation. E.g.: an owner can have maximum 2 house pets according to building rules. - store the link/evidence to store (via stable IDs) each element in the ontology - ability to classify ontology elements to level-1, level-2, level-3 - the ontology shall be version controlled and stored in git - future extendability: ability to add extra properties to ontology elements: terms, concepts, relations, rules, ... Do you recommend adopting one of the existing standard ontology file formats or do you recommend creating a custom file format?
**Options offered:** free text
**A:** (Claude, summary) Neither a pure standard nor a custom file format: a custom data model written in standard formats. Define the model in LinkML; keep the working records as YAML files in git (one file per record, stable opaque IDs, evidence IDs, a level enum, extensible slots). Generate the release as OWL 2 + SKOS + SHACL Turtle: OWL qualified cardinality for reasoning, SHACL for validating data. Model "max 2 pets per the building rules" as a sourced Rule record linked to the relation, so conflicting values in other manuals surface as contradictions. Added as an addendum to the [research report](../research/reports/Ontology%20formats%20and%20building%20process.md#addendum-2026-11-21-standard-format-or-custom-format).
**Effect:** Five requirements to carry into `/spec 0002`; format choice to be recorded as an app ADR in `/plan`.

### 2026-11-21 · idea · Q3
**Asked by:** user
**Q:** Check that I understood your proposal: - we are going to create a custom YAML fileformats (defined via LinkML) to store the ontology elements - the custom YAML files will be the single sourcer of truth - then we generate OWL 2 + SKOS + SHACL in Turtle to be able to use existing tools (e.g.: for reasoning), but not all the information will be there in the OWL 2 + SKOS + SHACL in Turtle files.
**Options offered:** free text
**A:** (Claude, summary) Yes on all three, with two refinements. (a) The flow is one-way: the Turtle files are generated build output and are never edited by hand; corrections go into the YAML. (b) "Not all information" is a choice we make in the export, not a limit of the format. The release keeps every approved element, with its level, status and evidence IDs as annotations. It leaves out the working state: rejected or excluded candidates, the review log, LLM confidence, chunk text. An optional "with-provenance" release variant can include more.
**Effect:** Understanding confirmed; the export content (what the release includes and what it leaves out) to be specified in `/spec 0002`.

### 2026-11-21 · idea · Q4
**Asked by:** user
**Q:** Explain this to me: "with-provenance" release that carries more, for example full PROV-O provenance and pending items". What is provenance and what do I need to know about the PRO-V format?
**Options offered:** free text
**A:** (Claude, summary) Provenance is the record of where an element came from and how it got its current state: the source text, the extraction run, the people who reviewed it, and when. PROV-O is the W3C vocabulary for writing that down in RDF (a Recommendation since 2013). It is a vocabulary, not a file format, written in Turtle or JSON-LD. Its core is Entity, Activity and Agent, linked by wasGeneratedBy, used, wasDerivedFrom, wasAttributedTo and wasAssociatedWith. It does not define confidence or review status, and it does not attach provenance to a single axiom such as a cardinality limit; that needs named graphs or OWL axiom annotations. The "with-provenance" release is a proposed second release file. It adds the full PROV-O trail and the items still waiting for review, for reviewers and auditors. The default release stays lean for apps that read the ontology. In the YAML the provenance is plain fields; PROV-O is only the export form.
**Effect:** None yet; whether to produce the with-provenance variant is decided in `/spec 0002`.

### 2026-11-21 · idea · Q5
**Asked by:** user
**Q:** Let's look into the options for review/governance/approval. I prefer review/governance/approval both - "textual review" on the extracted statements - "visual review" on the generated taxony diagrams and ontology diagrams With extra convenience options to make review, understanding and decision efficient: - filter by level - use special colors to highlight previously approved vs under-review and just-proposed elements - ability to type and create corrected or new statements in the GUI. I prefer a rich GUI interface so the users could work efficiently. Is there an existing ontology governance application with such a capability? If I need to create a custom GUI application, shall it use the editable custom YAML files or the generated read-only files or both?
**Options offered:** free text
**A:** (Claude, summary) No existing tool covers all of it. VocBench 3, TopBraid EDG, PoolParty and metaphactory do workflow and form editing well, but their diagrams are mostly for exploring. None shows source evidence per LLM candidate or colours nodes by review status, and none edits our LinkML YAML; a round trip would be lossy. The closest is metaphactory 6 (commercial), and the best open-source option is VocBench 3. A custom GUI should read and write only the YAML (the full state and the only editable source) and only read the build output (validation results, inferred hierarchy, contradiction issues) as overlays. Diagrams are drawn from the YAML model; Cytoscape.js + elkjs is a candidate. See the [report addendum](../research/reports/Ontology%20formats%20and%20building%20process.md#addendum-2026-11-21-review-gui-existing-tools-or-custom).
**Effect:** GUI requirements (textual and visual review, level filter, status colours, in-GUI authoring, roles) to carry into `/spec 0002`. Open: single-user local vs multi-user server; how approval maps to git PRs.

### 2026-11-21 · idea · Q6
**Asked by:** user
**Q:** Let's look into the consumers of the ontology. The ontology will be used for multiple use-cases. Use-case #1: education - a user reads generated (human friendly) level-1.md, level-2.md or level-3.md files tu understand the domain - the level*.md files contain: visual diagrams: taxonomy, ontology, ... and catalogs: concepts, relations, rules, ... - there is a raw version of the files which contains all the un-approved elements and a governed version which contains only the approved elements. Use-case #2: Domain AI assistant/agent - it is a chat interface to answer questions about a domain - the AI assistant/agent uses traditional keyword search, RAG search, knowledge graph search, .... as well as the ontology to answer the questions accurately and with consistent reliabiliy. Use-case #3: validation - validate texts against the governed ontology. - find contradictions, terminology drift. Do you recommend using the custom YAML files for those 3 use-cases or the generated standard OWL 2 + SKOS + SHACL in Turtle files?
**Options offered:** free text
**A:** (Claude, summary) The generated files, never the YAML. The YAML is OntologyBuilder's internal state; readers rely on the dataset contract (ADR-0013), which should describe the release. Build two release variants, governed and raw (the raw one replaces the earlier "with-provenance" idea). Each holds Turtle (OWL 2 + SKOS + SHACL), optional JSON-LD, level-1/2/3.md with Mermaid diagrams and catalogues (generated from the same model as the Turtle), and a manifest. Assistant: the governed Turtle in an embedded store; SPARQL for multi-hop questions, SKOS for synonyms; evidence IDs join with RAG chunks. Validation: the governed Turtle, which must also carry synonyms, non-preferred variants, scope notes and deprecated terms for drift detection. Put a shared loader in `libs/`. See the [report addendum](../research/reports/Ontology%20formats%20and%20building%20process.md#addendum-2026-11-21-which-files-the-consumers-read).
**Effect:** Three consumer use cases and the governed/raw release to carry into `/spec 0002`. Open: cumulative levels; validation as a separate app or a feature; chunk-ID contract.

### 2026-11-21 · idea · Q7
**Asked by:** Claude (open questions from Q6)
**Q:** [Claude] Are levels cumulative? Is the raw release variant committed to git, or only built locally?
**Options offered:** free text (raised as open questions in the Q6 answer)
**A:** "Level-2 contains everything from level-1 plus an extra set of concepts, relations, rules, ... Level-3 includes everything from level-2 and includes all the ontology elements. RAW should be also version controlled in git."
**Effect:** Levels are cumulative: L1 ⊂ L2 ⊂ L3, and L3 = every element in the ontology. Claude's reading (to confirm in `/spec`): elements marked `ignorable` are in no level, and in the raw variant L3 = every non-rejected, non-ignorable element. Both the governed and the raw release are committed to git, so `data/ontology-<name>/` is a `commit` dataset (ADR-0016). Still open: validation as a separate app or an OntologyBuilder feature; the chunk-ID contract.

### 2026-11-21 · idea · Q8
**Asked by:** user
**Q:** Validation mentioned in use-case 3 will be a dedicated app stored in this monorepo. But I think validation will be needed in the ontology governance rich GUI application as well (which will be also part of this monorepo). Can you propose alternatives to define chunk IDS? Criteria: - stanble IDs across changes. - the user manuals will be upgraded regularly - the OntologyBuilder should be able to ingest the new version and identify which statements are the same and which statements have been deleted/modified and propagate the changes to the ontology elements of the those statements
**Options offered:** free text
**A:** (Claude, summary)
- **Validation:** put the validation logic in a library under `libs/` that takes an RDF graph. The validation app passes it the governed release. The GUI passes it the graph built from its in-memory model, including unapproved items.
- **GUI location:** the GUI writes the YAML, so it should be part of the OntologyBuilder app, not a separate app; otherwise two apps would write one dataset (ADR-0013).
- **Chunk IDs:** six alternatives compared in [source_ids_and_change_propagation.md](../research/notes/Ontology%20formats%20and%20building%20process/source_ids_and_change_propagation.md). Recommended:
  - Keep source units (sentence or passage) apart from RAG chunks.
  - Give each unit a minted opaque ID in a source registry, with location and content hash as separate fields.
  - On each manual upgrade, an alignment step classifies units as unchanged, moved, modified, deleted or new, and a human decides grey-zone matches.
  - Propagate through evidence links: modified → re-extract, and back to under review if the meaning differs; deleted → element orphaned and deprecation proposed, never deleted automatically; new → proposed.
  - Use anchors embedded in the source where we control the manuals.
**Effect:** Validation is a dedicated app and is also needed in the GUI; carry into `/spec 0002`. Open: is the GUI part of the OntologyBuilder app; who owns the source registry (OntologyBuilder dataset or a separate `corpus-<name>` dataset).

### 2026-11-21 · idea · Q9
**Asked by:** Claude (open questions from Q8)
**Q:** [Claude] Is the review/governance GUI part of the OntologyBuilder app? Who owns the source registry: the OntologyBuilder dataset or a separate `corpus-<name>` dataset?
**Options offered:** GUI inside OntologyBuilder (recommended) / separate GUI app; registry in `data/ontology-<name>/` / separate `data/corpus-<name>/`
**A:** "Yes, let the OntologyBuilder app contain the rich GUI for users to review/govern the ontologies. I prefer storing the source registry in a sub-directory under data/ontology-<name> for the sake of simplicity."
**Effect:** The GUI is a component of the OntologyBuilder app, which is the only writer of `data/ontology-<name>/`. The source registry lives in a subdirectory of that dataset and is part of its contract, so the AI assistant reads source-unit IDs from there for RAG.

### 2026-11-21 · idea · Q10
**Asked by:** user
**Q:** A. Let's use number prefixes to express processing order for the sub-directories under data/ontology-<name> 00_sources/ 01_model/ 02_decisions 03_release/00_raw 03_release/01_governed B. Let's store the statements created by the user (in the rich GUI app) under 00_sources/90_user_statements/ So statements can be ingested from source text corpus or defined by the user, and all of them are stored under 00_sources/ directory.
**Options offered:** free text (user decision)
**A:** (Claude, summary) Accepted as the dataset layout. Consequences:
- User statements are source units like corpus passages: stable IDs, content hash, revisions. Their provenance is author plus timestamp instead of document plus location. They need no alignment step, because they are edited in place.
- Authored ontology elements cite them as evidence, so every element has evidence.
- Proposed numbering: `00`–`89` for ingested corpora, `90_user_statements` for authored ones.
- `00_sources/` (including user statements) and `03_release/` are in the dataset contract; `01_model/` and `02_decisions/` stay internal.
**Effect:** Dataset layout fixed for `/spec 0002`.

### 2026-11-21 · idea · Q11
**Asked by:** Claude
**Q:** [Claude] Does a statement authored by the domain admin need a second approver (four-eyes rule), or can the admin approve their own?
**Options offered:** free text (raised in the Q10 answer)
**A:** "Let's make it simple. So the domain admin can approve his/her own modifications next to the ingested/proposed elements and statements from regular (non-domain-admin) users."
**Effect:** No four-eyes rule. The domain admin approves LLM-proposed elements, regular users' statements and edits, and their own. Regular users cannot approve. Every approval is still recorded in `02_decisions/`, with who approved and when.
