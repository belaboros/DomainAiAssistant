# Dataset contract: ontology-pets-and-house-rules

| | |
|---|---|
| **Description** | Ontology of pet ownership and the house rules, built from the pet and building manuals: source registry, user statements and the raw and governed releases. |
| **Owner (only writer)** | `ontology-builder` |
| **Readers** | see the system map in the [root architecture](../../../docs/architecture/architecture.md) |
| **Location at runtime** | `${SHARED_DATA_DIR}/ontology-pets-and-house-rules/` (`SHARED_DATA_DIR` comes from the root `.env`) |
| **In git** | commit: see `git` in the root `components.json` and `.gitignore` (ADR-0016) |
| **Contract version** | 0.1.0 (see [CHANGELOG.md](CHANGELOG.md)); conforms to `ontology` 0.1.0 |

The contract is what readers may rely on (ADR-0013). Anything not written here is an implementation detail of `ontology-builder` and may change without notice.

## Format

This dataset conforms to the shared contract **[`ontology` 0.1.0](../ontology/README.md)** (ADR-0019): the layout of `00_sources/` and `03_release/`, the schemas, the `dai:` vocabulary, the IRIs and the level files are all defined there.

Dataset-specific values:
- **Ontology name:** `pets-and-house-rules`
- **Base IRI:** the default, `urn:domain-ai-assistant:ontology:pets-and-house-rules:`
- **Corpora:** the three manuals of the dataset `user-manuals-pets-and-house-rules`, read through [its contract](../user-manuals-pets-and-house-rules/README.md).

## Guarantees

The guarantees of the [`ontology` contract](../ontology/README.md#guarantees) apply. There are none in addition.

## Versioning

Semantic versioning of this thin contract. It changes when the pinned `ontology` version or a dataset-specific value changes: **major** for anything that can break a reader (removed or renamed fields, changed meaning), **minor** for additions readers can ignore, **patch** for clarifications. A major change needs a root ADR and a plan for every reader listed in the system map.
