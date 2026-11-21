# ADR-0006: Get the LLM's structured output through JSON structured outputs, not a forced tool call

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-9 to FR-14, edge case "LLM returns invalid output"; [plan 0002](../../../../../docs/specs/0002-ontology-builder/plan.md) § LLM; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q37; supersedes the "Force structured output" bullet of [ADR-0005](0005-two-pass-llm-extraction-with-curated-fixtures.md)

## Context

[ADR-0005](0005-two-pass-llm-extraction-with-curated-fixtures.md) decided that each extraction pass gets its answer as a single *forced* tool call (`tool_choice` of type `tool`), whose input schema is generated from the LinkML output classes. When the `llm` component was implemented (task T7), it turned out that the repo's default model, `claude-opus-5-5` (`CLAUDE_MODEL` in the root `.env.example`), rejects a forced `tool_choice` (`any` or `tool`) with HTTP 400. Claude Sonnet 5.5 and Claude Fable 5.1 and 5.2 reject it too. Only older models still accept it. The app must work with the configured default model, and changing the model must stay a configuration change (ADR-0005).

The Messages API offers another way to get schema-valid JSON: **structured outputs**, `output_config.format = {type: "json_schema", schema: …}`. The API then guarantees that the response text is JSON that matches the schema. It supports objects, arrays, enums, `anyOf`, `$ref`/`$defs` and required fields, but not numeric bounds (`minimum`, `maximum`), string bounds or patterns, array-length bounds (`minItems`), or `additionalProperties` other than `false`.

## Decision

We will:
- **Ask for JSON through `output_config.format`** with type `json_schema`, on every extraction call. No tools are sent and `tool_choice` is never forced.
- **Keep the schema single-sourced.** The schema is still the JSON Schema of the LinkML output classes (`model.tool_input_schema`). Before sending, the `llm` component removes the keywords the API does not support and sets `additionalProperties: false` on every object. The removed constraints (ID patterns, minimum counts, numeric bounds) are still enforced afterwards by the Pydantic validation in `extraction`, with the retry-once-then-report rule of ADR-0005 unchanged.
- **Hash the request as sent.** The replay fixture key is the SHA-256 of the canonical request, including the `output_config` schema, so a schema change makes a stale fixture fail loudly.

Everything else in ADR-0005 stays as decided.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| Strict tool (`strict: true`) with `tool_choice: auto` | Closest to ADR-0005's wording; tool input schema-valid | A tool call is not guaranteed; needs a "no call made" retry path | More code for a weaker guarantee |
| Keep the forced tool call and require a model that accepts it (e.g. `claude-opus-5`) | No change to the design | Excludes the default and newest models; model choice no longer a pure configuration change | Contradicts ADR-0005's "changing the model is a configuration change" |
| Free-text JSON with only client-side validation | Works everywhere | More invalid output, more retries | Structured outputs give the guarantee for free |

## Consequences

- **Positive:** works on every current model, including the default `claude-opus-5-5`. The response is always parseable JSON, so retries are only needed for constraints the API cannot express.
- **Negative / trade-offs:** some schema constraints are checked only client-side, so the model can still return, for example, an evidence ID with the wrong format; `extraction` drops and reports such items as before. A new schema has a one-time compilation latency on the API side.
- **Follow-up:** plan 0002 § LLM updated; the `llm` component (T7) implements it. No change to `components.json`, `architecture.md` dependencies, contracts or `.env.example`.
