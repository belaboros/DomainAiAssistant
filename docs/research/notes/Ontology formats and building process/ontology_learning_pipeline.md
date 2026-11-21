# Ontology Learning Pipeline: from Raw Text (e.g., User Manuals) to an Ontology — Classical and LLM-based Steps and Intermediate Artifacts

## Q1. What are the classical "ontology learning layer cake" steps and tools (Text2Onto, OntoGen)?

### Takeaway
The classical model (Buitelaar, Cimiano and Magnini, 2005) breaks ontology learning into stacked layers of increasing difficulty: terms → synonyms → concepts → concept hierarchy → relations → relation hierarchy → axiom schemata → general axioms. Each layer is a distinct intermediate artifact that the next layer consumes. Text2Onto showed how to store every learned object with a confidence score in a language-neutral model and how to update it incrementally when the corpus changes.

### Cited Findings
- The layer cake comes from the 2005 book *Ontology Learning from Text: Methods, Evaluation and Applications* (eds. Buitelaar, Cimiano, Magnini). It is modelled on Berners-Lee's Semantic Web layer cake: terms form the base, then synonyms, concepts, concept hierarchies and relations, with rules/axioms at the top — [Wikipedia: Ontology learning](https://www.wikipedia.org/wiki/Ontology_learning); [ACL J06-4009 book review](https://aclweb.org/anthology/J06-4009.pdf)
- Terms layer: learn the domain's relevant vocabulary. Synonym layer: find synonyms for the extracted terms. In practice this is mostly clustering terms that point to similar concepts — [Short Review for Ontology Learning, arXiv 2404.14991](https://arxiv.org/pdf/2404.14991); [Wikipedia](https://www.wikipedia.org/wiki/Ontology_learning)
- Concept layer: define each concept by its intension (definition), its extension (instances) and the lexical signs (terms) that refer to it. The lower layers extract terms, group synonyms under one concept, and then define the concept "both in intention and in extension" — [Wikipedia](https://www.wikipedia.org/wiki/Ontology_learning); [arXiv 2404.14991](https://arxiv.org/pdf/2404.14991)
- Criticism: at least one paper argues that splitting ontology learning into separate layers gives low-quality results. OLLM (NeurIPS 2024) also argues that solving subtasks in isolation misses how they interact — [arXiv 2404.14991](https://arxiv.org/pdf/2404.14991); [OLLM, arXiv 2410.23584](https://arxiv.org/abs/2410.23584v1)
- Text2Onto (Cimiano & Völker, NLDB 2005) stores learned knowledge as instantiated *modelling primitives* in a **Probabilistic Ontology Model (POM)**. Every learned object carries a confidence value, and the POM is independent of any target language, so it can be translated into any reasonably expressive KR formalism such as OWL or RDFS — [Text2Onto paper (KIT AIFB PDF)](https://www.aifb.kit.edu/images/archive/2/21/20090816103033%212005_907_Cimiano_Text2Onto_-_A_F_1.pdf); [KAON, Wikipedia](https://en.wikipedia.org/wiki/KAON)
- Text2Onto's **data-driven change discovery** updates the POM selectively when documents are added or changed, instead of reprocessing the whole corpus. It is a full redesign of the earlier TextToOnto — [Text2Onto paper](https://www.aifb.kit.edu/images/archive/2/21/20090816103033%212005_907_Cimiano_Text2Onto_-_A_F_1.pdf); [Bielefeld record](https://pub.uni-bielefeld.de/record/2497680)

### Inferences
- A data model for an OntologyBuilder app can mirror the layer cake directly. Each layer becomes an entity type: `Term`, `SynonymSet/TermVariant`, `Concept` (label + definition + instances + linked terms), `SubClassOf` edge, `Relation` (domain/range), `RelationHierarchy` edge, and `Axiom`. Each one carries a `confidence` and links back to its evidence, as in Text2Onto's POM.
- The POM idea suggests keeping an internal, format-neutral "candidate ontology" store and exporting OWL/Turtle/SKOS only at the end.
- Change discovery suggests making every artifact traceable to the documents and chunks it came from, so that re-ingesting one manual only re-derives the affected items.

### Gaps
- I did not reach the original 2005 book chapter, so the exact eight-layer naming (including "relation hierarchy" and "axiom schemata" vs "general axioms") comes from the task brief and secondary summaries rather than the primary text.
- I found no reliable detail on OntoGen (Fortuna et al.) in this search round. OntoGen is generally described as a semi-automatic, clustering-based topic-ontology editor, but that is unverified here.
- The full text of arXiv 2404.14991 could not be extracted (the PDF did not parse), so its specific per-layer technique lists are not cited.

## Q2. What do the classical methodologies (METHONTOLOGY, NeOn, Ontology Development 101, eXtreme Design/ODPs, competency questions, UPON Lite) contribute as steps and artifacts?

### Takeaway
The manual methodologies agree on one backbone: scope and requirements (competency questions), then a glossary of terms, then a taxonomy, then relations and attributes, then constraints and axioms, then instances, and finally testing against the requirements. They also name concrete intermediate documents (glossary, concept dictionary, binary-relations diagram, attribute tables, user stories, CQs) that an app can model as first-class artifacts.

### Cited Findings
- **Ontology Development 101** (Noy & McGuinness, Stanford, 2001) has seven steps:
  1. Determine the domain and scope (for example, "what is the domain that the ontology will cover?").
  2. Consider reusing existing ontologies.
  3. Enumerate important terms.
  4. Define the classes and the class hierarchy.
  5. Define the properties of classes (slots).
  6. Define the facets of the slots (constraints).
  7. Create instances.

  The process is iterative and steps may be revisited — [Ontology Development 101 (Protégé)](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html); [Ontology101 tutorial slides](https://protege.stanford.edu/conference/2004/slides/Ontology101_tutorial.pdf)
- Ontology 101 names three ways to build a hierarchy. **Top-down** starts from general classes. **Bottom-up** starts from the most specific classes and groups them into more general concepts. **Combination** defines the salient concepts first, then generalises and specialises them — [Ontology Development 101](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)
- **METHONTOLOGY**'s conceptualization activity turns an informal view of the domain into a semi-formal specification. It uses a set of *intermediate representations* (IRs) in tabular and graph notations, built in this order:
  1. Glossary of terms: concepts, instances, attributes and verbs, each with a natural-language definition.
  2. Concept taxonomy.
  3. Binary relations diagram.
  4. Concept dictionary.
  5. Attribute tables.

  Later substeps cover axioms, rules and instances — [Edinburgh KMM lecture L2](https://www.inf.ed.ac.uk/teaching/courses/kmm/PDF/L2-methodology.pdf); [Keet, Intro to Ontology Engineering §6.1](https://eng.libretexts.org/Bookshelves/Computer_Science/Programming_and_Computation_Fundamentals/An_Introduction_to_Ontology_Engineering_(Keet)/06%3A_Methods_and_Methodologies/6.01%3A_Methodologies_for_Ontology_Development); [METHONTOLOGY 2005 PDF](https://faculty.kutztown.edu/frye/secure/CSC480SW/Resources/Methontology2005.pdf)
- **UPON Lite** has six ordered steps, and each step produces a usable output on its own:
  1. Terminological lexicon.
  2. Domain glossary: the terms with textual descriptions and possible synonyms.
  3. Taxonomy: an ISA hierarchy.
  4. Predication: links property terms to the entities they describe.
  5. Parthood (meronymy).
  6. Not confirmed in the sources found (see Gaps).

  — [A Practical Application of UPON Lite, CEUR Vol-2835](https://ceur-ws.org/Vol-2835/paper7.pdf)
- **eXtreme Design (XD)** is iterative, test-driven and collaborative, and it reuses Ontology Design Patterns (ODPs), mainly *content patterns*. Each loop gathers requirements, locates and implements the ODPs that best fit them, then tests and validates the resulting components — [Pattern-based ontology design (OU)](https://oro.open.ac.uk/39265); [NeOn D2.5.2](https://research-archive.stem.open.ac.uk/stemra-data/uploads/sites/136/2025/03/NeOn_2010_D252.pdf)
- In XD, content-pattern requirements are expressed as **competency questions (CQs)**, contextual statements and reasoning requirements. CQs are obtained by generalising **user stories**. A well-documented ODP lists the CQs it answers, so the matching step pairs a cohesive group of CQs with a pattern — [NeOn D2.5.2 / Chapter 12](https://research-archive.stem.open.ac.uk/stemra-data/uploads/sites/136/2025/03/Chapter-12.pdf); [W3C ODP Tour](https://www.w3.org/2005/Incubator/decision/wiki/Decision_Incubator_Tools/ODP_Tour.html)
- CQs are natural-language questions that define an ontology's functional requirements. They are the usual requirements format in agile methods such as XD and SAMOD — [arXiv 2206.02485](https://arxiv.org/pdf/2206.02485v2.pdf); [Bench4KE, arXiv 2505.24554](https://arxiv.org/html/2505.24554v1)

### Inferences
- Methodology artifacts that map naturally onto app entities: `Scope/Purpose statement`, `UserStory`, `CompetencyQuestion` (with status: answered/unanswered, plus a test query), `GlossaryEntry` (term, definition, synonyms, kind = concept/instance/attribute/verb), `ConceptDictionaryEntry`, `BinaryRelation`, `AttributeTable`, `PatternApplication` (ODP used), `Instance`, and `TestResult`.
- UPON Lite's lexicon → glossary → taxonomy → predication → parthood order lines up closely with the layer cake. It is a good human-in-the-loop staging for a tool aimed at non-ontologists.
- Ontology 101's bottom-up strategy is effectively what an extraction pipeline does: generalise from specific terms found in manuals into higher-level classes.

### Gaps
- No primary source was retrieved for the **NeOn methodology** itself (its nine scenarios and the Ontology Requirements Specification Document, ORSD). It appears here only through XD/NeOn deliverables and NeOn-GPT (Q3).
- UPON Lite step 6 is not confirmed in the sources found.
- The METHONTOLOGY step list comes from lecture and secondary material, not from the original Fernández-López/Gómez-Pérez papers.

## Q3. What are the LLM-era approaches (2023–2026) and what do their pipelines and artifacts look like?

### Takeaway
LLM work falls into three families:
- **LLM-as-ontology-learner benchmarks.** LLMs4OL: term typing, taxonomy discovery, non-taxonomic relations, and Text2Onto (terms and types from raw documents).
- **LLM-assisted ontology engineering**, driven by requirements and competency questions: OntoChat, Ontogenia, NeOn-GPT, and multi-agent generators with reasoner/OOPS! repair loops.
- **LLM knowledge-graph construction from text**: GraphRAG, LangChain/LlamaIndex extractors, iText2KG, KGGen. These have well-specified intermediate artifacts (text units, entities, relationships, claims, communities) and put entity resolution and provenance at the centre.

### Cited Findings
**LLMs4OL (benchmark/challenge, TIB Hannover)**
- The original paper (Babaei Giglou et al., ISWC 2023) frames ontology learning for LLMs as three tasks: **Term Typing**, **Taxonomy Discovery** and **Non-Taxonomic Relation Extraction** — [LLMs4OL, arXiv 2307.16648](https://arxiv.org/pdf/2307.16648)
- The 2024 challenge (ISWC 2024) ran Task A, Term Typing (10 subtasks, 6 domains), Task B, Taxonomy Discovery, and Task C, Non-Taxonomic Relation Extraction (UMLS, GO, FoodOn). LLMs did well on term typing and taxonomy discovery, but **non-taxonomic relation extraction remained the hardest** — [LLMs4OL 2024 Overview, arXiv 2409.10146](https://arxiv.org/html/2409.10146v1)
- The 2025 challenge added a **Text2Onto** task: extract terms (A1) and their ontological types (A2) jointly from raw domain documents (Ecology, Scholarly, Engineering), scored by precision/recall/F1. Taxonomy Discovery gives a flat list of types and expects is-a parent–child pairs. One participant's best Text2Onto setup used retrieval-augmented few-shot prompting (Qwen3-Embedding neighbours, k=3) with structured output. For taxonomy discovery it used a cross-attention layer over type embeddings with a LoRA-fine-tuned small encoder. Reported term-extraction F1 was only ~0.44–0.65 — [LLMs4OL 2025 participant paper, arXiv 2508.19428](https://arxiv.org/html/2508.19428v1)
- Conflict: the task list for 2025 differs between sources. A search summary listed four core tasks (Text2Onto, Term Typing, Taxonomy Discovery, Non-Taxonomic Relation Extraction), while the participant paper describes three (A Text2Onto, B Term Typing, C Taxonomy Discovery) — [arXiv 2508.19428](https://arxiv.org/html/2508.19428v1). Check the official overview.
- A modular Python library, **OntoLearner**, exists for LLM-based ontology learning (2026) — [OntoLearner, arXiv 2607.01977](https://arxiv.org/pdf/2607.01977) (not read in detail).

**End-to-end taxonomy learning**
- **OLLM** (Lo, Jiang, Li, Jamnik; NeurIPS 2024) fine-tunes an LLM to generate whole *subgraphs* of the target ontology instead of single relations. A custom regulariser masks the loss on high-frequency concepts to reduce overfitting. It builds only the taxonomic backbone (concepts and is-a), with no axioms. On Wikipedia it beats subtask-composition baselines, and it was evaluated with new deep-learning-based graph-similarity metrics on Wikipedia and arXiv datasets. Code: andylolu2/ollm — [OLLM, arXiv 2410.23584](https://arxiv.org/abs/2410.23584v1); [NeurIPS 2024 poster](https://neurips.cc/virtual/2024/poster/94942)

**Requirements- and CQ-driven LLM ontology engineering**
- **OntoChat** is a conversational LLM agent for ontology requirements engineering. Its functions are **user-story creation, CQ extraction, CQ filtering and clustering, and ontology testing via verbalisation**. It was evaluated by replicating the Music Meta Ontology — [OntoChat, arXiv 2403.05921](https://arxiv.org/html/2403.05921v2); [Participatory prompting, arXiv 2408.15256](https://arxiv.org/html/2408.15256v3); [Bench4KE](https://arxiv.org/pdf/2505.24554)
- **Ontogenia** is a prompting technique that drafts OWL ontologies from user stories and CQs. With o1-preview it produced ontologies that met ontology engineers' requirements and significantly outperformed novice ontology engineers — [arXiv 2503.05388](https://arxiv.org/html/2503.05388v1)
- A study of reasoning models (DeepSeek, o1-preview) generated ontologies from **95 CQs across six domains** — [arXiv 2504.17402](https://arxiv.org/html/2504.17402v1)
- **NeOn-GPT** combines the NeOn methodology with GPT prompts to turn domain descriptions into OWL/Turtle ontologies. Its validation phase covers syntax, consistency and modelling pitfalls, using LLM-suggested fixes plus third-party tools. Its authors note that LLMs still lack the reasoning and domain precision to fully automate the task — [NeOn-GPT 2 (Soton eprint)](https://eprints.soton.ac.uk/511839/1/neon_gpt_2_final.pdf); [SWJ submission](https://semantic-web-journal.net/system/files/swj4014.pdf); [Bench4KE](https://arxiv.org/html/2505.24554v1)
- **Bench4KE** is a benchmark of gold-standard CQ sets from four real ontology projects, for evaluating automated CQ generation — [Bench4KE, arXiv 2505.24554](https://arxiv.org/pdf/2505.24554)

**KG construction from text with LLMs (artifact-rich pipelines)**
- **Microsoft GraphRAG** default dataflow:
  1. Compose **TextUnits**: chunks of 1,200 tokens by default, with configurable size, overlap and boundary handling.
  2. Link **Documents** to their TextUnits.
  3. **Graph extraction**: the LLM extracts **entities** (title, type, description) and **relationships** (source, target, description) per TextUnit as a subgraph. Entities with the same title and type are merged into an array of descriptions, which the LLM then summarises into one description. Relationships with the same source and target are merged the same way.
  4. Optional **claims/covariates**: positive factual statements about entities, with an evaluated status and time bounds. Off by default, and they usually need prompt tuning.
  5. **Graph augmentation**: hierarchical **Leiden community detection** produces **Communities**.
  6. **Community reports**: LLM summaries that reference key entities, relationships and claims, generated bottom-up.
  7. **Embeddings** of text units, entity descriptions and report content.

  TextUnits are referenced by the extracted items for provenance — [GraphRAG default dataflow (Microsoft)](https://microsoft.github.io/graphrag/index/default_dataflow)
- **LangChain `LLMGraphTransformer`** constrains extraction with `allowed_nodes` and `allowed_relationships`; the latter can be strings or (source, relation, target) tuples in v0.3. `strict_mode` (default True) filters out anything that does not match — [LangChain reference](https://reference.langchain.com/v0.3/python/experimental/graph_transformers/langchain_experimental.graph_transformers.llm.LLMGraphTransformer.html); [Neo4j guide](https://neo4j.com/developer/genai-ecosystem/importing-graph-from-unstructured-data/)
- **LlamaIndex `PropertyGraphIndex`** takes pluggable `kg_extractors`. `SchemaLLMPathExtractor` enforces a strict schema of allowed entity types, relation types, and which entities may connect through which relations. `DynamicLLMPathExtractor` takes `allowed_entity_types` and `allowed_relation_types`; when these are None, the LLM infers types on the fly — [LlamaIndex PG index guide](https://developers.llamaindex.ai/python/framework/module_guides/indexing/lpg_index_guide/); [Dynamic KG extraction](https://developers.llamaindex.ai/python/examples/property_graph/dynamic_kg_extraction/)
- **iText2KG** is zero-shot and incremental, with four modules: **Document Distiller → Incremental Entity Extractor → Incremental Relation Extractor → Graph Integrator**. It resolves entities and relations against semantically similar existing candidates as new documents arrive. The authors report lower false-discovery rates for unresolved entities than OpenAI Function, LangChain and LlamaIndex baselines, and note that resolution matters most with many chunks and complex unstructured text — [iText2KG, arXiv 2409.03284](https://arxiv.org/pdf/2409.03284)
- **KGGen** (NeurIPS 2025) extracts subject–predicate–object triples, then runs a **clustering** pass that merges nodes referring to the same entity and edges with equivalent meaning. This addresses the weak entity resolution and relation normalisation of OpenIE and GraphRAG. It ships with the **MINE** benchmark for KG usefulness — [KGGen, arXiv 2502.09956](https://arxiv.org/html/2502.09956v2)

### Inferences
- A practical LLM pipeline for user manuals, combining the above:
  1. `Document` → `Chunk`/`TextUnit` (with offsets).
  2. Per-chunk LLM extraction of `CandidateTerm`/`Mention`, `CandidateRelation` (triple) and optional `Claim`/`Statement` (with status/conditions).
  3. Entity resolution/canonicalisation into a `Concept` with `TermVariant`s and merged/summarised descriptions.
  4. Typing and taxonomy induction (`SubClassOf`).
  5. Non-taxonomic relations with domain/range.
  6. Clustering/communities into higher-level groupings.
  7. Axioms/rules.
  8. Validation against `CompetencyQuestion`s.
- Provenance should be stored as links from every mention, statement and concept to the `TextUnit`/`Document` (and ideally the character span) it came from. GraphRAG does this at TextUnit level. Span-level offsets are an inference, not a documented GraphRAG feature.
- Schema-guided extraction (LangChain/LlamaIndex allowed types) fits a mode where the ontology so far is fed back as the extraction schema. Open extraction fits a first pass. A builder app likely needs both modes.
- The weak LLMs4OL results on non-taxonomic relations and the ~0.44–0.65 F1 on term extraction suggest building human review into those stages.

### Gaps
- I did not verify span-level (character offset) provenance in any of the cited tools. The GraphRAG docs only confirm TextUnit-level references, and the exact field name (`text_unit_ids`) was not confirmed on the page read.
- No primary source was retrieved for a comprehensive 2024–2026 survey of "LLM-assisted ontology engineering". Findings come from individual papers.
- No source was found on prompting patterns specific to user manuals or other procedural/technical text.

## Q4. How are higher-level concepts and rules abstracted from extracted items (taxonomy induction, clustering)?

### Takeaway
Abstraction happens in three ways:
- **Grouping**: synonym clustering, entity-resolution clustering, graph community detection.
- **Hierarchy induction**: is-a pair classification (LLMs4OL Task B/C), whole-subgraph generation (OLLM), bottom-up generalisation (Ontology 101).
- **Summarisation of groups** into higher-level descriptions: GraphRAG community reports.

The sources found say little about rule or axiom induction.

### Cited Findings
- In the layer cake's synonym layer, terms associated with similar concepts are clustered together — [Wikipedia: Ontology learning](https://www.wikipedia.org/wiki/Ontology_learning)
- KGGen clusters nodes and edges after extraction to merge equivalent entities and relations — [KGGen](https://arxiv.org/html/2502.09956v2)
- GraphRAG applies hierarchical Leiden clustering to the entity graph and writes LLM reports per community, bottom-up, so higher levels summarise their child communities — [GraphRAG dataflow](https://microsoft.github.io/graphrag/index/default_dataflow)
- Taxonomy discovery as a task: given a flat list of types, predict is-a pairs. One strong 2025 approach scored candidate pairs with cross-attention over type embeddings plus sparsity-matched thresholding — [arXiv 2508.19428](https://arxiv.org/html/2508.19428v1)
- OLLM generates whole taxonomy subgraphs, avoiding error compounding from pairwise decisions — [OLLM](https://arxiv.org/abs/2410.23584v1)
- Ontology 101's bottom-up and combination strategies generalise specific classes into broader ones — [Ontology Development 101](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)

### Inferences
- In the app, a "propose generalisation" step can take a community or cluster of concepts and ask the LLM for a parent concept with a definition and a `SubClassOf` edge, marked as `proposed`, with links to the member concepts as evidence.
- Communities (GraphRAG-style) are useful as a *navigation/grouping* artifact, but they are not the same as is-a classes. The data model should keep `Cluster/Community` separate from `Concept`.

### Gaps
- No sources were retrieved on classical lexico-syntactic taxonomy induction (Hearst patterns, formal concept analysis), even though Text2Onto-era systems relied on them.
- No source found on LLM-based **axiom/rule induction** from text (e.g., disjointness, cardinality, conditional rules in manuals).

## Q5. How are extracted ontologies evaluated (gold standards, CQ answering, OOPS!, reasoners)?

### Takeaway
Evaluation combines four kinds of check:
- **Gold-standard comparison**: precision/recall/F1 on terms, types and is-a pairs, or graph-similarity metrics.
- **Requirement checks**: CQs turned into SPARQL and run against the ontology.
- **Structural/logical checks**: syntax via RDFLib, OWL reasoners such as HermiT, SHACL, and the OOPS! pitfall scanner.
- **Human or LLM-judge review.**

Recent LLM pipelines wrap these checks in iterative repair loops.

### Cited Findings
- LLMs4OL tasks are scored with precision/recall/F1 against gold ontologies (OBI, MatOnto, SWEET, DOID, Schema.org, FoodOn, PO, and others) — [arXiv 2508.19428](https://arxiv.org/html/2508.19428v1); [LLMs4OL 2024 overview](https://arxiv.org/html/2409.10146v1)
- OLLM introduced deep-learning-based metrics comparing generated and ground-truth graphs semantically and structurally — [OLLM](https://arxiv.org/abs/2410.23584v1)
- The **OOPS!** catalogue was built from an empirical analysis of over 693 ontologies. Pitfalls fall into Structural, Functional and Usability-Profiling dimensions, each with an importance level (critical, important, minor). OOPS! cannot detect pitfalls that depend on the domain or on a particular ontology's requirements. A 2013 paper reports that it automatically detected 21 catalogued pitfalls, and pitfalls P25–P29 were added later. It is hosted at oops.linkeddata.es — [Poveda-Villalón et al., IJSWIS 10(2) 2014](https://econpapers.repec.org/RePEc:igg:jswis0:v:10:y:2014:i:2:p:7-34); [Keet et al. 2013, The Current Landscape of Pitfalls](https://www.scitepress.org/Papers/2013/45179/)
- **MASEO** is a multi-agent ontology generator working from CQs. It includes a syntax-repair agent (RDFLib), a logical-consistency agent running the **HermiT** reasoner, and OOPS! pitfall checks — [CEUR Vol-4246 llms4kgoe-7](https://ceur-ws.org/Vol-4246/llms4kgoe-7.pdf)
- A neuro-symbolic drafting pipeline combines LLM drafting with **SHACL validation, OWL/DL reasoning and CQ testing** in a repair loop. Iterative repair helped only under *conservative* stopping policies, and aggressive CQ-driven repair made results *worse* — [CEUR Vol-4246 llms4kgoe-6](https://ceur-ws.org/Vol-4246/llms4kgoe-6.pdf)
- A 2026 multi-agent text-to-ontology system was evaluated with a panel of LLM judges and **CQ-driven SPARQL** evaluation. It reported better structural quality than a single-pass baseline — [arXiv 2604.23090](https://arxiv.org/html/2604.23090v1)
- OntoChat tests ontologies by verbalising them and checking them against CQs — [Elenchus/Bench4KE summaries; OntoChat arXiv 2403.05921](https://arxiv.org/html/2403.05921v2)

### Inferences
- Evaluation artifacts for the app: `CompetencyQuestion` → `TestQuery` (SPARQL) → `TestRun` (pass/fail, answer); `ValidationIssue` (source = reasoner/SHACL/OOPS!/LLM-judge, severity critical/important/minor, affected element); and `GoldStandard` comparison scores when a reference ontology exists.
- The finding that repair loops can make things worse suggests the app should keep versions or snapshots of the ontology and require review before auto-repairs are accepted.

### Gaps
- No quantitative cross-study comparison of these evaluation methods was found.
- The current size of the OOPS! catalogue and the live status of its web service were not confirmed.

## Q6. How can contradictions, ambiguity, terminology drift and gaps across documents be detected?

### Takeaway
Little work targets this specifically for ontology building or technical manuals. The closest evidence comes from cross-document contradiction detection in RAG and corpus-level inconsistency detection. These show the task is hard for LLMs and that structuring claims as a graph helps. Gap detection maps naturally onto unanswered competency questions, and contradiction detection onto reasoner inconsistency and conflicting claims.

### Cited Findings
- The **MAGIC** benchmark builds inter-context conflicts from knowledge-graph subgraphs. It finds that even advanced LLMs struggle with subtle cross-document inconsistencies — [MAGIC, arXiv 2507.21544](https://arxiv.org/html/2507.21544v3)
- An evaluation of LLMs as context validators covered self-contradictory documents, contradicting document pairs, and conditional contradictions across three documents. Detection is hard, performance varies by contradiction type, and larger models generally do better — [Contradiction Detection in RAG Systems, arXiv 2504.00180](https://arxiv.org/html/2504.00180v1)
- **CLAIRE** (Stanford, EMNLP 2025) is an agentic, retrieval-backed system that flags potentially inconsistent claims across a corpus (Wikipedia) for human review. It also explains specialised terminology to the reviewer — [Detecting Corpus-Level Knowledge Inconsistencies, arXiv 2509.23233](https://arxiv.org/html/2509.23233v1); [EMNLP 2025 PDF](https://almond-static.stanford.edu/papers/emnlp2025_inconsistency_detection.pdf)
- GraphRAG's claims carry an *evaluated status* and *time bounds*, which allows conflicting or time-limited statements to be represented — [GraphRAG dataflow](https://microsoft.github.io/graphrag/index/default_dataflow)
- OWL reasoners (HermiT) are used to detect logical inconsistency in generated ontologies — [CEUR llms4kgoe-7](https://ceur-ws.org/Vol-4246/llms4kgoe-7.pdf)

### Inferences
- **Contradictions**: store atomic `Statement`s with conditions or context (product version, model, section) and provenance. Flag pairs with the same subject and predicate but incompatible objects. Use reasoner unsatisfiability for axiom-level conflicts.
- **Ambiguity**: a `Term` linked to more than one `Concept` (polysemy), or a concept with a low-confidence definition.
- **Terminology drift**: several `TermVariant`s for one `Concept` spread unevenly across documents or versions. Entity-resolution output (KGGen/iText2KG-style clusters) is the raw material for this.
- **Gaps**: competency questions that cannot be answered, concepts with no definition or no parent, relations without domain/range, and OOPS! pitfalls such as missing annotations.
- These are design inferences, not sourced practices for manuals.

### Gaps
- No source was found that addresses terminology drift or contradiction detection in technical documentation or user manuals specifically.
- A 2026 preprint on inconsistencies across text, tables and KGs ([arXiv 2607.25959](https://arxiv.org/pdf/2607.25959)) was found but not read.
