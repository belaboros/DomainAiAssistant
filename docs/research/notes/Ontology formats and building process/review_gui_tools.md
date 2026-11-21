# GUI and review capabilities of ontology, taxonomy and KG tools, and UI building blocks for a custom review GUI

Research date: 2026-11-21. Scope: only GUI and review features for the OntologyBuilder app (idea 0002). It builds on [existing_tools.md](existing_tools.md) (tool coverage, licences, AI features) and [governance_process.md](governance_process.md) (roles, statuses, workflows), and does not repeat them.

Features checked:
- **F1** textual review: list or table, accept/reject/correct, with source evidence
- **F2** visual review: taxonomy tree diagrams and concept/relation graph diagrams
- **F3** filter by a custom property (level)
- **F4** colour by status
- **F5** type or create corrected or new statements in the GUI
- **F6** approval workflow with roles

Method: about 22 web searches and fetches. Many findings come from search-result summaries of vendor docs rather than full page reads, and those are marked "(summary)". No hands-on testing was done.

## 1. Which of F1–F6 does each tool support?

### Takeaway
The governance platforms (VocBench 3, TopBraid EDG, PoolParty, metaphactory) are strong on F5 (form editing) and F6 (roles and approval). Their diagram views, though, are mostly **for exploration, with colour by type or class, not by a custom status or level property**. The tools with flexible rule-based colouring (Neo4j Bloom, NeoDash, GraphDB Visual Graph through queries) have no ontology approval workflow. None of the tools shows LLM evidence snippets next to each candidate (F1 with evidence).

### Cited Findings

**VocBench 3 (open source, BSD-3, active)**
- The Graph View has three perspectives: data-oriented (close to the RDF graph), model-oriented (domain and range links between classes), and class-diagram (classes, with their properties listed inside each node). All three use a d3.js force-directed layout. There is no tree or hierarchical layout. The whole-ontology model graph is static. — [VocBench Graph View docs](https://vocbench.uniroma2.it/doc/user/graphs.jsf)
- In the graph you can add nodes from a tree or list, expand Sub/Super, and remove a class from the displayed graph. The docs do not describe editing ontology content in the graph itself. — [VocBench Graph View docs](https://vocbench.uniroma2.it/doc/user/graphs.jsf)
- Colours are fixed: a node's top stripe shows its resource type (for example, light blue for concepts). Edges are coloured by property kind (object properties blue, annotation properties yellow, datatype properties green). Filters cover language-tagged literals, relation partitions and class axioms, not custom property values. — [VocBench Graph View docs](https://vocbench.uniroma2.it/doc/user/graphs.jsf)
- With validation on, changed triples are reified and kept in a staging repository. Normal triples go to a staging graph for "temporary visualization". So pending changes can be previewed, but the docs do not say whether the Graph View marks them. — [NKOS 2017 slides (Stellato)](https://nkos-eu.github.io/2017/content/stellato.pdf) (summary); [VocBench 3 SWJ paper](https://journals.sagepub.com/doi/10.3233/SW-200370) (summary)
- Roles and validation (F6) are covered in governance_process.md. Form-based editing (F5) happens in the ResourceView, which shares filters with the Graph View. — [VocBench Data View](https://vocbench.uniroma2.it/doc/user/data_view.jsf) (summary)

**TopBraid EDG (commercial)**
- The EDG Diagram panel replaced the older Class Diagram, NeighborGram and Relationship Tree Diagram. You add nodes by drag and drop, for example from the class hierarchy. The context menu offers Expand (neighbourhood, inherited, associations), Focus Node and Zoom To Node. You can filter an expansion to chosen relationship types. Large diagrams get an overview pane. Diagrams can be saved and exported as PNG, SVG or GraphML. The properties shown in a node are controlled by DASH property roles. Line colour, thickness and style are configurable. — [EDG Simple Diagram Panel](https://www.topquadrant.com/doc/latest/reference/SimpleDiagramPanel.html) (summary); [Using EDG Diagrams 7.2](https://archive.topquadrant.com/doc/7.2/user_guide/working_with_asset_collections/using_edg_diagrams.html) (summary); [TopQuadrant blog: visual exploration of ontologies](https://topquadrant.com/blog/visual-exploration-of-ontologies-with-topbraid-edg)
- In the EDG 7.1 webinar Q&A, TopQuadrant said the EDG Diagram panel had **no data-editing capabilities**; edits are made in other panels and the diagram refreshes. Whether this is still true in 9.x was not confirmed. — [EDG 7.1 webinar Q&A](https://www.topquadrant.com/?p=510) (summary)
- Forms are generated from SHACL shapes (F5), and workflows have governance roles (F6): see governance_process.md.

**Graphwise PoolParty (commercial)**
- GraphViews is a visualisation add-on with an Overview (a radial diagram of concept schemes and top concepts), a Tree View and a Detail View. It has no database of its own; it is a visualisation layer. In 2026 it is installed as a Docker service. — [PoolParty GraphViews](https://www.poolparty.biz/poolparty-graphviews); [GraphViews UI docs](https://help.poolparty.biz/en/poolparty-graphviews/navigating-the-graphviews-user-interface.html); [Graphwise: install GraphViews](https://help.graphwise.ai/en/graphwise-documentation/how-to-install---manage-graphwise-components/installation---migration/add-on-applications/install-and-configure-graphviews.html)
- Editing happens in the core taxonomy tree (thesaurus manager) and in the separate GraphEditor, introduced in PoolParty 7.0 for editing parts of the knowledge graph. — [PoolParty GraphEditor](https://www.poolparty.biz/poolparty-grapheditor); [KMWorld on PoolParty 7.0](https://www.kmworld.com/Articles/News/News/PoolParty-Introduces-GraphEditor-in-New-PoolParty-7.0-Release-127055.aspx)
- The approval workflow (Draft / Suggested / Approved / Deprecated, with a workflow dashboard) is an Enterprise-tier feature. It is described in governance_process.md.

**metaphactory (commercial)**
- The visual ontology editor (since 4.0) supports exploration, visualisation, editing and documentation in a visual language that maps to OWL and SHACL. — [metaphactory 4.0](https://metaphacts.com/metaphactory-4-0); [metaphacts blog](https://blog.metaphacts.com/visual-ontology-modeling-for-domain-experts-and-business-users-with-metaphactory)
- 5.5 lets engineers configure **custom metadata properties** on ontologies and their elements. — [metaphactory 5.5](https://metaphacts.com/metaphactory-5-5) (summary)
- 5.6 added editorial workflows for vocabularies: the status is shown (in development, in review), reviews can be requested, review comments posted, and states locked. — [metaphactory 5.6](https://metaphacts.com/metaphactory-5-6)
- 6.0 (GA 2026-07-14) adds real-time collaborative visual editing with the metis assistant, plus semantic annotation of unstructured documents such as PDFs. — [metaphactory 6.0](https://metaphacts.com/metaphactory-6-0)
- No independent reviews of 6.0 were found. PeerSpot has no collected reviews. — [PeerSpot vendor page](https://www.itcentralstation.com/vendors/metaphacts-gmbh)
- Ontodia, the diagramming component metaphactory grew from, is documented with lifecycle and change management, versioning and an editorial workflow. — [metaphacts Ontodia page](https://metaphacts.com/ontodia) (summary)

**Stardog Designer / Explorer (commercial)**
- Designer is a no-code visual modelling tool. Each class gets an automatically assigned colour, which is used on the Designer canvas and in Explorer and can be changed in the class detail drawer. No evidence was found of colouring by property value. — [Stardog Designer docs](https://docs.stardog.com/stardog-applications/designer/) (summary)

**Neo4j Bloom / Explore and NeoDash (property graph, not OWL)**
- Bloom and Aura Explore have rule-based styling on string, numeric, boolean and temporal properties. The modes are single (one colour, size or caption under a condition), range (a gradient over numeric values) and unique values (a colour for each distinct value). Rules override the default style. — [Bloom Legend panel](https://Neo4J.com/docs/bloom-user-guide/current/bloom-visual-tour/legend-panel/); [Aura Explore styling](https://neo4j.com/docs/aura/explore/explore-visual-tour/styling/)
- NeoDash rule-based styling colours visualisation elements by a query's return values. It is enabled by default in NeoDash commercial from 3.2. — [NeoDash 2.4 rule-based styling](https://neo4j.com/labs/neodash/2.4/user-guide/extensions/rule-based-styling/); [NeoDash commercial](https://neo4j.com/docs/neodash-commercial/current/user-guide/extensions/rule-based-styling/)

**Ontotext GraphDB Workbench Visual Graph**
- In the visual graph config, a SELECT query sets node details, and the `?type` binding decides the colour. Expansion is controlled by a CONSTRUCT query. You could therefore bind `?type` to a status or level value to colour by it (inference). — [GraphDB workbench graph-config template (1.11.3)](https://unpkg.com/graphdb-workbench@1.11.3-TR1/dist/pages/graph-config/saveGraphConfig.html)
- Community answers (2021) say you cannot pick specific colours without changing source code, and that the colour for a type can change between visualisations. This may be outdated. — [Stack Overflow mirror: GraphDB colours](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/65926247/how-does-ontotext-graphdb-assign-colors-in-visual-graph)

**Protégé desktop + plugins, WebVOWL, WebProtégé**
- Protégé Desktop 5.6.9 is the current download. It is maintained as a community project, with Damien Goutte-Gattat as primary maintainer. — [Protégé software page](https://protege.stanford.edu/software)
- ProtégéVOWL has no published releases and warns that it has known bugs and implements only part of the VOWL spec. WebVOWL is the more complete VOWL implementation. — [stefborg/ProtegeVOWL](https://github.com/stefborg/ProtegeVOWL); [Protégé wiki: VOWL](https://protegewiki.stanford.edu/wiki/VOWL)
- WebProtégé: a `webprotege-gh-integration-service` repository (created 2023-10, last push reported 2025-09-23) manages integration with GitHub projects. The roadmap lists "Integrate with GitHub Issues" and push/pull integration with GitHub repositories as wishes. No released GitHub-backed editing was confirmed. — [ecosyste.ms: webprotege-gh-integration-service](https://awesome.ecosyste.ms/projects/github.com%2Fprotegeproject%2Fwebprotege-gh-integration-service); [WebProtégé Road Map](https://github.com/protegeproject/webprotege/wiki/WebProt%C3%A9g%C3%A9-Road-Map)

**Gra.fo (data.world): DISCONTINUED**
- data.world ended support for Gra.fo on 2026-03-13, after which accounts were no longer accessible. Users were told to download their work. — [data.world docs: Gra.fo](https://docs.data.world/en/60312-60312-Grafo.html)

**Chowlk (OEG-UPM, open source)**
- Converts draw.io diagrams drawn in the Chowlk notation into OWL (Turtle or RDF/XML), through a web service, a CLI or an API. Error files mark problem shapes in red. It is one-way (diagram to OWL). A 2026 ESWC poster describes a separate draw.io plugin that imports OWL in Graffoo notation. — [oeg-upm/Chowlk](https://github.com/oeg-upm/Chowlk); [ESWC 2026 poster](https://chrdebru.github.io/papers/2026-05-eswc-poster.pdf) (summary)

**LinkML tooling**
- schemasheets edits LinkML **schemas** (not instance data) in spreadsheets, both ways (`sheets2linkml`, `linkml2sheets`). It cannot talk to Google Sheets directly; COGS is recommended for git-like syncing. — [schemasheets Google Sheets how-to](https://linkml.io/schemasheets/howto/google-sheets); [linkml/schemasheets](https://github.com/linkml/schemasheets)
- linkml-browser generates standalone, schema-driven **faceted browsers** (read-only) for tabular JSON. It currently uses custom JSON schemas; native LinkML support is on its roadmap. — [ecosyste.ms: linkml/linkml-browser](https://awesome.ecosyste.ms/projects/github.com%2Flinkml%2Flinkml-browser)
- DataHarmonizer gives a spreadsheet-like data-entry UI for any "flat" LinkML schema. The LinkML Tool Implementer Guide suggests json-editor or react-jsonschema-form, after converting LinkML to JSON Schema, for schema-driven instance editing. — [DataHarmonizer wiki](https://github.com/cidgoh/DataHarmonizer/wiki/Managing-schema.yaml); [LinkML Tool Implementer Guide](https://linkml.io/linkml/developers/tool-developer-guide)
- Community projects: a LinkML Visual Schema Editor design spec (for schemas), SchemaLink (schema curation on Neo4j Arrows), LinkMLFormbuilder (forms to HTML or PDF), and the ChemDCAT-AP React Flow canvas editor that exports YAML. Their maintenance status was not verified. — [linkml-modeler-app design spec](https://adamlabadorf.github.io/linkml-modeler-app/design-spec); [SchemaLink docs](https://anacletolab.github.io/schemalink-docs); [LinkMLFormbuilder](https://pypi.org/project/LinkMLFormbuilder/); [Schema Graph Editor](https://hendrikborgelt.github.io/React_flow_test/)

### Inferences: feature matrix
(✓ documented; ~ partial or by workaround; – not found; ? not verified)

| Tool | Licence / status | F1 table + evidence | F2 tree diagram | F2 graph diagram | F3 filter by custom prop | F4 colour by status | F5 edit/create | F6 roles + approval |
|---|---|---|---|---|---|---|---|---|
| VocBench 3 | OSS BSD-3, active | ~ (validation lists; no evidence pane) | ~ (trees are UI lists, no diagram) | ✓ force layout | ~ (SPARQL/custom search, not in graph) | – (type colours only) | ✓ forms | ✓ |
| TopBraid EDG | Commercial | ~ (change sets, SHACL forms) | ~ (trees; diagram replaced tree diagram) | ✓ | ? | ? (line styling only) | ✓ forms; diagram read-only (7.1) | ✓ |
| PoolParty + GraphViews | Commercial (Enterprise for workflow) | ~ (workflow dashboard) | ✓ Tree View | ✓ Overview/Detail | ? | ? | ✓ tree + GraphEditor | ✓ |
| metaphactory 6 | Commercial | ~ | ? | ✓ visual editor | ~ (custom metadata props, 5.5) | ? | ✓ visually | ✓ editorial workflow (vocabularies) |
| Stardog Designer/Explorer | Commercial | – | – | ✓ | – | – (colour by class) | ✓ (model) | – |
| Neo4j Bloom / NeoDash | Commercial / Labs | ~ (NeoDash tables) | – | ✓ | ✓ | ✓ rule-based | ~ | – |
| GraphDB Visual Graph | Free/commercial | – | – | ✓ | ~ (config queries) | ~ (via `?type` binding) | – | – |
| Protégé + OntoGraf/VOWL | OSS, desktop | – | ~ | ~ (ProtégéVOWL buggy) | – | – | ✓ | – |
| WebProtégé | OSS | – | – (tree UI) | – | – | – | ✓ | ~ (permissions, comments) |
| WebVOWL | OSS, read-only viewer | – | – | ✓ | – | – | – | – |
| Chowlk | OSS | – | – | ✓ draw.io | – | ~ (manual draw.io styling) | ✓ (diagram to OWL) | – |
| Gra.fo | **Discontinued 2026-03-13** | – | – | – | – | – | – | – |
| LinkML tools (DataHarmonizer, linkml-browser) | OSS | ~ (grid / faceted read-only) | – | – | ✓ (facets) | – | ✓ (DataHarmonizer) | – |

### Gaps
- Not verified in this session: Progress Semaphore's visual views, Fluent Editor's GUI (covered as CNL authoring in existing_tools.md), OAK (a CLI and library, no GUI known), Wikibase, and NeoDash editable forms.
- Whether any commercial tool colours diagram nodes by a custom annotation value was not documented (EDG, PoolParty, metaphactory).
- Whether TopBraid EDG 9.x allows editing inside the diagram is unconfirmed.
- OntoGraf's 2025–2026 status and compatibility with Protégé 5.6 is unknown.

## 2. Custom properties, direct YAML/LinkML editing, round trip

### Takeaway
Only property-graph viewers (Bloom, NeoDash) and the GraphDB query-configured graph clearly support colouring by an arbitrary property. Every ontology governance tool needs RDF/OWL import into **its own store**: VocBench uses RDF4J/GraphDB, EDG its own store, PoolParty GraphDB, metaphactory a triple store. None edits LinkML YAML records directly. The LinkML tools that edit YAML (DataHarmonizer, JSON-Schema forms) have no diagram or approval workflow.

### Cited Findings
- Bloom rule-based styling colours by "unique values" of any property key, so `status` and `level` would each work directly. — [Bloom Legend panel](https://Neo4J.com/docs/bloom-user-guide/current/bloom-visual-tour/legend-panel/)
- The GraphDB Visual Graph colour comes from the `?type` binding of a configurable SELECT. — [GraphDB graph-config template](https://unpkg.com/graphdb-workbench@1.11.3-TR1/dist/pages/graph-config/saveGraphConfig.html)
- metaphactory supports custom metadata properties on ontology elements (5.5). Its use for diagram styling is not documented. — [metaphactory 5.5](https://metaphacts.com/metaphactory-5-5) (summary)
- VocBench keeps pending (unvalidated) changes as reified triples in a staging repository, which is its own internal store. — [NKOS 2017 slides](https://nkos-eu.github.io/2017/content/stellato.pdf) (summary)
- GraphViews is only a visualisation layer over PoolParty's data. — [PoolParty GraphViews](https://www.poolparty.biz/poolparty-graphviews)
- DataHarmonizer works on flat LinkML schemas; json-editor or react-jsonschema-form need a LinkML-to-JSON-Schema step. — [DataHarmonizer wiki](https://github.com/cidgoh/DataHarmonizer/wiki/Managing-schema.yaml); [LinkML Tool Implementer Guide](https://linkml.io/linkml/developers/tool-developer-guide)

### Inferences
- A round trip YAML → Turtle → tool → export → YAML is feasible but lossy and laborious. Our level, status and evidence IDs would have to be OWL/SKOS annotation properties. Each tool's own provenance (VocBench history, EDG change sets, PoolParty workflow status) lives in its store and would need to be mapped back. A diff on the export would be needed to turn it into YAML record changes. Tool-side identifiers and blank nodes (for example, OWL restrictions for cardinality) make stable reverse mapping hard. Expect an import/export adapter plus reconciliation, and treat the tool as source of truth while a review round is open. That conflicts with "YAML in git is the source of truth".
- Lower-friction pattern: keep YAML as the source of truth and use the external tool **read-only** for visual inspection (WebVOWL, GraphViews, GraphDB Visual Graph, Bloom). Do the decisions in a custom UI that writes YAML.

### Gaps
- No documentation was found of any tool's import/export preserving custom annotation properties through a full round trip. This needs testing.

## 3. Is there one tool covering all six features? Closest option and cost

### Takeaway
No. The closest are **metaphactory 6** (visual editing, custom metadata properties, editorial workflow, document annotation) and **PoolParty Enterprise with GraphViews/GraphEditor** (tree and graph views, concept-level approval with roles). Neither documents colour or filter by a custom level or status property, or evidence panes per LLM candidate. Among open-source tools, **VocBench 3** covers F5 and F6 and gives a basic force-directed graph. None publishes prices.

### Cited Findings
- metaphactory: visual editor, custom metadata, editorial workflow, 6.0 document annotation. — [5.5](https://metaphacts.com/metaphactory-5-5); [5.6](https://metaphacts.com/metaphactory-5-6); [6.0](https://metaphacts.com/metaphactory-6-0)
- PoolParty: GraphViews Tree and Overview views, GraphEditor. — [GraphViews](https://www.poolparty.biz/poolparty-graphviews); [GraphEditor](https://www.poolparty.biz/poolparty-grapheditor)
- VocBench Graph View: force layout only, colours by type. — [VocBench Graph View](https://vocbench.uniroma2.it/doc/user/graphs.jsf)

### Inferences
- Estimated coverage: metaphactory ≈ F2, F5, F6 plus partial F3; PoolParty ≈ F2, F5, F6 plus partial F1; VocBench ≈ F5, F6 plus partial F2. Every option misses F1 with evidence and F4 colour by status in diagrams, which are the two features most specific to an LLM-candidate review.

### Gaps
- Pricing for metaphactory, PoolParty, EDG, Stardog and Bloom is not public (consistent with existing_tools.md). Licence cost could not be quantified.

## 4. Libraries for a custom GUI

### Takeaway
A good fit is **Cytoscape.js (MIT)** with **elkjs** for both taxonomy trees (layered/mrtree) and relation graphs, with styling driven by data attributes (status, level). An alternative is **React Flow / xyflow** with elkjs or dagre, if rich editable node cards (inline forms) matter more than scale. **Reactodia (LGPL-2.1+)**, an RDF-native diagram workspace, is worth evaluating because it reads RDF directly. Use **Sigma.js + graphology** only if graphs grow beyond about 10k elements. **Mermaid** fits static docs and PR previews, not interactive review.

### Cited Findings
- Cytoscape.js core and all first-party extensions are MIT-licensed. — [js.cytoscape.org](https://js.cytoscape.org/); [cytoscape 3.34.4 README](https://unpkg.com/cytoscape@3.34.4/README.md)
- A `cytoscape-elk` adapter exists for ELK layouts in Cytoscape.js. — [npm: cytoscape-elk](https://npmjs.com/package/cytoscape-elk)
- Cytoscape.js can become sluggish with more than 10,000 elements and complex layouts or styling. This claim comes from a competitor (Linkurious Ogma). — [Ogma vs Cytoscape](https://doc.linkurious.com/ogma/latest/compare/cytoscape.html)
- Sigma.js renders with WebGL and is aimed at large graphs (about 100k nodes and edges cited by a blog). It is framework-agnostic and uses graphology for the model. These are secondary sources. — [Medium: rendering large network graphs](https://weber-stephen.medium.com/the-best-libraries-and-methods-to-render-large-network-graphs-on-the-web-d122ece2f4dc); [Cylynx comparison](https://dev.to/timlrx/a-comparison-of-javascript-graph-network-visualisation-libraries-34a8)
- React Flow suits editable node-based UIs. One user reports slowdowns above about 100 rich custom nodes (anecdotal). — [Reddit r/Frontend thread](https://axebps-redlib.hf.space/r/Frontend/comments/1khqfkq/best_tools_for_creating_interactive_ontology)
- React Flow ships official layout examples with elkjs (layered algorithm, ports) and dagre for trees. Stately uses React Flow (xyflow v12) with ELK. FINOS CALM Studio recorded an ADR choosing ELK for auto-layout. — [React Flow elkjs example](https://reactflow.dev/examples/layout/elkjs); [React Flow layouting guide](https://reactflow.dev/learn/layouting/layouting); [Stately pipeline](https://prod.stately.ai/docs/packages/graph/react-flow-elk-pipeline); [CALM ADR: use ELK](https://calm.finos.org/calm-studio/adrs/use-elk-for-auto-layout)
- Reactodia (`@reactodia/workspace`) is an open-source fork of the archived Ontodia, licensed LGPL-2.1-or-later. A ResearchSpace fork of Ontodia is GPL-3.0+. — [reactodia docs](https://reactodia.github.io/docs); [npm @reactodia/workspace](https://www.npmjs.org/package/@reactodia/workspace); [unpkg README 0.30.1](https://app.unpkg.com/@reactodia/workspace@0.30.1/files/README.md)
- There is no shared benchmark method across React Flow, Cytoscape.js and Sigma.js; benchmark with your own representative graph. — [dmccreary library analysis](https://dmccreary.github.io/graph-algorithms/library-analysis) (summary)

### Inferences (comparison; licence entries not cited above come from prior knowledge and are **unverified**)

| Library | Tree layout | Graph layout | Practical size | Click to edit / filter / style by data | Licence |
|---|---|---|---|---|---|
| Cytoscape.js | breadthfirst, dagre, ELK (mrtree, layered) via extensions | cose, fcose, ELK, cola | ~1k–10k elements comfortably | Selectors and data-mapped styles (e.g. `node[status="proposed"]`); filtering through collections; events | MIT (cited) |
| React Flow / xyflow | dagre, elkjs (official examples) | elkjs (external) | hundreds of rich nodes | Nodes are React components, so inline forms are natural; filter in app state | MIT (unverified) |
| Sigma.js + graphology | none built in (graphology layouts; ELK possible) | ForceAtlas2 | 10k–100k+ (WebGL) | Reducers style by attributes; less suited to inline editing | MIT (unverified) |
| Reactodia | built-in layouts | built-in layouts | moderate | RDF-aware: class/link types, property panels; customisable element templates | LGPL-2.1+ (cited) |
| elkjs | layered, mrtree | layered, force, stress | layout engine only (runs in a web worker) | n/a | EPL-2.0 (unverified) |
| D3 | d3-hierarchy tree/cluster | d3-force | depends (SVG/canvas) | anything, but you build it all | ISC (unverified) |
| vis-network | hierarchical layout | physics | ~ few thousand | groups/options by data | Apache-2.0 / MIT dual (unverified) |
| Mermaid | flowchart TD | flowchart, ER, class | small (static) | `classDef` colour by status at generation time; no live editing | MIT (unverified) |

- For OntologyBuilder: a table or queue view (F1, with evidence spans from the YAML evidence IDs), plus a Cytoscape.js or React Flow canvas with ELK for is-a trees and relation graphs (F2), data-driven styling (F4: approved / under review / proposed), and a level facet (F3). Forms generated from the LinkML schema (LinkML → JSON Schema → react-jsonschema-form) give F5. The backend writes YAML and makes a git commit or PR per decision batch, with role checks (F6). Mermaid output can go into PR descriptions for diff review.

### Gaps
- Official licence files for React Flow, Sigma.js, elkjs, D3 and vis-network were not fetched in this session.
- No independent benchmarks with ontology-like graphs (deep trees plus cross-links) were found.

## 5. Git-backed ontology or vocabulary editors with a web GUI

### Takeaway
Git-backed web tooling exists mainly as **publishing and validation on top of a git repository** (SkoHub Vocabs, VoCol, the ODK/OBO PR workflow in governance_process.md), not as rich web editors that write commits. WebProtégé has a GitHub integration service in development, but no released git-backed editing was confirmed. TurtleEditor (research) edits Turtle files in a GitHub repository from the browser.

### Cited Findings
- SkoHub Vocabs: you keep a SKOS vocabulary as Turtle on GitHub or GitLab. Branches and pull requests support review, and the vocabulary is published as a static site. The companion SkoHub Editor generates web forms from JSON Schema. — [SkoHub Vocabs blog](https://blog.lobid.org/2019/09/27/presenting-skohub-vocabs.html); [hbz/skohub-vocabs](https://github.com/hbz/skohub-vocabs); [SkoHub Editor blog](https://blog.lobid.org/2020/03/31/skohub-editor.html)
- VoCol / Git4Voc: collaborative vocabulary development with validation, querying, visualisation and documentation components on top of a standard git repository. — [Springer: VoCol](https://link.springer.com/doi/10.1007/978-3-319-49004-5_20) (summary)
- TurtleEditor: an ontology-aware web editor for Turtle files stored in a repository; GitHub's own web editor is a fallback. — [TurtleEditor paper (Zenodo)](https://zenodo.org/record/35499/files/paper.pdf) (summary)
- WebProtégé GitHub integration service (in development) and roadmap wishes. — [ecosyste.ms entry](https://awesome.ecosyste.ms/projects/github.com%2Fprotegeproject%2Fwebprotege-gh-integration-service); [Road Map](https://github.com/protegeproject/webprotege/wiki/WebProt%C3%A9g%C3%A9-Road-Map)
- Other web SKOS editors (iQvoc, ACDH Vocabs editor, ThesauRex) use a database; no git backend was confirmed. — [innoq/iqvoc](https://github.com/innoq/iqvoc); [ACDH Vocabs editor](https://vocabseditor.acdh.oeaw.ac.at/about); [ThesauRex](https://github.com/eScienceCenter/ThesauRex)
- schemasheets plus COGS sync Google Sheets with local files "using a git-like mechanism" (for LinkML schemas). — [schemasheets Google Sheets how-to](https://linkml.io/schemasheets/howto/google-sheets)

### Inferences
- The SkoHub pattern (files in git, PR as the approval step, CI renders previews) matches OntologyBuilder's "YAML in git is the source of truth". OntologyBuilder would add a web review UI that writes the PR on top of it. GitHub branch protection plus CODEOWNERS could map "domain admin" to required reviewers, as in the OBO/ODK workflow.

### Gaps
- No current (2025–2026) web editor was found that edits ontology files and opens PRs as a released, maintained product. VocBench has no documented git backend. Wikibase was not researched in this session (it is MediaWiki/database-backed, not git).
