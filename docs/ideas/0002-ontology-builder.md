# 0002 · OntologyBuilder: build leveled ontologies from text corpora and human input

- **Status:** done
- **Scope:** system
- **Captured:** 2026-11-20
- **Spec:** [0002-ontology-builder](../specs/0002-ontology-builder/spec.md) (approved) · [plan](../specs/0002-ontology-builder/plan.md) (approved)

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

### 2026-11-21 · spec · Q12
**Asked by:** Claude
**Q:** [spec · scope] I propose scope `system`: the spec adds a new app `ontology-builder`, a new shared dataset `data/ontology-<name>/` with a contract in `libs/contracts/ontology/` (its readers will be the AI assistant of idea 0001 and the future validation app), and reads the existing `user-manuals-pets-and-house-rules` dataset without changing it. Should this spec also define the shared validation library under `libs/` (used by both the GUI and the future validation app), or leave that library to the validation app's own spec?
**Options offered:** System; library later (Recommended) / System; library now / App only
**A:** "System; library later (Recommended)"
**Effect:** Scope = `system`. The spec covers the new app `ontology-builder`, the new dataset `ontology-<name>` and its contract, and reads `user-manuals-pets-and-house-rules` unchanged. No library in `libs/` in this spec; validation logic is extracted into one when the validation app is specified.

### 2026-11-21 · spec · Q13
**Asked by:** Claude
**Q:** [spec · scope] The idea has nine steps plus re-ingestion of upgraded manuals. Which belong in the first version (v1)? Anything not selected becomes a non-goal for v1 and a later spec.
**Options offered:** (multi-select) Core loop (steps 1, 2, 4, 5, 6, 8, 9) / LLM abstraction (step 3) / Quality issues (step 7) / Visual review + re-ingest
**A:** ""Core loop" above + detect/propose also synonyms. Generate level-*.md files."
**Effect:** v1 = ingest, extraction with evidence, level and ignorable proposals, synonym detection and proposals, textual review, authoring, domain-admin approval, governed + raw release including the `level-N.md` files. Non-goals for v1: LLM abstraction (higher-level concepts), contradiction/drift/gap/ambiguity detection, diagram-based review in the GUI, re-ingesting upgraded manuals (alignment and change propagation).

### 2026-11-21 · spec · Q14
**Asked by:** Claude
**Q:** [spec · clarifying question] How is the rich GUI run and who uses it at the same time?
**Options offered:** Local, one user (Recommended) / Shared server, many users / Local now, server later
**A:** "Local, one user (Recommended)"
**Effect:** The GUI runs locally against the git working copy, one user at a time. The role (user / domain admin) comes from a simple local identity, no login server. Multi-user editing is a non-goal.

### 2026-11-21 · spec · Q15
**Asked by:** Claude
**Q:** [spec · clarifying question] How does the domain admin's approval relate to git/GitHub?
**Options offered:** GUI status; git commits (Recommended) / GUI status + PR gate / PR approval only
**A:** "GUI status; git commits (Recommended)"
**Effect:** Approval is a status change in the GUI, recorded in `02_decisions/` with who and when. Changes are committed to git; pushing and merging a PR is an ordinary git step, not part of governance.

### 2026-11-21 · spec · Q16
**Asked by:** Claude
**Q:** [spec · clarifying question] For synonyms in v1: the pet corpus uses "lead" for two things, the rope (building rules 4.2, a synonym of "leash") and the owner's role (dog 6). Should v1 also handle one word naming different concepts (homonyms), so the rope rules attach to Leash and not to the role?
**Options offered:** Yes, synonyms + homonyms (Recommended) / Synonyms only
**A:** "Yes, synonyms + homonyms (Recommended)"
**Effect:** A term can belong to more than one concept; each mention is resolved to one concept in context. The LLM proposes synonym sets and sense splits, the user confirms. Added as must requirements.

### 2026-11-21 · spec · Q17
**Asked by:** Claude
**Q:** [spec · clarifying question] LLM output varies between runs. How should v1 prove that extraction works?
**Options offered:** Fixtures + answer-key eval (Recommended) / Live eval as a gate / Fixtures only
**A:** "Fixtures + answer-key eval (Recommended)"
**Effect:** Automated tests run on recorded LLM responses (deterministic, no API cost). A separate evaluation command runs the live LLM on the pet corpus, scores it against the answer key and reports the scores; it is not a CI gate. The answer key is read only by the evaluation, never by extraction.

### 2026-11-21 · spec · Q18
**Asked by:** Claude
**Q:** [spec · clarifying question] What can be ingested in v1, and how do corpora map to ontologies?
**Options offered:** Markdown; N corpora → 1 ontology (Recommended) / Markdown + PDF / Markdown; 1 corpus → 1 ontology
**A:** "Markdown; N corpora → 1 ontology (Recommended)"
**Effect:** v1 ingests Markdown files only. One ontology can ingest several corpora, each a numbered folder `00`–`89` under `00_sources/`. PDF, HTML and Word are non-goals for v1.

### 2026-11-21 · spec · Q19
**Asked by:** Claude
**Q:** [spec · clarifying question] Ingestion calls the Claude API and costs money. What guard do you want?
**Options offered:** Estimate + confirm (Recommended) / Hard budget limit / No guard
**A:** "Estimate + confirm (Recommended)"
**Effect:** Before an ingestion run the app shows the number of source units and an estimated token cost and asks for confirmation; actual tokens used are recorded per run. No hard limit.

### 2026-11-21 · spec · Q20
**Asked by:** Claude
**Q:** [spec · clarifying question] What happens when someone changes an element that is already approved, and can approved elements be removed?
**Options offered:** Back to review; deprecate (Recommended) / Admin edits stay approved / Back to review; delete allowed
**A:** "Back to review; deprecate (Recommended)"
**Effect:** Any edit to an approved element sets it back to under review; the governed release keeps the last approved version until it is approved again. Approved elements are never deleted, only deprecated, optionally with a replacement.

### 2026-11-21 · spec · Q21
**Asked by:** Claude
**Q:** [spec · clarifying question] The governed release holds only approved elements. What if an approved relation or rule refers to a concept that is not approved (e.g. 'Owner has at most 2 Pets' approved, 'Pet' still proposed)?
**Options offered:** Block the release (Recommended) / Leave them out / Prevent at approval
**A:** "Block the release (Recommended)"
**Effect:** The governed build fails and lists every approved element that depends on an unapproved one. The raw release is always built.

### 2026-11-21 · spec · Q22
**Asked by:** Claude
**Q:** [spec · clarifying question] Should each ontology have a scope record written by the domain admin (purpose, intended readers, what counts as level-1, examples of ignorable content), which the LLM uses when proposing levels and ignorable?
**Options offered:** Yes, required (Recommended) / Optional / No
**A:** "Yes, required (Recommended)"
**Effect:** Creating an ontology requires a scope record; ingestion uses it as guidance for level and ignorable proposals.

### 2026-11-21 · spec · Q23
**Asked by:** Claude
**Q:** [spec · clarifying question] When are the two releases built and versioned?
**Options offered:** Raw on save, governed on publish (Recommended) / Both on demand / Both on every save
**A:** "Raw on save, governed on publish (Recommended)"
**Effect:** The raw release is rebuilt whenever the GUI commits changes. The governed release is built only when the domain admin publishes, with a new semantic version and a change log against the previous governed version.

### 2026-11-21 · spec · Q24
**Asked by:** Claude
**Q:** [spec · clarifying question] Decisions in `02_decisions/` record who approved what, and the dataset is committed to this public repo (rule 10: no personal data). How should people be identified?
**Options offered:** Handle only (Recommended) / Git name + email
**A:** "Login window is simple: type in your userName and select your role. Anyone can be anyone in the MVP."
**Effect:** v1 has a simple login window: the user types a user name and picks a role (user / domain admin). No authentication; anyone can claim any role. The typed user name is what decisions record. Real authentication is a non-goal for v1. The window tells users to use a handle, not a real name or email, because the dataset is public.

### 2026-11-21 · spec · Q25
**Asked by:** Claude
**Q:** [spec · clarifying question] Which review conveniences must the textual review GUI have in v1? (The level filter and status colours from Q5 are already in.)
**Options offered:** (multi-select) Bulk actions / Evidence first / Queue by confidence / Search and filters
**A:** "Bulk actions, Evidence first, Search and filters"
**Effect:** Must requirements: bulk include/exclude/approve on a selection; the source passage is shown before the LLM's proposal; full-text search and filters by element type, status, corpus/document and level. Ordering the queue by LLM confidence is not in v1.

### 2026-11-21 · spec · Q26
**Asked by:** Claude
**Q:** [spec · clarifying question] What should the first ontology, built from the pet manuals, be called? (Its folder is `data/ontology-<name>/`.)
**Options offered:** pets-and-house-rules (Recommended) / pet-ownership
**A:** "pets-and-house-rules (Recommended)"
**Effect:** The first ontology is `data/ontology-pets-and-house-rules/`.

### 2026-11-21 · spec · Q27
**Asked by:** Claude
**Q:** [spec · approval] Do you approve spec 0002 OntologyBuilder (docs/specs/0002-ontology-builder/spec.md)? Its scope is `system`. v1 is the core loop plus synonym and sense detection plus the level-N.md files. Non-goals are LLM abstraction, contradiction detection, visual review and re-ingestion. Nothing blocking is left open.
**Options offered:** Approve / Changes needed
**A:** "Add use-case: as a power user of a domain or employee/developer in the domain, I want to read level-1/2/3.md files to understand the domain the fulles. "
**Effect:** Added scenario 9 (power user, employee or developer reads level-1 to level-3 for the fullest understanding). Covered by the existing FR-33, FR-34 (cumulative levels, level-3 holds every non-ignorable element). Spec still draft; approval asked again.

### 2026-11-21 · spec · Q28
**Asked by:** Claude
**Q:** [spec · approval] I added scenario 9: a power user, employee or developer in the domain reads level-1 to level-3 to understand the domain as fully as possible. The existing FR-33/FR-34 already cover it, since levels are cumulative and level-3 holds every non-ignorable element. Do you now approve spec 0002 OntologyBuilder?
**Options offered:** Approve / Changes needed
**A:** "Approve"
**Effect:** Spec 0002 set to `approved`; idea set to `specified`; both indexes updated. Next: `/plan 0002`.

### 2026-11-21 · plan · Q29
**Asked by:** Claude
**Q:** [plan · tech stack] The back end will be Python: LinkML, rdflib, pySHACL and the Anthropic SDK are all Python-native, so the YAML → OWL/SKOS/SHACL path stays in one language. Which GUI approach do you want for the local review app?
**Options offered:** Python + htmx (Recommended) / Python API + React/TS / Python-only UI framework (NiceGUI or Streamlit)
**A:** "I want to see prototypes with mock data for each of them and decide."
**Effect:** Back end is Python. GUI choice deferred: Claude builds a clickable prototype of each option on the same mock pet-manual data and asks again.

### 2026-11-21 · plan · Q30
**Asked by:** Claude
**Q:** [plan · contract] Every ontology-<name> dataset has the same layout. tools/monorepo/system-map.sh requires libs/contracts/<dataset>/README.md for each dataset. How should the contract be organised?
**Options offered:** Shared + thin per-dataset (Recommended) / Shared only, change tooling / Full contract per dataset
**A:** "Shared + thin per-dataset (Recommended)"
**Effect:** One versioned contract `libs/contracts/ontology/` (layout, schemas, RDF vocabulary, guarantees); each dataset has a thin `libs/contracts/ontology-<name>/README.md` that names owner, location, git mode and the ontology contract version it conforms to. No tooling change. Recorded as a root ADR in this plan.

### 2026-11-21 · plan · Q31
**Asked by:** Claude
**Q:** [plan · source units] How fine-grained should source units be? Evidence points at units, and every unit goes through the LLM and the ignorable check.
**Options offered:** Markdown block (Recommended) / Sentence
**A:** "Markdown block (Recommended)"
**Effect:** One source unit per Markdown block (paragraph, list item, blockquote, table row); deterministic splitting. Evidence may add an optional quoted span (W3C TextQuoteSelector) inside a unit.

### 2026-11-21 · plan · Q32
**Asked by:** Claude
**Q:** [plan · tech stack] After trying the three prototypes at https://claude.ai/artifact/Mjnmp1uWZACjGzufk6wi2r, which GUI approach should the OntologyBuilder review app use?
**Options offered:** A · Python + htmx (Recommended) / B · Python API + React/TS / C · Python-only (NiceGUI)
**A:** "Which prototype can support interactove diagrams showing the taxonomy and ontology? I want to be able to perform the same steps via the list or via the diagram in v2 of the app."
**Effect:** New forward constraint for the plan: v2 adds interactive taxonomy and ontology diagrams that offer the same review actions as the list. The v1 GUI choice must not block that. Claude's answer is in Q33.

### 2026-11-21 · plan · Q33
**Asked by:** user (follow-up to Q32)
**Q:** Which prototype can support interactive diagrams showing the taxonomy and ontology, with the same steps via the list or via the diagram in v2?
**Options offered:** free text
**A:** (Claude, summary) All three can show diagrams. In every option the interactive diagram is a JavaScript component (Cytoscape.js + elkjs), so v2 brings in TypeScript and its quality gate whichever option is chosen. The options differ in how naturally the list and the diagram share one selection, one filter set and one set of actions. **B (React/TS)** fits best: one client store, with the list and the diagram as two views of it that call the same action functions. **A (htmx)** can host a Cytoscape island that calls the same backend routes, but keeping the selection and filters in sync between server-rendered HTML and a JS canvas needs custom glue, which grows with every diagram feature. **C (NiceGUI)** needs a custom Vue component for Cytoscape; clicks reach Python handlers easily, but richer interaction (lasso selection, drag to merge) is custom JS anyway. Either way the back end is API-first: a JSON service layer holds every governance rule, so the front end can change without touching it. Given the v2 goal, Claude now recommends B.
**Effect:** Recommendation changed from A to B; GUI choice asked again (Q34).

### 2026-11-21 · plan · Q34
**Asked by:** Claude
**Q:** [plan · tech stack] v2 needs interactive taxonomy and ontology diagrams that offer the same review actions as the list. Every option then needs a TypeScript diagram component (Cytoscape.js + elkjs). Which GUI approach should v1 use?
**Options offered:** B · React/TS now (Recommended) / A now, React island in v2 / Prototype the diagram first / C · NiceGUI
**A:** "B · React/TS now (Recommended)"
**Effect:** v1 GUI is a React + TypeScript single-page app (Vite) on top of an API-first FastAPI back end. The plan starts with `/add-language python`, and `/add-language js-ts` comes before the first front-end task. Recorded as an app ADR.

### 2026-11-21 · plan · Q35
**Asked by:** Claude
**Q:** [plan · scaffold] The plan's app ADRs, app components.json and Commands section belong in apps/ontology-builder/, which doesn't exist yet. Shall I scaffold now (docs and registration only, no code)? That means the app `ontology-builder` and the dataset `ontology-pets-and-house-rules` (git mode commit, owner ontology-builder), plus a `reads` edge to `user-manuals-pets-and-house-rules`.
**Options offered:** Scaffold now (Recommended) / Scaffold as a task
**A:** "Scaffold now (Recommended)"
**Effect:** App and dataset scaffolded in the planning change with `tools/monorepo/new.sh`; the reads edge was added and the system map regenerated. App ADRs, app architecture and commands are written in the same change.

### 2026-11-21 · plan · Q36
**Asked by:** Claude
**Q:** [plan · plan approval] Do you approve plan 0002 (docs/specs/0002-ontology-builder/plan.md + tasks.md)? The summary covered: an API-first Python back end with 13 components and a React + TS front end; LinkML YAML records; Markdown-block source units with ULID IDs; two-pass extraction tested on curated replay fixtures, with the live run scored by eval; a pending change set saved atomically as one git commit, never pushed; deterministic Turtle and level-N.md releases, the governed release using approved snapshots; the shared contract libs/contracts/ontology/ (root ADR-0019) and app ADRs 0001–0005; 31 tasks, T1 /add-language python, T22 /add-language js-ts, live LLM runs in T8/T28/T29 with cost confirmation.
**Options offered:** Approve / Changes needed
**A:** "Approve"
**Effect:** Plan set to `approved`; ADR-0019 and ontology-builder/ADR-0001 to 0005 set to `accepted`; idea set to `planned`; indexes updated. Next: `/implement 0002`.

### 2026-11-21 · implement · Q37
**Asked by:** Claude
**Q:** [implement · deviation] Plan 0002 (LLM section, ontology-builder/ADR-0005) says the LLM's structured output is "a single forced tool call". But the repo's default model `claude-opus-5-5` rejects forced `tool_choice` (`any`/`tool`) with a 400, as do Sonnet 5.5 and Fable 5.1/5.2. How should T7 get schema-valid JSON from Claude?
**Options offered:** Structured outputs (Recommended): `output_config.format` with the JSON Schema generated from the LinkML output classes; unsupported constraints are stripped from the sent schema and still checked by Pydantic / Strict tool, auto choice: a `strict: true` tool with `tool_choice: auto` and a retry when no call is made / Keep forced tool call: require a model that still accepts forced tool use
**A:** "Structured outputs (Recommended)"
**Effect:** The llm component asks for JSON through `output_config.format` (type `json_schema`) instead of a forced tool call. The schema still comes from the LinkML output classes; constraints the API does not support are removed from the sent schema and validated client-side by the Pydantic models. Plan updated; recorded as ontology-builder/ADR-0006, which supersedes the "force structured output" bullet of ADR-0005.

### 2026-11-21 · implement · Q38
**Asked by:** Claude
**Q:** [implement · deviation] The plan has the LLM cite source units by their full IDs (e.g. su_01M7YZMHG0B9D5MPJTB9D5MPJW). IDs minted in one run differ only in their last characters (…MPJW, …MPJX), so one miscopied character silently points evidence at the neighbouring unit. That ID is still valid, so validation can't catch it. How should T8's prompt and output refer to units?
**Options offered:** Short aliases (Recommended): number the units per prompt (U1, U2, …), map each alias back to its su_ ID, drop and report an unknown alias; the LinkML output classes change from the su_ pattern to an alias pattern, records hold only real IDs / Full IDs, as planned
**A:** "Short aliases (Recommended)"
**Effect:** The prompts of pass 1 and pass 2 show each unit with a short alias `U<n>` that is unique in that prompt. The LLM output classes (`Candidate.evidence`, `UnitVerdict.unit`, `CandidateMention.unit`, `Sense.mentions`) take aliases. Extraction maps them back to the units' `su_` IDs before any record is built; an alias that is not in the prompt counts as an unknown unit (dropped and reported, FR-10). Plan updated (Approach 4, LLM).

### 2026-11-21 · implement · Q39
**Asked by:** Claude
**Q:** [implement · cost confirmation] T8 records the pass 1 fixtures with one live run over the three pet manuals: 37 documents and 58 source units, so 37 requests to claude-opus-5-5. The estimate (offline heuristic) is about 143K input tokens and up to about 86K output tokens, so about $2.29; output will probably be lower. Requests that already have a fixture are replayed, never re-recorded. Afterwards I curate the responses by hand. Shall I run it?
**Options offered:** Run it (~$2.29) / Not now
**A:** "Run it (~$2.29)"
**Effect:** The pass 1 fixtures are recorded live with `tests/test_record_llm_fixtures.py` (marker `live`), then curated by hand.

### 2026-11-21 · implement · Q40
**Asked by:** Claude
**Q:** [implement · deviation] The live API refuses the pass 1 output schema: "compiled grammar is too large" (a separate limit allows at most 16 nullable or union fields). I tested variants, and each 400 cost nothing: pruning, required-plus-nullable, no null, no enums, flattened rules and a single flat item type all fail. What compiles is splitting it: (a) verdicts, statements, terms, concepts and relations, and (b) rules and properties. How should pass 1 get its output?
**Options offered:** Two calls per document (Recommended): call A gives verdicts, statements, terms, concepts and relations; call B gets the same units and A's candidate keys and labels and gives rules and properties; both keep schema-constrained output; 74 calls instead of 37, roughly $3.5–4.5 to record; new app ADR-0007 / One call, schema in prompt: no grammar, the JSON Schema in the prompt text, validated by Pydantic with one retry; cheaper (~$2.3) but the shape is not guaranteed; new app ADR-0007 supersedes ADR-0006 for pass 1
**A:** "Two calls per document (Recommended)"
**Effect:** Pass 1 makes two structured-output calls per document. Call A (`ConceptsOutput`): unit verdicts, statements, terms, concepts, relations. Call B (`RulesOutput`): rules and properties, with the candidates of call A listed by key and the ignorable units named. Each call has its own one retry. If call A gives no usable answer the document is reported and call B is not made; if call B fails, A's candidates are kept and the failure is reported. Recorded as ontology-builder/ADR-0007; plan (Approach 4) and T8 updated. The recording cost confirmed in Q39 (~$2.29) does not cover the new estimate, so it is asked again.

### 2026-11-21 · implement · Q41
**Asked by:** Claude
**Q:** [implement · cost confirmation] With two calls per document (Q40), recording the pass 1 fixtures is now 74 requests to claude-opus-5-5. The offline estimate is about 198K input tokens and up to about 119K output tokens, so about $3.18. Call B prompts grow a little with A's candidates, and output will likely be lower. Your earlier approval (Q39) covered ~$2.29. Shall I run the recording?
**Options offered:** Run it (~$3.18) / Not now
**A:** "Run it (~$3.18)"
**Effect:** The pass 1 fixtures (calls A and B) are recorded live, then curated by hand.

### 2026-11-21 · implement · Q42
**Asked by:** Claude
**Q:** [implement · live LLM call] T9 needs a curated pass 2 (term resolution) fixture for the pet manuals. One live call to claude-opus-5-5 is estimated at ~26k input + ~15.6k output tokens ≈ $0.42. How should I create the fixture?
**Options offered:** Record live, then curate (Recommended): one live call (~$0.42) seeds the fixture, then it is curated by hand to the leash/lead answer the pipeline must handle, as in T8 / Hand-write the fixture: no API cost, the leash/lead group and split plus a few cross-document merges written by hand, less realistic
**A:** "Record live, then curate (Recommended)"
**Effect:** The pass 2 fixture is recorded live with `tests/test_record_llm_fixtures.py::test_record_pass2_fixture` (marker `live`), then curated by hand.

### 2026-11-21 · implement · Q43
**Asked by:** Claude
**Q:** [implement · deviation] For T10, the plan lets `ingestion` depend only on sources, extraction, store and llm, and import-linter forbids `ingestion → model`. But the run orchestration has to build and validate model records: Run (the run record of FR-6), Estimate, Decision (`not_ignorable`), SourceUnit verdicts and the element types. How should ingestion get them?
**Options offered:** Add ingestion → model (Recommended): add `model` to ingestion's mayDependOn, update architecture.md, regenerate `.importlinter`, new app ADR-0008; Ce of ingestion goes from 4 to 5 (warn band, not a failure) / Re-export through store: no new edge, the store's public API re-exports the record classes; Ce stays 4, but model is hidden behind store
**A:** "Add ingestion → model (Recommended)"
**Effect:** `ingestion` may depend on `model` (app `components.json`, `architecture.md`, `.importlinter`); recorded as ontology-builder/ADR-0008; plan (Architecture impact) updated.

### 2026-11-21 · implement · Q44
**Asked by:** Claude
**Q:** [implement · deviation] T18: the `workflows` component (the use-case layer api and cli call) has to open the ontology dataset (a `DatasetStore` from `store`) and build the LLM client for ingestion (an `LlmClient` from `llm`). Its plan lets it import only ingestion, governance, release and vcs, and api and cli can't import store or llm either. How should workflows get them?
**Options offered:** Add workflows → store, llm (Recommended): workflows becomes the composition root that opens the store and builds the client; Ce 4 → 6 (warn band); app components.json, architecture.md, .importlinter, new app ADR-0009 / Factories in lower components: governance gets open_dataset(), ingestion gets client_from_settings(); no new edge, Ce stays 4, but store and llm are hidden behind other components
**A:** "Add workflows → store, llm (Recommended)"
**Effect:** `workflows` may depend on `store` and `llm` (app `components.json`, `architecture.md`, `.importlinter`); recorded as ontology-builder/ADR-0009; plan (Architecture impact) updated. The journal of the pending change set is serialised by governance's `ChangeSet`, so workflows needs no `model` edge.

### 2026-11-21 · implement · Q45
**Asked by:** Claude
**Q:** [implement · deviation] Plan 0002 lists `confirm_ignorable` and `not_ignorable` among the `POST …/actions` of the API (T19). The back end has neither as an element action: `not_ignorable` already exists as on-demand extraction (estimate → confirm → run), and nothing can set a corpus unit's ignorable verdict to `confirmed` (the change set holds only elements and user statements). No FR or AC needs `confirm_ignorable`. How should T19 handle them?
**Options offered:** Drop confirm (Recommended): drop `confirm_ignorable` from v1; `not_ignorable` goes through the ingestion routes (`POST …/ingestions/estimate {units}`, then `POST …/ingestions {units, confirm: true}`) / Implement confirm too: extend governance so the change set also holds corpus-unit verdicts, `confirm_ignorable` sets `ignorable.status = confirmed` with a decision
**A:** "Drop confirm (Recommended)"
**Effect:** `confirm_ignorable` is not part of v1. Marking a unit not ignorable (FR-14) uses the ingestion routes with `units` instead of `folder`, with the same estimate-then-confirm flow. Plan (HTTP API) updated.

### 2026-11-21 · implement · Q46
**Asked by:** Claude
**Q:** [implement · deviation] T20: `ontology-builder serve <name>` has to start the API server (`api.serve`), but plan 0002 lets `cli` depend only on `workflows` and `evaluation`. `workflows` can't host it either, because `api` already depends on `workflows` (that would make a cycle). How should `serve` reach the API?
**Options offered:** Add cli → api (Recommended): add `api` to cli's mayDependOn, Ce 2 → 3; app components.json, architecture.md, .importlinter, ontology-builder/ADR-0010 / Separate serve entry: `api` gets its own console script (e.g. `ontology-builder-serve`), no new edge, the plan's `serve` command is renamed
**A:** "Add cli → api (Recommended)"
**Effect:** `cli` may depend on `api` (app `components.json`, `architecture.md`, `.importlinter`); recorded as ontology-builder/ADR-0010; plan (Architecture impact) updated.

### 2026-11-21 · implement · Q47
**Asked by:** Claude
**Q:** [add-language · decide] T22: which package manager should the JavaScript/TypeScript quality gate use? One workspace at the repo root, with `apps/ontology-builder/web` as its first member; the Mermaid CLI dev tool moves in too. npm 11 is installed; pnpm is not.
**Options offered:** npm workspaces (Recommended): already installed, the root `package.json` and `package-lock.json` are npm already, native Dependabot and `npm audit` support / pnpm workspaces: faster, stricter installs and `pnpm-workspace.yaml`, but pnpm must be installed locally and in CI and the lockfile replaced
**A:** "npm workspaces (Recommended)"
**Effect:** The JS/TS gate uses npm workspaces at the repo root (`package.json` `workspaces`, one `package-lock.json`); recorded in the root ADR written by `/add-language js-ts`.

### 2026-11-21 · implement · Q48
**Asked by:** Claude
**Q:** [adr · status] T23 needs a generator for the GUI's TypeScript API client, and the plan doesn't name one. Proposed ontology-builder/ADR-0011: generate only the types with openapi-typescript and make the calls with openapi-fetch. The alternative, @hey-api/openapi-ts, puts about 2,000 lines of client code into `src/`. That code fails the gate (strict ESLint, CC 39, a type-only import cycle), so it would need to be excluded from lint, formatting and boundaries, plus an npm override for a high-severity js-yaml advisory. Accept the ADR?
**Options offered:** Accept (Recommended): the generated types file is committed and passes the gate unchanged; a nested TypeScript 5.9 is installed for code generation only / Use @hey-api instead: its generated folder is excluded from ESLint, Prettier and dependency-cruiser, plus a js-yaml override / Leave proposed
**A:** "Accept (Recommended)"
**Effect:** ontology-builder/ADR-0011 accepted. `web/src/api/schema.gen.ts` is generated by `npm run gen:api` (`web/scripts/gen-api.ts`) and drift-tested; calls go through openapi-fetch in `web/src/api/index.ts`.

### 2026-11-22 · implement · Q49
**Asked by:** Claude
**Q:** [implement · deviation] T26 needs to list source units for three dialogs: the evidence picker (author an element), choosing a user statement to edit, and choosing an ignorable passage to mark not ignorable. Plan 0002's HTTP API has no route that lists units. How should the GUI get them?
**Options offered:** Add GET …/units (Recommended): new read route `GET /api/ontologies/{name}/units` returning typed `UnitOut` (id, kind, corpus, document, text, ignorable verdict, and for user statements author and revision count), unsaved statements included; plan (HTTP API) updated; no new component edge / Evidence from elements only: no new route; the picker offers only units already cited by some element plus statements created in this browser session; no marking passages not ignorable, no editing older statements
**A:** "Add GET …/units (Recommended)"
**Effect:** The API gets `GET /api/ontologies/{name}/units` (typed `UnitOut`, user statements from the change set included). Plan (HTTP API) and the T26 note updated.

### 2026-11-22 · implement · Q50
**Asked by:** Claude
**Q:** [implement · deviation] `POST …/ingestions` is synchronous: it returns once the run has finished. What should "then the run progress" in the ingest dialog show?
**Options offered:** Running state, then record (Recommended): while the request runs, the dialog shows "Running…" with the confirmed counts; afterwards the run record from `GET …/runs/{id}` (status, model, tokens used, start and end, skipped items) and the commit or hook output; no back-end change / Live progress (async run): `POST …/ingestions` starts the run in the background and the GUI polls `GET …/runs/{id}` for batches done/total; changes the ingestion API, threading and locking (bigger plan change, likely an ADR)
**A:** "Running state, then record (Recommended)"
**Effect:** The ingest dialog shows a running state during the synchronous run, then the run record and the commit. No back-end change; noted in T26.

### 2026-11-22 · implement · Q51
**Asked by:** Claude
**Q:** [implement · live LLM cost] T28 runs `ontology-builder eval` live: it ingests the three pet manuals (37 documents, 58 source units) with the model in CLAUDE_MODEL. The estimate is about 329k input and up to 197k output tokens, roughly $5.26. Should I run it now?
**Options offered:** Run it (Recommended): spend about $5.26 on one live eval run, then review the report / Use a cheaper model: run eval with `--model` set to a cheaper model / Not now: skip T28 and move on to T30
**A:** "Run it (Recommended)"
**Effect:** One live eval run with the configured model.

### 2026-11-22 · implement · Q52
**Asked by:** Claude
**Q:** [implement · T28 report review] The live eval with claude-opus-5-5 scored 61/61 (ignorable 4/4, kept content 4/4, leash/lead 3/3, concepts 25/25, rules 19/19, traps 6/6), using 388k input and 103k output tokens (about $3.61; estimate $5.26). Not scored: some concepts appear under several unmerged labels ("pet textile" under 4 labels, "residual waste" / "residual waste bin") and some rules appear twice ("Rabies vaccination renewed every year"). T28 only asks to change the prompts where the leash/lead split or the traps fail, and none failed. How should I go on?
**Options offered:** Accept, tick T28 (Recommended): keep prompts and fixtures, commit the report, duplicates are left for human review in the GUI / Iterate on duplicates: tighten pass 2, re-record and re-curate fixtures, eval again (about $4 more) / Accept, note duplicates: tick T28 and note the duplicates as a follow-up idea
**A:** "Accept, tick T28 (Recommended)"
**Effect:** Prompts and fixtures unchanged; the report `apps/ontology-builder/docs/evaluations/2026-11-22-claude-opus-5-5.md` is kept; T28 ticked.

### 2026-11-22 · implement · Q53
**Asked by:** Claude
**Q:** [implement · next task] T28 is done (report saved, not committed yet). T29 creates `data/ontology-pets-and-house-rules/` with the user as domain admin: write the scope record together, ingest the three manuals live (about $3.60, judging by the eval), and commit. How should I go on?
**Options offered:** Start T29 now (Recommended): draft the scope record from the eval's pet_scope.yaml, then show the estimate before ingesting / Commit T28 first: run /commit-push-merge-feature-branch, then T29 in a fresh session / Skip to T30: the JSON-LD twin first
**A:** "Start T29 now (Recommended)"
**Effect:** T29 started in this session.

### 2026-11-22 · implement · Q54
**Asked by:** Claude
**Q:** [implement · T29 scope record] The real ontology `pets-and-house-rules` needs a scope record (purpose, readers, level 1–3 guidance, ignorable examples, base IRI). The draft is the eval's scope record (`evaluation/pet_scope.yaml`), which scored 61/61. Which scope record should be used?
**Options offered:** Use the eval draft (Recommended) / Edit the draft
**A:** "Use the eval draft (Recommended)"
**Effect:** The ontology is created with the eval's scope record unchanged.

### 2026-11-22 · implement · Q55
**Asked by:** Claude
**Q:** [implement · T29 admin handle] Which handle should be recorded as the domain admin who creates the ontology (it lands in committed decision records; the repo is public, so no email)?
**Options offered:** belaboros (the user's GitHub login) / admin (a neutral role-style handle)
**A:** "belaboros"
**Effect:** The ontology is created and ingested as `belaboros`.

### 2026-11-22 · implement · Q56
**Asked by:** Claude
**Q:** [implement · T29 live ingestion] The ontology `pets-and-house-rules` is created and committed (759da11). Ingesting the three manuals with claude-opus-5-5 is estimated at dog $2.00, cat $1.56, building rules $1.70 ($5.26 total; the eval's identical run cost about $3.61). Each ingestion commits `data/ontology-pets-and-house-rules/`. Run all three?
**Options offered:** Run all three (Recommended): dog, cat, building rules in the eval's order, one commit per run / Dog manual only / Not now
**A:** "Run all three (Recommended)"
**Effect:** The three manuals are ingested live, one run and one commit each.

### 2026-11-22 · implement · Q57
**Asked by:** Claude
**Q:** [implement · T31 deviation] T31's check asks for an /arch-metrics result of `pass`. The result is `warn` for the system and for ontology-builder, and the same warnings were already in the 2026-11-21 baseline, so none are new: the SDP edge workflows → ingestion (I 0.667 → 0.833, an edge ADR-0009 accepted), Ce 5 and 6 for ingestion and workflows, and D > 0.5 for the stable, concrete Python components (model, store, llm, vcs). Nothing is `fail`. Reaching `pass` would mean a refactor that isn't in the plan (e.g. Protocols to raise abstractness, splitting workflows). How should I go on?
**Options offered:** Accept warn (Recommended): change T31's check to "no fail, no new violations" and record the warnings / Refactor to pass: plan change with app ADRs / Stop here: leave T31 unticked
**A:** "Accept warn (Recommended)"
**Effect:** T31's check is now "/arch-metrics: no `fail`, no new violations against the previous snapshot"; the remaining warnings are listed in the T31 note.

### 2026-11-22 · implement · Q58
**Asked by:** Claude
**Q:** [implement · commits] T30 (JSON-LD twin, contract 0.2.0, rebuilt raw release) and the T31 docs are on the branch spec/0002-t30-t31 and not committed yet. Make one commit per task?
**Options offered:** Commit per task (Recommended): two commits, nothing pushed / Don't commit
**A:** "Commit per task (Recommended)"
**Effect:** T30 and T31 are committed separately on spec/0002-t30-t31; nothing is pushed.

### 2026-11-22 · review · Q59
**Asked by:** Claude
**Q:** [review-spec · spec gap] The independent review passes all 33 acceptance criteria. One finding (medium): the GUI has no screen for creating an ontology or editing the scope record; both exist only in the API (POST /api/ontologies, PUT …/scope) and the CLI (`create`). FR-3 says "the GUI enforces the role … edit the scope record", which reads as if the GUI offered it. How should this be resolved?
**Options offered:** Clarify spec: CLI/API (Recommended): state in FR-1/FR-3 that create and scope editing are CLI/API actions in v1 / Add a follow-up GUI task (T32, scope editor dialog)
**A:** "Clarify spec: CLI/API (Recommended)"
**Effect:** FR-1 and FR-3 say that creating an ontology and editing its scope record are CLI/API actions in v1; the API refuses them for a user (403).

### 2026-11-22 · review · Q60
**Asked by:** Claude
**Q:** [review-spec · small fixes] Low-severity review findings: (2) the contract doesn't say the governed release leaves out approved ignorable elements; (3) ingestion has its own require_scope that may raise RecordInvalidError instead of a refusal for an invalid scope record; (4) the plan's verification map names 2 renamed tests; (5) a no-op assertion in test_extraction_terms.py. Which to fix now?
**Options offered (multi-select):** Contract wording (2) / Unify require_scope (3) / Plan test names (4) / No-op assert (5)
**A:** all four
**Effect:** Fixed as follow-up T32 to T35 in tasks.md.

### 2026-11-22 · implement · Q61
**Asked by:** Claude
**Q:** [Claude] Bug found after the review: the user saw no taxonomy edges in `level-1.md`. When a run's new concept is merged into a concept already in the ontology (e.g. the building manual's "dog → pet" into the existing "dog" from the dog run), `extraction/terms_apply.py::_fold_merged` drops its parents and evidence silently. So dog and cat have no parent "pet", and level-1.md's taxonomy has no edges. (Also by design: level-N.md draws only is-a edges whose two ends are in the level.) How should a run treat a concept that already exists?
**Options offered:** Add, mark for review (Recommended): the run adds the new evidence and parents to the existing concept and records a decision; an approved concept goes back to `included` and the governed release keeps the approved version / Keep as a new concept: no merge into existing concepts, a reviewer merges by hand / Only report the loss: keep the rule, list dropped parents and evidence in the run's skipped items
**A:** "Add, mark for review (Recommended)"
**Effect:** Spec FR-11 extended, app ADR added, tasks T36–T37 added; spec 0002 reopened.

### 2026-11-22 · implement · Q62
**Asked by:** Claude
**Q:** [Claude] How to repair `data/ontology-pets-and-house-rules/` once the code is fixed?
**Options offered:** Re-ingest from scratch (Recommended): recreate the ontology and ingest the three manuals again (about $3.60; estimate shown first; nothing has been reviewed yet) / Fix by hand in the GUI / Leave it for now
**A:** "Re-ingest from scratch (Recommended)"
**Effect:** Task T37: recreate the ontology with the same scope record and re-ingest the three manuals live after the estimate is confirmed.

### 2026-11-22 · implement · Q63
**Asked by:** Claude
**Q:** [implement · T37 live ingestion] The fix is committed (e9c14cd) and the ontology `pets-and-house-rules` is re-created with the same scope record and handle (e90c876). Ingesting the three manuals with claude-opus-5-5 is estimated at dog $2.00, cat $1.56, building rules $1.70 ($5.26 total; the last identical run cost about $3.60). Each run commits the dataset. Run all three?
**Options offered:** Run all three (Recommended): dog, cat, building rules in the earlier order, one commit per run / Not now
**A:** "Run all three (Recommended)"
**Effect:** The three manuals are re-ingested live, one run and one commit each.

### 2026-11-22 · implement · Q64
**Asked by:** Claude
**Q:** [Claude] The user still saw no taxonomy diagram in `level-1.md`. The diagram does exist and renders, but 20 of its 22 concepts have no is-a link within level 1; Mermaid lays them out side by side, so the diagram is one row 22 boxes wide and shrinks to an unreadable strip. How should the taxonomy diagram be built?
**Options offered:** Linked concepts only (Recommended): diagram of linked concepts, the rest listed below it / Linked + other levels: also draw level-2/3 children, faded / Keep all, wrap rows: unlinked concepts in a box laid out in several rows
**A:** "Keep all, wrap rows"
**Effect:** Task T38: the taxonomy diagram puts concepts without an is-a link in the level into a "not linked yet" box, laid out in rows.
