# ADR-0019: Add the ontology-builder app and `ontology-<name>` datasets that share one contract

- **Status:** accepted
- **Scope:** system (a new app, a new kind of shared dataset and its contract)
- **Date:** 2026-11-21
- **Related:** [idea 0002](../../ideas/0002-ontology-builder.md) (Q9, Q10, Q12, Q30, Q35), [spec 0002](../../specs/0002-ontology-builder/spec.md), [plan 0002](../../specs/0002-ontology-builder/plan.md), [ADR-0010](0010-monorepo-of-loosely-coupled-applications.md), [ADR-0013](0013-shared-data-through-owned-datasets-and-contracts.md), [ADR-0015](0015-libraries-in-libs-folder.md), [ADR-0016](0016-commit-or-ignore-each-data-folder.md)

## Context

Spec 0002 introduces OntologyBuilder: an app that builds leveled ontologies from Markdown manuals and from statements people type in, and publishes them for other apps. The AI assistant of idea 0001 and a future validation app will read these ontologies, so each one is a shared dataset (ADR-0013) with exactly one writer.

There will be more than one ontology (`data/ontology-<name>/`, one per domain), and every one of them has the same layout and the same release format. The monorepo tooling (`tools/monorepo/system-map.sh`, `new.sh`) expects one contract folder per dataset, `libs/contracts/<dataset>/README.md`. One full contract per ontology would duplicate the same text, and the copies would drift. Changing the tooling so that several datasets share one folder would change scripts inherited from the template and cause friction on `copier update`.

Ontologies are small, contain no personal data (the GUI asks for handles, not names), and both the governed and the raw release must be versioned in git (Q7).

## Decision

We will:
- **Add the app `ontology-builder`.** It is the only writer of every `ontology-<name>` dataset and reads `user-manuals-pets-and-house-rules` through its contract.
- **Write one shared, versioned contract for the kind:** `libs/contracts/ontology/`. It describes the public parts of every ontology dataset: `00_sources/` (corpora, user statements, the source registry with stable unit IDs) and `03_release/` (`00_raw/` and `01_governed/`, each with `ontology.ttl`, `level-1/2/3.md` and `manifest.json`). It also holds the `dai:` vocabulary, the IRI scheme, the guarantees and the JSON Schemas. `01_model/` and `02_decisions/` stay internal to the app.
- **Give each dataset a thin contract:** `libs/contracts/ontology-<name>/README.md` names the owner, location and git mode, and the version of the `ontology` contract it conforms to. Its own CHANGELOG records only pin changes.
- **Commit every `ontology-<name>` dataset to git** (ADR-0016).
- **Create the first dataset,** `ontology-pets-and-house-rules`.

`libs/contracts/ontology/` is a contract family, not a dataset. It is not registered in `components.json` and needs no tooling change, because the tooling only checks that each registered dataset has its own contract folder.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| A full contract per ontology dataset | Fits the tooling as it is | The same text copied N times; the copies drift | Duplication |
| One shared folder, with `system-map.sh` and `new.sh` following each dataset's `contract` field | No thin files | Changes template tooling; friction on `copier update` | More cost than the thin files |
| One dataset `ontologies` holding every ontology | One contract, one registration | One commit history and one version for unrelated domains; readers of one domain depend on all of them | Too coarse |
| Git-ignore the datasets and rebuild them | Smaller repo | An LLM run is neither free nor reproducible, and the review decisions can't be rebuilt | They must be versioned (Q7) |

## Consequences

- **Positive:** readers depend on one stable description of every ontology. A new ontology is a scaffold plus a thin README. The system map shows each ontology dataset with its owner and its readers.
- **Negative / trade-offs:** a breaking change of `libs/contracts/ontology/` is a major version that affects every ontology dataset and every reader at once. It needs a root ADR and a task per reader. The thin READMEs must be updated when the family version changes.
- **Follow-up:**
  - Done in the planning change: scaffold the app and the dataset, add the `reads` edge, regenerate the system map.
  - Plan 0002, T2: write `libs/contracts/ontology/` (README, CHANGELOG, schemas, `vocab.ttl`), make the dataset contract thin, and add a line about contract families to `libs/contracts/README.md`.
  - Plan 0002, T31: root `architecture.md` §1, §2 and §6.
