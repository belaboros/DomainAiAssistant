# ADR-0005: Extract in two LLM passes behind a replaceable client, tested on curated fixtures

- **Status:** accepted; its "Force structured output" bullet is superseded by [ADR-0006](0006-json-structured-outputs-instead-of-a-forced-tool-call.md); its "Run pass 1 per document" bullet (one call, units with their IDs) is superseded by [ADR-0007](0007-pass-1-as-two-structured-output-calls-per-document.md)
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-6, FR-9 to FR-14, FR-38, NFR "Determinism", "Cost"; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q16, Q17, Q19

## Context

The LLM proposes the building blocks, their levels, ignorable passages, synonyms and senses. The synonym "leash"/"lead" spans two manuals, and the homonym "lead" (rope vs. the owner's role) spans two documents. So some judgements need the whole corpus, while evidence needs unit-level precision. Automated tests must not need a network or an API key (Q17), and LLM output varies between runs. Every run needs a cost estimate and a confirmation first (Q19).

## Decision

We will:
- **Run pass 1 per document** (`extraction`). Input: the scope record, the level rubric of the idea, and the document's units with their IDs. Output: an ignorable verdict for each unit (with category and reason) and, for the other units, the candidate elements with evidence IDs, a level and a reason.
- **Run pass 2 once per ingestion** (`extraction`). Input: every candidate term with its mentions and contexts, plus the concepts already in the ontology. Output: synonym groups and sense splits, written as terms with mentions and scope notes.
- **Force structured output** through a single tool call whose input schema is generated from the LinkML output classes. Output is validated; an invalid item is retried once, then reported in the run record and dropped. Items citing unknown unit IDs are dropped and reported.
- **Put the model behind a client port** (`llm`) with three modes: `live`, `record` and `replay` (`ONTOLOGY_BUILDER_LLM_MODE`). Replay looks up fixtures by the SHA-256 of the canonical request, so a changed prompt fails loudly instead of replaying stale data. The model comes from `CLAUDE_MODEL`.
- **Curate the fixtures by hand.** Fixtures for the pet manuals are recorded once live, then edited to the answer the pipeline must handle. They test our code, not the model. The model is judged by the live `evaluation` command against the answer key, which only `evaluation` reads.
- **Estimate cost before every run.** Tokens are counted with the API's count-tokens endpoint, or estimated without a key; the price comes from `pricing.yaml`, which carries the date it was checked. The LLM is called only after confirmation, and the run record stores the model, the tokens actually used and the times.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| One pass over the whole corpus | Fewer calls; sees everything at once | Too large a context for real manuals; weaker evidence IDs | Precision and scale |
| One pass per unit | Smallest prompts | No document context; many calls; no cross-document synonyms | Cost and quality |
| Plain recorded fixtures (not curated) | No hand work | Tests would assert whatever the model returned once | Tests must pin required behaviour |
| A live LLM run as a CI gate | Tests the real model | Costs money, flaky, needs a secret in CI | Q17 |

## Consequences

- **Positive:** tests are deterministic and free. Prompts stay small, and the leash/lead case is handled where it can be seen. Changing the model is a configuration change, judged by `eval`.
- **Negative / trade-offs:** curated fixtures must be re-curated when prompts change. Pass 2 grows with the number of terms and may need batching for large corpora.
- **Follow-up:** the `llm`, `extraction`, `ingestion` and `evaluation` components; `ONTOLOGY_BUILDER_LLM_MODE` in `.env.example`; T7 to T10, T21, T28.
