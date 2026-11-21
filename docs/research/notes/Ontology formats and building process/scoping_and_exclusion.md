# Scoping an Ontology Built from Text: What to Exclude and How to Tier by Importance

## Scoping methods: ORSD/NeOn, competency questions, purpose/scope/users, TBox vs ABox, universals vs particulars, procedural vs declarative

### Takeaway
The standard scoping tools all tie the ontology to a stated purpose. NeOn's ORSD and Noy and McGuinness's Ontology 101 both record purpose, intended uses, end users, and competency questions (CQs), and use them as the "litmus test" for what goes in. Two distinctions draw the line for exclusion in a principled way. One is TBox (terminology, schema-like) versus ABox (assertions about concrete situations). The other is the BFO/OBO rule that ontology terms denote universals/types, while particulars belong to data. Procedural "how-to" knowledge is generally treated as a separate kind of knowledge with its own ontologies (PROHOW, PKO), not as part of a declarative domain ontology.

### Cited Findings
- **ORSD purpose.** The ontology requirements specification activity "is to state why the ontology is being built, what its intended uses are, who the end-users are, and which requirements the ontology should fulfill." The ODBASE 2009 paper by Suárez-Figueroa, Gómez-Pérez and Villazón-Terrazas systematizes the activity into guidelines for producing the ORSD — [Springer, How to Write and Use the ORSD](https://link.springer.com/doi/10.1007/978-3-642-05151-7_16); [NeOn D5.4.1](https://research-archive.stem.open.ac.uk/stemra-data/uploads/sites/136/2025/03/NeOn_2008_D5.4.1.pdf)
- **CQs as requirements.** "Most of the existing methodologies suggest the identification of competency questions (CQs) as the technique for establishing the ontology requirements." CQs are natural-language questions the ontology must answer, and they are agreed between ontology engineers, users and domain experts — [NeOn ORSD paper, via search snippet](https://link.springer.com/doi/10.1007/978-3-642-05151-7_16)
- **ORSD template slots.** The template has general (non-functional) requirements with optional priorities. Its functional requirements are groups of CQs with their answers, each with optional priorities per group and per CQ. A **pre-glossary of terms** lists the terms extracted from the CQs and their answers, with their frequencies. (The CQ-derived pre-glossary is a natural "in-scope" seed list.) — [NeOn ORSD paper](https://link.springer.com/doi/10.1007/978-3-642-05151-7_16)
- **A recent ORSD application.** DAOnt (EU Data Act ontology, 2026) built its ORSD with NeOn. It split its CQs into general-coverage and article-specific sets, and validated them with OWL reasoners and SPARQL — [arXiv 2604.16386](https://arxiv.org/pdf/2604.16386)
- **Ontology 101 step 1.** Determine domain and scope by asking what domain the ontology covers, what it will be used for, what questions it should answer, and who will use and maintain it. "The answers to these questions may change during the ontology-design process, but at any given time they help limit the scope of the model." — [Noy & McGuinness, Ontology Development 101](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)
- **Explicit exclusion principle.** "The ontology should not contain all the possible information about the domain: you do not need to specialize (or generalize) more than you need for your application." The wine example: "we do not need to know what paper is used for the labels or how to cook shrimp dishes." Concepts for managing winery inventory or restaurant employees are also left out, although related — [Ontology 101](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)
- **CQs as a litmus test.** The CQs "will serve as the litmus test later: Does the ontology contain enough information to answer these types of questions?" They are a sketch and need not be exhaustive — [Ontology 101](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)
- **Class or instance.** "Individual instances are the most specific concepts represented in a knowledge base." "The level of granularity is in turn determined by a potential application of the ontology." "If concepts form a natural hierarchy, then we should represent them as classes." — [Ontology 101 §4.6](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)
- **Class or property value.** Create a new class when the distinction matters elsewhere in the model; "Otherwise, we represent the distinction in a slot value." "Usually numbers, colors, locations are slot values and do not cause the creation of new classes." — [Ontology 101 §4.5](https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html)
- **TBox vs ABox.** A description logic knowledge base "typically comes in two parts: a terminological and an assertional one" (TBox and ABox). The TBox "represents knowledge about the structure of the domain (similar to a database schema), while the ABox represents knowledge about a concrete situation" — [Baader, Horrocks & Sattler, Handbook of KR ch. 3](https://www.cse.sc.edu/~mgv/csce781sp13/presentations/BaHS07a.pdf); [Baader et al., An Introduction to Description Logic (Cambridge excerpt)](https://assets.cambridge.org/97805218/73611/excerpt/9780521873611_excerpt.pdf)
- **Realism behind the OBO Foundry.** Metaphysical realism is "the doctrine according to which universals or types exist in reality," and is the methodology behind the OBO Foundry — [Smith & Ceusters, Ontological Realism (philarchive)](https://philarchive.org/archive/SMIORA-2)
- **Universals vs particulars in BFO.** "Particulars are individual denizens of reality restricted to specific times and places, which instantiate universals, but which cannot be instantiated. Universals are repeatable across time and space." Ontology terms such as those in the Gene Ontology "refer to types; experiments carried out by biologists in their labs refer to corresponding instances" — [BFO-related papers on philarchive](https://philarchive.org/archive/SMIBOv2); [ICBO 2019 paper 16](https://ceur-ws.org/Vol-2931/ICBO_2019_paper_16.pdf)
- **Critique of strict realism.** The strict reading, that all classes must be Aristotelian universals with instances, has costs. Hoehndorf's example: an electron can be a class, but under this rule a Higgs boson could not be one until instances were found (FOIS 2010). His workaround reifies classes as information about types — [Realism for Scientific Ontologies (slides)](https://www.slideshare.net/slideshow/realism-for-scientific-ontologies/4127608). Seyed & Shapiro note there are "no formal, principled criteria that a candidate ontology must meet for ratification" — [ICBO 2011](https://cse.buffalo.edu/~shapiro/Papers/seysha2011a)
- **Procedural knowledge as its own kind.** Pareti's PROHOW work focuses on "procedural knowledge, or in other words, 'how humans do things', and in particular on step-by-step instructions". It contrasts this with declarative knowledge, which resources like DBpedia and ConceptNet already cover well. PROHOW has represented over 200,000 sets of instructions as Linked Data — [Pareti, UKON 2016](https://ce.ncl.ac.uk/media/sites/conferencewebsites/ukon2016/UKON_2016_paper_8.pdf); [arXiv 1410.8808](https://arxiv.org/pdf/1410.8808v1.pdf)
- **A dedicated procedure ontology.** The Procedural Knowledge Ontology (PKO) was built "to enable the explicit modeling of procedures and their executions," reusing existing ontologies — [arXiv 2503.20634](https://arxiv.org/abs/2503.20634)

### Inferences
- These sources map directly onto the app's "ignorable" bucket. Personal stories, specific recipes, concrete CLI invocations and one-off incidents are particulars/ABox content (instances in a concrete situation), so they fall outside a TBox-style domain ontology by both the DL and BFO criteria.
- Procedures (how-to steps, CLI command sequences) can be excluded from the declarative ontology on principled grounds, because the literature models them as a separate kind of knowledge (PROHOW/PKO). A useful middle ground: keep the *types* of task or action ("deploy an app", "house-train a puppy") as level-2 concepts and drop the step-by-step instance.
- The ORSD's CQ priorities and the pre-glossary term frequencies are a ready-made mechanism for tiering. Terms appearing in high-priority CQs suggest L1/L2, and terms appearing only in low-priority or edge-case CQs suggest L3.
- Ontology 101's class-versus-property-value rule gives a second exclusion filter. Colors, numbers, locations and version numbers should usually be attributes, not concepts.

### Gaps
- I did not retrieve the full ORSD template text or its exact guideline steps; details beyond the snippets need the primary PDF.
- I found no source that explicitly defines a "level-1/2/3" importance tiering inside an ORSD. CQ priorities are optional and coarse.

## Criteria and term-extraction measures for excluding content

### Takeaway
Automatic term recognition (ATR) supplies statistical filters that separate domain terms from general vocabulary and noise. C-value/NC-value handles termhood for multi-word, nested terms. Weirdness and domain specificity compare frequency in the domain corpus against a general reference corpus. OntoLearn's domain relevance and domain consensus measures require a term to be both distinctive to the domain and evenly spread across many documents. Together these give principled grounds to drop terms that are generic, idiosyncratic to one document (anecdotes), or rare.

### Cited Findings
- **C-value/NC-value** (Frantzi, Ananiadou & Mima, Int. J. Digital Libraries 3:115–130, 2000) is a domain-independent method for extracting multi-word terms that combines linguistic and statistical information. C-value enhances frequency of occurrence so that it is sensitive to nested terms (it uses a log of candidate length weighted by frequency, discounted for nesting). NC-value adds context words that tend to appear with terms. C-value improved extraction of nested terms, and NC-value improved multi-word term extraction in general — [Springer](https://link.springer.com/article/10.1007/s007999900023); [Ananiadou PDF](https://personalpages.manchester.ac.uk/staff/sophia.ananiadou/GIW00P106.pdf)
- **Contrastive termhood measures.** Periñán-Pascual lists TF-IDF (Singhal et al. 1996), C-value (Frantzi & Ananiadou 1996), Weirdness (Ahmad et al. 2000) and Domain-Specificity (Park et al. 2002) as termhood statistics, and notes that many rely on differences between the target corpus and a general-language reference corpus — [Periñán-Pascual, Terminology 21:2](https://benjamins.com/catalog/term.21.2.02per)
- **Weirdness** (Ahmad et al., University of Surrey, TREC-8) compares a word's normalised frequency in the specialist corpus with its frequency in a general-language reference corpus, roughly (w_s/t_s)/(w_g/t_g). High scores flag domain-distinctive words — [Ahmad, Gillam & Tostevin, TREC-8](https://trec.nist.gov/pubs/trec8/papers/surrey2.pdf); formula via [blog summary](https://andersonmorillo.github.io/post/extract-important-words-weirdness) (secondary source). Kit & Liu (2007) propose a rank-difference variant that compares rank in the domain corpus with rank in a background corpus — [Liu & Kit, PACLIC 22](https://waseda.repo.nii.ac.jp/record/29046/files/PACLIC_22_Liu.pdf)
- **OntoLearn** (Navigli & Velardi, Computational Linguistics 30:2, 2004) applies three filters to terminology:
  - **Domain relevance** compares a term's frequency in the target domain with its distribution across contrastive domain corpora.
  - **Domain consensus** requires the term to appear across several documents. It is entropy-based, so a good term is roughly uniformly distributed across the domain's documents, and it is meant to "simulate specialist consensus on concepts choice".
  - **Contrastive corpora and glossaries** prune terminology that is not domain-specific.
  
  — [Navigli & Velardi 2004](https://direct.mit.edu/coli/article/30/2/151/1851/Learning-Domain-Ontologies-from-Document); [ACL J04-2002](https://preview.aclanthology.org/fix_video/J04-2002.pdf)
- **Consensus across a community.** In related work by Missikoff, Navigli and Velardi, candidate concepts are "selected among the terms that are frequently and consistently referred in the documents produced by the virtual community," and the ConSys tool supports human validation — [Navigli/Velardi related papers](https://link.springer.com/content/pdf/10.1007/3-540-48005-6_6.pdf)
- **Instance-level and volatile content.** The two scoping principles in the first section, Ontology 101's "should not contain all the possible information" and the TBox/ABox and universals/particulars distinctions, are the principled grounds in the literature for excluding instance-level facts.

### Inferences
- **Domain consensus is a natural anecdote filter.** A personal story's vocabulary (a dog's name, a specific trip) is concentrated in one document, so it gets low entropy and low consensus.
- **Weirdness/domain relevance against a general reference corpus filters generic words** ("thing", "use", "time"). It can also over-promote rare jargon, such as CLI flags or product SKUs, which score as highly "weird". A separate instance-versus-type check (named entity, code literal, version string) is therefore needed. I found no source that names this interaction; it is my reasoning.
- **A practical exclusion checklist**, synthesized from the cited principles:
  - (a) Named individual or particular → ABox, so ignore.
  - (b) Step sequence, command or recipe → procedural, so ignore or keep only its task type.
  - (c) Numeric, colour, version or location attribute → property value, not a concept.
  - (d) Low consensus (one-document) term → candidate anecdote.
  - (e) Low domain relevance (general language) → drop.
- **Version-specific or ephemeral facts** (e.g., UI labels in a given product release) have no direct treatment in these sources. They fit the particular/ABox side, and also fail domain consensus across manual versions.

### Gaps
- I found no source dedicated to excluding "opinions", "examples" or "ephemeral/version-specific facts" in ontology learning. Those criteria are inferred, not sourced.
- I could not verify the exact OntoLearn DR/DC formulas (the snippets were garbled), nor find an authoritative primary statement of the weirdness formula.
- Unithood was not covered by the retrieved sources.

## Techniques for ranking concepts by centrality and importance

### Takeaway
Three bodies of work support tiering. Rosch's basic-level categories predict which abstraction level people find most informative and natural. Guarino's top-level / domain / task / application layering gives an abstraction-based stratification. Ontology summarization research ranks concepts by combining graph centrality, density, coverage, name simplicity and popularity. The main example is Peroni, Motta & d'Aquin's Key Concept Extraction, which correlated strongly with expert choices.

### Cited Findings
- **Rosch et al. 1976** ("Basic Objects in Natural Categories", Cognitive Psychology 8:382–439). In taxonomies of concrete objects, one level of abstraction (e.g., *chair*, *car*) carries the most information, has the highest cue validity, and is most differentiated from other categories. Feature listing found that basic-level categories had about 8 category-wide attributes on average, versus few for superordinates such as *furniture*. People name objects at the basic level, recognize basic-level objects fastest, and interact with members of basic-level categories in similar motor ways — [Rosch et al. 1976 PDF](https://www.cns.nyu.edu/~msl/courses/2223/Readings/Rosch-CogPsych1976.pdf)
- **Expertise shifts the basic level.** Tanaka & Taylor (1991) argue that the basic level depends on the perceiver's domain expertise — [Tanaka & Taylor 1991](https://www.ece.uvic.ca/~bctill/papers/learning/Tanaka_Taylor_1991.pdf). Corter & Gluck (1992) ground basic-level effects in patterns of feature co-occurrence — [Corter & Gluck 1992](https://brainhealth.rutgers.edu/wp-content/uploads/2022/04/Corter-Gluck-1992.pdf)
- **Guarino (FOIS 1998)** separates top-level, domain, task and application ontologies:
  - Top-level ontologies cover general, domain-independent categories.
  - Task ontologies cover a generic task or activity, like diagnosing or selling.
  - Application ontologies cover concepts that depend on both a domain and a task.
  
  Task ontologies are rarely addressed in practice. These definitions come from Borgo et al.'s 2018 commentary; I did not verify the exact 1998 wording — [Guarino 1998 PDF](https://www.loa.istc.cnr.it/wp-content/uploads/2020/03/FOIS98.pdf); [IOS Press commentary](https://ebooks.iospress.nl/volumearticle/51434)
- **Peroni, Motta & d'Aquin 2008, Key Concept Extraction (KCE)** identifies the concepts that best summarize an ontology by combining:
  - **Natural categories** (Rosch-inspired; favours simple labels and penalizes compound names).
  - **Density** (number of subclasses, properties and instances; global and local variants).
  - **Coverage** (the selected set should cover all parts of the hierarchy; the covered set of a concept is the concept plus its sub- and superclasses).
  - **Popularity** (number of web search hits for the concept name).
  
  The latest version showed strong correlation with the key concepts chosen by human experts. KCE powers the KC-Viz ontology navigation tool — [Peroni et al. 2008 PDF](https://research-archive.stem.open.ac.uk/stemra-data/uploads/files/Paper191.pdf); [ORO record](https://oro.open.ac.uk/23484); [KMi KCE page](https://kmi.open.ac.uk/technologies/name/kce)
- **Survey of measures.** The ontology summarization survey (arXiv 1801.01937) catalogues these assessment measures: degree, closeness, betweenness, bridging, harmonic centrality, radiality, ego centrality, relative cardinality, eigenvector centrality, frequency, name simplicity, density, coverage, popularity and reference. It also catalogues these methods: RDF sentence graph (Zhang et al.), personalized summaries, Peroni's key concepts, Queiroz-Sousa/Pires's "Ontology understanding without tears", and Troullinou's RDF Digest — [arXiv 1801.01937](https://arxiv.org/pdf/1801.01937); see also [Graph-based Ontology Summarization: A Survey](https://arxiv.org/pdf/1805.06051). (The section list came from the PDF outline; I could not read the body text.)
- **Zhang, Cheng & Qu (WWW 2007).** The paper treats the "RDF sentence" as the unit of summarization, builds an RDF Sentence Graph, measures salience by centrality (degree, betweenness and eigenvector variants), and re-ranks for diversity. It was evaluated against human expert "ground truth" summaries using Kendall's tau (per the 2018 survey). The authors report the approach is feasible; I did not obtain the numbers — [Zhang et al. 2007](https://archives.iw3c2.org/www2007/htmlpapers/paper565/index.html)

### Inferences
- **Mapping to the app's tiers:**
  - **L1** ≈ top-level/domain-core concepts at or just above the basic level. They have high density, high centrality and simple labels (e.g., *Dog*, *Owner*, *Building*, *Permit*, *Compute instance*, *Ingredient*).
  - **L2** ≈ task/application-level concepts needed for the typical activities (task ontology: feeding, vaccination, applying for a permit, deploying).
  - **L3** ≈ low-centrality leaves, subordinate-level specializations, and exception/error concepts.
- **KCE's criteria can be operationalized for text-derived candidates.** Name simplicity is computed from the label. Density comes from the number of extracted sub-concepts and relations. Coverage ensures every branch keeps at least one representative in L1/L2. Popularity can be replaced by corpus frequency or document frequency.
- **Coverage is important for avoiding a lopsided L1.** Pure centrality would pick hub concepts from the most verbose manual sections. KCE's coverage term explicitly counters this.
- **The basic level shifts with expertise** (Tanaka & Taylor). The "core" tier should be calibrated to the intended user stated in the ORSD: dog owners versus veterinarians, or cloud novices versus SREs.

### Gaps
- I did not obtain KCE's exact weights or correlation numbers. Sources indicate the survey reports specific density sub-weights, which should be checked against the original paper.
- I found no source on "ontology modularization by abstraction level" specifically; that sub-question remains open.
- I found no empirical study validating a three-tier core/happy-path/peripheral scheme.

## LLM-based classification of relevance or level: techniques and failure modes

### Takeaway
LLM ontology-learning work (LLMs4OL 2023 and its 2024–2026 challenges, OntoLearner, NeOn-GPT-style pipelines) shows the following. Zero-shot LLMs are weak at term typing, deciding which type or category a term belongs to, but better at taxonomy discovery. Retrieval, grounding and deterministic post-filters improve precision. Failure modes include hallucinated but plausible items, error propagation through pipeline stages, narrow domain coverage, logical inconsistency, low evaluator agreement on LLM-generated CQs, and systematically overconfident, coarse verbalized confidence scores.

### Cited Findings
- **LLMs4OL (Babaei Giglou et al., ISWC 2023)** tested zero-shot prompting across nine LLM families on three tasks: term typing, taxonomy discovery and non-taxonomic relation extraction. The tests used WordNet, GeoNames and UMLS — [arXiv 2307.16648](https://arxiv.org/pdf/2307.16648). Per a secondary summary, term typing was hardest (biomedical typing roughly 16–38%), while taxonomy discovery reached about 78% F1 with GPT-4 on UMLS. Zero-shot LLMs alone were judged insufficient, and fine-tuning helped — [AlphaXiv overview](https://alphaxiv.org/overview/2307.16648v2) (secondary; check the paper's tables). Term typing is scored with MAP@1 — [LLMs4OL GitHub](https://github.com/HamedBabaei/LLMs4OL/blob/main/TaskA/README.md); the 2024 challenge repeated the task design — [LLMs4OL 2024 overview](https://arxiv.org/pdf/2409.10146)
- **OntoLearner (2026).** "Failure modes scale with ontological complexity rather than model size or architectural sophistication." The bottleneck is "a structural mismatch" between how models encode knowledge and how ontologies are structured — [OntoLearner](https://www.alphaxiv.org/abs/2607.01977)
- **Error propagation.** "Errors introduced during these early stages propagate to subsequent ontology learning tasks." The pro-team paper proposes a deterministic, vocabulary-constrained filter that uses exact lexical matching — [arXiv 2608.27101](https://arxiv.org/pdf/2608.27101)
- **Hallucination in extraction.** A model "generates a triple that is plausible but not supported by the source text" — [arXiv 2504.12915](https://arxiv.org/pdf/2504.12915) (from search snippet). Another pipeline refines LLM candidates with "a rule-based three-filter filtering module" using cross-prompt agreement, evidence grounding and surface-form alignment — [arXiv 2410.23584](https://arxiv.org/pdf/2410.23584v1)
- **Grounding as a relevance safeguard.** ConExion-style extraction ensures "that all identified concepts are grounded in the original document" — [arXiv 2410.23584](https://arxiv.org/pdf/2410.23584v1) (attribution per search summary)
- **Persistent limits.** In LLM-assisted ontology learning, "logical inconsistencies persisted (Fathallah et al. 2024), outputs remained domain-narrow" — [AMCIS 2025](https://aisel.aisnet.org/amcis2025/sig_odis/sig_odis/15); see also NeOn-GPT — [Southampton eprint](https://eprints.soton.ac.uk/511839/1/neon_gpt_2_final.pdf); [review: Ontology Learning stride to LLMs](https://arxiv.org/html/2404.14991v2)
- **CQ generation with LLMs.**
  - LLM-generated CQs "generate a lower level of agreement, require more knowledge to be understood and are more complex" than manual or pattern-based CQs — [arXiv 2507.02989](https://arxiv.org/pdf/2507.02989).
  - RAG with domain knowledge improves CQ precision and consistency over zero-shot — [arXiv 2409.08820](https://arxiv.org/pdf/2409.08820).
  - Retrofitted CQs reach recall close to 1 with varying precision (over-generation) — [arXiv 2311.05662](https://arxiv.org/pdf/2311.05662).
  - Evaluation lacks standardization (Bench4KE) — [arXiv 2505.24554](https://arxiv.org/pdf/2505.24554).
  - CQ4OE evaluates ontology generation with CQ-to-term and CQ-to-axiom provenance — [arXiv 2609.26029](https://arxiv.org/pdf/2609.26029)
- **Confidence scores.**
  - LLM verbalized confidence is generally overconfident; calibration improves with model size — [Xiong et al., arXiv 2306.13063](https://arxiv.org/pdf/2306.13063).
  - Most models were overconfident most of the time — [arXiv 2405.02917](https://arxiv.org/html/2405.02917v1).
  - Overconfidence appeared at every model size tested — [arXiv 2412.14737](https://arxiv.org/pdf/2412.14737).
  - In classification, verbalized confidence is very sparse (e.g., Qwen3-32B used only eight distinct values), partly due to numeric-token preferences — [ACL Findings 2026](https://aclanthology.org/2026.findings-acl.1671.pdf).
  - Proposed fixes: ConfTuner (training with a proper scoring rule) — [arXiv 2508.18847](https://arxiv.org/html/2508.18847v1); DINCo (normalizing against self-generated distractors) — [arXiv 2509.25532](https://arxiv.org/pdf/2509.25532); a distribution over the answer space — [arXiv 2511.14275](https://arxiv.org/pdf/2511.14275)

### Inferences
- **Classifying a component into L1/L2/L3/ignore is structurally a term-typing task**, which LLMs4OL found to be the hardest zero-shot task. Expect noisy labels unless the prompt carries the following:
  - (a) an explicit rubric per level, derived from the ORSD purpose and intended users;
  - (b) few-shot examples per domain (dog care, building rules, cloud, cookbook), including hard negatives such as "a specific recipe" (ignore) versus "braising" (L2 technique) versus "Recipe" (L1);
  - (c) the source passage, for grounding.
- **Raw verbalized confidence should not be used as a threshold.** The literature shows it is overconfident and coarse. Better signals: self-consistency or cross-prompt agreement (as in the three-filter approach), plus statistical signals from the corpus (domain consensus, C-value, centrality) used as features alongside the LLM label.
- **Likely failure modes for this app**, each extrapolated from the cited findings:
  - Promoting vivid anecdote content (hallucination/plausibility bias).
  - Class/instance confusion for named products or commands (term-typing weakness).
  - Tier inflation, everything marked "core" (overconfidence).
  - Inconsistent labels across chunks, which deterministic post-filters and cross-chunk aggregation should mitigate (error propagation).
  - A skewed L1 when hub concepts come from verbose sections (centrality without coverage).
- **A deterministic post-pass can enforce the hard exclusion rules** (code literals, version strings, proper names, numbered step lists → ignore) before or after the LLM, as the pro-team paper does for vocabulary constraints.

### Gaps
- I found no published study that specifically evaluates LLMs on *importance-tier* classification of ontology concepts, or on excluding anecdotes and procedures. The failure modes above are extrapolated from term typing, extraction and CQ-generation results.
- Several 2026 preprints (OntoLearner, pro-team LLMs4OL 2026, CQ4OE) were seen only through search snippets; their quantitative results were not verified.
- LLMs4OL per-model numbers come from a secondary summary and should be checked against the paper.
