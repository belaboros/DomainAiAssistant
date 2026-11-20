# Pet manuals corpus: answer key (idea 0001)

Answer key for the sample manuals of [idea 0001](../../../ideas/0001-manual-ontology-assistant.md): an AI assistant and an ontology builder working over a small set of user manuals.

The manuals are in [data/user-manuals-pets-and-house-rules/](../../../../data/user-manuals-pets-and-house-rules/). This file stays **outside** that folder on purpose: it lists the issues seeded into the manuals and the expected behaviour, so if the assistant can read it, every test below is spoiled.

## Layout

One Markdown file per chapter, named `NN-slug.md`. A chapter with sub-chapters is a folder `NN-slug/` holding `NN-slug.md` files. Each file starts with a heading that carries the chapter number (and the sub-chapter number), so answers can cite e.g. "dog 5.3".

| Manual | Chapters | Chapters that are folders |
|--------|----------|---------------------------|
| [dog-owners-manual/](../../../../data/user-manuals-pets-and-house-rules/dog-owners-manual/) | 10 | 3 Health and Care (3 files), 5 Walking and the Leash (3 files) |
| [cat-owners-manual/](../../../../data/user-manuals-pets-and-house-rules/cat-owners-manual/) | 9 | 4 Health and Care (3 files) |
| [building-and-house-rules/](../../../../data/user-manuals-pets-and-house-rules/building-and-house-rules/) | 10 | 4 Pets (3 files) |

References below use `dog`, `cat` and `rules` plus the chapter number.

## Seeded issues (required by the idea)

### Gap: dog and cat conflicts

**Question:** "What shall I do to prevent a fight between my dog and cat?"
**Expected:** the assistant says the manuals don't cover this. No file mentions how dogs and cats get along, how to introduce them, or conflicts between pets (dog 4 limits socialisation to people, sounds, surfaces and traffic). The assistant may list nearby facts it does have, but must not invent advice.

### Terminology drift: "leash" and "lead"

| Where | Word | Meaning |
|-------|------|---------|
| dog 5.1–5.3, dog 10 | leash | the rope or strap attached to the collar |
| dog 6 | lead | a role: the owner as the dog's calm, consistent leader |
| rules 4.2 | lead | the rope or strap (the dog manual's "leash") |

**Expected:** the ontology builder flags two things. "Lead" has two meanings across documents (homonym), and "leash" and "lead" name the same object in different documents (synonym). It proposes one preferred term per concept, for example `Leash` (equipment, alias "lead" in the building rules) and `OwnerAsLeaderRole` ("lead" in dog 6). The building-rule facts about the lead (mandatory in yard, stairwells and lifts; at most 2 m) must attach to `Leash`, not to the role.

### Contradiction: how long a dog may be left alone

| Where | Statement |
|-------|-----------|
| dog 8 | Never leave an adult dog alone for more than **6 hours** (puppies: 2 hours) |
| rules 4.2 | The maximum time **depends on the dog's education (training) and its breed** |

**Question:** "How long may I leave my dog alone?"
**Expected:** the assistant gives both statements with their sources and says that they conflict: a fixed limit against a limit that depends on training and breed. It must not quietly pick one. A good answer adds that the 2-hour limit for puppies is not contradicted.

## Questions that need 3+ hops

| # | Question | Chain of facts | Expected conclusion |
|---|----------|----------------|---------------------|
| H1 | My cat goes out into the inner yard. What does it need before that? | Cats may move freely in the inner yard (rules 4.3) → going into the yard makes it an outdoor cat (cat 2, *inference*) → an outdoor cat must be vaccinated and microchipped before its first time outside (cat 2) → outdoor cats need a rabies vaccination, renewed every year (cat 4.2) | Microchip and vaccinations, including rabies, before the first outing; rabies renewed yearly. Flag that "the yard counts as outdoors" is an inference: a candidate statement for governance |
| H2 | It is 23:00 and my 4-month-old puppy needs to go out. What must I consider? | 4 months < 6 months → puppy (dog 4) → must go out every 2–3 hours (dog 5.3) → may not relieve itself in the yard, must leave the complex (rules 4.2) → main doors are locked 22:00–06:00, open with own key (rules 7) → quiet hours, no persistent barking (rules 2) → on a lead of at most 2 m in stairwell, lift and yard (rules 4.2) | Take the puppy out of the complex on a lead of at most 2 m, bring your key, keep it quiet, pick up the waste |
| H3 | Where does the waste go when I clean my cat's litter box? | Used litter → residual waste (cat 4.3, rules 5) → residual waste bin is in the bin room (rules 5) → the bin room is in building B (rules 5) | Residual waste bin in the bin room of building B; not the toilet, not the compost |
| H4 | I just got a 5-month-old dog. What must I do, and by when? | 5 months > 4 months → register with the local authority and microchip (dog 1) → register with the house management within 14 days (rules 4.1) → rabies vaccination, mandatory, yearly (dog 3.2) → liability insurance recommended, mandatory and obedience test required for dangerous breeds (dog 10, dog 7, dog 2) | Local authority registration and microchip; house-management registration within 14 days; rabies vaccination; insurance (mandatory only for a dangerous breed) |
| H5 | Can I wash my dog's bed in the laundry room? | Dog's bed and blankets must be washed weekly at 60 °C (dog 3.3) → dog bed is a pet textile (*inference*) → pet textiles may not be washed in the shared machines (rules 8) → the shared machines are in the laundry room, cellar of building A (rules 8) | No: not in the shared machines; wash it elsewhere (the manuals don't say where) |
| H6 | I'm moving into building C with my outdoor cat. What applies in the first weeks? | Moving house → keep an outdoor cat indoors for at least 2 weeks (cat 9) → register the cat with the house management within 14 days of moving in (rules 4.1) → announce the move 7 days in advance (rules 9) → once it goes out it may use the inner yard (rules 4.3), so H1 applies | Announce the move, register the cat within 14 days, keep it indoors 2 weeks, then the outdoor-cat requirements of H1 |

## Higher-level concepts the ontology builder may propose

These are not stated in the manuals. The builder should propose them for review, not assert them.

- `Pet` as a superclass of `Dog` and `Cat` (rules 4.1: "every pet (dog or cat)").
- `JuvenilePet` (puppy, kitten: both younger than 6 months) with shared rules: more meals, first vaccinations at 8 weeks.
- `PetOwner` as a subclass of `Resident` (rules 1), inheriting the building obligations.
- `MaxAloneTime` as a property of `Pet`, with values per species and age (dog 6 h, puppy 2 h, cat 24 h) and the open conflict from rules 4.2.
- `PetTextile` covering dog beds and blankets.
- Rule: a pet that enters the inner yard is an outdoor pet.
- Rule: a breed classified as dangerous triggers mandatory insurance and an obedience test.

## Further quality issues (not planned, but present)

A good quality check may also report these:

- **Undefined term:** "education" in rules 4.2 is explained only by "(training)"; the dog manual uses "training" (dog 7) and never "education".
- **Vague term:** "waste bin" (dog 5.3) against "residual waste bin" (rules 5): the dog manual doesn't say which bin.
- **Gap:** the building rules require dogs on a lead in the yard but say nothing about free-running areas; dog 10 allows free running only "where a sign allows".
- **Gap:** rules 4.1 requires registering pets but doesn't say what registration involves or what happens if it is missed.
- **Gap:** the cat manual doesn't say whether an indoor cat needs a microchip.
- **Gap:** rules 8 forbids washing pet textiles in the shared machines, but dog 3.3 requires weekly washing at 60 °C and nothing says where.
- **Different age limits:** puppies may leave the mother at 8 weeks (dog 4), kittens at 12 weeks (cat 5). Not a contradiction (different species), but a check that compares `JuvenilePet` rules should not merge them.
