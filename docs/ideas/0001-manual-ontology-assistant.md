# 0001 · Ontology-backed AI assistant over pet and building user manuals

- **Status:** captured
- **Scope:** TBD (decided by `/spec`: `system`, or the name of one app) (mentions: AI assistant app, ontology builder app)
- **Captured:** 2026-11-20
- **Spec:** _none yet_

## Original idea

> Generate a set of short user manuals:
> * dog owner's user manual
> * cat owner's user manual
> * house and building rules
>
> Purpose of the user manuals:
> * Create an AI assistant app that
>      - can answer questions intelligently across the user manuals
>      - can detect which questions cannot be answered (and avoid hallucination)
>      - can detect contradictions, terminology drift, gaps and other quality issues within and across the user manuals
>       - can make logical conclusions and decisions based on facts and/or ontologies (built from the user manuals)
>        - can answer questions across 3+ hops along the ontology (which is not possible for a typical keyword or RAG search engine)
> * build an ontology from the user manuals which
>        - contains the concepts, relations, rules, properties
>        - contains higher-level concepts, relations, rules (proposed by LLM)
> * add governance process to the ontology builder app which
>        - allows the user to review, accept/reject/correct the proposed ontologies
>        - allows the user to create additional statements (missing from the user manuals) to extend the ontology
>
> Dog owner's manual:
>  - short summary what to know if you want to have a dog
>  - it shall have 4-7 chapters and 2 chapters shall have 2-3 sub-chapters
>
> Can owner's manual:
>  - short summary what to know if you want to have a cat
>  - it shall have 4-7 chapters and one chapter shall have 2-3 sub-chapters
>
> Building/house rules
>  - a small manual about the rules, obligations to live together in a set of building with a shared inner yard
>
>
> Extra expectations
> * intentional gap: (which cannot be answered from manuals) ?What shall I do to prevent fight between my dog and cat.
> * terminology drift: "leash" -> "lead"
>     - the dog manual contains instructions about the leash (rope) for dogs
>     - the dogs manual explains how the owner shall behave as a lead (role) for his/her dog
>     - the house/building manual uses the "lead" word in the sense of the rope
>     - the ontology builder shall detect the terminology drift
> * intentional contradiction:
>      - dog owners manual mentions 6 hours max time to leave the dog alone at home
>      - building rules manual mentions that the maximum time depends on the education and the specific breed of the dog
>      - the AI assistant shall detect the contradiction when someone asks how long may I leave my dog alone.

2026-11-20 (follow-up message):

> Final destination:
>  - data/user-manuals-pets-and-house-rules/dog-owners-manual/
>  - data/user-manuals-pets-and-house-rules/cat-owners-manual/
>  - data/user-manuals-pets-and-house-rules/building-and-house-rules/
>
> Each manual shall consist of 8-12 chapters.
> Most of the chapters are single files.
> But there are 1-2 chapters which are sub-directories holding 2-3 files as sub-chapters.

Material: the manuals are in [data/user-manuals-pets-and-house-rules/](../../data/user-manuals-pets-and-house-rules/), owned by the app [generate-pets-and-building-user-manual](../../apps/generate-pets-and-building-user-manual/README.md) (ADR-0018), whose [instructions](../../apps/generate-pets-and-building-user-manual/instructions/generation-instructions.md) produced them; their answer key (seeded issues, expected answers, multi-hop questions) is in [docs/research/notes/pet-manuals-corpus/](../research/notes/pet-manuals-corpus/README.md).

## Q&A log

<!--
Append one entry per question, oldest first. Never delete entries.

### YYYY-MM-DD · <stage: idea | spec | plan | implement | review | architecture | scaffold> · Q<n>
**Asked by:** Claude | user
**Q:** [<skill · stage>] <question exactly as asked>
**Options offered:** <list, or "free text">
**A:** <the answer, verbatim if it is the user's; a summary if it is Claude's>
**Effect:** <what changed because of it, e.g. "added FR-4 to spec">
-->
