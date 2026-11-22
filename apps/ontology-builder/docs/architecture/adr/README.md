# ontology-builder · Architecture Decision Records

Decisions that concern only the ontology-builder app. They are numbered on their own and cited as `ontology-builder/ADR-NNNN`. Anything another app can see (shared datasets and contracts, shared code, base environment variables, repo tooling) is a [root ADR](../../../../../docs/architecture/adr/README.md) instead (ADR-0011).

Create one with `/adr --app ontology-builder <decision>`, from [the template](../../../../../docs/templates/adr.md).

| ADR | Decision | Status | Date |
|-----|----------|--------|------|
| [0001](0001-linkml-yaml-records-as-source-rdf-releases-as-output.md) | Keep LinkML-defined YAML records as the only source; generate RDF and Markdown releases one way | accepted | 2026-11-21 |
| [0002](0002-api-first-python-back-end-with-react-typescript-front-end.md) | Build an API-first Python back end with a React + TypeScript front end | accepted | 2026-11-21 |
| [0003](0003-markdown-block-source-units-with-minted-ids.md) | Split sources into Markdown-block units with minted, opaque IDs | accepted | 2026-11-21 |
| [0004](0004-pending-change-set-atomic-save-one-commit.md) | Hold changes in a pending change set; save them atomically as one git commit | accepted | 2026-11-21 |
| [0005](0005-two-pass-llm-extraction-with-curated-fixtures.md) | Extract in two LLM passes behind a replaceable client, tested on curated fixtures | accepted (structured-output part superseded by 0006; one-call pass 1 superseded by 0007) | 2026-11-21 |
| [0006](0006-json-structured-outputs-instead-of-a-forced-tool-call.md) | Get the LLM's structured output through JSON structured outputs, not a forced tool call | accepted | 2026-11-21 |
| [0007](0007-pass-1-as-two-structured-output-calls-per-document.md) | Run pass 1 as two structured-output calls per document, citing units by short alias | accepted | 2026-11-21 |
| [0008](0008-ingestion-depends-on-model.md) | Let ingestion depend on model | accepted | 2026-11-21 |
| [0009](0009-workflows-depends-on-store-and-llm.md) | Let workflows depend on store and llm | accepted | 2026-11-21 |
| [0010](0010-cli-depends-on-api.md) | Let cli depend on api | accepted | 2026-11-21 |
| [0011](0011-api-types-with-openapi-typescript-calls-through-openapi-fetch.md) | Generate the GUI's API types with openapi-typescript and call the API through openapi-fetch | accepted | 2026-11-21 |
