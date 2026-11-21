# App: generate-pets-and-building-user-manual

This file adds to the root `CLAUDE.md`; everything there applies here too. Purpose: Holds the instructions used to generate the pets and building user manuals.

## Where things live for this app

| Path | What it holds |
|------|---------------|
| `apps/generate-pets-and-building-user-manual/docs/architecture/architecture.md` | This app's internal architecture: its components and runtime flows |
| `apps/generate-pets-and-building-user-manual/docs/architecture/components.json` | This app's components and their allowed dependencies (paths are relative to the repo root) |
| `apps/generate-pets-and-building-user-manual/docs/architecture/adr/` | Decisions that concern this app only, cited as `generate-pets-and-building-user-manual/ADR-NNNN` |
| `apps/generate-pets-and-building-user-manual/docs/specs/` | Specs whose scope is this app only. Ideas always live in the root `docs/ideas/` |
| `apps/generate-pets-and-building-user-manual/instructions/generation-instructions.md` | The instructions for generating the manuals: the user's requests (verbatim) and the generation conventions |
| `apps/generate-pets-and-building-user-manual/.env.example` | Variables this app adds to, or overrides in, the root `.env.example` |

## Rules specific to working in an app

1. **Never import from another app.** Use libraries from `libs/` (listed in this app's `mayDependOn` in the root `docs/architecture/components.json`) or a shared dataset through its contract.
2. **Shared data goes through contracts.** This app writes only the datasets it owns and reads others only as described in `libs/contracts/<dataset>/`. A new read or write is a change to the root `components.json` (and possibly a root ADR).
3. **Decide where a decision belongs.** If it changes anything another app can see (a contract, libraries, a base env variable, repo tooling), it is a root ADR; otherwise an app ADR here.
4. **Configuration comes from the environment**, loaded by `tools/env/with-env.sh generate-pets-and-building-user-manual`. Never read `.env` files from code paths of your own, never hard-code secrets.

## Commands

None: this app has no code. When you change the manuals in `data/user-manuals-pets-and-house-rules/`:
- follow `instructions/generation-instructions.md`;
- keep the seeded issues intact (part B4);
- update the answer key in `docs/research/notes/pet-manuals-corpus/README.md`;
- add a new user request to part A verbatim, with its date.
