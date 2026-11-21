# ADR-0007: Run pass 1 as two structured-output calls per document, citing units by short alias

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-9 to FR-14, edge cases "LLM returns invalid output" and "LLM cites a source-unit ID that does not exist"; [plan 0002](../../../../../docs/specs/0002-ontology-builder/plan.md) Approach 4; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q38, Q40; supersedes the "Run pass 1 per document" bullet of [ADR-0005](0005-two-pass-llm-extraction-with-curated-fixtures.md) as far as it says "one call" and "units with their IDs"; builds on [ADR-0006](0006-json-structured-outputs-instead-of-a-forced-tool-call.md)

## Context

[ADR-0005](0005-two-pass-llm-extraction-with-curated-fixtures.md) runs extraction pass 1 once per document. In that call, Claude gets the document's source units with their IDs. It returns a verdict per unit (ignorable or not) and candidate statements, terms, concepts, relations, rules and properties. [ADR-0006](0006-json-structured-outputs-instead-of-a-forced-tool-call.md) gets that answer through JSON structured outputs: the API compiles the JSON Schema of the output class into a grammar and guarantees a response that matches it.

Two problems showed up when pass 1 was built and first run live (task T8):

1. **The schema is too large for one grammar.** The API refused the pass 1 schema with HTTP 400 "The compiled grammar is too large". Each failing request costs nothing, so we tested these variants against the API:
   - removing unused `$defs`;
   - making every nullable field required;
   - removing `null` altogether;
   - turning enums into plain strings;
   - flattening the nested limit and cardinality of rules;
   - removing `minItems` and descriptions.

   Every variant failed. A single flat item type that holds the fields of all six candidate types hit a second limit: at most 16 nullable or union-typed fields. Every candidate list compiles on its own, and so does every set of up to five lists in the planned order. The schema fails as soon as rules join the verdicts, statements, terms, concepts and relations. Rules and properties together also compile.
2. **Full IDs are easy to miscopy.** Unit IDs are ULIDs, and IDs minted in the same run share their timestamp part and count up in the random part. Two units of one document can therefore differ only in their last characters (`…MPJW`, `…MPJX`). If the model miscopies one character, the evidence points at a neighbouring unit. That ID is still valid, so no check can catch the mistake.

## Decision

We will run pass 1 as **two structured-output calls per document**. Each call cites units by a short alias.

- **Aliases.** Each prompt shows each unit as `[U1]`, `[U2]`, … in document order. The output classes take these aliases (pattern `^U[1-9][0-9]*$`) wherever they cite a unit: `Candidate.evidence`, `UnitVerdict.unit`, `CandidateMention.unit` and, for pass 2, `Sense.mentions`. `extraction` maps each alias back to its `su_` ID before it builds any record. An alias that was not in the prompt counts as an unknown unit: the item is dropped and reported (FR-10). Records and the dataset only ever hold real IDs.
- **Call A** (output class `ConceptsOutput`) returns the unit verdicts, statements, terms, concepts and relations.
- **Call B** (output class `RulesOutput`) gets the same system prompt and units. It also gets the candidates of call A as `kind key: label` lines and the list of units call A marked ignorable. It returns only rules and properties, which refer to call A's candidates by key.
- **Retries and failures.** Each call gets its own single retry: for invalid items, or for an answer that cannot be used at all (ADR-0005).
  - If call A still gives no usable answer, the document is reported in the run record and call B is not made.
  - If call B still gives no usable answer, call A's candidates are kept and the failure is reported.
  - If every unit of a document is ignorable, call B is skipped.
- **Merging.** The answers of the two calls are merged before the cross-reference checks. A key that call B reuses from call A is skipped and reported.
- **The merged output.** `ExtractionOutput` stays in the schema as the merged answer of one document. It is never sent to the API.
- **Cost estimate.** It counts both calls of every document (`pass1_requests`). Call B is counted without call A's candidates, which are not known yet.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| One call with the JSON Schema in the prompt text and no grammar | One call per document; cheapest (recording ~$2.3) | The answer's shape is no longer guaranteed, so retries and dropped items become more likely; it gives up most of what ADR-0006 bought | The user chose to keep schema-constrained output (Q40) |
| One call with a smaller schema (pruned defs, required nullable fields, no null, enums as strings, flat rules, one flat item type) | Keeps one call | Every variant tested was still refused by the API (grammar too large, or more than 16 union fields) | Does not work |
| A call per element type (six or seven calls per document) | Smallest grammars | About three times the calls and input tokens; more context lost between calls | Two calls are enough to fit the limit |
| Full `su_` IDs in the prompt, as ADR-0005 planned | No alias mapping | A one-character copy error silently cites the neighbouring unit | The user chose aliases (Q38) |

## Consequences

- **Positive:** Both answers stay schema-constrained. Units can no longer be confused by a miscopied ID. Prompts are shorter, because an alias is 2–3 characters instead of 29. Call B sees call A's concepts and relations by key, so rules and properties attach to them without guessing.
- **Negative / trade-offs:**
  - There are twice as many calls per document. Recording the pet fixtures was estimated at about $3.18 instead of $2.29 (Q41).
  - Call B sees only the keys and labels of call A's candidates, not their full records.
  - A rule that needs a concept call A missed cannot reference it, so it is dropped as dangling, or the model folds the concept into the rule's text.
  - The fixtures hold two recordings per document.
- **Follow-up:**
  - The LinkML schema has `ConceptsOutput` and `RulesOutput` and alias patterns (done in T8).
  - The plan's Approach 4 and task T8 are updated.
  - The app `architecture.md` ingestion flow names both calls.
  - The ingestion estimate (T10) uses `pass1_requests`.
  - Pass 2 (T9) cites units by alias too.
  - No change to `components.json`: the components and their dependencies are unchanged.
