# ontology-builder

Builds leveled ontologies from Markdown corpora and user statements, through LLM proposals, human review and governed releases.

| | |
|---|---|
| **Kind** | application in the monorepo ([system architecture](../../docs/architecture/architecture.md)) |
| **Instructions for Claude** | [CLAUDE.md](CLAUDE.md) (adds to the root [CLAUDE.md](../../CLAUDE.md)) |
| **Architecture** | [docs/architecture/architecture.md](docs/architecture/architecture.md) · [ADRs](docs/architecture/adr/README.md) |
| **Specs** | [docs/specs/](docs/specs/README.md) (specs that concern this app only) |
| **Environment** | [.env.example](.env.example), layered over the root [.env.example](../../.env.example) |

## Run

Every command runs with the layered environment (root `.env`, then `apps/ontology-builder/.env`):

```bash
tools/env/with-env.sh ontology-builder --check
OB="tools/env/with-env.sh ontology-builder -- uv run --package ontology-builder ontology-builder"

$OB create <name> --scope scope.yaml --user <handle>     # domain admin: new data/ontology-<name>/, committed
$OB ingest <name> <folder> --user <handle>               # shows the estimate, asks, then runs and commits
$OB ingest <name> <folder> --user <handle> --resume <run-id>   # continue a failed run
$OB build <name>                                         # rebuild the raw release (no commit)
$OB serve <name> [--port 8765]                           # the review GUI on http://127.0.0.1:<port>
$OB eval [--model <model>] [--yes]                       # live evaluation of the pet manuals (costs money)
```

`<folder>` is relative to `SHARED_DATA_DIR`, e.g. `user-manuals-pets-and-house-rules/dog-owners-manual`. Use a handle, never a real name or email address: the dataset is public. Publishing a governed release is done in the GUI, signed in as domain admin. Nothing is ever pushed.

`eval` ingests the three pet manuals live into a throw-away ontology in a temporary folder (no git, no commit), after showing the estimate and asking. Only then does it read the [answer key](../../docs/research/notes/pet-manuals-corpus/answer-key.yaml), print a score per section and write `docs/evaluations/YYYY-MM-DD-<model>.md`. It is not a gate (FR-38).
