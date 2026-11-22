# ADR-0012: Let a run extend concepts and terms already in the ontology

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-22
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-11, FR-24, FR-26; [plan 0002](../../../../../docs/specs/0002-ontology-builder/plan.md) Approach 5; tasks T36, T37; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q61, Q62; [ADR-0005](0005-two-pass-llm-extraction-with-curated-fixtures.md)

## Context

Pass 2 runs once per ingestion and may merge a run's new concept into a concept already in the ontology (e.g. the building manual's "dog" into the "dog" of the dog manual). The code followed the rule "a concept already in the ontology is never changed by a run": the new concept was left out, and its parents and evidence were dropped without a trace. In `data/ontology-pets-and-house-rules/` this lost "dog → pet" and "cat → pet" (stated in the building manual: "Every pet (dog or cat) …") and all the building manual's evidence for dog and cat, so `level-1.md` had a taxonomy without edges. Terms had the same gap: a run's term with the label of an existing term became a second term record.

## Decision

We will let a run **extend** an element that is already in the ontology:

- a new concept merged into an existing one adds its evidence and parents to it;
- a new term whose label matches an existing term (ignoring case) adds its mentions and evidence to it, and is left out.

`extraction` returns these existing elements, extended, next to the run's new elements; it changes no status. `ingestion` writes them in the run's one commit with an `extend` decision each (user and role of the run, old and new values). An extended **approved** element goes back to `included` and keeps its approved snapshot, as an edit does (FR-24), so a domain admin re-approves it and the governed release keeps the approved version until then. The label, definition and level of an existing element are never changed by a run.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| Keep the new concept as a separate proposal | Existing records never change | Duplicates for every concept that two manuals share; the reviewer merges them by hand | Q61 |
| Keep the rule, report the loss in the run's skipped items | Smallest change | The links and evidence still have to be re-created by hand | Q61 |

## Consequences

- **Positive:** Is-a links and evidence that a later corpus states are kept; one term record per label across runs.
- **Negative / trade-offs:** A run can send approved elements back to review. Ingesting a corpus after review means re-approving the concepts it adds to.
- **Follow-up:** `DecisionAction` gets `extend`; the pass 2 cache stores the extended elements; the pets ontology is re-created and re-ingested (T37).
