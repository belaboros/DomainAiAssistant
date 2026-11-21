# ADR-0021: Introduce JavaScript/TypeScript and its quality gate

- **Status:** accepted
- **Scope:** system
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../specs/0002-ontology-builder/spec.md) · [plan 0002](../../specs/0002-ontology-builder/plan.md) task T22 (tools named there, plan approved) · idea 0002 Q47 (package manager) · `ontology-builder/ADR-0002` · [ADR-0005](0005-modularity-metrics.md) · [ADR-0006](0006-enforce-modularity-per-language.md) · [ADR-0008](0008-security-checks-for-a-public-repository.md) · [ADR-0010](0010-monorepo-of-loosely-coupled-applications.md) · [ADR-0020](0020-introduce-python-and-its-quality-gate.md)

## Context
The `ontology-builder` app has a React + TypeScript front end in `apps/ontology-builder/web/` (`ontology-builder/ADR-0002`). It is the first JavaScript/TypeScript code in the repo. ADR-0006 requires a quality gate before the first source file of a language: complexity limits, boundary rules derived from `components.json` at both levels, a metrics collector for `/arch-metrics`, hooks (Claude → pre-commit → CI) and the security checks of ADR-0008. The gate is repo-wide: later JS/TS apps and libraries use the same setup (ADR-0010).

Two version constraints shaped the choice. TypeScript 7 (the native port) is out, but typescript-eslint, which the type-aware lint rules need, supports TypeScript only up to 6.0.x. And ADR-0008's 7-day cooldown applies to the first setup too, so a release younger than a week is not adopted.

The repo already had a root `package.json` with npm and `package-lock.json`, holding the Mermaid CLI for the release render test (plan 0002, T15).

## Decision
We will use one **npm workspace** at the repo root for all JS/TS code (idea 0002, Q47):

- **Runtime and packages:** Node.js **26** (LTS), pinned in `.nvmrc` and `engines`. npm workspaces: each JS/TS app or library is a workspace with its own `package.json`, listed in the root `workspaces`; the first is `apps/ontology-builder/web`. One `package-lock.json` at the root is committed. The Mermaid CLI stays a root dev tool.
- **Language:** TypeScript **6.0.3**, `strict` plus `noUncheckedIndexedAccess`, `noImplicitOverride`, `verbatimModuleSyntax` and `isolatedModules`, in `tsconfig.base.json`; every workspace extends it. The gate's own tools (`tools/quality/js-ts/*.ts`) are TypeScript too, run directly by Node's type stripping (`erasableSyntaxOnly`), and type-checked by the root `tsconfig.json`.
- **Lint and complexity:** ESLint **10.15.0** (flat config `eslint.config.mjs`) with typescript-eslint **8.72.2** (`strictTypeChecked`). `complexity` fails above 15; `max-depth` 4, `max-params` 6, `max-statements` 50 and `max-lines-per-function` 100 (blank lines and comments not counted) limit nesting, arguments and size, in line with the Python limits of ADR-0020. ESLint has one threshold per rule, so CC 11–15 is reported as a warning by `tools/quality/js-ts/cc_report.ts`, which reads ESLint's own complexity count for every function; the metrics collector uses the same count. **Prettier 3.10.1** checks the formatting of JS/TS files (print width 100).
- **Boundaries:** dependency-cruiser **18.7.2**. Its rules are **generated** by `tools/quality/js-ts/gen_depcruise.ts` from the root and every app `components.json` into `.dependency-cruiser.json` (a drift check fails when it is stale): no module cycles; no unresolvable imports; no packages missing from `package.json`; at system level no app → app import, no library → app import, no import of a library outside `mayDependOn` and none past its `public` entry points; at app level no import of a component outside `mayDependOn` and none past its `public` entry points. `tools/quality/js-ts/boundaries.ts` adds what dependency-cruiser cannot express: cycles between components (rather than between modules).
- **Metrics collector:** `tools/quality/js-ts/collect_metrics.ts <components.json>` (dependency-cruiser's module graph mapped to components through the `paths` globs, ESLint's complexity count, the TypeScript compiler API for abstractness: interfaces and abstract classes among all interfaces and classes) emits the snapshot schema of `docs/architecture/metrics/README.md`. The shared step `tools/quality/arch_metrics.py` (ADR-0020) merges it with the Python snapshot; it now merges component rows by name, so a component measured by both languages keeps the data of each.
- **Tests:** **Vitest 5.1.0** for unit and component tests and **Playwright 1.65.1** for end-to-end tests, per workspace (`npm test`, `npm run e2e`).
- **Security:** `npm audit --audit-level=high` (`tools/quality/js-ts/audit.sh`) in pre-commit and CI; **eslint-plugin-security 4.2.1** as the static security analysis; the existing `npm` entry in `.github/dependabot.yml` (root, 7-day cooldown) now covers every workspace.
- **Hooks:** a Claude `PostToolUse` hook (`tools/quality/js-ts/lint-file.sh`) runs ESLint and Prettier on each edited JS/TS file and returns exit 2 with the findings; local pre-commit hooks run Prettier, ESLint, the type check, the CC report, the dependency-cruiser drift check, dependency-cruiser, the component-cycle check, the tests and the audit; CI runs the same gate in `.github/workflows/js-ts.yml` (SHA-pinned actions, read-only permissions).

## Alternatives considered
| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| pnpm workspaces | Faster, stricter installs (no phantom dependencies) | Not installed; a second lockfile format; extra CI setup | User chose npm (Q47); npm is installed and already used at the root |
| TypeScript 7 (native) | Much faster type checks | typescript-eslint does not support it yet (peer range < 6.1) | Type-aware lint rules matter more than check speed for now |
| Biome instead of ESLint + Prettier | One fast tool | No type-aware rules, no security plugin, no per-function complexity count that matches the metrics | The gate needs complexity and security rules |
| eslint-plugin-boundaries instead of dependency-cruiser | Editor feedback | Weaker cycle detection and no module graph for the metrics | dependency-cruiser gives both the rules and the graph |
| husky + lint-staged | Common in JS projects | A second hook system next to pre-commit | pre-commit already runs every other gate (playbook) |
| Gate tools as `.mjs` with JSDoc types | No type stripping needed | Strict `checkJs` needs JSDoc on every parameter | Node 26 runs `.ts` natively |

## Consequences
- **Positive:** One `npm ci` installs every JS/TS workspace; one `npm run lint` and one `npm test` cover them all. Boundary rules can't drift from `components.json`. JS/TS metrics merge with Python's in `/arch-metrics`.
- **Negative / trade-offs:** The repo now needs Node 26 and npm next to uv. TypeScript stays on 6.0.x until typescript-eslint supports 7. Type-aware linting is slower than plain linting.
- **Follow-up:** register `js-ts` in `tools/quality/languages.json`; root `package.json` workspaces and scripts, `package-lock.json`, `.nvmrc`, `tsconfig.base.json`, `tsconfig.json`, `eslint.config.mjs`, `.prettierrc.json`, `.prettierignore`; the `tools/quality/js-ts/` scripts and the generated `.dependency-cruiser.json`; `.pre-commit-config.yaml`, `.claude/settings.json`, `.github/workflows/js-ts.yml`, `.github/dependabot.yml`; merge component rows by name in `tools/quality/arch_metrics.py`; the JS/TS commands in the root `CLAUDE.md` Conventions and in `apps/ontology-builder/CLAUDE.md`; a baseline `/arch-metrics` snapshot.
