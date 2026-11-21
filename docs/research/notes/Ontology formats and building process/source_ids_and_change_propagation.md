# Stable source IDs and change propagation

Claude's analysis written for idea 0002 on 2026-11-21. It is a design proposal for `/spec 0002`: unlike the other notes in this folder it is **not sourced research**. The only external standard it relies on is the W3C Web Annotation Data Model ([TextQuoteSelector](https://www.w3.org/TR/annotation-model/#text-quote-selector), [TextPositionSelector](https://www.w3.org/TR/annotation-model/#text-position-selector)).

## The problem

User manuals are upgraded regularly. When OntologyBuilder ingests a new version it must:

- tell which source statements are unchanged, which were modified, which were deleted and which are new;
- carry the IDs forward so that evidence links stay valid;
- propagate the change to every ontology element whose evidence points at a changed statement.

## Key idea: keep identity and content apart

A single ID cannot be both stable across edits and a fingerprint of the content. Every source unit therefore gets three things:

| Part | Example | Changes when |
|---|---|---|
| **Stable ID** (identity) | `src:dog-owners-manual:01JD3K…` | never; it is carried forward by alignment |
| **Location** (where it is now) | `dog-owners-manual/04-feeding.md#daily-routine/p3` | the unit moves, or a heading is renamed |
| **Content hash** (what it says now) | `sha256:9f2c…` of normalised text | the text changes |

## Alternatives

| # | Scheme | Stable across upgrades? | Detects modified vs deleted? | Cost | Verdict |
|---|---|---|---|---|---|
| A | **Position**: path + chunk index or line numbers | ❌ inserting one paragraph shifts every later ID | ❌ | trivial | reject |
| B | **Structural path**: path + heading path + paragraph number within the section | ⚠️ stable when *other* sections change; breaks on a heading rename, a file move or an insert within the section | ⚠️ | low, readable | use as a **location** and an alignment feature, not as the identity |
| C | **Content hash** of normalised text | ❌ a typo fix gives a new ID, so it looks like delete + add; identical text in two places collides | ✅ shows *that* something changed | low, needs no stored state | use as a **fingerprint**, not as the identity |
| D | **Minted opaque ID + alignment registry** | ✅ the ID survives edits, moves and renames | ✅ | medium: needs a registry and an alignment algorithm | **recommended as the identity** |
| E | **Anchors embedded in the source** (e.g. `<!-- id: s-0042 -->` in the Markdown) | ✅✅ stable by construction | ✅ | needs control over the source files | **use when we control the source**, e.g. our generated manuals; not possible for third-party manuals |
| F | **W3C Web Annotation selectors** (quote + prefix + suffix, plus character offsets) | ✅ re-anchors approximately after edits | ⚠️ | low | use for **span-level evidence** inside a unit |

## Recommended combination

1. **Granularity: separate source units from RAG chunks.**
   - A *source unit* is a sentence or a short passage, the thing a statement is extracted from. Evidence links point to source units.
   - *RAG chunks* are retrieval windows that list the source units they cover.

   This way re-tuning chunk size for retrieval never breaks the ontology's evidence.
2. **Identity:** mint an opaque ID (a ULID or a counter, never derived from text or position) the first time a unit is seen. Store it in a **source registry**: ID, document ID, location, content hash, normalised text and the first and last document version it was seen in. Documents also get stable IDs, so a renamed file is not a new document.
3. **On each new manual version, run an alignment step** that maps new units to registered ones, in order of confidence:
   1. Same hash, same location: **unchanged**.
   2. Same hash, different location: **moved**. Keep the ID and update the location.
   3. Same or nearby location, high text similarity (edit distance or token overlap first, then embeddings for rewordings): **modified**. Keep the ID and record a new revision, with old and new text.
   4. A similarity score in a grey band: a **human decides** in the review GUI ("is this the same statement?").
   5. A registered unit with no match: **deleted**. Mark it retired in that version; never remove it from the registry.
   6. A new unit with no match: **new**. Mint an ID.

   One unit split into two, or two merged into one, is recorded as a link between the old and new IDs.
4. **Propagation to ontology elements**, using the evidence links:

   | Source change | Effect on elements whose evidence includes the unit |
   |---|---|
   | unchanged or moved | nothing; approved elements stay approved |
   | modified | re-extract from the new text and compare the result with the element. If it is equivalent, keep the status and record the new evidence revision. If it differs, open an issue and set the element back to *under review*, with an old/new text diff in the GUI |
   | deleted | remove that evidence link. If the element has no evidence left, flag it as **orphaned** for review, with deprecation proposed; never delete it automatically (OBO-style obsoletion) |
   | new | normal extraction; new candidates are *proposed* |

   Authored elements with no source evidence are not affected.
5. **Anchors (E) as a shortcut.** Where the generator of the manuals is under our control (the `generate-pets-and-building-user-manual` app), have it write stable anchors into the Markdown. Alignment then reduces to reading the anchors and comparing hashes. The registry and alignment remain the general path for manuals we do not control.

## Who owns the registry

The registry must have **one writer**: if two apps each chunk the manuals and mint IDs, they will mint different IDs (ADR-0013 one-writer rule).

- **Option 1:** OntologyBuilder owns it and publishes it in `data/ontology-<name>/`. The assistant reads it from there for RAG.
- **Option 2:** a separate corpus dataset, e.g. `data/corpus-<name>/`, written by one ingestion component, which OntologyBuilder and the assistant both read.

Option 2 is cleaner if the same corpus feeds several ontologies, or feeds the assistant without an ontology. `/spec` decides.
