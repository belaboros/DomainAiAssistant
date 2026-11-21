# ADR-0002: Build an API-first Python back end with a React + TypeScript front end

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q14, Q29 to Q34; [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-2, FR-3, FR-16 to FR-20, NFR "Local only" and "Responsiveness"; [GUI prototypes](https://claude.ai/artifact/Mjnmp1uWZACjGzufk6wi2r)

## Context

The review GUI runs locally for one user at a time (Q14). It must show evidence before the LLM's proposal, filter and search 5,000 elements in under a second, run bulk actions, and enforce roles even when someone calls the back end directly (AC-3). The ontology tooling (LinkML, rdflib, pySHACL, the Anthropic SDK) is Python-native.

The user compared three clickable prototypes: htmx, React/TS and NiceGUI (Q29). For v2, the user wants interactive taxonomy and ontology diagrams that offer the same review actions as the list (Q32). In every option such a diagram is a JavaScript component (Cytoscape.js + elkjs). The difference is how naturally the list and the diagram share one selection, one filter set and one set of actions.

## Decision

We will:
- **Write the back end in Python, API-first.** Every rule (roles, transitions, evidence, releases) lives in Python components behind one use-case layer (`workflows`). The FastAPI `api` (JSON, localhost only), the `cli` and the `evaluation` command are thin callers of it.
- **Write the GUI as a React + TypeScript single-page app** (Vite, in `apps/ontology-builder/web/`). Its TypeScript client is generated from the API's OpenAPI schema, with a drift check, and the front end talks to the back end only over HTTP. In v2 the diagram becomes a second view on the same client store and actions.
- **Filter and search in the browser,** on a compact element index the API returns, so it stays instant at 5,000 elements. The server checks role and transition for every action again.
- **Guard the local server:** it binds to `127.0.0.1`, checks the Host header, requires a custom header on writes, and allows one process per dataset.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| FastAPI + Jinja2 + htmx | One language and one quality gate; GUI tests in pytest | Keeping the list and a v2 diagram in sync needs growing glue code between server HTML and a JS canvas | The v2 diagram goal (Q32–Q34) |
| NiceGUI (or Streamlit) | Quickest start; Python only | Least control over layout and markup; no HTTP API for the role checks; the diagram needs a custom Vue component; Streamlit re-runs the whole script on every click | Control and testability |
| React SPA with a Node back end | One language | Loses the Python ontology tooling | The tooling decides the back end |

## Consequences

- **Positive:** the core is testable without a browser, and AC-3 holds by construction. The GUI is ready for the v2 diagram, and the CLI and the evaluation reuse the same use cases.
- **Negative / trade-offs:** two languages, so two quality gates (`/add-language python` and `js-ts`), two dependency audits and a front-end build step. It needs the most front-end code of the three options.
- **Follow-up:** the `api`, `workflows`, `cli` and `web` components in `components.json`; `/add-language python` (T1) and `/add-language js-ts` (T22); the commands in `apps/ontology-builder/CLAUDE.md`; `ONTOLOGY_BUILDER_PORT` in `.env.example`.
