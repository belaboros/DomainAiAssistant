# Instructions for generating the pets and building user manuals

These are the instructions used to generate the dataset [`user-manuals-pets-and-house-rules`](../../../data/user-manuals-pets-and-house-rules/) (contract: [libs/contracts/user-manuals-pets-and-house-rules/](../../../libs/contracts/user-manuals-pets-and-house-rules/README.md)). To regenerate or extend the manuals, give an LLM this whole file and follow it.

- Part A holds the user's requests, word for word. They come from [idea 0001](../../../docs/ideas/0001-manual-ontology-assistant.md).
- Part B holds the conventions Claude added while generating the files.
- Where A and B disagree, A wins. Where two requests in A disagree, the later one wins.

## Part A · The user's requests (verbatim)

### A1 · 2026-11-20 · Content, purpose and seeded issues

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

### A2 · 2026-11-20 · Location and structure (replaces the chapter counts in A1)

> Final destination:
>  - data/user-manuals-pets-and-house-rules/dog-owners-manual/
>  - data/user-manuals-pets-and-house-rules/cat-owners-manual/
>  - data/user-manuals-pets-and-house-rules/building-and-house-rules/
>
> Each manual shall consist of 8-12 chapters.
> Most of the chapters are single files.
> But there are 1-2 chapters which are sub-directories holding 2-3 files as sub-chapters.

## Part B · Conventions added during generation

### B1 · Structure

| Manual | Chapters | Chapters that are folders |
|--------|----------|---------------------------|
| dog-owners-manual | 10 | 03 Health and Care, 05 Walking and the Leash (3 files each). This keeps the "2 chapters with sub-chapters" from A1. |
| cat-owners-manual | 9 | 04 Health and Care (3 files). This keeps the "one chapter with sub-chapters" from A1. |
| building-and-house-rules | 10 | 04 Pets (3 files) |

### B2 · Files and headings

- **File names:** one file per chapter, `NN-kebab-slug.md`, numbered from `01`. A chapter with sub-chapters is a folder `NN-kebab-slug/` holding `NN-kebab-slug.md` files numbered from `01`. A chapter folder has no file of its own for the chapter.
- **Headings:** each file has exactly one level-1 heading that carries the numbers:
  - chapter: `# N. Title`
  - sub-chapter: `# N. Chapter Title — N.M Sub-chapter Title`
- **Content:** no other files go into the manual folders: no README, no index, no notes about the seeded issues.

### B3 · Writing style

- Keep chapters short: 2 to 6 sentences or a short list.
- State facts as checkable rules: numbers, ages, times, places and obligations ("must", "may not"). The assistant can then chain them across manuals.
- Write in plain English and use the same word for the same thing within a manual. The leash/lead drift is the only deliberate exception.

### B4 · Keep the seeded issues intact

- **Gap:** no file may say anything about how dogs and cats get along, how to introduce them, or conflicts between pets or animals. Socialisation in the dog manual is limited to people, sounds, surfaces and traffic. Check with `grep -riE "dog.*cat|cat.*dog|anim|other pet"` over the dog and cat manuals: the only hits allowed are "social animals" (dog 8) and "dog food is not suitable for cats" (cat 4.1).
- **Terminology drift:**
  - the dog manual says "leash" for the rope (chapters 5 and 10);
  - only dog chapter 6 says "lead", and it means the owner's role;
  - the building rules say "lead" for the rope (4.2).
- **Contradiction:** dog chapter 8 says that an adult dog may be left alone for 6 hours at most. Building rules 4.2 say that the limit depends on the dog's education (training) and its breed. No other file may settle the question.
- **Multi-hop chains:** keep the facts that the six multi-hop questions in the answer key rely on. If you change one, update the answer key.

### B5 · Answer key

The seeded issues, the expected answers and the multi-hop questions are in [docs/research/notes/pet-manuals-corpus/README.md](../../../docs/research/notes/pet-manuals-corpus/README.md), outside `data/`, so that the assistant can't read them. Update that file whenever the manuals change.

### B6 · Contract

The layout in B2 is the dataset contract. If you change file names, numbering or the heading format, you change the contract: follow [the contract's versioning rules](../../../libs/contracts/user-manuals-pets-and-house-rules/README.md#versioning).
