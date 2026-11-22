# Spec 0002 · OntologyBuilder

- **Status:** implemented
- **Scope:** system
- **Idea:** [0002-ontology-builder](../../ideas/0002-ontology-builder.md)
- **Last updated:** 2026-11-22

## Problem
Teams that want an AI assistant, a learning path or a text validator for a domain need an ontology of that domain: its concepts, relations and rules, sorted by how important they are. They want to build it from the user manuals they already have, plus their own knowledge. Today no tool does this end to end (see the [research report](../../research/reports/Ontology%20formats%20and%20building%20process.md)). LLMs can propose candidates from text but get the typing and the levels wrong often enough that every candidate needs a human decision, with the source text next to it. Commercial platforms govern ontologies but don't review LLM candidates with evidence, don't assign importance levels, and don't edit a git-friendly source. The AI assistant of idea 0001 and a future validation app both wait for a governed ontology they can read.

## Goals
- Build an ontology from one or more Markdown corpora and from statements typed in by people.
- Have the LLM propose the building blocks (statements, terms, concepts, synonyms and senses, relations, rules) and a level for each (level-1, level-2, level-3, ignorable), and have people review, correct, author and approve them in a local GUI.
- Every element traces back to the source text or the user statement it came from, through stable IDs.
- Publish two releases from the same model: a governed one (approved only) and a raw one (everything still in play), each as standard RDF (OWL 2 + SKOS + SHACL in Turtle) and as human-readable `level-1.md`, `level-2.md`, `level-3.md`.
- Keep everything version-controlled in git as a committed dataset `data/ontology-<name>/`, starting with `data/ontology-pets-and-house-rules/`.

## Non-goals
All of these are out of scope for v1 and may get their own specs later.
- LLM abstraction: proposing higher-level concepts, relations and rules that the text does not state (e.g. `Pet`, `JuvenilePet`, `PetTextile`) (idea step 3). People can still author them by hand.
- Detecting contradictions, terminology drift, gaps and ambiguity (idea step 7).
- Diagram-based (visual) review in the GUI. Diagrams appear only in the generated `level-N.md` files.
- Re-ingesting an upgraded version of a corpus that was already ingested (alignment of source units, change propagation).
- Ingesting anything other than Markdown (PDF, HTML, Word).
- Ordering the review queue by LLM confidence; auto-approving anything.
- Multi-user or server deployment, real authentication, concurrent editing.
- A four-eyes rule: the domain admin may approve their own work (Q11).
- Shared libraries in `libs/` (loader, validation); they come with the readers' specs (Q12).
- Changes to the manuals dataset or its generator app (e.g. embedded anchors).
- Pushing to GitHub or managing PRs from the GUI.

## Users and scenarios
Roles: **user** (reviews, corrects and authors) and **domain admin** (does everything a user does, and governs: approves, rejects, deprecates, publishes).

1. As a domain admin, I want to create an ontology with a scope record (purpose, intended readers, what counts as level-1, examples of ignorable content), so that the LLM's level proposals follow my rubric.
2. As a user, I want to ingest a folder of Markdown manuals into the ontology and see an estimated cost before the LLM runs, so that I stay in control of spending.
3. As a user, I want to see each proposed element with its source passage first and the LLM's proposal second, so that I judge the text, not the LLM.
4. As a user, I want to include, exclude (with a reason), correct, change the level of, merge synonyms of or split the senses of proposed elements, one at a time or in bulk, so that review of hundreds of candidates is fast.
5. As a user, I want to type a statement the manuals are missing ("A dog and a cat must be introduced gradually") and create concepts, relations and rules from it, so that the ontology is not limited to the corpus.
6. As a domain admin, I want to approve or reject included elements (with a reason) and deprecate approved ones, so that only governed content reaches the readers.
7. As a domain admin, I want to publish a new governed release with a version and a change log, so that the AI assistant and the validator read a stable, approved ontology.
8. As a newcomer to the domain, I want to read `level-1.md` and then `level-2.md`, with diagrams and catalogues, so that I understand the domain step by step without ontology tools.
9. As a power user of the domain, or an employee or developer working in it, I want to read `level-1.md`, `level-2.md` and `level-3.md` up to the full detail of level-3 (including the special cases and error scenarios), so that I understand the domain as fully as possible.
10. As the developer of the AI assistant (idea 0001), I want to load the governed Turtle and resolve each element's evidence to source-unit IDs, so that the assistant can cite the manual and join ontology hits with RAG hits.

## Functional requirements

### Ontology, scope and sign-in
| ID   | Requirement | Priority |
|------|-------------|----------|
| FR-1 | A domain admin can create an ontology by giving a kebab-case name and a scope record (purpose, intended readers, level-1/2/3 guidance, examples of ignorable content). This creates `data/ontology-<name>/` with the layout of FR-30. Ingestion is refused while the scope record is missing, empty or incomplete. In v1, creating an ontology and editing its scope record are CLI and API actions; the GUI has no screen for them (Q59). | must |
| FR-2 | The GUI opens with a sign-in window: the person types a user name and picks a role (user or domain admin). There is no password; anyone can take any role. The window says to use a handle, not a real name or email address, because the dataset is public. Every recorded action carries this user name. | must |
| FR-3 | The GUI and the API enforce the role: only a domain admin can approve, reject, deprecate, edit the scope record and publish a governed release. Scope editing is offered through the API and CLI only (Q59); the API refuses it for a user. | must |

### Ingestion and source units
| ID   | Requirement | Priority |
|------|-------------|----------|
| FR-4 | A user can ingest a folder of Markdown files (sub-folders included) as a new corpus of an ontology. Each corpus gets a numbered folder `00`–`89` under `00_sources/`; one ontology can hold several corpora. | must |
| FR-5 | Ingestion splits each document into **source units** (a sentence or short passage). Each document and each unit gets a minted, opaque, stable ID that is never derived from its text or position, and the source registry stores for each unit: its ID, document ID, location (file path, heading path, position in the section), content hash and normalised text. | must |
| FR-6 | Before the LLM runs, the app shows the number of documents and source units and an estimated token count and cost, and starts only after the user confirms. Each run records the model, the tokens actually used and its start and end time. | must |
| FR-7 | Ingesting a corpus whose source folder was already ingested into the same ontology is refused with a message (re-ingestion is a later spec). | must |
| FR-8 | An interrupted or failed ingestion run leaves no partial records behind: either the run can be resumed, or the dataset is as it was before the run. | must |

### Extraction and proposals
| ID   | Requirement | Priority |
|------|-------------|----------|
| FR-9 | The LLM proposes **statements** (atomic claims) from source units, and from them **terms**, **concepts** (label, definition if the text gives one), **relations** (between concepts, with domain, range and cardinality where stated), **rules** (who must or must not do what, under which condition, with any limit or cardinality, e.g. "a dog on a lead of at most 2 m in the stairwell") and **properties** of any of these. | must |
| FR-10 | Every proposed element cites at least one source unit as evidence, by ID. An element without evidence is never created by ingestion. | must |
| FR-11 | The LLM proposes **synonyms**: different terms that name one concept (e.g. "leash" in the dog manual and "lead" in the building rules), as a preferred label plus alternative labels. | must |
| FR-12 | The LLM proposes **senses** for homonyms: one term that names different concepts in different places (e.g. "lead" the rope vs "lead" the owner's role). Each mention is resolved to one concept, so facts attach to the right concept (the 2 m lead rule attaches to the leash concept, not to the role). | must |
| FR-13 | The LLM proposes a level for every element: `level-1`, `level-2`, `level-3` or `ignorable`, guided by the scope record and the level definitions of the idea, with a short reason. | must |
| FR-14 | The LLM proposes whole source units as `ignorable` with a reason category (instance-level/anecdote, generic or historical story, quote or motivational text, procedure/step list, other). Nothing is extracted from a unit proposed ignorable. If a user marks such a unit as not ignorable, extraction runs on it on demand (after the cost confirmation of FR-6). | must |
| FR-15 | The data model allows new properties to be added to any element type later without invalidating existing records or breaking the release build. | must |

### Review and authoring (textual GUI)
| ID   | Requirement | Priority |
|------|-------------|----------|
| FR-16 | The GUI lists elements and shows, for the selected one, the source passage(s) first and the LLM's proposal (type, label, level, reason) after them. | must |
| FR-17 | A user can include an element, exclude it (with a reason), correct any of its fields, override its level, merge it with another element as a synonym, split a term into senses, and reassign a mention to another concept. | must |
| FR-18 | A user can select several elements and include, exclude or set the level of all of them in one step; a domain admin can also approve or reject them in one step. | must |
| FR-19 | The list can be filtered by element type, status, level, corpus and document, and searched by full text over labels, definitions and evidence text. | must |
| FR-20 | Status is shown by colour **and** by a text label or icon, distinguishing at least approved, waiting for approval, just proposed, excluded/rejected and deprecated. | must |
| FR-21 | A user can type a **user statement**. It is stored as a source unit under `00_sources/90_user_statements/` with a stable ID, content hash, author and timestamp; editing it creates a new revision, not a new ID. | must |
| FR-22 | A user can author concepts (with or without a definition), relations, rules, terms and properties. Each authored element cites at least one user statement or corpus source unit as evidence. | must |

### Governance
| ID   | Requirement | Priority |
|------|-------------|----------|
| FR-23 | Element statuses: `proposed` (from the LLM), `included` (accepted by a user or authored, waiting for approval), `excluded` (by a user, with reason), `approved`, `rejected` (by the domain admin, with reason), `deprecated`. Only a domain admin moves an element to `approved`, `rejected` or `deprecated`. | must |
| FR-24 | Any change to an approved element puts it back to `included`. Until it is approved again, the governed release keeps the last approved version of it. | must |
| FR-25 | Approved elements are never deleted. A domain admin can deprecate one, optionally naming the element that replaces it. Excluded and rejected elements are kept with their reasons. | must |
| FR-26 | Every decision (include, exclude, correct, level change, merge, split, approve, reject, deprecate, publish) is recorded in `02_decisions/` with the user name, role, timestamp, element ID, old and new values and the reason if any. | must |
| FR-27 | Each save in the GUI creates a git commit in the local working copy that contains only the changed files of that ontology's dataset (records, decisions and the rebuilt raw release). The GUI never pushes and never bypasses git hooks; if a hook fails, nothing is committed and the GUI shows the hook's message. | must |

### Releases
| ID   | Requirement | Priority |
|------|-------------|----------|
| FR-28 | The **raw release** (`03_release/00_raw/`) is rebuilt on every save. It contains every element except excluded, rejected and ignorable ones, each with its status. | must |
| FR-29 | The **governed release** (`03_release/01_governed/`) is built only when a domain admin publishes. It contains approved and deprecated elements only, except those whose level is ignorable (as in the raw release, FR-28). The admin picks a semantic version (default: next minor). It includes a change log of elements added, changed, deprecated and removed against the previous governed version. | must |
| FR-30 | The dataset layout is `00_sources/` (corpora `00`–`89`, `90_user_statements/`, source registry), `01_model/` (element records, scope record), `02_decisions/`, `03_release/00_raw/`, `03_release/01_governed/`. `00_sources/` and `03_release/` form the dataset contract; `01_model/` and `02_decisions/` are internal to the app. | must |
| FR-31 | Each release holds: `ontology.ttl` (OWL 2 + SKOS + SHACL, RDF 1.1 Turtle), `level-1.md`, `level-2.md`, `level-3.md` and `manifest.json` (ontology name, variant, version, build time, source git commit, element counts per type, status and level, checksum of each file). | must |
| FR-32 | `ontology.ttl` carries for each element: its stable ID as IRI, labels (SKOS preferred, alternative and hidden labels), definition, scope notes separating senses, level, evidence (source-unit IDs), status (raw release) and deprecation with replacement. Cardinality limits are written both as OWL qualified cardinality and as SHACL shapes. Rules keep their condition, scope and evidence. | must |
| FR-33 | Levels are cumulative: `level-2.md` contains everything in level-1 plus level-2 elements; `level-3.md` contains all non-ignorable elements of that release. Ignorable elements appear in no level. Deprecated elements are left out of the `level-N.md` files. | must |
| FR-34 | Each `level-N.md` contains Mermaid diagrams (a taxonomy and a concept-relation diagram) and catalogues of concepts (with synonyms and definitions), relations and rules, each with links to their evidence. A diagram too large to read is split by top-level concept. In the raw release, elements that are not approved are visibly marked. | must |
| FR-35 | The governed build fails, and lists the offenders, if an approved relation, rule or property refers to an element that is not approved. The raw release is built regardless. | must |
| FR-36 | Building a release twice from the same records produces byte-identical files (apart from the build time in the manifest). | must |
| FR-37 | Each release also has a JSON-LD file with the same graph as `ontology.ttl`. | could |

### Evaluation
| ID   | Requirement | Priority |
|------|-------------|----------|
| FR-38 | An evaluation command runs a live ingestion of the pet manuals into a throw-away ontology and scores the result against the [answer key](../../research/notes/pet-manuals-corpus/README.md): ignorable passages, the leash/lead synonym and sense split, expected concepts and rules, and the exclusion traps. It prints the scores and writes a dated report; it is not a CI gate. The answer key is read only by this command, never by ingestion. | must |

## Apps and shared data affected
- **New app `ontology-builder`**: ingestion, extraction, local GUI, governance and release build. It is the only writer of every `ontology-<name>` dataset (Q9). Created by `/scaffold` in `/plan`. Because this spec also defines a shared dataset contract, it stays at the root (scope `system`).
- **New dataset `ontology-pets-and-house-rules`** (`data/ontology-pets-and-house-rules/`), git mode `commit` (Q7), owner `ontology-builder`. Further ontologies are further datasets of the same kind.
- **New contract** `libs/contracts/ontology/` (or per dataset, decided in `/plan` with a root ADR): describes `00_sources/` and `03_release/`. Future readers: the AI assistant (idea 0001) and the validation app (Q8).
- **Read, unchanged**: dataset `user-manuals-pets-and-house-rules` (via its contract). The root `components.json` gets `reads` for it.
- **Base environment**: uses the existing `ANTHROPIC_API_KEY`, `CLAUDE_MODEL` and `SHARED_DATA_DIR`. Any app-only variable goes into `apps/ontology-builder/.env.example`.
- **Libraries**: none in this spec.
- **Answer key** in `docs/research/notes/pet-manuals-corpus/` is read by the evaluation command only.

## Non-functional requirements
- **Determinism:** automated tests use recorded LLM responses and run without network or API key. Releases are deterministic (FR-36), so git diffs show only real changes.
- **Cost:** estimate and confirm before every LLM run (FR-6); no hard budget in v1.
- **Privacy:** only corpus text and user statements are sent to the Claude API. No secrets or personal data are written to the dataset; the sign-in hint (FR-2) asks for handles.
- **Local only:** the GUI listens on localhost only and serves one user at a time.
- **Responsiveness:** with up to 5,000 elements, filtering, search and a single review action respond within 1 second on a developer laptop.
- **Validity:** every record is validated against the data model's schema before it is written; an invalid record is never committed.
- **Accessibility:** status and level are never shown by colour alone (FR-20).
- **Format decisions** already made with the user (Q2, Q3, Q6): schema-defined YAML records (LinkML preferred) as the only editable source; RDF release generated one way, never edited by hand. `/plan` records them as app ADRs.

## Acceptance criteria
Tests marked *(fixture)* run on recorded LLM responses; *(eval)* is the live evaluation of FR-38 and reports a score instead of passing or failing.

- [x] AC-1 (FR-1): Given no ontology, when a domain admin creates `pets-and-house-rules` with a scope record, then `data/ontology-pets-and-house-rules/` exists with the folders of FR-30 and the scope record; when the scope record is empty, ingestion is refused with a message.
- [x] AC-2 (FR-2): Given the GUI is opened, when a person signs in as `alice` / user, then every decision they make is recorded with user name `alice` and role `user`; the sign-in window shows the handle hint.
- [x] AC-3 (FR-3): Given a person signed in as user, when they try to approve, reject, deprecate, edit the scope record or publish (in the GUI or through its backend API), then the action is refused and nothing changes.
- [x] AC-4 (FR-4, FR-5): *(fixture)* Given the dog manual and the building rules ingested as two corpora, then `00_sources/` holds `00_…` and `01_…` folders, every unit has an opaque ID, document ID, location, content hash and normalised text, and no ID contains text or position of the unit.
- [x] AC-5 (FR-5): Given a unit's text is edited in the registry fixture, when its hash is recomputed, then the hash changes and the ID does not.
- [x] AC-6 (FR-6): Given an ingestion is started, then the app shows the document count, unit count and estimated tokens and cost and calls the LLM only after confirmation; after the run, its record holds model, tokens used and times.
- [x] AC-7 (FR-7): Given a corpus folder already ingested, when it is ingested again into the same ontology, then the app refuses with a message and the dataset is unchanged.
- [x] AC-8 (FR-8): *(fixture)* Given the recorded LLM fails after half of the units, then afterwards either resuming completes the run with the same result as an uninterrupted run, or `git status` shows the dataset unchanged.
- [x] AC-9 (FR-9, FR-10): *(fixture)* Given the recorded responses for the pet manuals, then the records contain statements, terms, concepts, relations, rules and properties, each citing at least one existing source-unit ID; a test that removes the evidence from a record makes validation fail.
- [x] AC-10 (FR-9, FR-32): *(fixture)* Given the building rule "a dog on a lead of at most 2 m", then a rule record holds the limit, and `ontology.ttl` expresses it with its evidence; the cardinality of a relation (e.g. a recorded "at most 2 pets" rule) appears both as `owl:maxQualifiedCardinality` and as a SHACL `sh:qualifiedMaxCount` shape.
- [x] AC-11 (FR-11, FR-12): *(fixture)* Given the pet manuals, then one concept for the leash has "leash" as preferred or alternative label and "lead" (building rules) as alternative label; another concept for the owner's leading role is linked to "lead" in dog 6; the 2 m lead rule refers to the leash concept. *(eval)* The live run scores whether it found both.
- [x] AC-12 (FR-13): *(fixture)* Every element has a proposed level from the four values and a reason; a record with another level value fails validation.
- [x] AC-13 (FR-14): *(fixture)* The Bodza paragraph (dog 1), the Egyptian story (cat 1) and the Cicero quote and its paragraph (rules 1) are proposed ignorable with the right reason categories, and no element cites them as evidence; marking one of them not ignorable runs extraction on it after a cost confirmation. *(eval)* The live run scores the same, plus the traps: no `Bodza`, `Bastet` or `Egypt` concept, no "shared interest" rule, "13 years" not used as lifespan evidence.
- [x] AC-14 (FR-15): Given a new optional property is added to the concept schema, then every existing record still validates and both releases still build.
- [x] AC-15 (FR-16): Given an element is selected, then the GUI shows its evidence passage(s) above the LLM's proposal (GUI test checks the order).
- [x] AC-16 (FR-17, FR-26): For each action (include, exclude with reason, correct a field, override level, merge as synonym, split senses, reassign a mention), a GUI or API test performs it and checks the record and a decision entry with user name, role, timestamp, old and new value and reason.
- [x] AC-17 (FR-18): Given 20 elements selected, when a user sets them to level-3 in one step, then all 20 change and 20 decisions are recorded; a domain admin can bulk-approve, a user cannot.
- [x] AC-18 (FR-19): Given the pet fixture, filtering by type = rule, level = level-1 and document = building rules returns exactly the matching records; searching "lead" returns the elements whose labels, definitions or evidence contain it.
- [x] AC-19 (FR-20): Each status is rendered with a distinct colour and a distinct text label or icon (GUI test reads both).
- [x] AC-20 (FR-21): Given a user types a statement, then a unit appears in `00_sources/90_user_statements/` with ID, hash, author and timestamp; editing it keeps the ID, adds a revision and changes the hash.
- [x] AC-21 (FR-22): Given a user authors a concept without a definition from a user statement, then the concept record cites that statement and is `included`; authoring an element with no evidence is refused.
- [x] AC-22 (FR-23, FR-3): Status transitions follow FR-23; a test tries every forbidden transition (e.g. user → approved, excluded → approved) and expects each to be refused.
- [x] AC-23 (FR-24): Given an approved concept in governed release 1.0.0, when a user edits its definition, then it becomes `included`, and a governed build made before re-approval contains the old definition.
- [x] AC-24 (FR-25): Given an approved element, when the admin deprecates it with a replacement, then the record remains with `deprecated` and the replacement ID; the Turtle marks it `owl:deprecated` with the replacement; no operation deletes an approved, excluded or rejected record.
- [x] AC-25 (FR-27): Given a save in the GUI, then exactly one new commit exists that touches only `data/ontology-<name>/`, while unrelated changes in the working copy stay uncommitted; given a failing pre-commit hook, no commit is made and the GUI shows the hook output; nothing is pushed.
- [x] AC-26 (FR-28, FR-33): Given elements in every status and level, then the raw release contains all except excluded, rejected and ignorable ones, each with status; `level-1.md` ⊂ `level-2.md` ⊂ `level-3.md` by element ID, and no ignorable or deprecated element is in any `level-N.md`.
- [x] AC-27 (FR-29): Given governed release 1.0.0 and later approvals, when the admin publishes, then the governed folder holds version 1.1.0 by default, only approved and deprecated elements, and a change log listing added, changed, deprecated and removed elements against 1.0.0.
- [x] AC-28 (FR-30, FR-31): A test checks the dataset layout and that both release folders contain `ontology.ttl`, `level-1.md`, `level-2.md`, `level-3.md` and `manifest.json` with the fields of FR-31 and matching checksums.
- [x] AC-29 (FR-32): `ontology.ttl` of both variants parses as RDF 1.1 Turtle, and for a sample element it contains the IRI, SKOS labels, definition, level, evidence IDs, and (raw) status; the SHACL shapes in it validate the pet fixture without errors.
- [x] AC-30 (FR-34): Each `level-N.md` contains at least one taxonomy and one concept-relation Mermaid diagram that render without error (Mermaid CLI), and catalogues of concepts, relations and rules whose evidence links resolve to source-unit IDs; in the raw release every non-approved element is marked.
- [x] AC-31 (FR-35): Given an approved rule that refers to a `proposed` concept, when the admin publishes, then the governed build fails listing that rule and concept, the governed folder is unchanged, and the raw release is built.
- [x] AC-32 (FR-36): Building each release twice from the same records gives identical files, except the build time in `manifest.json`.
- [x] AC-33 (FR-38): The evaluation command runs on the pet manuals, writes a dated report with a score per answer-key item (AC-11, AC-13 and the expected concept and rule lists), and a test confirms ingestion code never opens the answer-key path.

## Edge cases and failure modes
- **No API key or API down:** ingestion stops before any change and says so; the GUI still works for review, authoring and releases.
- **LLM returns invalid output:** the response is validated against the schema; invalid items are retried once, then reported in the run record and skipped; no invalid record is written.
- **LLM cites a source-unit ID that does not exist:** the item is dropped and reported (FR-10).
- **An empty Markdown file, or one with no headings:** ingested as a document with zero or one-section units; no error.
- **Identical sentences in two places:** they are separate units with separate IDs and the same hash.
- **A user merges two concepts that both have approved relations:** the merged concept goes back to `included` (FR-24) and the relations follow it.
- **A user splits a sense of an approved term:** both resulting concepts are `included`; the governed release keeps the old version until approved.
- **Deprecating an element that others refer to:** allowed; the governed build warns and lists the referring elements (they keep pointing at the deprecated one until fixed).
- **The governed build fails (FR-35):** the previous governed release stays as it was; nothing is half-written.
- **Two GUI windows open on the same ontology:** the second refuses to start or opens read-only (single user, FR-27).
- **The working copy is on a branch with conflicts, or git is unavailable:** saving is refused with a message; nothing is written outside a commit.
- **The user types an email address as user name:** the GUI warns before signing in (FR-2).
- **An ignorable unit holds real content too** (e.g. dog 1 story followed by lifespan facts in the next paragraph): units are small enough that the story and the facts are separate units; a reviewer can mark a unit not ignorable (FR-14).

## Open questions
None blocking. To be settled in `/plan`, with ADRs at the right level:
- Tech stack of the app and the GUI, and the format choice (LinkML YAML records → OWL 2 + SKOS + SHACL Turtle) as app ADRs.
- Whether all `ontology-<name>` datasets share one contract `libs/contracts/ontology/` and how they are declared in `components.json` (root ADR).
- Exact source-unit granularity (sentence vs paragraph) and the ID format.
- How large Mermaid diagrams are split, and how evidence links in `level-N.md` point to the source text.
