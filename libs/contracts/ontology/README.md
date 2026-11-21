# Shared contract: ontology (contract family)

| | |
|---|---|
| **Applies to** | every dataset `ontology-<name>` (`data/ontology-<name>/`); each has a thin contract `libs/contracts/ontology-<name>/README.md` that pins a version of this one |
| **Owner (only writer)** | `ontology-builder` |
| **Readers** | see each dataset in the system map of the [root architecture](../../../docs/architecture/architecture.md) |
| **Contract version** | 0.1.0 (see [CHANGELOG.md](CHANGELOG.md)) |
| **Decision** | [ADR-0019](../../../docs/architecture/adr/0019-ontology-builder-app-and-shared-ontology-contract.md) |

This is a **contract family**, not a dataset: it is not registered in `components.json`. It describes what readers of any ontology dataset may rely on (ADR-0013). Anything not written here, in particular `01_model/` and `02_decisions/`, is internal to `ontology-builder` and may change without notice.

## Layout

```
data/ontology-<name>/
├── 00_sources/                          CONTRACT: the source registry
│   ├── <NN>_<corpus-slug>/              one folder per ingested corpus, NN = 00..89
│   │   ├── corpus.yaml
│   │   ├── documents/<doc-id>.yaml
│   │   └── units/<doc-id>.yaml
│   └── 90_user_statements/<su-id>.yaml  statements typed in by people
├── 01_model/                            internal
├── 02_decisions/                        internal
└── 03_release/                          CONTRACT: the releases
    ├── 00_raw/                          rebuilt on every save
    │   ├── ontology.ttl
    │   ├── level-1.md  level-2.md  level-3.md
    │   └── manifest.json
    └── 01_governed/                     rebuilt only when a domain admin publishes
        ├── ontology.ttl
        ├── level-1.md  level-2.md  level-3.md
        ├── CHANGELOG.md
        └── manifest.json
```

Files in YAML are UTF-8 YAML 1.2 with sorted keys. Readers must ignore keys, files and RDF terms they do not know: adding any of them is a minor version.

## `00_sources/`: the source registry

**`corpus.yaml`**: `id` (`co_` + ULID), `number` (0–89, the `NN` of the folder), `slug`, `source_path` (the ingested folder, relative to `SHARED_DATA_DIR`), `ingest_run` (ID of the run that ingested it).

**`documents/<doc-id>.yaml`**: `id` (`doc_` + ULID), `corpus_id`, `path` (relative to the corpus source folder), `title` (first heading, or the file name), `content_hash` (`sha256:` of the file's bytes).

**`units/<doc-id>.yaml`**: the document's source units as a YAML list, in document order. Each item follows [source-unit.schema.json](source-unit.schema.json).

**`90_user_statements/<su-id>.yaml`**: one source unit of kind `user_statement`, also per [source-unit.schema.json](source-unit.schema.json), with `author`, `created_at` and every revision. Editing a statement adds a revision and changes `text` and `content_hash`; the ID stays.

A **source unit** is one Markdown block: a paragraph, a list item, a blockquote or a table row (ontology-builder/ADR-0003). Its fields: `id`, `document_id`, `kind`, `location` {`path`, `heading_path`, `index_in_section`, `line_start`, `line_end`}, `content_hash`, `text` and, when the LLM proposed it as ignorable, `ignorable` {`proposed`, `category`, `reason`, `status`}.

## `03_release/`: the releases

| Variant | Folder | Contains | Built |
|---------|--------|----------|-------|
| **raw** | `00_raw/` | every element except excluded, rejected and ignorable ones, each with its status | on every save |
| **governed** | `01_governed/` | approved and deprecated elements only, in their approved version | when a domain admin publishes a version |

Both variants hold the same files:

- **`ontology.ttl`**: RDF 1.1 Turtle with OWL 2, SKOS and SHACL, and the `dai:` vocabulary of [vocab.ttl](vocab.ttl). See [The RDF graph](#the-rdf-graph).
- **`level-1.md`, `level-2.md`, `level-3.md`**: human-readable views. See [The level files](#the-level-files).
- **`manifest.json`**: per [manifest.schema.json](manifest.schema.json): `ontology`, `variant`, `version` (governed: semantic version; raw: `raw+<short git sha>`), `built_at`, `source_commit`, `counts` {`by_type`, `by_status`, `by_level`}, and `files`, the `sha256:` checksum of every other file in the folder.
- **`CHANGELOG.md`** (governed only): for each published version, newest first, the elements added, changed, deprecated and removed against the previous governed version, by ID and label.

The history of `01_governed/` in git is the history of the published versions.

## The RDF graph

**IRIs.** Every element and every source unit has the IRI `<base IRI><id>`. The default base IRI is `urn:domain-ai-assistant:ontology:<name>:`, e.g. `urn:domain-ai-assistant:ontology:pets-and-house-rules:cn_01JDK7F3Q8…`. A dataset may set another base IRI; it is stated in the ontology header. The IDs are minted (type prefix + ULID): `st_` statement, `tm_` term, `cn_` concept, `rl_` relation, `ru_` rule, `pr_` property, `su_` source unit, `doc_` document.

**Vocabulary.** `dai:` is `urn:domain-ai-assistant:vocab#`, defined in [vocab.ttl](vocab.ttl).

| Element | RDF |
|---------|-----|
| Ontology header | `owl:Ontology` with `owl:versionIRI`, `owl:versionInfo` (the manifest version) and `dcterms:description` (the purpose of the ontology) |
| Concept | `owl:Class` and `skos:Concept` (the same IRI); `skos:prefLabel`, `skos:altLabel` (synonyms), `skos:hiddenLabel` (non-preferred variants), `skos:definition`, `skos:scopeNote` (one per sense when a term names several concepts); is-a as `rdfs:subClassOf` and `skos:broader` |
| Relation | `owl:ObjectProperty` with `rdfs:label`, `rdfs:domain` and `rdfs:range` |
| Cardinality (of a relation or a rule) | both an `owl:Restriction` with `owl:onProperty`, `owl:onClass` and `owl:minQualifiedCardinality` / `owl:maxQualifiedCardinality`, as a superclass of the domain class (an inlined blank node), and a `sh:NodeShape` with the IRI `<element IRI>-shape`, `sh:targetClass` the domain class, and a property shape with `sh:path`, `sh:qualifiedValueShape` [`sh:class` the range] and `sh:qualifiedMinCount` / `sh:qualifiedMaxCount` |
| Rule | an individual of `dai:Rule` with `rdfs:label`, `dai:modality`, `dai:actor`, `dai:action`, `dai:condition`, `dai:limitComparator`, `dai:limitValue`, `dai:limitUnit`, `dai:scope`, `dai:refersTo` (only those that apply) |
| Statement | an individual of `dai:Statement` with `rdfs:label` (its text) |
| Property | an individual of `dai:Property` with `dai:propertyOf`, `dai:propertyName`, `dai:propertyValue`, `dai:propertyUnit` |
| Source unit | an individual of `dai:SourceUnit`, for every unit cited as evidence, with `rdfs:label` (its text) |
| On every element | `dai:level` (`dai:level-1`, `dai:level-2` or `dai:level-3`), one or more `dai:evidence` (source-unit IRIs), `dai:status` (raw only); when deprecated, `owl:deprecated true` and `dcterms:isReplacedBy` (if it has a replacement) |

Terms are not separate resources: a term is the label (`skos:prefLabel`, `skos:altLabel` or `skos:hiddenLabel`) of the concept each of its mentions points to.

## The level files

- **Levels are cumulative:** `level-2.md` holds everything in `level-1.md` plus the level-2 elements; `level-3.md` holds every element of the release. Ignorable and deprecated elements are in no level file.
- **Sections, in order:** title and version; a taxonomy diagram (Mermaid `flowchart TB`, is-a); a concept-relation diagram (Mermaid `flowchart LR`); catalogues of concepts (labels, synonyms, definition), relations and rules; an **Evidence** appendix.
- **Large diagrams:** a diagram with more than 40 nodes is split into one diagram per top-level concept.
- **Evidence links:** every catalogue entry links to `#su_…`. The Evidence appendix has one anchor `<a id="su_…"></a>` per cited unit, with its text and location, so every link resolves inside the same file.
- **Raw release:** every element that is not approved carries a text badge (`● proposed`, `◐ waiting for approval`) and a dashed Mermaid class.

## Guarantees

- **One writer.** Only `ontology-builder` writes an ontology dataset.
- **Atomic.** A save or a publish replaces the dataset folder in one swap, then commits it. Readers never see a half-written release, and every committed state has a matching manifest.
- **Deterministic.** Two builds from the same records give byte-identical files, apart from `built_at` in `manifest.json`. Git diffs therefore show only real changes.
- **Stable IDs.** IDs are minted, opaque and never derived from a unit's text or position. An ID is never reused, and an approved element is never deleted: it is deprecated, optionally with a replacement.
- **Evidence.** Every element in a release cites at least one source unit that exists in `00_sources/`.
- **Governed means approved.** `01_governed/` contains approved and deprecated elements only, and a publish fails rather than publish an approved element that refers to an element that is not approved.
- **No personal data.** User names are handles; only corpus text and user statements are stored.

## Versioning

Semantic versioning of this contract: **major** for anything that can break a reader (a removed or renamed field, file or RDF term, or a changed meaning), **minor** for additions readers can ignore, **patch** for clarifications. A major change needs a root ADR and a task for every reader of every `ontology-<name>` dataset. Each thin dataset contract states the version of this contract it conforms to.
