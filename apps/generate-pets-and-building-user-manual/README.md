# generate-pets-and-building-user-manual

Holds the instructions used to generate the pets and building user manuals.

| | |
|---|---|
| **Kind** | application in the monorepo ([system architecture](../../docs/architecture/architecture.md)) |
| **Instructions for Claude** | [CLAUDE.md](CLAUDE.md) (adds to the root [CLAUDE.md](../../CLAUDE.md)) |
| **Architecture** | [docs/architecture/architecture.md](docs/architecture/architecture.md) · [ADRs](docs/architecture/adr/README.md) |
| **Specs** | [docs/specs/](docs/specs/README.md) (specs that concern this app only) |
| **Environment** | [.env.example](.env.example), layered over the root [.env.example](../../.env.example) |

## Contents

- [instructions/generation-instructions.md](instructions/generation-instructions.md): the instructions used to generate the manuals in [data/user-manuals-pets-and-house-rules/](../../data/user-manuals-pets-and-house-rules/).

There is no code and no run command. To regenerate the manuals, give the instructions to Claude and follow the contract in [libs/contracts/user-manuals-pets-and-house-rules/](../../libs/contracts/user-manuals-pets-and-house-rules/README.md).
