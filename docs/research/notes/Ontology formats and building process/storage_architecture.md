# Storage architecture for an ontology under development (single file vs modular files vs triplestore / graph DB)

Scope: how an "OntologyBuilder" app in a git monorepo should physically store each ontology under `data/ontology-<name>/`. The ontology includes extracted candidates (statements, terms, concepts, relations, rules), proposed levels, provenance to source text, review status, authored content and a final built ontology. Research date: 2026-11-20.

## How do established projects organise source vs release artefacts, and how should ontologies be modularised?

### Takeaway
Mature projects keep a small **editable source** under version control and **generate** the release artefacts from it with a build pipeline. In OBO/ODK that means one `-edit` file plus imports, components and ROBOT/DOSDP templates, with a Makefile producing the base and full releases. SNOMED publishes tab-delimited RF2 Full, Snapshot and Delta files. Schema.org keeps the vocabulary as Turtle in `data/`. Wikidata is the exception: it is a live database with a separate SPARQL query service. Modularity in OBO comes from import modules and components merged at build time, not from many hand-edited files.

### Cited Findings
- **ODK edit file as the source of truth:** the ODK Makefile "encodes the rules by which ontology release files should be derived from the source of truth (the edit file)". ODK also sets up CI (GitHub Actions) to run checks. — [OBO Academy ODK reference](https://oboacademy.github.io/obook/reference/odk/)
- **Edit formats and defaults:** ODK's `edit_format` accepts `obo` or `owl` (default `owl`). `release_artefacts` can be base, full, baselite, simple, non-classified, simple-non-classified and basic, and the default is `["full", "base"]`. Import `module_type` can be slme, minimal or custom (default `slme`), plus `mirror` per product. `use_templates` (ROBOT templates) and `use_dosdps` both default to `false`. — [ODK project schema](https://incatools.github.io/ontology-development-kit/project-schema)
- **Release artefacts:** the full release holds all logical axioms, including inferred subclass relationships, and "All imports and components are merged into the full release artefact". The non-classified release reflects the "unmodified state of the editors file at release time". The simple release strips "all axioms referencing foreign (imported) classes". Basic is the simple release restricted to part-of relationships. An import is "a module of an external ontology which contains all the axioms necessary for the source ontology". — [OBO Academy release artefacts](https://oboacademy.github.io/obook/reference/release-artefacts/)
- **Components:** these are listed under `components: products:` in `src/ontology/<name>-odk.yaml`. A component can come from a ROBOT template, be curated by hand in Protégé, or be downloaded from a URL with a `source` attribute. Template TSVs go in `src/templates/`. — [AIO ODK components docs](https://berkeleybop.org/artificial-intelligence-ontology/odk-workflows/components/), [NMDO ODK guide](https://nmdo-sprints-documentation.readthedocs.io/en/latest/technical-documentation/guides/standard-ODK-workflows/manage-your-ODK-repository.html)
- **DOSDP:** enabled with `use_dosdps: true`. Generated classes are merged into `src/patterns/definitions.owl`. A DOSDP template is a separate YAML file paired with a TSV of data, whereas a ROBOT template keeps its template in the header row of the same table. — [OBO Academy DOSDP + ODK](https://oboacademy.github.io/obook/tutorial/dosdp-odk), [OBO Academy templates for OBO](https://oboacademy.github.io/obook/lesson/templates-for-obo)
- **ROBOT template format:** CSV or TSV. Row 1 holds headers, row 2 holds template strings (`ID`, `LABEL`, `TYPE`, `SC %`, `DOMAIN` …), and each remaining row is one term. `robot template --template t.csv --prefix … --ontology-iri … --output t.owl` produces OWL. It supports `--merge-before` / `--merge-after`, and `--errors <path>` writes errors to a table. — [ROBOT template](https://robot.obolibrary.org/template)
- **Gene Ontology:** the go-ontology repo is "primarily for the developers of the GO" and is not a download source. GitHub Actions tests every commit or PR, Jenkins builds a snapshot every second day, and another Jenkins job builds the monthly production release. — [geneontology/go-ontology](https://github.com/geneontology/go-ontology). Release formats are go.obo, go.owl and go.json, plus go-basic.obo, which is filtered to be acyclic. — [GO downloads](https://geneontology.org/docs/download-ontology/)
- **Why Mondo and Uberon edit in OBO format:** OBO format "looks clear in diffs such as git diffs". OWL Functional Syntax is the more widespread editor format because its changes "are much easier to be reviewed". — [OBO Academy OWL format variants](https://oboacademy.github.io/obook/explanation/owl-format-variants)
- **SNOMED CT RF2:** RF2 is published as tab-delimited UTF-8 text. *Full* holds the complete history, *Snapshot* the latest version of each component, and *Delta* only the rows changed since the previous release. Delta and Snapshot can be derived from Full, and every package must include Full. — [SNOMED starter guide §13](https://docs.snomed.org/snomed-ct-practical-guides/snomed-ct-starter-guide/13-release-schedule-and-file-formats), [RF2 release types](https://docs.snomed.org/snomed-ct-specifications/snomed-ct-release-file-specification/release-types-packages-and-files/3.2-release-types)
- **Schema.org:** the core vocabulary is `data/schema.ttl`, written in RDFS/Turtle. Examples are kept in separate `*-examples.txt` files and release snapshots under `data/releases/`. The project moved from RDFa to Turtle as of v8.0. — [schema.org developers](https://auto.schema.org/docs/developers.html), [schema.org README](https://cdn.jsdelivr.net/gh/schemaorg/schemaorg@main/README.md), [Dataliberate blog](https://www.dataliberate.com/?p=1604)
- **Wikidata:** this is a database, not files. The query service runs a separate triplestore (Blazegraph) that could not keep up with Wikidata's scale. The graph was split into a main graph and a scholarly graph on 2025-05-09, and benchmarks named QLever the fastest replacement candidate. — [Wikidata WDQS graph split FAQ](https://meta.wikimedia.org/wiki/WikiCite/WDQS_graph_split), [Wikidata workshop 2025 paper](https://wikidataworkshop.github.io/2025/papers/paper3.pdf). Wikipedia reports that in 2026 WDQS began replacing Blazegraph with QLever. — [Wikipedia: QLever](https://en.wikipedia.org/wiki/QLever) (secondary source; the migration status is not confirmed).

### Inferences
- The common pattern is **source ≠ release**. Editors and pipelines touch small, diff-friendly source files: an edit file, TSV templates and pattern YAML. Everything users consume (merged, reasoned, multi-format) is generated, and OBO projects usually only commit it at release time.
- ROBOT templates and DOSDP TSVs closely match "extracted candidate components" for OntologyBuilder: one row per candidate term or relation, with extra columns for provenance and status that the template step can ignore or turn into annotations.
- SNOMED's Full/Snapshot/Delta model is a useful precedent for keeping the review history (status changes over time) as append-only tabular rows.

### Gaps
- I could not fetch a page that states the GO edit-file path or format (`src/ontology/go-edit.obo` is widely assumed but was not verified here).
- I found no primary-source best-practice document on `owl:imports` granularity beyond the OBO import-module and component material above.

## Git-friendliness: diffs, merge conflicts, canonical serialisations, file-per-concept, TSV templates

### Takeaway
Text RDF/OWL works in git only if every writer uses **one deterministic serialiser**. The options are OWLAPI/ROBOT for OFN/OBO, EDM Council rdf-toolkit, or rdflib `longturtle` with `canon=True`, ideally enforced by a pre-commit hook. Blank nodes are the main source of diff noise. Use semantic diffs (`robot diff`) to review changes. Tabular sources (TSV) diff and merge best of all.

### Cited Findings
- **EDM Council rdf-toolkit:** built for git-based version control of ontology files, aiming for as few differences between commits as possible. It can run as a pre-commit hook that re-serialises files, and writes Turtle, RDF/XML, TriG and other formats. — [edmcouncil/rdf-toolkit](https://www.github.com/edmcouncil/rdf-toolkit)
- **Blank nodes:** a small change can cause blank nodes to be relabelled, so text diffs flag unchanged structures. IRIs and literals diff cleanly. — [W3C semantic-web list, 2024-09](https://lists.w3.org/Archives/Public/semantic-web/2024Sep/0016.html). W3C RDF Dataset Canonicalization (RDFC-1.0) is the standard canonical form. — [W3C RDF Canon](https://www.w3.org/TR/rdf-canon/)
- **rdflib `longturtle`:** added in 6.1.1 to make git-friendly Turtle. It is standard Turtle with more line breaks. `serialize(canon=True)` canonicalises blank nodes for deterministic output. PR #2997 sorts blank nodes by their serialised description, but top-level blank nodes with no inbound links are still not sorted. — [rdflib longturtle docs](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.plugins.serializers.longturtle/), [rdflib PR #2997](https://github.com/RDFLib/rdflib/pull/2997), [rdflib-dev thread](https://groups.google.com/g/rdflib-dev/c/EUW2fawv4mw)
- **Other sorted serialisers:** otsrdflib (ordered Turtle) and flatttl (flattened, sorted Turtle). Sorted N-Triples or N-Quads lines also work for large, simple graphs. — [otsrdflib](https://pypi.org/project/otsrdflib/0.4.2), [flatttl](https://github.com/rybesh/flatttl), [rdflib-dev thread](https://groups.google.com/g/rdflib-dev/c/EUW2fawv4mw). Overview of approaches: [W3C wiki: How to diff RDF](https://www.w3.org/2001/sw/wiki/How_to_diff_RDF)
- **`robot diff`:** compares two ontologies **semantically** and ignores layout. Output formats are plain (OFN), pretty (labels and CURIEs), html and markdown (Manchester syntax). It can compare against a release IRI. — [ROBOT diff](https://robot.obolibrary.org/diff)
- **Merge conflicts in OBO practice:** resolve the conflict markers, then reopen and re-save the file in Protégé, or run a make target such as `normalize_obo_src` to re-serialise. — [OBO Academy: fixing conflicts](https://oboacademy.github.io/obook/howto/fixing-conflicts). Use current OWLAPI-based tools, which give "canonical ordering in serialization, minimizing spurious diffs". — [ODK editors workflow (COB)](https://obofoundry.org/COB/odk-workflows/EditorsWorkflow/)
- **Tool-generated RDF/XML:** a bad choice for version control. — [Chris Mungall, W3C list 2017](https://lists.w3.org/Archives/Public/semantic-web/2017Jan/0102.html). Contributors using different editors cause consistency problems and conflicts. — [Git4Voc (arXiv 1601.02433)](https://arxiv.org/pdf/1601.02433)
- **VoCol (EKAW 2016):** an integrated environment for vocabulary development in version control. It covers modelling, population and testing, with validation (Rapper, Jena RIOT), querying, documentation (Widoco) and visualisation (WebVOWL) loosely coupled on top of a plain git repository. — [VoCol, Springer](https://link.springer.com/doi/10.1007/978-3-319-49004-5_20), [VoCol preprint](https://zenodo.org/records/15023/files/vocol.pdf). A related paper covers decentralised collaborative knowledge management with git (Quit Store). — [arXiv 1805.03721](https://arxiv.org/pdf/1805.03721)

### Inferences
- For OntologyBuilder, **TSV/CSV or YAML/JSON records are the most git-friendly representation of candidates and review state**. Each candidate is a row or file with a stable ID, so concurrent changes rarely touch the same line. RDF/OWL is a build output.
- File-per-concept (for example `candidates/<id>.yaml`) gives the fewest merge conflicts and the clearest per-item history (`git log -- file`). The cost is many small files and a loader step. A sorted TSV per component type is a good middle ground at hundreds to tens of thousands of rows.
- Any hand- or LLM-authored Turtle or OWL should be normalised by a pre-commit step: ROBOT `convert` to OFN, or rdflib `longturtle` with `canon=True`. Avoid blank nodes in authored content (use skolem IRIs) so diffs stay stable.

### Gaps
- I found no direct confirmation that rdf-toolkit's Turtle output follows RDFC-1.0 (a 2024 post says work was planned in issue 76).
- I found no published, quantitative study comparing merge-conflict rates across serialisations.
- I searched for "OntoGit" and found no reliable source for it.

## When is a triplestore or graph DB warranted?

### Takeaway
A server triplestore is warranted for **live multi-user writes, large data (millions of triples or more), always-on SPARQL endpoints or heavy reasoning at query time**. None of these applies to a small-to-medium ontology built by a git-driven pipeline. Embedded stores (rdflib in memory, Oxigraph or pyoxigraph) cover querying and validation at build time. Property graphs (Neo4j + n10s) import only a subset of OWL and lose RDF features such as multi-valued literals by default.

### Cited Findings
- **Jena TDB2:** one active write transaction and many concurrent read transactions, using copy-on-write MVCC with serializable isolation. Several JVMs sharing the same TDB files is "not supported and has a high risk of data corruption", so use the Fuseki server for shared access. Bulk loaders are not transactional. — [Jena TDB transactions](https://jena.apache.org/documentation/tdb/tdb_transactions.html), [Jena TDB FAQ](https://jena.apache.org/documentation/tdb/faqs.html)
- **Oxigraph:** both an RDF/SPARQL toolkit and a graph database on RocksDB, with Python bindings (pyoxigraph). oxrdflib lets rdflib use Oxigraph as a store: SPARQL queries run in pyoxigraph, SPARQL updates still go through rdflib, and transactions are not yet implemented. — [oxigraph GitHub](https://github.com/oxigraph/oxigraph), [oxrdflib](https://pypi.org/project/oxrdflib). Use offline `oxigraph load` for large bulk loads. — [x-cmd Oxigraph guide](https://x-cmd.com/install/oxigraph/) (third-party)
- **rdflib in memory:** the R `rdflib` package's storage vignette (an R wrapper, not Python rdflib) calls the in-memory store fine for small datasets but impractical for millions of triples, and points to disk-backed stores (Postgres, Virtuoso). — [rOpenSci rdflib storage](https://docs.ropensci.org/rdflib/articles/storage.html). An older paper measured Python RDFlib at about 777 s to load 5M triples, and could not run larger tests because of memory limits. — [TripleID-Q, arXiv 1807.01409](https://arxiv.org/pdf/1807.01409). A 2026 benchmark compares frameworks at 100K, 1M and 10M triples; I did not extract its numbers. — [RDF Framework Benchmark](https://datatreehouse.github.io/trainmarks/)
- **Neo4j n10s:** self-hosted Neo4j only, not available on Aura. Import requires a uniqueness constraint on `:Resource(uri)`. By default it keeps only one value per literal property (the last one parsed). The ontology loader imports only classes, subclass and subproperty hierarchies, property definitions, domain/range and `owl:Restriction`, and "all other elements will be ignored". — [n10s import](https://neo4j.com/labs/neosemantics/5.14/import/), [n10s importing ontologies](https://neo4j.com/labs/neosemantics/4.3/importing-ontologies/), [n10s overview](https://neo4j.com/labs/neosemantics/)
- **Scale example:** Wikidata, at a scale many orders of magnitude beyond this use case, outgrew Blazegraph and had to split its graph. That shows when a dedicated, tuned store becomes unavoidable. — [WDQS graph split](https://meta.wikimedia.org/wiki/WikiCite/WDQS_graph_split)

### Inferences
- **Thresholds (rule of thumb, from the sources above):**
  - Below about 1M triples, in-memory rdflib or pyoxigraph is enough for build-time SPARQL and SHACL.
  - From about 1M to 100M triples, use an embedded persistent store (Oxigraph, TDB2) or Fuseki.
  - Beyond that, or with many concurrent writers, use a server store (GraphDB, Stardog, Virtuoso, RDFox, Neptune, QLever).
  - Hundreds to tens of thousands of statements is far below the first threshold.
- A server store adds a second source of truth, backup and migration work, and breaks "diff in a PR" review. It is only worth it if OntologyBuilder needs many people editing in real time through a UI or a public SPARQL endpoint.
- Property graphs suit graph analytics and visualisation of candidate networks, but are a poor fit as the canonical store for OWL axioms and rules.

### Gaps
- I found no vendor-neutral, sourced size thresholds. The numbers above are inferences.
- I did not research GraphDB, Stardog, RDFox, Virtuoso, Blazegraph or Neptune licensing and reasoning features in detail.
- I found no current pyoxigraph benchmark numbers.

## Hybrid pattern: files in git as the source of truth, loaded into an embedded store at build time

### Takeaway
This is the dominant practice. ODK keeps files in git and uses ROBOT and reasoners at build time, VoCol puts validation and query services on top of git, and GO and schema.org build releases from repository sources. For OntologyBuilder: keep tabular or record files plus a small amount of authored OWL/Turtle in git. Have a build step that loads them into rdflib or pyoxigraph (or ROBOT), runs SHACL, SPARQL checks and a reasoner, and writes deterministic release files.

### Cited Findings
- **ODK:** the Makefile derives releases from the edit file, and CI checks each PR. — [OBO Academy ODK](https://oboacademy.github.io/obook/reference/odk/), [go-ontology](https://github.com/geneontology/go-ontology)
- **Full release:** merges imports and components and includes inferred axioms, which needs a reasoner at build time. — [OBO Academy release artefacts](https://oboacademy.github.io/obook/reference/release-artefacts/)
- **VoCol:** loosely couples validation, querying, analytics, visualisation and documentation over a standard git repository. — [VoCol](https://link.springer.com/doi/10.1007/978-3-319-49004-5_20)
- **Embedded engines usable at build time:** pyoxigraph and oxrdflib. — [oxrdflib](https://pypi.org/project/oxrdflib). TDB2 is fine for a single process but should not be shared across JVMs. — [Jena TDB transactions](https://jena.apache.org/documentation/tdb/tdb_transactions.html)

### Inferences
Suggested layout for `data/ontology-<name>/`, where only `source/` is hand- or app-authored and committed:
- `source/candidates/*.tsv`: one TSV per component type (terms, concepts, relations, statements, rules). Columns: stable ID, proposed level, label, definition, `source_doc`, `source_span` (char offsets or quote), extractor, run ID and timestamp.
- `source/review.tsv` or `review/*.yaml`: append-only decisions (`candidate_id`, status, reviewer, date, note), in the style of SNOMED Delta.
- `source/authored/*.ttl` or `.ofn`: hand-authored axioms and rules, normalised by a pre-commit step.
- `templates/`: ROBOT/DOSDP header mappings.
- `build/` (git-ignored or committed only at release): merged `ontology.ttl`, `ontology.owl`, `ontology.jsonld` and a reasoned/full variant, plus a `robot diff` against the previous release.

Provenance can stay in the TSVs and be exported as PROV-O or annotation properties only in a "full / with-provenance" artefact, so the clean release stays lean. This mirrors ODK base vs full.

### Gaps
- I found no published case study of an LLM-extraction-to-review-to-ontology pipeline that uses this exact layout.

## Pros/cons and recommendation for a small-to-medium ontology (hundreds to tens of thousands of statements)

### Takeaway
Recommendation: **modular files in git as the source of truth** (tabular candidates and review log, plus normalised authored OWL/Turtle), with a **generated single-file release** in several serialisations. Use an **embedded in-memory store** (rdflib or pyoxigraph, optionally ROBOT and a reasoner) only during build and validation. Defer any server triplestore until real-time multi-user editing or a public SPARQL endpoint is needed.

### Cited Findings
| Option | Pros | Cons | Evidence |
|---|---|---|---|
| Single file (one `.ttl`, `.ofn` or `.obo` edit file) | Simple; one artefact; tools such as Protégé open it directly | Merge conflicts concentrate in one file; serialiser churn; cannot hold review state cleanly | [OBO Academy fixing conflicts](https://oboacademy.github.io/obook/howto/fixing-conflicts), [Git4Voc](https://arxiv.org/pdf/1601.02433) |
| Modular files (edit file + imports + components + TSV templates) | Clean diffs; parallel work; generated outputs; proven at OBO scale | Needs a build pipeline (Makefile/ROBOT); more moving parts | [ODK schema](https://incatools.github.io/ontology-development-kit/project-schema), [ROBOT template](https://robot.obolibrary.org/template), [ODK components](https://berkeleybop.org/artificial-intelligence-ontology/odk-workflows/components/) |
| File-per-concept | Lowest conflict rate; per-item history | Many files; needs an aggregator | Inference (no primary source found) |
| Embedded store at build time (rdflib, pyoxigraph, TDB2) | SPARQL/SHACL checks; no server; data is disposable | Not a source of truth; rdflib slows at millions of triples | [oxrdflib](https://pypi.org/project/oxrdflib), [rOpenSci rdflib](https://docs.ropensci.org/rdflib/articles/storage.html) |
| Server triplestore (Fuseki, GraphDB, Stardog, …) | Concurrent users; endpoint; scale; reasoning | Ops burden; second source of truth; no PR diffs; TDB single writer | [Jena TDB transactions](https://jena.apache.org/documentation/tdb/tdb_transactions.html) |
| Property graph (Neo4j + n10s) | Graph analytics and visualisation; Cypher | Imports a subset of OWL; one literal value by default; self-hosted only | [n10s import](https://neo4j.com/labs/neosemantics/5.14/import/), [n10s ontologies](https://neo4j.com/labs/neosemantics/4.3/importing-ontologies/) |

### Inferences
- **Fit with the monorepo's dataset contracts (ADR-0013, ADR-0016).** OntologyBuilder owns and writes `data/ontology-<name>/`. Readers depend on the contract for the *built* artefacts (for example `build/ontology.ttl` plus a manifest), not on the internal candidate TSVs. That keeps the source layout free to change.
- **Enforce determinism:** a pre-commit hook sorts TSVs by ID and normalises any RDF (ROBOT `convert` to OFN, or rdflib `longturtle` with `canon=True`). PR reviews include a `robot diff --format markdown` of the built ontology against `main`.
- **Upgrade path:** if real-time collaborative review becomes a requirement, add Fuseki or Oxigraph-server as a *derived* index loaded from git, not as the source of truth. Only move the source of truth into a database (the Wikibase model) if git-PR review becomes the bottleneck.

### Gaps
- None of the sources compares the cost of these options for LLM-generated candidate volumes specifically. The recommendation is a synthesis.
