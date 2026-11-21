# ADR-0001: Keep LinkML-defined YAML records as the only source; generate RDF and Markdown releases one way

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q2, Q3, Q6; [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-15, FR-28 to FR-36; [research report, addenda](../../../../../docs/research/reports/Ontology%20formats%20and%20building%20process.md)

## Context

The ontology's working state includes more than a standard ontology file holds. It has:
- candidates in six statuses;
- evidence links to source units;
- levels with reasons;
- approved snapshots;
- review decisions.

All of this must diff well in git, be easy for an LLM to produce, and allow new properties later without breaking old data (FR-15). Readers (the assistant, the validator, people) need standard RDF (OWL 2 + SKOS + SHACL) and readable Markdown. In OWL, evidence, level and status would all be axiom annotations, which are verbose, unstable in diffs and awkward for an LLM. A fully custom format would lose reasoners, SHACL validation and SPARQL.

## Decision

We will:
- **Define every record in one LinkML schema** (`model` component): the scope record, source units, the six element types, mentions, evidence, decisions, runs, and the LLM output classes.
- **Keep the records as YAML,** one file per element, under `01_model/`. They are the only editable source.
- **Generate from the schema** the Pydantic models (committed, with a regeneration drift test) and the JSON Schema used as Claude's tool input schema. Every record is validated before it is written.
- **Generate the releases one way and never edit them by hand.** The `release` component builds `ontology.ttl` with rdflib (OWL 2 classes and object properties, SKOS labels and notes, OWL qualified cardinality and SHACL shapes for limits, `dai:` annotations for level, status and evidence) and `level-1/2/3.md` (Jinja2 + Mermaid), both from the same in-memory model, so the Markdown and the Turtle can't disagree.
- **Make the output deterministic:** sorted YAML keys, Turtle without blank-node labels (restrictions and shapes are inlined), and stable ordering everywhere. Two builds from the same records are byte-identical except for `built_at` (FR-36).
- **Make new slots optional by default,** so old records stay valid.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| OWL/Turtle as the editable source | Standard; tools read it directly | Evidence, level and status become axiom annotations; noisy diffs; hard for an LLM | Four of the five requirements are metadata on statements (Q2) |
| Fully custom YAML/JSON with no schema language | Total freedom | No validation, no generated JSON Schema, no standard export mapping | We would rebuild what LinkML gives |
| Hand-written Pydantic models, no LinkML | Fewer dependencies | No single source for JSON Schema and the RDF mapping; schema drift | LinkML is the research recommendation and keeps one definition |

## Consequences

- **Positive:** one schema drives validation, the LLM output format and the release mapping. Git diffs show real changes only. Adding a property is a schema change plus an optional slot.
- **Negative / trade-offs:** LinkML is a heavy dependency that sometimes lags behind new Python versions; T1 pins a supported interpreter. If rdflib's Turtle output turns out not to be byte-stable, we need our own sorted Turtle writer.
- **Follow-up:** the `model` and `release` components in `components.json`; T3, T14 to T16.
