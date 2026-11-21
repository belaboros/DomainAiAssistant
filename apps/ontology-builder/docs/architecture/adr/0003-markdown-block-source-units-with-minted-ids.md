# ADR-0003: Split sources into Markdown-block units with minted, opaque IDs

- **Status:** accepted
- **Scope:** app `ontology-builder` (the resulting registry format is published through the root `ontology` contract, ADR-0019)
- **Date:** 2026-11-21
- **Related:** [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q8, Q10, Q31; [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-4, FR-5, FR-21; [source IDs note](../../../../../docs/research/notes/Ontology%20formats%20and%20building%20process/source_ids_and_change_propagation.md)

## Context

Every element cites the source units it came from. Readers such as the AI assistant will join ontology hits with RAG hits through these unit IDs. So units need IDs that never change when text is fixed, moved or renamed (re-ingestion comes later), and the IDs must not be derived from text or position (FR-5).

The size of a unit is a trade-off. Sentences give precise evidence but are fragile to split ("e.g.", "2 m.", quotes) and roughly triple the units, and so the LLM calls. Whole sections are too coarse to tell a story from the facts next to it, as in the dog manual's chapter 1.

## Decision

We will:
- **Make one source unit per Markdown block:** a paragraph, a list item, a blockquote or a table row. Units are parsed with markdown-it-py, which gives line positions. Headings are not units; they form each unit's heading path.
- **Mint the IDs:** each document gets `doc_` + ULID and each unit `su_` + ULID, minted once. The ID never carries text or position.
- **Keep the rest as separate fields:** the location (file path, heading path, index in section), `content_hash` (`sha256:` of NFC- and whitespace-normalised text) and the normalised text. Identical blocks get separate IDs and the same hash.
- **Treat user statements as units too,** under `00_sources/90_user_statements/`. Editing one adds a revision and keeps the ID.
- **Allow an optional quoted span** (W3C TextQuoteSelector style) in evidence, for precision inside a unit.
- **Number corpus folders `00`–`89`** in ingestion order, named `NN_<source-folder-slug>`.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| Sentence-level units | Precise evidence | Fragile splitting; about 3× the units and cost; context has to be passed in from neighbouring sentences | Q31 |
| Position or structural-path IDs | Readable; no registry | Break on any insert or rename | The research rejects them as identity |
| Content-hash IDs | No stored state | A typo fix looks like delete + add; identical text collides | The hash is kept as a fingerprint only |
| Anchors embedded in the manuals | Stable by construction | Changes the manuals dataset (a non-goal) and doesn't work for third-party manuals | Possible later for manuals we control |

## Consequences

- **Positive:** stable, opaque IDs that readers can rely on. Splitting is deterministic and cheap. The pet corpus has about 100 units, and the anecdote, the quote and their neighbours fall into separate units.
- **Negative / trade-offs:** a long paragraph that mixes topics is one unit; the optional quote span softens that. ULIDs carry a creation timestamp, which is not text or position.
- **Follow-up:** the `sources` component; `source-unit.schema.json` in `libs/contracts/ontology/` (T2); T6.
