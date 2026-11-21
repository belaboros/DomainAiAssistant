# App: ontology-builder

This file adds to the root `CLAUDE.md`; everything there applies here too. Purpose: Builds leveled ontologies from Markdown corpora and user statements, through LLM proposals, human review and governed releases.

## Where things live for this app

| Path | What it holds |
|------|---------------|
| `apps/ontology-builder/docs/architecture/architecture.md` | This app's internal architecture: its components and runtime flows |
| `apps/ontology-builder/docs/architecture/components.json` | This app's components and their allowed dependencies (paths are relative to the repo root) |
| `apps/ontology-builder/docs/architecture/adr/` | Decisions that concern this app only, cited as `ontology-builder/ADR-NNNN` |
| `apps/ontology-builder/docs/specs/` | Specs whose scope is this app only. Ideas always live in the root `docs/ideas/` |
| `apps/ontology-builder/.env.example` | Variables this app adds to, or overrides in, the root `.env.example` |

## Rules specific to working in an app

1. **Never import from another app.** Use libraries from `libs/` (listed in this app's `mayDependOn` in the root `docs/architecture/components.json`) or a shared dataset through its contract.
2. **Shared data goes through contracts.** This app writes only the datasets it owns and reads others only as described in `libs/contracts/<dataset>/`. A new read or write is a change to the root `components.json` (and possibly a root ADR).
3. **Decide where a decision belongs.** If it changes anything another app can see (a contract, libraries, a base env variable, repo tooling), it is a root ADR; otherwise an app ADR here.
4. **Configuration comes from the environment**, loaded by `tools/env/with-env.sh ontology-builder`. Never read `.env` files from code paths of your own, never hard-code secrets.

## Commands

Stack (plan 0002, `ontology-builder/ADR-0002`): a Python back end (FastAPI, LinkML, rdflib, pySHACL, the Anthropic SDK; package `ontology_builder` in `src/`, managed by uv), and a React + TypeScript front end in `web/` (Vite, Vitest, Playwright). Python is set up (root ADR-0020: uv workspace member, Python 3.13; lint, types and boundaries are the repo-wide commands in the root `CLAUDE.md`). TypeScript is added by `/add-language js-ts` (task T22); until then no `.ts` or `.tsx` file may be written.

- Add a back-end dependency: `uv add --package ontology-builder <package>==<version>`
- Regenerate the Pydantic models after a change to `src/ontology_builder/model/schema/ontology_builder.yaml`: `uv run python apps/ontology-builder/tools/gen_model.py` (never edit `model/_generated.py` by hand; a test fails when it drifts). New slots must be optional (FR-15).
- Back-end tests: `uv run --package ontology-builder pytest apps/ontology-builder/tests` (add `-m mermaid` for the Mermaid render test)
- Mermaid render test setup (once): `npm ci --ignore-scripts && npx --no-install puppeteer browsers install chrome-headless-shell` at the repo root. The Mermaid CLI is a root dev tool (`package.json`) until `/add-language js-ts` (T22); CI runs it in its own job.
- Export the OpenAPI schema after an API change (the TypeScript client is generated from it; a drift test fails until you do): `uv run python apps/ontology-builder/tools/export_openapi.py` writes `web/openapi.json`
- Front-end tests: `npm --prefix apps/ontology-builder/web test`; end to end: `npm --prefix apps/ontology-builder/web run e2e`
- Build the GUI: `npm --prefix apps/ontology-builder/web run build`
- Create an ontology (domain admin): `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder create <ontology-name> --scope <scope.yaml> --user <handle>`
- Run the GUI: `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder serve <ontology-name> [--port <port>]`
- Ingest: `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder ingest <ontology-name> <folder> --user <handle> [--yes] [--resume <run-id>]` (shows the cost estimate and asks first)
- Rebuild the raw release without a commit: `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder build <ontology-name>`
- Live evaluation (costs money; not a gate): `tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder eval [--model <model>] [--yes] [--report-dir <dir>]`: ingests the pet manuals into a throw-away ontology (no commit), then scores it against `docs/research/notes/pet-manuals-corpus/answer-key.yaml` and writes `docs/evaluations/YYYY-MM-DD-<model>.md`

Rules for this app:
- Tests never call the live LLM: `ONTOLOGY_BUILDER_LLM_MODE=replay` with the curated fixtures in `tests/fixtures/llm/`.
- Record missing LLM fixtures (live, costs money: show the estimate and ask first): `tools/env/with-env.sh ontology-builder -- uv run pytest -m live apps/ontology-builder/tests/test_record_llm_fixtures.py -s`. Existing fixtures are replayed, never overwritten; curate the new ones by hand (responses only). The pet corpora and `PET_SCOPE` in `tests/conftest.py` are frozen, because the request hashes depend on them.
- Only the `evaluation` component may refer to `docs/research/notes/pet-manuals-corpus/`.
- The app never pushes and never bypasses git hooks.
