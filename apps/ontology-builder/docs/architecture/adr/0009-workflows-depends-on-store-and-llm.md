# ADR-0009: Let workflows depend on store and llm

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-1, FR-6, FR-8, FR-27; [plan 0002](../../../../../docs/specs/0002-ontology-builder/plan.md) Approach 1 and 6, Architecture impact; task T18; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q44

## Context

The plan let `workflows` depend on `ingestion`, `governance`, `release` and `vcs`, so its efferent coupling (Ce) was 4, the top of the pass band. The generated import-linter contracts therefore forbid `workflows → store` and `workflows → llm`.

`workflows` is the one use-case layer that `api` and `cli` call (Approach 1), so it is where the use cases are put together. Building it (task T18) showed that it must itself:

- open the dataset of an ontology, a `DatasetStore` with its clock and ID minter, to create, open, save and publish it, and to check its tree hash before a save;
- build the `LlmClient` for an ingestion or an on-demand extraction from the layered environment (`ONTOLOGY_BUILDER_LLM_MODE`, `CLAUDE_MODEL`).

`api` and `cli` cannot do it for workflows: they may not import `store` or `llm` either. None of the four allowed components owns these objects. `store` and `llm` do.

## Decision

We will add `store` and `llm` to the `mayDependOn` of `workflows` in `apps/ontology-builder/docs/architecture/components.json`. Workflows imports `DatasetStore` from `ontology_builder.store` and `make_client` / `LlmSettings` from `ontology_builder.llm`, their public entry points, and passes the objects down to the components that use them. Its Ce becomes 6, which is in the warn band (5–7) of the metrics thresholds, not a failure. The journal of the pending change set is serialised by governance's `ChangeSet`, which owns it, so workflows needs no edge to `model`.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| Factories in lower components (`governance.open_dataset()`, `ingestion.client_from_settings()`) | No new edge; Ce stays 4 | It hides real dependencies behind components that do not own them, like the re-export rejected in ADR-0008 | The user chose the explicit edges (Q44) |
| Let `api` and `cli` build the store and the client and pass them in | `workflows` keeps Ce 4 | Two callers would each need the same two new edges, and the composition would be duplicated | More edges, same coupling |

## Consequences

- **Positive:** The composition root is explicit and enforced by import-linter like every other edge. `store` and `llm` are more stable than `workflows`, so the edges point towards stability.
- **Negative / trade-offs:** `workflows` has Ce 6, and `/arch-metrics` reports it in the warn band.
- **Follow-up:** `components.json` and `architecture.md` of the app are updated, `.importlinter` is regenerated, and the plan's Architecture impact names the edges. No root change: no other app can notice this.
