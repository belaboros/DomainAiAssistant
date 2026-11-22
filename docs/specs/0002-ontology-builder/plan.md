# Plan 0002 · OntologyBuilder

- **Status:** approved
- **Spec:** [spec.md](spec.md)
- **Idea:** [0002-ontology-builder](../../ideas/0002-ontology-builder.md) (plan decisions: Q29–Q35; implement-stage changes: Q37–Q50)
- **Last updated:** 2026-11-22

## Approach

`ontology-builder` is one app with a **Python back end** and a **React + TypeScript single-page front end** (Q34). It is the only writer of every `data/ontology-<name>/` dataset.

1. **API-first core.** Every rule of the spec (roles, status transitions, evidence, levels, releases) lives in Python components behind one use-case layer (`workflows`). The FastAPI `api`, the `cli` and the `evaluation` command are thin callers of that layer. The GUI never decides anything the back end doesn't check again, so AC-3 holds "through its backend API" by construction.
2. **One schema, many outputs** (Q2, Q3, Q6). A LinkML schema defines the records: source units, the six element types, decisions, runs and the scope record. It also defines the LLM's structured output. From it we generate the Pydantic models used everywhere (validation before every write) and the JSON Schema sent to Claude as the tool input schema. Records are YAML, one file per element, in `01_model/`. The YAML is the only editable source.
3. **Source units are Markdown blocks** (Q31): one unit per paragraph, list item, blockquote or table row, parsed with `markdown-it-py` (which gives the line positions). Every document and unit gets a minted ID: a type prefix plus a ULID, e.g. `su_01JDK7F3Q8…`. The ID never comes from the unit's text or position. The registry holds the location, the SHA-256 of the normalised text and the text itself.
4. **Two-pass extraction.** Pass 1, per document: Claude gets the scope record, the level rubric and the document's units, each with a short alias. It returns, for each unit, an ignorable verdict (with category and reason) and, for the rest, candidate statements, terms with mentions, concepts, relations, rules and properties, each with evidence, a level and a reason. Because the API cannot compile one grammar for all six candidate types, pass 1 is two calls per document (Q40, [ontology-builder/ADR-0007](../../../apps/ontology-builder/docs/architecture/adr/0007-pass-1-as-two-structured-output-calls-per-document.md)): call A returns the verdicts, statements, terms, concepts and relations; call B gets the same units plus A's candidates by key and returns the rules and properties that refer to them. Pass 2, per ingestion: Claude gets every candidate term with its mentions and contexts, plus the concepts already in the ontology. It returns synonym groups (several terms → one concept) and sense splits (one term → several concepts, each mention resolved). Output comes back as schema-shaped JSON (structured outputs, ADR-0006) and is validated against the full schema. Invalid items are retried once, then reported in the run record and dropped. Items that cite unknown units are dropped and reported (FR-10). In both prompts each unit is shown with a short alias (`U1`, `U2`, …) that is unique in that prompt, and the output cites units by alias; extraction maps the aliases back to the `su_` IDs before building any record, so a miscopied ID can never point evidence at a neighbouring unit (Q38). Pass 2 shows concepts the same way (`C1`, `C2`, …; new concepts first, then those already in the ontology), and a synonym group lists the new concepts it merges (`merge`): their evidence and parents go to the kept concept and every reference is re-pointed to it. A concept already in the ontology is never merged away or changed by pass 2 (merging approved concepts is a review action, FR-17).
5. **Synonyms and senses are modelled through terms.** A `Term` is a word with mentions `{unit, concept}`. A concept's SKOS alternative labels are the labels of the terms that point to it. A homonym is a term whose mentions point to two concepts, each with a scope note. Merge, split and reassign are operations on mentions (FR-11, FR-12, FR-17).
6. **Pending change set, atomic save, one commit.** GUI actions change an in-memory copy of the ontology and add to a pending change set. The change set is journaled in a git-ignored work folder, so a crash loses nothing. **Save** validates every changed record, writes the records and decisions, rebuilds the raw release in a staging copy, swaps the staging copy in, and makes one `git commit` limited to `data/ontology-<name>/`, with hooks running. If anything fails, the old dataset folder is swapped back and the GUI shows the message. Nothing is ever pushed (FR-27). Ingestion writes the same way at the end of a run; until then the LLM responses are cached per batch in the work folder, so an interrupted run can resume (FR-8).
7. **Releases are generated one way and deterministically.** The `release` component builds `ontology.ttl` (rdflib; OWL 2 + SKOS + SHACL; Turtle with no blank-node labels, because every restriction and shape is inlined), `level-1/2/3.md` (Jinja2 templates with Mermaid), `CHANGELOG.md` (governed only) and `manifest.json`. Raw is built on every save; governed only on publish, after the dependency check of FR-35.
8. **FR-24 by approved snapshots.** When an element is approved, its approved content is stored in the record (`approved_snapshot`). A later edit puts the element back to `included` but keeps the snapshot. The governed build uses the snapshot for any element that has one and is not deprecated.
9. **One shared ontology contract** (Q30): `libs/contracts/ontology/` describes `00_sources/` and `03_release/`. Each dataset has a thin `libs/contracts/ontology-<name>/README.md` that pins the contract version it conforms to.

## Alternatives considered

- **GUI: FastAPI + Jinja2 + htmx** (prototype A): one language and simpler tests. Not chosen because v2 needs the list and an interactive diagram to share one selection and one set of actions (Q32–Q34); with htmx that needs growing glue code between server-rendered HTML and a JS canvas.
- **GUI: NiceGUI or Streamlit** (prototype C): quickest start. Not chosen: least control over the evidence-first layout and the tested markup, no HTTP API for the role checks, and diagrams would need a custom Vue component.
- **Turtle or OWL as the editable source:** rejected in the research (Q2). Evidence, level and status become axiom annotations, which diff badly and are hard for the LLM.
- **Write each action to disk at once, commit on Save:** simpler, but files would sit on disk outside a commit, and a failing hook would leave a half-saved dataset. The edge case "nothing is written outside a commit" rules it out.
- **One LLM pass over the whole corpus:** cheaper in calls, but it exceeds a useful context size for real manuals and gives worse evidence IDs. Per-document extraction plus one term-resolution pass keeps prompts small and still finds cross-document synonyms (leash/lead).
- **Sentence-level source units:** rejected in Q31 (fragile splitting, about 3× the units).
- **A graph store (Oxigraph or Fuseki):** not needed at 5,000 elements. All records are loaded in memory (research §3).
- **Contract per dataset, or changing `system-map.sh` to share one folder:** rejected in Q30.

## Components and files

All paths are under `apps/ontology-builder/` unless shown otherwise. Python package `ontology_builder` (src layout); front end in `web/`.

| Path | New/changed | Responsibility |
|------|-------------|----------------|
| `src/ontology_builder/model/` | new | **model**: Defines the LinkML schema of every record and validates records against it. |
| `src/ontology_builder/store/` | new | **store**: Reads and writes the files of one ontology dataset, atomically. |
| `src/ontology_builder/sources/` | new | **sources**: Splits Markdown documents and user statements into registered source units. |
| `src/ontology_builder/llm/` | new | **llm**: Calls Claude or replays recorded responses, and estimates tokens and cost. |
| `src/ontology_builder/extraction/` | new | **extraction**: Turns source units into validated proposed elements with evidence and levels. |
| `src/ontology_builder/ingestion/` | new | **ingestion**: Runs one ingestion or on-demand extraction, resumable and all-or-nothing. |
| `src/ontology_builder/governance/` | new | **governance**: Applies review, authoring and governance actions under the role and status rules, recording each decision. |
| `src/ontology_builder/release/` | new | **release**: Builds the raw and governed release files from the records. |
| `src/ontology_builder/vcs/` | new | **vcs**: Commits the changed files of one dataset path to the local git working copy. |
| `src/ontology_builder/workflows/` | new | **workflows**: Runs the app's use cases (create, ingest, review, save, publish) across the components below it. |
| `src/ontology_builder/api/` | new | **api**: Exposes the use cases as a localhost JSON API and serves the built front end. |
| `src/ontology_builder/cli/` | new | **cli**: Exposes the use cases as `ontology-builder` commands. |
| `src/ontology_builder/evaluation/` | new | **evaluation**: Scores a live ingestion of the pet manuals against the answer key. |
| `web/` | new | **web**: Renders the review GUI in the browser and talks to the API only over HTTP. |
| `src/ontology_builder/llm/pricing.yaml` | new | Price per million tokens per model, with the date it was checked (filled from Anthropic's pricing page when implemented). |
| `tests/` (+ `tests/fixtures/`) | new | pytest suites, curated LLM fixtures for the pet manuals, a temp-git-repo helper. |
| `web/src/**/*.test.tsx`, `web/e2e/` | new | Vitest + Testing Library component tests; Playwright end-to-end tests. |
| `apps/ontology-builder/docs/evaluations/` | new | Dated evaluation reports (FR-38). |
| `docs/research/notes/pet-manuals-corpus/answer-key.yaml` | new | Machine-readable form of the answer key, read only by `evaluation`. |
| `libs/contracts/ontology/` | new | Shared contract: README, CHANGELOG, `manifest.schema.json`, `source-unit.schema.json`, `vocab.ttl`. |
| `libs/contracts/ontology-pets-and-house-rules/README.md` | changed | Thin contract that pins `ontology` contract 0.1.0. |
| `apps/ontology-builder/.env.example` | changed | App variables (below). |
| `.gitignore` | changed | `apps/ontology-builder/.work/`, `apps/ontology-builder/web/node_modules/`, `apps/ontology-builder/web/dist/`, `/data/.*.staging/`, `/data/.*.previous/`. |
| `pyproject.toml`, `uv.lock` (root workspace) | new | Created by `/add-language python`; the app is a workspace member. |

## Data and interfaces

### Dataset layout (FR-30; contract = `00_sources/` + `03_release/`)

```
data/ontology-<name>/
├── 00_sources/
│   ├── 00_<corpus-slug>/                corpus 00–89, one per ingested folder
│   │   ├── corpus.yaml                  id, number, source path (relative to SHARED_DATA_DIR), ingest run id
│   │   ├── documents/<doc-id>.yaml      id, path, title, content hash
│   │   └── units/<doc-id>.yaml          ordered list of the document's source units
│   └── 90_user_statements/<su-id>.yaml  one file per statement, with revisions
├── 01_model/                            internal
│   ├── scope.yaml                       purpose, readers, level-1/2/3 guidance, ignorable examples, base IRI
│   └── elements/<type>/<id>.yaml        one record per element (type ∈ statement, term, concept, relation, rule, property)
├── 02_decisions/                        internal
│   ├── YYYY-MM-DD.jsonl                 append-only, one decision per line
│   └── runs/<run-id>.yaml               model, tokens in/out, start/end, status, skipped items
└── 03_release/
    ├── 00_raw/       ontology.ttl, level-1.md, level-2.md, level-3.md, manifest.json
    └── 01_governed/  the same + CHANGELOG.md
```

**Source unit** (contract): `id` (`su_` + ULID), `document_id` (`doc_` + ULID), `kind` (paragraph | list_item | blockquote | table_row | user_statement), `location` {`path`, `heading_path[]`, `index_in_section`}, `content_hash` (`sha256:` of the text after normalising whitespace and Unicode NFC), `text`, `ignorable` {`proposed`, `category`, `reason`, `status`}. A user statement also has `author`, `created_at` and `revisions[]` {`rev`, `text`, `content_hash`, `author`, `at`}; the ID never changes (FR-21). Two units with identical text keep separate IDs and share a hash.

**Element record** (internal, LinkML): common slots are `id` (type prefix `st_ tm_ cn_ rl_ ru_ pr_` + ULID), `label`, `definition`, `level` (enum `level-1 | level-2 | level-3 | ignorable`), `level_reason`, `status` (enum of FR-23), `status_reason`, `evidence[]` {`unit`, `quote?`} (min 1), `origin` {`kind`: llm | user, `run_id?`, `author?`, `created_at`}, `approved_snapshot?`, `replaced_by?`. Then by type:
- **Term:** `mentions[]` {`unit`, `concept`}.
- **Concept:** `parents[]` (is-a links to concepts).
- **Relation:** `subject`, `object` (concepts), `predicate_label`, `cardinality` {`min?`, `max?`}.
- **Rule:** `modality` (must | must_not | may), `actor`, `action`, `condition?`, `limit?` {`comparator`, `value`, `unit`}, `cardinality?` {`relation`, `min?`, `max?`}, `scope` (corpus or document IDs), `refers_to[]`.
- **Property:** `of` (element), `name`, `value`, `unit?`.
- **Statement:** `text`.

Every new slot is optional by default, so adding one never invalidates old records (FR-15, AC-14).

**Decision:** `id`, `at`, `user`, `role`, `action`, `element_id`, `field`, `old`, `new`, `reason`. The clock and the ID minter are injected, so tests are deterministic.

### Status transitions (FR-23 to FR-25)

| From \ action | include (any) | exclude + reason (any) | approve (admin) | reject + reason (admin) | deprecate (admin) | edit, level, merge, split (any) |
|---|---|---|---|---|---|---|
| proposed | included | excluded | approved (records include + approve) | rejected | refused | stays proposed |
| included, never approved | refused | excluded | approved | rejected | refused | stays included |
| included, has approved snapshot | refused | refused (deprecate instead) | approved | refused | deprecated | stays included |
| approved | refused | refused | refused | refused | deprecated (+ optional replacement) | → included, snapshot kept |
| excluded | included | refused | refused | refused | refused | refused |
| rejected, deprecated | refused | refused | refused | refused | refused | refused |

Nothing deletes a record. Merging an approved concept deprecates it with `replaced_by`, so only a domain admin can do that.

### RDF mapping (FR-32)

- **IRIs.** An element's IRI is `<base IRI><id>`. The default base IRI is `urn:domain-ai-assistant:ontology:<name>:`, set in the scope record. The vocabulary for level, status, evidence and rule parts is `urn:domain-ai-assistant:vocab#` (prefix `dai:`), declared in `libs/contracts/ontology/vocab.ttl`.
- **Concept** → `owl:Class` and `skos:Concept` (punning). It carries `skos:prefLabel` (its label), `skos:altLabel` (synonym terms), `skos:hiddenLabel` (non-preferred variants), `skos:definition` and `skos:scopeNote` (one per sense of a homonym). Its is-a links become `rdfs:subClassOf` and `skos:broader`.
- **Relation** → `owl:ObjectProperty` with `rdfs:domain` and `rdfs:range`.
- **Cardinality** of a relation or rule → both an `owl:Restriction` with `owl:maxQualifiedCardinality` / `owl:minQualifiedCardinality` on the domain class (inlined blank node), and a `sh:NodeShape` (IRI `<element IRI>-shape`) with `sh:qualifiedValueShape` and `sh:qualifiedMaxCount` / `sh:qualifiedMinCount`.
- **Rule** → a `dai:Rule` individual with `dai:modality`, `dai:actor`, `dai:action`, `dai:condition`, `dai:limitComparator`, `dai:limitValue`, `dai:limitUnit`, `dai:scope` and `dai:refersTo`.
- **Statement and Property** → `dai:Statement` and `dai:Property` individuals.
- **On every element:** `dai:level`, `dai:evidence` (the source unit's IRI, `<base IRI><su-id>`), `dai:status` (raw release only), and `owl:deprecated true` + `dcterms:isReplacedBy` when deprecated.
- **Ontology header:** `owl:Ontology` with `owl:versionIRI`, `owl:versionInfo` and `dcterms:description` (the scope record's purpose).

### `level-N.md` (FR-33, FR-34)

- **Sections:** title and version, a taxonomy diagram (`flowchart TB`, is-a), a concept-relation diagram (`flowchart LR`), catalogues of concepts (labels, synonyms, definition), relations and rules (structure and limits), and an **Evidence** appendix with one anchor per cited unit (`<a id="su_…">`) holding the unit's text and location.
- **Links.** Catalogue entries link to `#su_…`, so every link resolves inside the file.
- **Large diagrams.** A diagram with more than 40 nodes is split into one diagram per top-level concept (a concept with no parent in the level).
- **Raw release.** Non-approved elements carry a text badge (`● proposed`, `◐ waiting for approval`) and a dashed Mermaid class.
- **Levels are cumulative,** and deprecated and ignorable elements are left out.

### `manifest.json` (FR-31)
`ontology`, `variant` (raw | governed), `version` (governed: semver; raw: `raw+<short git sha>`), `built_at`, `source_commit`, `counts` {`by_type`, `by_status`, `by_level`}, `files` {name → `sha256`}. Schema: `libs/contracts/ontology/manifest.schema.json`. `built_at` is the only field that varies between identical builds (FR-36).

### HTTP API (localhost only; JSON; OpenAPI → generated TypeScript client)
- **Session:** `POST /api/session` {user, role} → session cookie. The response warns when the user name looks like an email address, and names the ontology the server opened (the GUI addresses the routes below by it). `DELETE /api/session` signs out.
- **Ontologies:** `GET /api/ontologies`, `POST /api/ontologies` (admin: name + scope), `PUT /api/ontologies/{name}/scope` (admin).
- **Elements:** `GET /api/ontologies/{name}/elements` (compact index of every element, for filtering in the client; typed entries `IndexEntryOut` and corpora `CorpusOut`, so the generated TypeScript types cover them) and `GET …/elements/{id}` (full record + evidence units + decisions; typed `ElementDetailOut`: `EvidenceOut`, `RecordOut` with the common fields typed and the type-specific ones passed through, `DecisionOut`).
- **Units:** `GET …/units` (every corpus unit and user statement, unsaved statements included; typed `UnitOut`: kind, corpus, document, text, ignorable verdict, and for a statement its author and revisions). The GUI's evidence picker, statement editing and the not-ignorable dialog choose from it (Q49).
- **Actions:** `POST …/actions` {action, ids[], payload}. Actions are include, exclude, approve, reject, deprecate, level, correct, merge, split and reassign. The server checks role and transition for every ID and returns per-ID results. Marking units not ignorable (FR-14) is an on-demand ingestion (below); confirming an ignorable verdict is not part of v1 (Q45).
- **Authoring:** `POST …/statements`, `PUT …/statements/{id}` (new revision), `POST …/elements` (authored element; needs evidence).
- **Ingestion:** `POST …/ingestions/estimate` {folder} or {units[]} (not ignorable) → {documents, units, tokens, cost}; `POST …/ingestions` {folder or units[], confirm: true} → run id; `GET …/runs/{id}`. The run is synchronous: the GUI shows a running state, then the run record (Q50).
- **Save and publish:** `POST …/save` → {commit sha} or {hook output}; `POST …/publish` (admin) {version} → {version, changelog} or {offenders}.

**Guards:**
- The server binds to `127.0.0.1` only.
- It rejects any Host header other than `127.0.0.1:<port>` or `localhost:<port>` (DNS rebinding).
- Every write needs a same-origin request with the header `X-Ontology-Builder: 1`.
- One server process per dataset: a lock in the work folder; a second process refuses to start.
- A second browser session on the same server is read-only.

### CLI
`ontology-builder create <name> --scope <file> --user <handle>` · `ontology-builder ingest <name> <folder> [--yes] [--resume <run-id>]` (shows the estimate and asks unless `--yes`) · `ontology-builder build <name>` (raw release, no commit) · `ontology-builder serve <name> [--port]` · `ontology-builder eval [--model …]`. Publishing is GUI-only (it needs a signed-in domain admin).

### LLM
- **Client.** The `anthropic` SDK, with the model from `CLAUDE_MODEL`. Structured output uses JSON structured outputs (`output_config.format`, type `json_schema`) with the schema generated from the LinkML output classes; keywords the API does not support (patterns, numeric and length bounds) are removed before sending and still validated by Pydantic. A forced tool call was planned first, but current models reject a forced `tool_choice` (Q37, [ontology-builder/ADR-0006](../../../apps/ontology-builder/docs/architecture/adr/0006-json-structured-outputs-instead-of-a-forced-tool-call.md)).
- **Modes.** `ONTOLOGY_BUILDER_LLM_MODE=live|record|replay`. Replay looks up `tests/fixtures/llm/<sha256 of the canonical request>.json`. Tests always replay.
- **Fixtures** for the pet manuals are seeded from one live recording, then **curated by hand** to the answer the pipeline must handle. They test our code, not the model; the model is judged by `eval`.
- **Cost estimate.** Tokens are counted with the API's count-tokens endpoint when a key is set, or estimated as characters ÷ 3.5 without one. Expected output is assumed to be 0.6 × input. The price per token comes from `pricing.yaml`; for an unknown model only tokens are shown.

### Evaluation (FR-38)
- `ontology-builder eval` creates a throw-away ontology in a temporary `SHARED_DATA_DIR`, with no git and no commit.
- It ingests the three manuals live and reads `docs/research/notes/pet-manuals-corpus/answer-key.yaml` only after the ingestion has finished.
- It scores each item: ignorable passages and their categories, the leash/lead synonym and sense split, the expected concepts and rules (by normalised label or synonym), and the traps (no `Bodza`, `Bastet` or `Egypt` concept, no "shared interest" rule, "13 years" never cited for the lifespan).
- It prints the scores and writes `apps/ontology-builder/docs/evaluations/YYYY-MM-DD-<model>.md`.

### Configuration
App-only variables in `apps/ontology-builder/.env.example`: `ONTOLOGY_BUILDER_PORT=8765`, `ONTOLOGY_BUILDER_WORK_DIR=apps/ontology-builder/.work`, `ONTOLOGY_BUILDER_LLM_MODE=live`. The base variables `ANTHROPIC_API_KEY`, `CLAUDE_MODEL` and `SHARED_DATA_DIR` are unchanged.

### Commands (go into `apps/ontology-builder/CLAUDE.md`; exact tool versions are pinned by `/add-language`)
- Back-end tests: `uv run --package ontology-builder pytest apps/ontology-builder/tests`
- Front-end tests: `npm --prefix apps/ontology-builder/web test`, and `npm --prefix apps/ontology-builder/web run e2e` (Playwright)
- Build the GUI: `npm --prefix apps/ontology-builder/web run build`
- Run: `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder serve pets-and-house-rules`
- Evaluate: `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder eval`

The package manager for the front end (npm or pnpm) is asked in `/add-language js-ts`. The commands above use npm until then.

## Architecture impact

- **System level** (root `docs/architecture/components.json`, then `tools/monorepo/system-map.sh`):
  - **Apps / libraries / datasets added:** app `ontology-builder`; dataset `ontology-pets-and-house-rules` (git `commit`, owner `ontology-builder`). Both were scaffolded in this planning change (Q35). No library (Q12).
  - **New edges:** `ontology-builder` writes `ontology-pets-and-house-rules` and reads `user-manuals-pets-and-house-rules`. No app → app edge.
  - **Dataset contract changes:** new shared contract `libs/contracts/ontology/` 0.1.0, and the thin `libs/contracts/ontology-pets-and-house-rules/` 0.1.0, which conforms to it. The manuals contract is unchanged.
  - **Base environment variables:** none.
  - **Root docs:** `architecture.md` §1 (purpose), §2 (context: users, Claude API, git) and §6 (flow: ontology-builder publishes a release → future readers) are filled in task T31.
- **App level** (`apps/ontology-builder/docs/architecture/components.json` and `architecture.md`, written in this change):
  - **Components added:** model, store, sources, llm, extraction, ingestion, governance, release, vcs, workflows, api, cli, evaluation, web.
  - **Dependencies** (all acyclic, pointing towards more stable components; efferent coupling ≤ 4 for each, except ingestion at 5 and workflows at 6):
    - model → none
    - store → model
    - sources → model
    - llm → none
    - extraction → model, llm
    - ingestion → model, sources, extraction, store, llm (Ce 5, warn band; Q43, [ontology-builder/ADR-0008](../../../apps/ontology-builder/docs/architecture/adr/0008-ingestion-depends-on-model.md))
    - governance → model, store
    - release → model, store
    - vcs → none
    - workflows → ingestion, governance, release, vcs, store, llm (Ce 6, warn band; the composition root that opens the dataset and builds the LLM client; Q44, [ontology-builder/ADR-0009](../../../apps/ontology-builder/docs/architecture/adr/0009-workflows-depends-on-store-and-llm.md))
    - api → workflows, model
    - cli → workflows, evaluation, api (`serve` runs the API server; Q46, [ontology-builder/ADR-0010](../../../apps/ontology-builder/docs/architecture/adr/0010-cli-depends-on-api.md))
    - evaluation → workflows, store
    - web → api, over HTTP only (no import edge; the types generated from `openapi.json` are the contract, ontology-builder/ADR-0011)
  - **Answer-key isolation:** only `evaluation` may refer to the answer-key path. A test enforces this (AC-33).
- **ADRs:**
  - Root [ADR-0019](../../architecture/adr/0019-ontology-builder-app-and-shared-ontology-contract.md): add the ontology-builder app and the `ontology-<name>` datasets with one shared contract.
  - [ontology-builder/ADR-0001](../../../apps/ontology-builder/docs/architecture/adr/0001-linkml-yaml-records-as-source-rdf-releases-as-output.md): LinkML YAML records as the only source; RDF and Markdown releases generated one way.
  - [ontology-builder/ADR-0002](../../../apps/ontology-builder/docs/architecture/adr/0002-api-first-python-back-end-with-react-typescript-front-end.md): API-first Python back end with a React + TypeScript front end.
  - [ontology-builder/ADR-0003](../../../apps/ontology-builder/docs/architecture/adr/0003-markdown-block-source-units-with-minted-ids.md): Markdown-block source units with minted IDs.
  - [ontology-builder/ADR-0004](../../../apps/ontology-builder/docs/architecture/adr/0004-pending-change-set-atomic-save-one-commit.md): pending change set, atomic save, one commit per save.
  - [ontology-builder/ADR-0005](../../../apps/ontology-builder/docs/architecture/adr/0005-two-pass-llm-extraction-with-curated-fixtures.md): two-pass LLM extraction behind a replaceable client with curated fixtures.
  - [ontology-builder/ADR-0008](../../../apps/ontology-builder/docs/architecture/adr/0008-ingestion-depends-on-model.md): ingestion may depend on model (implement stage, Q43).
  - [ontology-builder/ADR-0009](../../../apps/ontology-builder/docs/architecture/adr/0009-workflows-depends-on-store-and-llm.md): workflows may depend on store and llm (implement stage, Q44).
  - [ontology-builder/ADR-0010](../../../apps/ontology-builder/docs/architecture/adr/0010-cli-depends-on-api.md): cli may depend on api (implement stage, Q46).
  - [ontology-builder/ADR-0011](../../../apps/ontology-builder/docs/architecture/adr/0011-api-types-with-openapi-typescript-calls-through-openapi-fetch.md): the GUI's API types are generated with openapi-typescript, calls go through openapi-fetch (implement stage, Q48).
  - [ontology-builder/ADR-0006](../../../apps/ontology-builder/docs/architecture/adr/0006-json-structured-outputs-instead-of-a-forced-tool-call.md): JSON structured outputs instead of a forced tool call (implement stage, Q37).
  - The language ADRs are written by `/add-language` (T1, T22).
- **App environment variables:** `ONTOLOGY_BUILDER_PORT`, `ONTOLOGY_BUILDER_WORK_DIR`, `ONTOLOGY_BUILDER_LLM_MODE`.
- **New languages:** Python (`/add-language python`, T1) and TypeScript (`/add-language js-ts`, T22, before any front-end file).

## Verification map

Back-end tests live in `apps/ontology-builder/tests/`, front-end tests in `apps/ontology-builder/web/src/` and `web/e2e/`. *(fixture)* = replayed LLM responses.

| Acceptance criterion | How it is verified (test name / command) |
|----------------------|------------------------------------------|
| AC-1  | `test_ontology_create.py::test_create_makes_layout_and_scope`, `::test_ingest_refused_when_scope_missing_or_empty` |
| AC-2  | `test_api_session.py::test_decisions_carry_user_and_role`, `::test_email_like_name_warns`; `web/src/signin/SignIn.test.tsx::shows_handle_hint` |
| AC-3  | `test_api_roles.py::test_user_refused[approve,reject,deprecate,scope,publish]`: 403, and the dataset tree hash is unchanged; `web/src/review/Actions.test.tsx::admin_actions_disabled_for_user`, `web/src/dialogs/PublishDialog.test.tsx::user_cannot_publish` |
| AC-4  | `test_sources_registry.py::test_two_corpora_get_00_and_01` (fixture), `::test_unit_fields_present`, `::test_ids_contain_no_text_or_position` |
| AC-5  | `test_sources_registry.py::test_text_edit_changes_hash_not_id` |
| AC-6  | `test_ingestion_estimate.py::test_no_llm_call_before_confirm` (spy client), `::test_run_record_has_model_tokens_times`; `web/src/dialogs/IngestDialog.test.tsx::shows_counts_tokens_cost`, `::runs_after_confirm_then_shows_the_run_record` |
| AC-7  | `test_ingestion_refusals.py::test_same_folder_twice_refused_dataset_unchanged` |
| AC-8  | `test_ingestion_atomic.py::test_fail_halfway_then_resume_equals_uninterrupted`, `::test_fail_halfway_without_resume_leaves_git_status_clean` (fixture, temp git repo) |
| AC-9  | `test_extraction_pets.py::test_all_element_types_cite_existing_units` (fixture); `test_model_validation.py::test_record_without_evidence_is_invalid` |
| AC-10 | `test_release_rdf.py::test_lead_limit_rule_record_and_turtle`, `::test_max_two_pets_as_owl_and_shacl` (fixture user statement "at most 2 pets") |
| AC-11 | `test_extraction_terms.py::test_leash_lead_synonym_and_lead_senses` (fixture); `ontology-builder eval` reports the live score |
| AC-12 | `test_model_validation.py::test_every_element_has_level_and_reason` (fixture), `::test_unknown_level_is_invalid` |
| AC-13 | `test_extraction_ignorable.py::test_bodza_egypt_cicero_ignorable_with_categories`, `::test_no_element_cites_ignorable_units`, `::test_not_ignorable_runs_extraction_after_confirm` (fixture); `web/src/dialogs/NotIgnorableDialog.test.tsx::extraction_runs_after_the_cost_confirmation`; `eval` reports the live score and the traps |
| AC-14 | `test_model_extensibility.py::test_new_optional_concept_slot_keeps_records_valid_and_releases_build` |
| AC-15 | `web/src/review/ElementDetail.test.tsx::evidence_rendered_before_proposal`; `web/e2e/save.spec.ts` (in the browser) |
| AC-16 | `test_governance_actions.py::test_action_records_decision[include,exclude,correct,level,merge,split,reassign]`; `web/src/review/Actions.test.tsx::each_action_calls_api` |
| AC-17 | `test_governance_bulk.py::test_bulk_level3_on_20_records_20_decisions`, `::test_bulk_approve_admin_only`; `web/src/review/BulkBar.test.tsx` |
| AC-18 | `test_api_elements.py::test_filter_rule_level1_building_rules`, `::test_search_lead_matches_label_definition_evidence`; `web/src/review/filter.test.ts` (same cases on the client filter) |
| AC-19 | `web/src/review/StatusBadge.test.tsx::each_status_has_distinct_colour_class_and_label`; `web/e2e/save.spec.ts` (computed colours) |
| AC-20 | `test_user_statements.py::test_statement_unit_fields`, `::test_edit_keeps_id_adds_revision_changes_hash`; `web/src/dialogs/StatementDialog.test.tsx` |
| AC-21 | `test_authoring.py::test_concept_without_definition_from_statement_is_included`, `::test_authoring_without_evidence_refused`; `web/src/dialogs/AuthorDialog.test.tsx::concept_without_definition_from_a_statement`, `::evidence_is_required` |
| AC-22 | `test_governance_transitions.py::test_allowed_transitions`, `::test_forbidden_transition_refused` (parametrised over the table above) |
| AC-23 | `test_release_governed.py::test_edit_after_approval_governed_keeps_old_definition` |
| AC-24 | `test_governance_deprecate.py::test_deprecate_with_replacement`, `::test_no_operation_deletes_approved_excluded_rejected`; `test_release_rdf.py::test_deprecated_has_owl_deprecated_and_replacement` |
| AC-25 | `test_vcs_commit.py::test_save_makes_one_commit_touching_only_dataset`, `::test_unrelated_changes_stay_uncommitted`, `::test_failing_hook_no_commit_returns_output`, `::test_never_pushes` (temp git repo with a remote and a failing hook); `web/src/dialogs/SaveDialog.test.tsx`; `web/e2e/save.spec.ts` |
| AC-26 | `test_release_levels.py::test_raw_excludes_excluded_rejected_ignorable_with_status`, `::test_levels_cumulative_by_id`, `::test_no_ignorable_or_deprecated_in_levels` |
| AC-27 | `test_release_governed.py::test_publish_defaults_to_next_minor_with_changelog`; `web/src/dialogs/PublishDialog.test.tsx::default_version_is_the_next_minor` |
| AC-28 | `test_release_layout.py::test_dataset_layout`, `::test_release_files_and_manifest_checksums` (validated against `manifest.schema.json`) |
| AC-29 | `test_release_rdf.py::test_both_variants_parse_as_turtle`, `::test_sample_element_triples`, `::test_shacl_shapes_validate_fixture_data` (pySHACL) |
| AC-30 | `test_release_markdown.py::test_each_level_has_taxonomy_and_relation_diagrams_and_catalogues`, `::test_evidence_links_resolve_to_unit_ids`, `::test_raw_marks_non_approved`; `test_mermaid_render.py` (marker `mermaid`, runs Mermaid CLI on every diagram) |
| AC-31 | `test_release_governed.py::test_approved_rule_on_proposed_concept_blocks_publish` (offenders listed, governed folder unchanged, raw rebuilt); `web/src/dialogs/PublishDialog.test.tsx::offenders_are_listed` |
| AC-32 | `test_release_determinism.py::test_two_builds_identical_except_built_at[raw,governed]` |
| AC-33 | `test_evaluation.py::test_report_scores_each_answer_key_item` (fixture run), `::test_ingestion_never_opens_answer_key` (open/Path hooks during a fixture ingestion) and `::test_only_evaluation_mentions_answer_key_path` (source scan); live: `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder eval` |
| NFR responsiveness | `test_api_perf.py::test_5000_elements_list_and_action_under_1s`; `web/src/review/filter.perf.test.ts` (filter 5,000 in < 100 ms) |
| NFR local only | `test_api_guards.py::test_binds_localhost_rejects_foreign_host_and_missing_header` |
| Edge cases | `test_extraction_validation.py` (invalid output retried once then reported; unknown unit ID dropped), `test_sources_registry.py::test_empty_and_headingless_files`, `::test_identical_text_separate_ids_same_hash`, `test_workflows_lock.py::test_second_server_refused`, `test_vcs_commit.py::test_refuse_on_conflicts_or_no_git`, `test_release_governed.py::test_deprecated_reference_warns` |

## Risks and mitigations

- **LinkML and its generators lag behind new Python versions** (3.15 is installed locally) → `/add-language python` pins a supported interpreter through uv (likely 3.13). The generated Pydantic code is committed, with a test that regenerating it changes nothing.
- **rdflib's Turtle output may not be byte-stable** → all blank nodes are inlined, so there are no labels. AC-32 tests it. If it still varies, `release` gets its own small sorted Turtle writer, and its output is checked against rdflib by graph isomorphism.
- **The curated fixtures could drift from what the model really returns** → `eval` runs live and reports the gap. Fixtures are re-recorded and re-curated when prompts change, and the request hash makes a stale fixture fail loudly.
- **The live LLM may miss the leash/lead split or the traps** → that is what `eval` is for. Prompt iteration is part of T28, and the scores go in the report, not a gate.
- **Two stacks to build and secure** → an API-first back end, a TypeScript client generated from OpenAPI with a drift check, and the quality gates of both languages from T1/T22.
- **Pre-commit hooks make Save slow** (gitleaks, check-yaml) → the GUI shows a "Saving…" state. Save is explicit, not on every action.
- **`check-added-large-files` (500 KB) may block a large `ontology.ttl`** → the pet ontology is far below that. A larger ontology needs a root ADR to raise the limit; we never bypass the hook.
- **Mermaid CLI needs headless Chromium** → the render test runs under its own pytest marker and in its own CI step.
- **Manual edits to the dataset while the GUI runs** → Save first checks that the dataset tree hash still matches the one loaded. If it doesn't, Save is refused with "reload".
- **Prompt injection from corpus text** → the model gets no tools; its only output is JSON in the output schema. Output is validated against the schema, and every element is reviewed by a person.
- **Stale pricing** → `pricing.yaml` carries the date it was checked. For an unknown model, only tokens are shown.

## Out of scope for this plan

- Everything under the spec's non-goals: LLM abstraction, contradiction/drift/gap detection, diagram-based review (v2), re-ingesting upgraded corpora, non-Markdown input, ordering the queue by confidence, multi-user or server deployment, the four-eyes rule, libraries in `libs/`, changes to the manuals dataset, pushing to GitHub.
- A JSON-LD release (FR-37, `could`) is task T30. It may be dropped without blocking review.
- Git tags for governed versions; release history is the git history of `03_release/01_governed/`.
