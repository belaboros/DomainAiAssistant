# Changelog · ontology contract family

## 0.2.0 · 2026-11-22
- Both releases also hold `ontology.jsonld`, the graph of `ontology.ttl` as JSON-LD (spec 0002, FR-37); the manifest lists it. Readers that ignore unknown files are not affected.

## 0.1.0 · 2026-11-21
- Contract created (plan 0002, ADR-0019); owner `ontology-builder`.
- Layout of `00_sources/` (corpora `00`–`89`, `90_user_statements/`) and `03_release/` (`00_raw/`, `01_governed/`).
- `source-unit.schema.json`, `manifest.schema.json` (JSON Schema 2020-12) and the `dai:` vocabulary `vocab.ttl`.
- IRI scheme, RDF mapping (OWL 2 + SKOS + SHACL), the level files and the guarantees.
