# ADR-0011: Generate the GUI's API types with openapi-typescript and call the API through openapi-fetch

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-2; [plan 0002](../../../../../docs/specs/0002-ontology-builder/plan.md) HTTP API, Risks ("a TypeScript client generated from OpenAPI with a drift check"); task T23; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q48; [ontology-builder/ADR-0002](0002-api-first-python-back-end-with-react-typescript-front-end.md); root ADR-0021 (JS/TS quality gate)

## Context

The review GUI (`web/`, React + TypeScript) talks to the Python back end only over HTTP. The plan makes the API's OpenAPI schema the contract between the two: the back end exports it to `web/openapi.json` (a Python drift test keeps that file current), and the front end uses a TypeScript client generated from it, with a drift check of its own. When the API changes and nobody regenerates, the drift check fails, so the GUI cannot silently call routes or send bodies the server no longer accepts.

The plan does not name a generator. Whatever we pick has to:

- run under the repo's TypeScript 6.0.3 toolchain (root ADR-0021);
- produce code that is committed and passes the repo-wide JS/TS gate (Prettier, ESLint strict type-checked, CC ≤ 15, no dependency cycles), or else be excluded from that gate;
- pass `npm audit --audit-level=high`;
- generate the same text every time, so a drift test can compare it.

## Decision

We will generate **only the types** of the API with **openapi-typescript** (7.13.0, a dev dependency), and make the calls with **openapi-fetch** (0.17.0, a runtime dependency), a small typed `fetch` wrapper driven by those types.

- `web/scripts/gen-api.ts` renders `web/src/api/schema.gen.ts` from `web/openapi.json` and formats it with the repo's Prettier settings. `npm run gen:api` writes it.
- `web/src/api/schema.drift.test.ts` renders the same text and fails while the committed file differs.
- All API calls go through `web/src/api/index.ts`. It sends same-origin cookies and the write header `X-Ontology-Builder: 1` that the server's guard requires, and it turns a refusal into an `ApiError` that carries the server's `detail` message and the HTTP status.
- The generated file is committed and checked by the gate like hand-written code. Nothing is excluded from lint, formatting or the boundary check.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| openapi-typescript + openapi-fetch (chosen) | One generated file of types only, which passes the gate unchanged; the runtime is a small maintained npm package, not vendored code | openapi-typescript declares a peer of TypeScript 5, so npm installs its own nested TypeScript 5.9.3 for code generation (the repo stays on 6.0.3) | — |
| @hey-api/openapi-ts 0.99.0 (types + SDK + bundled fetch client) | Generates one typed function per route; supports TypeScript 6 | Vendors about 2,000 lines of client runtime into `src/`, which fail the gate: strict ESLint errors, a function with CC 39, and a type-only import cycle between its own files. Using it means excluding the folder from ESLint, Prettier and dependency-cruiser. It also pins js-yaml 4.2.0, which has a high-severity advisory, so `npm audit` fails without an `overrides` entry | Weakens the gate for a large block of code we did not write |
| Hand-written types and fetch calls | No generator dependency | Nothing ties them to `openapi.json`; drift is found only at run time | The plan asks for a generated client with a drift check |

## Consequences

- **Positive:** the contract between GUI and API is checked at compile time and by a drift test; the gate covers every committed file; no vendored client code to review or keep up to date; no npm overrides.
- **Negative / trade-offs:** calls are written as `api.POST("/api/session", { body })` rather than one named function per route, so `src/api/index.ts` wraps the ones the screens use. A second TypeScript (5.9.3) sits in `node_modules` for code generation only.
- **Follow-up:**
  - After an API change: `uv run python apps/ontology-builder/tools/export_openapi.py`, then `npm run gen:api --workspace apps/ontology-builder/web` (added to `apps/ontology-builder/CLAUDE.md`).
  - When an openapi-typescript release supports TypeScript 6, upgrade it to drop the nested TypeScript 5.
  - `architecture.md`: the `web` component reaches `api` through these generated types (no new component or dependency; `components.json` is unchanged).
