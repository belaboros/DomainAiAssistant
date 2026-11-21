# Existing tools for building ontologies / knowledge graphs / taxonomies from a text corpus, with human review and governance

Research date: 2026-11-20. Target use case ("OntoBuilder"): ingest user manuals -> LLM-assisted extraction of terms, concepts, relations and rules -> propose higher-level concepts -> tag importance levels -> human review, authoring and approval -> final ontology.

Pipeline steps used in the coverage tables below:
**S1** ingest corpus · **S2** term/concept extraction · **S3** relation/rule extraction · **S4** propose higher-level concepts (generalisation/hierarchy) · **S5** importance levels / modularisation · **S6** human review and approval workflow · **S7** authoring/editing and formal ontology output (OWL/SKOS/RDF) · **P** provenance to source text · **C** contradiction/consistency detection.

## 1. Ontology editors and governance platforms: what do they cover, and how are they licensed?

### Takeaway
Commercial semantic platforms (Graphwise PoolParty, TopBraid EDG, metaphactory, Progress Semaphore, Stardog) now ship LLM "copilots" that suggest concepts and have governance workflows (voting, approval steps, term-level provenance). Only PoolParty (and partly Semaphore) has real **corpus analysis** that mines terms from documents. The open-source editors (Protégé/WebProtégé, VocBench 3, Fluent Editor) are good at authoring (S7) and collaboration (S6) but don't extract anything from text.

### Cited findings

**Graphwise (PoolParty + GraphDB), commercial**
- Semantic Web Company (PoolParty) and Ontotext (GraphDB) announced their merger on 2024-10-23 and formed Graphwise. The GraphDB and PoolParty brands continue, and the old names will eventually be folded into "Graphwise". — [KMWorld](https://www.kmworld.com/Articles/News/News/Semantic-Web-Company-and-Ontotext-merge-to-rebrand-as-knowledge-graph-and-AI-powerhouse-Graphwise-166526.aspx); [Blocks & Files](https://blocksandfiles.com/2024/10/23/graphwise/); [Graphwise blog](https://graphwise.ai/blog/graphwise-merger-swc-ontotext)
- PoolParty corpus analysis suggests terms and relations for building taxonomies, flags gaps in the taxonomy, offers RDF-based analysis via SPARQL, and provides co-occurrence statistics. — [PoolParty text corpus analysis](https://poolparty.biz/text-corpus-analysis)
- Each project has one corpus. The analysis produces concept lists and term scores. — [PoolParty Semantic Integrator](https://www.poolparty.biz/semantic-integrator)
- PoolParty Extractor scores terms by their relevance to the text rather than by raw frequency, and links extracted concepts to the thesaurus (with synonyms and multilingual labels). — [PoolParty Extractor](https://www.poolparty.biz/poolparty-extractor)
- Graphwise 10.2 (March 2026) replaced the concept tagging engine with a Lucene-based design that supports 40+ languages natively and rebuilds the extraction model automatically. — [Graphwise release page](https://graphwise.ai/?p=250401)
- The Graphwise Concept Extractor (UnifiedViews DPU, docs dated 2026-03-11) takes a Corpus ID to adjust scores using corpus analysis, plus an optional tf-idf weighting flag. — [Graphwise help: concept extractor](https://help.graphwise.ai/en/graph-automation/graphwise-unifiedviews/data-processing-units--dpus-/extractor-dpus/graphwise-concept-extractor.html)

**TopBraid EDG (TopQuadrant), commercial**
- EDG 8.3 (Feb 2025) introduced "AI-agent automation" for classifying and managing data. — [TopQuadrant EDG 8.3](https://www.topquadrant.com/blog/topquadrant-unveils-topbraid-edg-8-3-advancing-ai-agent-automation-data-governance-and-collaboration)
- EDG 8.5 added OWL file import and in-app creation of OWL classes. EDG Copilot uses AI and a built-in vector database for cross-collection linking. — [TopBraid EDG 8.5](https://www.topquadrant.com/?p=21009)
- EDG 9.2 added an option for voting workflows (one vote per governance role) and `sh:agentInstruction`, which gives declarative hints to agentic workflows. — [EDG 9.2 release notes](https://www.topquadrant.com/?p=23925)
- EDG 9.3 added human-in-the-loop approval steps for compliance-sensitive reviews, and an MCP server for AI-agent access. The notes call this the first piece of a broader unified AI assistant. — [EDG 9.3 release notes](https://www.topquadrant.com/?p=24889)

**metaphactory (metaphacts), commercial**
- 5.7 added term-level provenance and collaboration features for vocabulary governance. — [metaphactory 5.7](https://metaphacts.com/metaphactory-5-7)
- 5.8 introduced a built-in AI modeling agent for building, editing and managing semantic models. — [metaphactory 5.8](https://metaphacts.com/metaphactory-5-8)
- 5.9 re-architected the Semantic Modeling Assistant (powered by "metis") to make its changes more transparent and reliable. — [metaphactory 5.9](https://www.metaphacts.com/metaphactory-5-9-delivers-powerful-enhancements-to-power-trustworthy-ai-driven-knowledge-modeling-decision-making)
- 5.10 (Jan 2026) added modular ontology management, assistant support for reusing existing ontologies, and deprecation of ontology elements. — [metaphactory 5.10](https://metaphacts.com/metaphactory-5-10)
- 5.11 added a template-based Excel vocabulary importer and the first phase of real-time concurrent ontology editing. — [metaphactory 5.11](https://metaphacts.com/metaphactory-5-11)
- 6.0 (available from 2026-07-14) embeds the metis AI modeling assistant in the collaborative visual ontology editor. — [metaphactory 6.0](https://metaphacts.com/metaphactory-6-0)
- The AI-assisted modeling page describes the assistant suggesting classes and relations from curated ontology repositories (not explicitly from a document corpus). — [metaphacts AI-assisted modeling](https://metaphacts.com/solutions/semantic-knowledge-modeling/ai-assisted-modeling)

**Progress Semaphore, commercial**
- AI Model Builder (introduced in Semaphore 5.10, Aug 2024) suggests child concepts for a given parent, narrower terms, alternative labels and model structures. It requires human validation of the suggestions. 5.10.1 widened the choice of LLM providers. — [Progress blog: AI Model Builder](https://www.progress.com/blogs/how-to-boost-semantic-projects-with-semaphore-ai-model-builder); [Semaphore docs](https://docs.progress.com/bundle/semaphore-5-knowledge-model-management-how-to/page/topics/kmm-how-to/how-to-build-a-model/add-a-concept-ai-model-builder.html); [KMWorld on 5.10](https://www.kmworld.com/Articles/News/News/Progress-Semaphore-5.10-delivers-AI-assisted-quality-oriented-knowledge-modeling-165602.aspx); [Semaphore 5.10.1 blog](https://www.progress.com/blogs/model-smarter--not-harder-with-semaphore-5.10.1--boosting-productivity-and-insights)
- In advanced mode, users can change, add to or remove the information sent to the AI Model Builder. — [Progress blog](https://www.progress.com/blogs/how-to-boost-semantic-projects-with-semaphore-ai-model-builder)

**Stardog Designer + Voicebox, commercial**
- Voicebox for Designer is an agent that helps create an ontology, map data sources and refine the model, with human review of mappings. — [Stardog docs: guided ontology creation](https://docs.stardog.com/voicebox/guided-ontology-creation-and-mapping/)
- Voicebox turns plain-language descriptions into a Stardog data model, which can then be refined in Designer. Stardog says expressivity is limited and Designer is not meant to replace Protégé. — [Stardog blog](https://www.stardog.com/blog/stardog-voicebox-makes-building-data-models-dead-simple/)
- The Voicebox docs list a RAG pipeline for unstructured text, but its contents were not checked. — [Stardog Voicebox docs](https://docs.stardog.com/voicebox)

**VocBench 3, open source (BSD-3)**
- VocBench 3 was released publicly in Sept 2017 under BSD-3. — [FAO AIMS blog](https://aims.fao.org/activity/blog/vocbench-3-free-and-open-source-platform-editing-ontologies-thesauri-and-rdf-datasets)
- It is actively maintained: VocBench 15.1.2 and ShowVoc 6.1.2 were released 2026-07-16 (15.1.1 was mainly security updates). Interoperable Europe still lists 15.1 (2026-05-07) as the latest version. — [vocbench-user group](https://groups.google.com/g/vocbench-user/c/pjIfpsgPC3E); [Interoperable Europe](https://interoperable-europe.ec.europa.eu/it/node/720048/releases)
- Its design (multi-user, role-based, SKOS/OWL/OntoLex, with validation and history) is described in the Semantic Web Journal paper. — [SWJ: VocBench 3](https://journals.sagepub.com/doi/10.3233/SW-200370)

**WebProtégé / Protégé, open source**
- The GitHub releases page lists WebProtégé 4.0.2 (bug-fix release) and points end users to the hosted instance at webprotege.stanford.edu. — [protegeproject/webprotege releases](https://www.github.com/protegeproject/webprotege/releases)

**Fluent Editor (Cognitum), free**
- A Cognitum representative wrote in May 2025 that the tool is still used and downloaded dozens of times a day, and that the company is seeking funding for a new version, which it hopes to release as open source. — [Fluent Editor Google Group](https://groups.google.com/g/fluenteditor/c/TDgfpgEfF5A)
- Its controlled-English approach lets people author OWL without knowing OWL syntax. — [Habr review](https://habr.com/en/articles/173015)

### Inferences
- Coverage: PoolParty covers S1, S2, partly S4 (corpus-driven gap suggestions), S6 and S7. TopBraid EDG, metaphactory and Semaphore cover S4 (LLM suggestions), S6 and S7, but S1/S2 come only through LLM chat or import. VocBench and WebProtégé cover S6 (collaboration and roles) and S7 only.
- No vendor page describes **importance levels** for concepts (S5). metaphactory's "modular ontology management" is the closest match to modularisation.
- TopBraid EDG's SHACL foundation and VocBench's validation give constraint-based consistency checking (C), but not detection of contradictions *between source documents*.

### Gaps
- Pricing of the commercial platforms was not found (none publish it).
- Protégé desktop's latest release and LLM plugins (for example ChatGPT-based Protégé plugins), and the maintenance cadence of WebProtégé in 2025–2026, were not verified in this session.
- OntoStudio (semafora) status: no results. Possibly discontinued or niche. Unverified.
- Whether Stardog Voicebox can produce an ontology directly from documents (rather than from descriptions or structured sources) was not confirmed.

## 2. Text-to-ontology and text-to-KG tools: what do they cover?

### Takeaway
Text-to-ontology/KG tools split into three groups:
- **Research ontology tools** (OntoGPT/SPIRES, DRAGON-AI, OntoChat, Ontogenia, OntoKGen, OLLM). These are closest to "ontology" semantics.
- **LLM graph-extraction frameworks** (GraphRAG, Neo4j KG Builder, LangChain, LlamaIndex, KGGen, iText2KG, Cognee, Graphiti). These are built for RAG, not governed ontologies.
- **Commercial text-to-graph APIs** (Lettria Perseus, WhyHow, Diffbot).

The classic ontology-learning tools (Text2Onto, OntoGen) are legacy.

### Cited findings

**Classic ontology learning (legacy)**
- Text2Onto is a framework for automatic or semi-automatic generation of ontologies from text, and a redesign of TextToOnto (KIT/AIFB, c. 2005). — [Cimiano & Völker, Text2Onto](https://www.aifb.kit.edu/images/archive/2/21/20090816103033%212005_907_Cimiano_Text2Onto_-_A_F_1.pdf)
- OntoGen is a semi-automatic, data-driven editor for topic ontologies. A 2009 user study found only a handful of extraction tools publicly available (OntoGen, Text2Onto, TextToOnto). — [Manchester study](https://www.cs.man.ac.uk/~sjupp/publications/onto-learning/index.html); [Academia.edu copy](https://www.academia.edu/7715875/Can_Educators_Develop_Ontologies_Using_Ontology_Extraction_Tools_An_End_User_Study)

**OntoGPT / SPIRES (Monarch Initiative), open source**
- OntoGPT is a Python package for generating ontologies and knowledge bases with LLMs. It uses LiteLLM for model access. Its SPIRES method recursively prompts an LLM to fill a **user-defined schema** (LinkML) and grounds entities to identifiers in existing ontologies. — [SPIRES paper (arXiv 2304.02711)](https://arxiv.org/html/2304.02711v2); [Bioinformatics/PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10924283)
- SPIRES grounding maps to unique identifiers far more consistently than LLM querying alone. — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10924283)

**DRAGON-AI (part of CurateGPT), open source**
- It generates both textual and logical ontology components, using existing ontologies and unstructured text via RAG. It was evaluated on ten ontologies (J. Biomedical Semantics vol. 15, Oct 2024). The authors stress that expert curators and editors must drive the process. — [arXiv 2312.10904](https://arxiv.org/pdf/2312.10904); [JBMS DOI](https://api.crossref.org/works/10.1186%2FS13326-024-00320-3)

**OntoChat (King's College London), research prototype**
- It is a conversational LLM framework for the *requirements* phase: user stories -> competency questions (CQs) -> CQ filtering and analysis -> testing early ontology versions. It was evaluated by replicating the Music Meta Ontology. — [arXiv 2403.05921](https://arxiv.org/html/2403.05921v2)
- Users struggled to prompt it for user stories. A follow-up introduced participatory-prompting templates. — [arXiv 2408.15256 / AAAI-SS](https://arxiv.org/html/2408.15256v3)

**Other recent research (2024–2026)**
- OntoKGen (arXiv 2412.00608) is an interactive conversational interface. It takes a seed ontology or a description, uses an LLM with iterative chain-of-thought to extract an ontology, and generates a KG in Neo4j (domain: reliability and maintenance). — [arXiv 2412.00608](https://arxiv.org/pdf/2412.00608)
- Ontogenia / "Memoryless CQbyCQ" (arXiv 2503.05388) reports that o1-preview with Ontogenia produced ontologies the authors judged sufficient for engineers, and that it outperformed novice engineers. — [arXiv 2503.05388](https://arxiv.org/abs/2503.05388v1)
- OLLM (NeurIPS 2024) fine-tunes an LLM to generate a taxonomy backbone end to end from a domain corpus. It is fully automatic. — [arXiv 2410.23584](https://arxiv.org/pdf/2410.23584v1)
- OntoLearner (2026) is a modular Python library for ontology learning with LLMs. — [arXiv 2607.01977](https://arxiv.org/pdf/2607.01977)
- "Generative Ontology Induction" (2026) does domain-agnostic schema discovery from document corpora. — [arXiv 2607.16201](https://arxiv.org/pdf/2607.16201)
- LLM triplet extraction for automated ontology generation from software-engineering standards: a close analogue to technical manuals. — [arXiv 2509.00140](https://arxiv.org/html/2509.00140v1)

**LLM KG-construction frameworks (open source)**
- Microsoft GraphRAG: `graphrag prompt-tune` reads the corpus and generates domain-adapted extraction prompts. Entity-type discovery is on by default and can be switched to predefined types with `--no-discover-entity-types`. It produces entity/relation extraction prompts and community report prompts. Microsoft advises refining them by hand afterwards. — [GraphRAG auto prompt tuning](https://microsoft.github.io/graphrag/prompt_tuning/auto_prompt_tuning); [manual tuning](https://microsoft.github.io/graphrag/prompt_tuning/manual_prompt_tuning)
- Neo4j LLM Knowledge Graph Builder (Neo4j Labs): the schema can be predefined, taken from an existing DB, or suggested by the LLM from the text. Clean-up after extraction is configurable, and graph schema consolidation standardises labels. — [Neo4j Labs page](https://neo4j.com/labs/genai-ecosystem/llm-graph-builder); [Neo4j blog](https://neo4j.com/blog/developer/llm-knowledge-graph-builder/)
- neo4j-graphrag-python `SimpleKGPipeline`: the schema can be manual, auto-extracted once by the LLM, or "FREE". Structured output enforces conformance to the schema. The docs mark the feature experimental. — [neo4j-graphrag user guide](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html)
- LangChain `LLMGraphTransformer`: `allowed_nodes` / `allowed_relationships` (including (source, rel, target) tuples) and `strict_mode` (default True). A GitHub issue reports that the tuple constraints are not enforced in the generated pydantic model. — [LangChain reference](https://reference.langchain.com/python/langchain-neo4j/graph_transformers/llm/LLMGraphTransformer); [issue #24615](https://github.com/langchain-ai/langchain/issues/24615)
- KGGen (Stanford, NeurIPS 2025): an open-source Python package that extracts KGs from plain text and clusters and de-duplicates entities. It ships the MINE benchmark and claims better information retention than GraphRAG. — [arXiv 2502.09956](https://arxiv.org/html/2502.09956v2)
- A third-party 2025 benchmark measured knowledge retention for KGGen at 66% (GPT-4o) and 73% (Claude 3.5 Sonnet), against 83% for the authors' own method. It lists iText2KG as few-shot, general-domain and document-level. — [arXiv 2510.11297](https://arxiv.org/pdf/2510.11297)
- Cognee: an optional RDF/OWL ontology is parsed with RDFLib. Extracted entities and types are checked against it and matching nodes are marked valid. OWL classes become EntityType nodes. Cognee has **no ontology authoring** (it suggests using e.g. Protégé). — [Cognee docs: ontologies](https://docs.cognee.ai/core-concepts/ontologies); [Cognee ontology support](https://docs.cognee.ai/how-to-guides/cognee-sdk/ontology-support); [Cognee blog](https://www.cognee.ai/blog/deep-dives/grounding-ai-memory)
- Graphiti (Zep): custom entity and edge types are Pydantic models (no OWL input). Adding types to data already ingested means re-ingesting it. `excluded_entity_types` is supported. — [Graphiti custom entity types](https://help.getzep.com/graphiti/core-concepts/custom-entity-and-edge-types)

**Commercial text-to-graph services**
- Lettria Perseus: a fine-tuned text-to-graph model and SDK that returns entities, relations and **source attribution**. Its Ontology Toolkit proposes hierarchical classes and properties from domain documents. It is API-based (e.g. openCypher output for Amazon Neptune). Accuracy and speed figures are vendor-reported. — [Lettria Perseus](https://www.lettria.com/perseus); [Ontology Toolkit](https://lettria.com/blogpost/say-goodbye-to-manual-ontology-building-introducing-the-ontology-toolkit); [Toolkit v2 eval](https://www.lettria.com/blogpost/how-lettrias-ontology-toolkit-v2-outperforms-handcrafted-ontologies-an-evaluation); [AWS Builder Center](https://builder.aws.com/content/3BRTYfwNCdKrORxLPiOrvBqiqDv/building-knowledge-graphs-from-unstructured-text-with-lettria-perseus-and-amazon-neptune)
- WhyHow.AI Knowledge Graph Studio: open source (MIT), built on MongoDB, alongside a hosted enterprise offering. It offers schema-guided triple creation and a separate "Knowledge Table" tool. — [Medium: KG Studio](https://medium.com/enterprise-rag/whyhow-ai-kg-studio-platform-beta-rag-native-graphs-1105e5a84ff2); [ecosyste.ms listing](https://awesome.ecosyste.ms/projects/github.com%2Fwhyhow-ai%2Fknowledge-graph-studio); [SDK docs](https://whyhow-ai.github.io/whyhow-sdk-docs)

### Inferences
- OntoGPT/SPIRES and DRAGON-AI are the most "ontology-native" open-source options: schema-driven extraction, grounding to existing ontologies, OBO/OWL-oriented. They are biomedical by heritage but domain-agnostic in mechanism.
- RAG-oriented frameworks (GraphRAG, Neo4j, LangChain, LlamaIndex, KGGen, Graphiti) produce **instance graphs** (property graphs). They are good for S2/S3 and need a schema from elsewhere. They don't produce governed OWL/SKOS. GraphRAG's community reports and KGGen's clustering are useful signals for S4 (proposing higher-level groupings).
- Cognee is the only framework found that validates extraction against an OWL ontology. This matches a "approved ontology then guides re-extraction" loop.

### Gaps
- LlamaIndex `PropertyGraphIndex` / `SchemaLLMPathExtractor` details were not retrieved in this session (not searched successfully).
- No current sources were retrieved on Diffbot (commercial NLP API with a Knowledge Graph), txtai (open-source embeddings DB with graph features) or iText2KG's repository status.
- Whether OntoChat, OntoKGen and Ontogenia have maintained public repos in 2026 was not verified.
- Text2Onto and OntoGen: no official discontinuation notice found, but there are no signs of maintenance in any 2024–2026 source. Treat them as legacy.

## 3. Which tools support human-in-the-loop review, provenance, importance levels or modularisation, and contradiction detection?

### Takeaway
Review and approval workflows are mature only in the commercial governance platforms (TopBraid EDG, metaphactory, PoolParty, Semaphore) and in VocBench. Source-text provenance appears in Lettria (source attribution), metaphactory (term-level provenance) and, implicitly, in chunk-linked graphs (Neo4j KG Builder). **Importance levels** are not a first-class feature anywhere. Contradiction detection is limited to SHACL/OWL-reasoner consistency checks and research-stage "pitfall detectors".

### Cited findings
- TopBraid EDG has voting workflows with one vote per governance role (9.2) and human-in-the-loop approval steps (9.3). — [EDG 9.2](https://www.topquadrant.com/?p=23925); [EDG 9.3](https://www.topquadrant.com/?p=24889)
- metaphactory has term-level provenance (5.7), deprecation and modular ontology management (5.10), and concurrent editing (5.11). — [5.7](https://metaphacts.com/metaphactory-5-7); [5.10](https://metaphacts.com/metaphactory-5-10); [5.11](https://metaphacts.com/metaphactory-5-11)
- Semaphore AI Model Builder suggestions require human validation. — [Progress blog](https://www.progress.com/blogs/how-to-boost-semantic-projects-with-semaphore-ai-model-builder)
- Stardog Voicebox includes human review of generated mappings. — [Stardog docs](https://docs.stardog.com/voicebox/guided-ontology-creation-and-mapping/)
- Lettria Perseus returns source attribution with extracted entities and relations. — [Lettria Perseus](https://www.lettria.com/perseus)
- DRAGON-AI's authors state that expert curators must drive generation. — [arXiv 2312.10904](https://arxiv.org/pdf/2312.10904)
- LLM-generated ontologies show characteristic flaws that human modellers rarely produce: semantic redundancy, hierarchy conflicts and property-modelling artefacts. A pitfall detector has been proposed for them. — [CEUR Vol-4246 llms4kgoe-4](https://ceur-ws.org/Vol-4246/llms4kgoe-4.pdf)
- Extended NeOn-GPT pairs LLM drafts with automated verification and finds that expert-curated ontologies still outperform LLM-generated ones against gold standards. — [NeOn-GPT 2 (Southampton eprints)](https://eprints.soton.ac.uk/511839/1/neon_gpt_2_final.pdf)
- A 2025 systematic review names hybrid workflows that combine LLM automation with human expertise as a key open challenge. — [SWJ swj4001](https://www.semantic-web-journal.net/system/files/swj4001.pdf)
- A 2025 LLM-KG survey says semi-automated pipelines keep human experts at critical checkpoints. A study of human-LLM collaboration in ontology extension proposed a process framework. — [arXiv 2510.20345](https://arxiv.org/pdf/2510.20345); [CEUR Vol-4020 Paper 8](https://ceur-ws.org/Vol-4020/Paper_ID_8.pdf)
- KGGen's entity clustering and de-duplication addresses a part of consistency (duplicate concepts). — [arXiv 2502.09956](https://arxiv.org/html/2502.09956v2)
- The academic PERSEUS framework (Kansas State, unrelated to Lettria) verifies each extracted triple against source evidence. — [CEUR Vol-4246 llms4kgoe-5](https://ceur-ws.org/Vol-4246/llms4kgoe-5.pdf)

### Inferences
- HITL approval is available off the shelf (EDG, metaphactory, VocBench), but the reviewer is approving *edits to the ontology*, not *LLM-extracted candidates traced back to manual passages*. A candidate queue with evidence snippets per proposal would need custom work, or the use of PoolParty's corpus suggestions.
- "Importance levels" could be represented in SKOS/OWL as an annotation property (for example a custom `:importance` with values core/important/peripheral), or through modules or named graphs. No tool computes it. PoolParty term scoring and GraphRAG community structure could feed a heuristic.
- Contradiction detection *across manuals* (for example two manuals stating different rules) is not offered by any tool found. OWL reasoners and SHACL only detect logical inconsistency within the ontology itself.

### Gaps
- No source found describing a tool that assigns importance or criticality levels to ontology concepts.
- No product found that detects contradictions between source documents during ontology building.

## 4. Does anything cover the full use case end to end? What would need custom building?

### Takeaway
No single tool covers the whole pipeline (manuals -> LLM extraction with provenance -> higher-level concept proposals -> importance tagging -> review and approval -> formal ontology). The nearest commercial match is **Graphwise PoolParty** (corpus analysis + concept extraction + taxonomy governance) plus an LLM assistant. The nearest open-source combination is **OntoGPT/SPIRES or DRAGON-AI (extraction and generation) + VocBench 3 or WebProtégé (review and authoring)**, with custom glue for the candidate queue, provenance, importance levels and contradiction checks.

### Coverage matrix (based on the findings above; ✓ = documented, ~ = partial, – = not found)

| Tool | Licence | S1 ingest | S2 terms | S3 relations/rules | S4 higher-level | S5 importance/modules | S6 review/approve | S7 OWL/SKOS authoring | P provenance | C consistency |
|---|---|---|---|---|---|---|---|---|---|---|
| Graphwise PoolParty (+GraphDB) | Commercial | ✓ | ✓ (scored) | ~ (relation suggestions) | ~ (gap suggestions) | ~ (term scores) | ✓ | ✓ SKOS/OWL | ~ | ~ |
| TopBraid EDG | Commercial | – | ~ (Copilot) | ~ | ~ | – | ✓ voting/approval | ✓ OWL/SHACL | – | ✓ SHACL |
| metaphactory 6 | Commercial | ~ (Excel import) | ~ (AI assistant) | ~ | ✓ (assistant) | ✓ modular | ✓ | ✓ OWL/SHACL | ✓ term-level | ~ |
| Progress Semaphore | Commercial | – | – | – | ✓ (child concepts) | – | ✓ validation | ✓ | – | – |
| Stardog Designer/Voicebox | Commercial | ~ | ~ | ~ | ~ | – | ~ (mapping review) | ~ (limited expressivity) | – | – |
| VocBench 3 | OSS BSD-3 | – | – | – | – | – | ✓ (roles/validation) | ✓ | – | ~ |
| WebProtégé / Protégé | OSS | – | – | – | – | – | ~ (collab) | ✓ | – | ✓ reasoners (Protégé) |
| Fluent Editor | Free | – | – | – | – | – | – | ✓ (CNL) | – | ~ |
| OntoGPT / SPIRES | OSS | ✓ | ✓ (grounded) | ✓ (schema-driven) | – | – | – | ~ (LinkML/OWL output) | ~ | – |
| DRAGON-AI / CurateGPT | OSS | ✓ | ✓ | ✓ (logical defs) | ✓ | – | ~ (curator-driven) | ~ | – | – |
| OntoChat | Research | – | – (requirements) | – | – | – | ~ | – | – | ~ (CQ testing) |
| Microsoft GraphRAG | OSS (MIT) | ✓ | ✓ (type discovery) | ✓ | ~ (communities) | ~ (community levels) | – | – | ✓ (text units) | – |
| Neo4j LLM KG Builder | OSS (Labs) | ✓ | ✓ | ✓ | – | – | – | – (property graph) | ✓ (chunks) | ~ (schema consolidation) |
| LangChain LLMGraphTransformer | OSS | ~ | ✓ | ✓ | – | – | – | – | ~ | – |
| KGGen | OSS | ✓ | ✓ | ✓ | ~ (clusters) | – | – | – | – | ~ (de-dup) |
| Cognee | OSS (core) | ✓ | ✓ | ✓ | – | – | – | – (consumes OWL) | ~ | ✓ (validates against OWL) |
| Graphiti (Zep) | OSS | ✓ | ✓ | ✓ | – | – | – | – | ~ (episodes) | – |
| Lettria Perseus / Ontology Toolkit | Commercial | ✓ | ✓ | ✓ | ✓ (class hierarchy) | – | – | ~ | ✓ | – |
| WhyHow KG Studio | OSS (MIT) + hosted | ✓ | ✓ | ✓ | – | – | – | – | ~ | – |

(Provenance marks for GraphRAG, Neo4j and Graphiti are inferred from their chunk/text-unit/episode data models. They are not explicitly cited above.)

### Cited findings
- PoolParty combines corpus term suggestions, relation suggestions and gap detection with thesaurus management. — [PoolParty corpus analysis](https://poolparty.biz/text-corpus-analysis)
- Cognee expects the ontology to be authored elsewhere (e.g. Protégé) and only consumes it. — [Cognee ontology docs](https://docs.cognee.ai/core-concepts/ontologies)
- The 2025 HITL search found no single tool combining interactive generation, corpus extraction and governance. Ontogenia and OntoKGen were the closest interactive research prototypes. — [arXiv 2503.05388](https://arxiv.org/abs/2503.05388v1); [arXiv 2412.00608](https://arxiv.org/pdf/2412.00608)

### Inferences (what to custom-build for OntoBuilder)
1. **Candidate store with evidence**: each proposed term, concept, relation or rule keeps links to manual, section and page, the quoted span, the extractor/model version, and a confidence score. Off-the-shelf editors don't keep LLM candidates separate from approved ontology content.
2. **Rule extraction from procedural text** (warnings, constraints, "if X then Y" in manuals). Generic KG extractors produce triples, not rules. This needs a custom schema (e.g. a SPIRES/LinkML template for Rule, Condition, Action) and an output target (SHACL, SWRL or a rule annotation).
3. **Higher-level concept proposals**: combine LLM generalisation (DRAGON-AI style), embedding clustering (KGGen) and community detection (GraphRAG), with the reviewer accepting or rejecting each proposal.
4. **Importance levels**: a custom annotation scheme plus scoring heuristics (frequency/tf-idf as in PoolParty, centrality, safety-criticality keywords). Not supported anywhere.
5. **Review UI and workflow** (accept, edit, merge, reject, with an audit log). Either build a lightweight one or push approved candidates into VocBench 3 or WebProtégé (open source) or EDG/metaphactory (commercial) for formal governance.
6. **Contradiction detection across manuals**: compare candidate rules and relations from different sources (an LLM-as-judge plus OWL reasoner/SHACL on the merged ontology). No tool found does this.
7. **Export** to OWL/SKOS/Turtle, and a feedback loop where the approved ontology constrains the next round of extraction (Cognee/SPIRES pattern).

### Gaps
- No public benchmarks comparing these tools on technical or user-manual corpora specifically.
- Licences for some components (Cognee enterprise tier, Neo4j Labs app licence, Graphiti licence) were not verified in this session.
