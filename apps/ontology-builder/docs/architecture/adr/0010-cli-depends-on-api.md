# ADR-0010: Let cli depend on api

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-2, NFR local only; [plan 0002](../../../../../docs/specs/0002-ontology-builder/plan.md) CLI, Architecture impact; task T20; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q46

## Context

The plan gives the app one command, `ontology-builder`, with the sub-commands `create`, `ingest`, `build`, `serve` and `eval`. `serve <name>` opens the ontology and runs the local HTTP server of the review GUI. That server is the `api` component: `create_app` builds the FastAPI app and `serve` runs it on 127.0.0.1 only.

The plan lets `cli` depend only on `workflows` and `evaluation`, so the generated import-linter contracts forbid `cli → api`. `workflows` cannot start the server for the CLI either: `api` already depends on `workflows`, so `workflows → api` would be a cycle.

## Decision

We will add `api` to the `mayDependOn` of `cli` in `apps/ontology-builder/docs/architecture/components.json`. The `serve` command opens the ontology through `workflows` and passes it to `ontology_builder.api.serve`, the public entry point of `api`. The efferent coupling of `cli` becomes 3, inside the pass band (≤ 4).

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| A separate console script in `api` (e.g. `ontology-builder-serve`) | No new edge | Two commands instead of the plan's one; `serve` would not share the CLI's options and environment handling | The user chose the edge (Q46) |
| Let `workflows` start the server | No edge from cli | `workflows → api` closes a cycle with `api → workflows` | Cycles are forbidden (rule 7) |

## Consequences

- **Positive:** One command for every use case, as planned. The edge points from the least stable component (`cli`, nothing depends on it) to a more stable one.
- **Negative / trade-offs:** `cli` now changes when the `serve` signature of `api` changes.
- **Follow-up:** `components.json` and `architecture.md` of the app are updated, `.importlinter` is regenerated, and the plan's Architecture impact names the edge. No root change: no other app can notice this.
