# Tasks 0002 · OntologyBuilder

- **Plan:** [plan.md](plan.md)

Each task is small enough for one focused session, leaves the repo in a working state, and names how it is checked. Every task also runs the full test suite and the quality gate (lint, complexity, boundary check) of the languages it touches. Tasks that add a component update `apps/ontology-builder/docs/architecture/components.json` and `architecture.md` if anything differs from the plan (rule 5). All tasks touch the app `ontology-builder` unless marked otherwise; `[component]` names the app component.

Tick a box only once its check passes.

### Foundations
- [x] T1 · `/add-language python`: uv workspace at the repo root with `apps/ontology-builder` as a member, a pinned interpreter that LinkML supports, ruff (C901 ≤ 10, PLR rules), mypy strict, import-linter contracts generated from both `components.json` levels, the metrics collector, a pytest pre-commit hook, CI, pip-audit, bandit/ruff S, and Dependabot. Root ADR written by the skill. — covers: none (prerequisite) — check: the skill's step 8 proof (CC > 15, an in-app boundary break, an app → app import and a cycle each fail the gate)
- [x] T2 · [system] Write the shared contract `libs/contracts/ontology/`: README with the layout of `00_sources/` and `03_release/`, IRIs, the `dai:` vocabulary, the guarantees (one writer; atomic swap; deterministic files; IDs never reused or derived from text or position; governed = approved + deprecated only), versioning, `CHANGELOG.md` 0.1.0, `manifest.schema.json`, `source-unit.schema.json` and `vocab.ttl`. Make `libs/contracts/ontology-pets-and-house-rules/README.md` thin and pin `ontology` 0.1.0. Add a line about contract families to `libs/contracts/README.md`. — covers: AC-28 (schema), FR-30 — check: `pre-commit run check-json --all-files`, `tools/monorepo/system-map.sh --check`, and `test_contract_schemas.py` (the JSON Schemas are valid Draft 2020-12; `vocab.ttl` parses)

### Back end
- [x] T3 · [model] LinkML schema for the scope record, corpus, document, source unit, the six element types, mentions, evidence, decision and run, plus the LLM output classes. Generate the Pydantic models (committed, with a regeneration drift test) and the JSON Schema for the LLM tool. Validate every record before writing. — covers: AC-9 (validation half), AC-12, AC-14 — check: `pytest apps/ontology-builder/tests/test_model_validation.py tests/test_model_extensibility.py` — note: the "both releases still build" half of AC-14 is added to `test_model_extensibility.py` in T16; the fixture half of AC-12 is re-checked on the curated pet fixtures in T8
- [x] T4 · [store] Read and write the dataset layout: deterministic YAML (sorted keys, fixed style), one file per element, the decisions JSONL appender, run records, and an atomic swap through `data/.<dataset>.staging/` and `.previous/` with a rollback. Add the `.gitignore` lines from the plan. Inject the clock and the ID minter. — covers: AC-28 (layout) — check: `pytest …/test_release_layout.py::test_dataset_layout tests/test_store_atomic.py`
- [x] T5 · [governance] Create an ontology (domain admin only): name check (kebab-case, not already present), the layout, a validated scope record and its default base IRI. Refuse ingestion while the scope record is missing or empty. — covers: AC-1 — check: `pytest …/test_ontology_create.py`
- [x] T6 · [sources] Split Markdown into block units with markdown-it-py: heading path, index in the section, NFC + whitespace normalisation, SHA-256, `doc_` and `su_` ULIDs. Number corpus folders `00`–`89`. Write the registry. Handle empty files, files without headings and identical blocks. — covers: AC-4, AC-5 — check: `pytest …/test_sources_registry.py`
- [x] T7 · [llm] Client port with `live`, `record` and `replay` modes, a request-hash fixture store, JSON structured output (`output_config.format`, ADR-0006), a token estimate (count-tokens API or a heuristic) and `pricing.yaml`, checked against Anthropic's current price list on the day. No key → a clear error before any change. — covers: AC-6 (estimate half) — check: `pytest …/test_llm_client.py`
- [x] T8 · [extraction] Pass 1 per document, as two calls (Q40, ontology-builder/ADR-0007: A = verdicts, statements, terms, concepts, relations; B = rules and properties referring to A's keys): the prompt (scope record, level rubric, units by alias, Q38), the ignorable verdict per unit with its category, candidates with evidence, levels and reasons. Validate the output, retry once, report and drop invalid items or unknown unit IDs. Record and then curate the fixtures for the three pet manuals (a live call: show the estimate and ask the user first). — covers: AC-9, AC-12, AC-13 (fixture half) — check: `pytest …/test_extraction_pets.py tests/test_extraction_ignorable.py tests/test_extraction_validation.py`
- [x] T9 · [extraction] Pass 2, term resolution: synonym groups and sense splits across documents and against existing concepts, written as terms with mentions and scope notes. Curated fixture for leash/lead. — covers: AC-11 (fixture) — check: `pytest …/test_extraction_terms.py`
- [x] T10 · [ingestion] Run orchestration:
  - refuse a folder that was already ingested;
  - estimate, then confirm;
  - cache responses per batch in the work folder;
  - keep the run record;
  - write everything in one atomic swap at the end;
  - resume a run with `--resume`;
  - run on-demand extraction for a unit marked not ignorable.

  — covers: AC-6, AC-7, AC-8, AC-13 (on-demand) — check: `pytest …/test_ingestion_estimate.py tests/test_ingestion_refusals.py tests/test_ingestion_atomic.py tests/test_extraction_ignorable.py::test_not_ignorable_runs_extraction_after_confirm`
- [x] T11 · [governance] The status machine of the plan's table, role checks, decision records, bulk actions with per-ID results, deprecation with a replacement, the approved snapshot, and no delete path anywhere. — covers: AC-3 (service level), AC-17, AC-22, AC-24 (records) — check: `pytest …/test_governance_transitions.py tests/test_governance_bulk.py tests/test_governance_deprecate.py`
- [x] T12 · [governance] Review actions: correct a field, override the level, merge as a synonym (relations follow, approved targets go back to included, merging an approved concept needs an admin), split senses, reassign a mention. Each action writes a decision with its old and new values. — covers: AC-16 — check: `pytest …/test_governance_actions.py`
- [x] T13 · [governance] User statements (a unit in `90_user_statements/`, revisions, the same ID) and authored elements (evidence required; status `included`). — covers: AC-20, AC-21 — check: `pytest …/test_user_statements.py tests/test_authoring.py`
- [x] T14 · [release] Turtle builder: the OWL 2 + SKOS + SHACL mapping of the plan, inlined blank nodes, `dai:` annotations, the status in raw only, and deprecation with its replacement. Add a fixture user statement "a resident may keep at most 2 pets" for the cardinality case. — covers: AC-10, AC-24 (Turtle), AC-29 — check: `pytest …/test_release_rdf.py`
- [x] T15 · [release] `level-N.md` builder: Jinja2 templates, taxonomy and concept-relation Mermaid diagrams split above 40 nodes, catalogues, the evidence appendix with anchors, and raw badges with a dashed class. Add `@mermaid-js/mermaid-cli` for the render test (as a root dev tool until T22 sets up the front-end package). — covers: AC-26 (levels), AC-30 — check: `pytest …/test_release_markdown.py` and `pytest -m mermaid …/test_mermaid_render.py`
- [x] T16 · [release] Raw and governed builds:
  - what goes into each variant;
  - governed uses the approved snapshots;
  - the FR-35 dependency check, with a warning for references to deprecated elements;
  - the next-minor default version;
  - the change log (added, changed, deprecated, removed) by comparing with the previous governed `ontology.ttl`;
  - the manifest with checksums;
  - an atomic folder swap;
  - byte-identical output.

  — covers: AC-23, AC-26, AC-27, AC-28, AC-31, AC-32 — check: `pytest …/test_release_governed.py tests/test_release_levels.py tests/test_release_layout.py tests/test_release_determinism.py`
- [x] T17 · [vcs] `git add` + `git commit -- data/ontology-<name>/` with hooks: return the hook output on failure, refuse on conflicts, a missing git or a detached state, and offer no push code path. Test helper: a temp repo with a bare remote and a failing pre-commit hook. — covers: AC-25 (back end) — check: `pytest …/test_vcs_commit.py`
- [x] T18 · [workflows] Use cases:
  - open an ontology, taking the process lock in the work folder;
  - the pending change set with its journal;
  - save: check the tree hash, validate, write, rebuild raw, swap, commit; roll back on failure;
  - publish, ingest and create.

  — covers: AC-8 (end to end), AC-25, edge cases — check: `pytest …/test_workflows_save.py tests/test_workflows_lock.py` — note: workflows also depends on store and llm (Q44, ontology-builder/ADR-0009); its public API returns IDs and outcome records, not model classes
- [x] T19 · [api] FastAPI app:
  - session sign-in with the email warning;
  - role checks on every route, returning 403;
  - the element index, detail and action routes;
  - authoring, ingestion, save and publish routes;
  - the guards: localhost bind, Host check, the custom header, a read-only second session;
  - serves `web/dist`, and exports the OpenAPI schema to `web/openapi.json` with a drift test.

  — covers: AC-2, AC-3, AC-18 (server), NFR responsiveness, NFR local only — check: `pytest …/test_api_session.py tests/test_api_roles.py tests/test_api_elements.py tests/test_api_perf.py tests/test_api_guards.py`
- [x] T20 · [cli] `ontology-builder create | ingest | build | serve` with Typer (`eval` is added with the evaluation component in T21). `ingest` shows the estimate and asks unless `--yes`. Add the run commands to `apps/ontology-builder/CLAUDE.md` and `README.md`. — covers: AC-6 (CLI) — check: `pytest …/test_cli.py` — note: `serve` needs `cli → api` (Q46, ontology-builder/ADR-0010)
- [x] T21 · [evaluation] Write `docs/research/notes/pet-manuals-corpus/answer-key.yaml` (system: docs) from the README, plus the scoring, the dated report, the isolation tests and the `ontology-builder eval` command. Scoring is tested on a replayed run. — covers: AC-33, AC-11/AC-13 (eval scoring) — check: `pytest …/test_evaluation.py` — note: the throw-away ontology is a `workflows` use case (`create_scratch`: no lock, no git, no commit); the manuals are ingested as three corpora, so the replayed run scores the leash/lead synonym as missed (single-manual pass 2 has no fixture) and the test also scores it on the curated three-manual pass 2

### Front end
- [x] T22 · `/add-language js-ts`: TypeScript strict, ESLint complexity ≤ 10/15, dependency-cruiser rules from `components.json`, Vitest, Playwright, npm audit, eslint-plugin-security and Dependabot, with `apps/ontology-builder/web` as the workspace. Root ADR written by the skill. Ask npm vs pnpm there. — covers: none (prerequisite) — check: the skill's step 8 proof — note: npm workspaces (Q47), root ADR-0021; TypeScript 6.0.3, because typescript-eslint does not support TypeScript 7 yet
- [x] T23 · [web] Vite + React app shell, a TypeScript client generated from `openapi.json` (drift check), and the sign-in screen with the handle hint and the email warning. — covers: AC-2 (GUI) — check: `npm --prefix apps/ontology-builder/web test -- SignIn` — note: types by openapi-typescript, calls by openapi-fetch (Q48, ontology-builder/ADR-0011); the GUI warns before signing in with an email-like name, and shows the server's warning too
- [x] T24 · [web] Element list:
  - filters by type, status, level, corpus and document, and full-text search over the client index;
  - status badges with a colour and a text label plus icon;
  - level badges;
  - multi-select with a bulk bar (include, exclude, set level; approve and reject for an admin only).

  — covers: AC-17, AC-18, AC-19 — check: `npm --prefix apps/ontology-builder/web test -- filter StatusBadge BulkBar` — note: the session response names the open ontology, and the index entries are typed in OpenAPI; the client filter test repeats the server's AC-18 cases on part of the pet fixture's index (`web/src/review/fixtures/pet-index.json`, with the server's answers; kept in step by `test_api_elements.py::test_gui_pet_index_fixture_matches`, because the whole index is over the 500 KB file limit); bulk actions act on the selected elements that are shown; also `filter.perf.test.ts` (NFR responsiveness)
- [x] T25 · [web] Element detail:
  - evidence passages first, then the LLM proposal (type, label, level, reason);
  - action buttons for every FR-17 action, with reason dialogs;
  - admin-only actions disabled for users, with a refusal message;
  - the decision history;
  - keyboard shortcuts (j/k, x, i, e, 1–3, a).

  — covers: AC-15, AC-16 (GUI), AC-3 (GUI) — check: `npm --prefix apps/ontology-builder/web test -- ElementDetail Actions` — note: the detail response is typed in OpenAPI (`ElementDetailOut`, checked by `test_api_elements.py::test_element_detail_is_typed_in_openapi`); one dialog spec per action (`actionDialogs.ts`) sends the payload keys the governance handlers read; merge offers concepts only, split and reassign show for terms only; `a` as a user shows the refusal and calls nothing; the list label opens an element, and j/k step through the shown elements (`ReviewScreen.test.tsx`)
- [x] T26 · [web] Dialogs:
  - new and edit user statement;
  - author an element, with an evidence picker;
  - ingest a folder, showing the estimate before confirming, then the run progress;
  - mark a passage not ignorable, with the cost confirmation;
  - Save, showing the commit SHA or the hook output;
  - Publish (admin), with the version, the change log or the offenders.

  — covers: AC-6 (GUI), AC-13 (GUI), AC-20/AC-21 (GUI), AC-25 (GUI), AC-27/AC-31 (GUI) — check: `npm --prefix apps/ontology-builder/web test -- dialogs` — note: the dialogs open from a work bar above the review panes (`web/src/dialogs/`, one test file per dialog); the evidence picker, statement editing and the not-ignorable dialog choose from the new `GET …/units` (typed `UnitOut`, Q49; `test_api_elements.py::test_units_*`), and run records are typed `RunOut`; the run is synchronous, so the ingest dialog shows a running state and then the run record (Q50); the work bar is disabled for a read-only session and Publish is disabled for a user, with the reason; review shortcuts are ignored while a dialog is open
- [x] T27 · [web] Playwright end-to-end tests against `ontology-builder serve` on a fixture dataset in a temp git repo: sign in → filter → bulk level → save (one commit, nothing pushed) → failing hook shown → admin publish blocked by FR-35 → fix → publish 1.0.0. — covers: AC-25 (end to end), AC-15, AC-19 — check: `npm --prefix apps/ontology-builder/web run e2e` — note: `tools/e2e_server.py` seeds the fixture (three proposed concepts, a statement, an approved rule on the proposed concept "lead") in a temporary git repository with a bare remote, and serves it as `ontology-builder serve` does; the pre-commit hook fails while the git config `e2e.hookfails` is `true` (so the test needs no file writes), and the server removes the folder on SIGTERM; `npm run e2e` builds the GUI first; CI's js-ts job installs uv, the Python workspace and Chromium for it

### With the user (live LLM, costs money; ask before each run)
- [ ] T28 · Run `ontology-builder eval` live, review the report with the user, and iterate the prompts where the leash/lead split or the traps fail. Re-curate the fixtures if the prompts change. — covers: AC-11/AC-13 (eval), AC-33 (live) — check: `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder eval` writes `apps/ontology-builder/docs/evaluations/2026-…-<model>.md`
- [ ] T29 · [system: dataset] Create `data/ontology-pets-and-house-rules/` with the user as domain admin: write the scope record together, ingest the three manuals live (after the estimate is confirmed), and commit. The first review and publishing are up to the user. — covers: spec goal "starting with data/ontology-pets-and-house-rules/" — check: `tools/monorepo/system-map.sh --check`; `ontology-builder build pets-and-house-rules` succeeds; `git log -1 -- data/ontology-pets-and-house-rules/`

### Optional and closing
- [ ] T30 · [release] JSON-LD twin of `ontology.ttl` in both releases, deterministic, listed in the manifest (FR-37, `could`). — covers: FR-37 — check: `pytest …/test_release_jsonld.py`
- [ ] T31 · [system: docs]
  - Root `architecture.md`: §1 purpose, §2 context (users, the Claude API, git), §6 the flow (ontology-builder publishes → future readers), §7 cross-cutting rows for errors, logging and security.
  - Refresh the app `architecture.md` diagrams and flows to match the code.
  - Run `/arch-metrics` for the system and the app.
  - Update the indexes.

  — covers: rule 5, rule 11 — check: `tools/monorepo/system-map.sh --check`; `/arch-metrics` result `pass`
