# ADR-0008: Let ingestion depend on model

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-6 to FR-8, FR-14; [plan 0002](../../../../../docs/specs/0002-ontology-builder/plan.md) Architecture impact; task T10; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q43

## Context

The plan let `ingestion` depend on `sources`, `extraction`, `store` and `llm`, so its efferent coupling (Ce) was 4, the top of the pass band. The generated import-linter contracts therefore forbid `ingestion → model`.

When the run orchestration was built (task T10), it turned out that `ingestion` has to build and validate model records itself:

- the run record `Run` with its `Estimate` and skipped items (FR-6);
- the `not_ignorable` `Decision` of an on-demand extraction (FR-14, FR-26);
- the ignorable verdict on each `SourceUnit` it writes;
- the element records it caches per batch and reads back on resume (FR-8).

None of the four allowed components owns these classes. `model` does.

## Decision

We will add `model` to the `mayDependOn` of `ingestion` in `apps/ontology-builder/docs/architecture/components.json`. Ingestion imports the record classes and `validate_record` from `ontology_builder.model`, its public entry point. Its Ce becomes 5, which is in the warn band (5–7) of the metrics thresholds, not a failure.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| Re-export the record classes through the public API of `store` | No new edge; Ce stays 4 | It hides a real dependency behind `store`, and `store` would export classes it does not own | The user chose the explicit edge (Q43) |
| Move the run record and the cache into `store` | Ce stays 4 | `store` would learn about LLM runs, batches and resumption, which are ingestion's responsibility; cohesion drops | Wrong owner |

## Consequences

- **Positive:** The dependency is visible in the component diagram and enforced by import-linter like every other edge. `model` is the most stable component (Ce 0), so depending on it points towards stability.
- **Negative / trade-offs:** `ingestion` has Ce 5, and `/arch-metrics` reports it in the warn band.
- **Follow-up:** `components.json` and `architecture.md` of the app are updated, `.importlinter` is regenerated, and the plan's Architecture impact names the edge. No root change: no other app can notice this.
