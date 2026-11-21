# ADR-0020: Introduce Python and its quality gate

- **Status:** accepted
- **Scope:** system
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../specs/0002-ontology-builder/spec.md) · [plan 0002](../../specs/0002-ontology-builder/plan.md) task T1 (tools named there, plan approved) · [ADR-0005](0005-modularity-metrics.md) · [ADR-0006](0006-enforce-modularity-per-language.md) · [ADR-0008](0008-security-checks-for-a-public-repository.md) · [ADR-0010](0010-monorepo-of-loosely-coupled-applications.md)

## Context
The `ontology-builder` app (plan 0002, `ontology-builder/ADR-0002`) has a Python back end. It is the first Python code in the repo. ADR-0006 requires every language to have a quality gate before its first source file: complexity limits, boundary rules derived from `components.json` at both levels, a metrics collector for `/arch-metrics`, hooks (Claude → pre-commit → CI) and the security checks of ADR-0008. The gate is repo-wide: every later Python app or library uses the same setup (ADR-0010).

LinkML and pySHACL, which the app needs, support Python up to 3.13 and 3.14. The machine has 3.15 installed by default.

## Decision
We will use one **uv workspace** at the repo root for all Python code:

- **Interpreter:** CPython **3.13**, pinned in `.python-version` and `requires-python = ">=3.13,<3.14"`. Each Python app or library is a workspace member with its own `pyproject.toml` (src layout); `uv.lock` at the root is committed.
- **Lint and complexity:** `ruff` 0.17.6, rules `E F W I B UP S PL C90 SIM RUF`. `C901` fails above CC 15 (`max-complexity = 15`); `PLR0912` (branches > 12), `PLR0913` (arguments > 6), `PLR0915` (statements > 50) and `PLR1702` (nested blocks > 4) limit size, arguments and nesting. Ruff cannot warn, so CC 11–15 is reported as a warning by the metrics collector (radon 6.0.1) and printed by `tools/quality/python/cc_report.py` (which uses the same radon count and also fails above 15, because radon counts comprehension branches that ruff's C901 does not). Ruff's `S` rules (the bandit rule set) are the static security analysis.
- **Types:** `mypy` 2.4.1, `strict = true`.
- **Boundaries:** `import-linter` 2.17. Its contracts are **generated** by `tools/quality/python/gen_importlinter.py` from the root and every app `components.json` into `.importlinter` (a drift check fails when it is stale): one `forbidden` contract per app component (everything not in its `mayDependOn`), one `forbidden` contract per Python app or library at system level (other apps, libraries outside `mayDependOn`; generated once there are two Python units), and an `acyclic_siblings` contract per app package. `tools/quality/python/lint-imports.sh` runs it with every `apps/*/src` and `libs/*/src` on the path. A second checker, `tools/quality/python/boundaries.py` (grimp 3.20), checks what import-linter cannot express: imports into another component only through its `public` entry points, and cycles between components.
- **Metrics collector:** `tools/quality/python/collect_metrics.py <components.json>` (grimp + radon) emits the snapshot schema of `docs/architecture/metrics/README.md`. `tools/quality/arch_metrics.py` is the shared, language-neutral step of `/arch-metrics`: it runs every registered language's collector per level, merges the snapshots, and writes `history/<date>.json`, `latest.md` and the coupling diagram of `architecture.md`.
- **Tests:** `pytest` 9.2.0, run by pre-commit and CI.
- **Security:** `pip-audit` 2.10.1 on the exported lock file (`tools/quality/python/audit.sh`) (pre-commit and CI); ruff `S`; a `uv` entry in `.github/dependabot.yml` with the 7-day cooldown.
- **Hooks:** a Claude `PostToolUse` hook (`tools/quality/python/lint-file.sh`) runs ruff on each edited `.py` file and returns exit 2 with the findings; local pre-commit hooks run ruff, ruff format, mypy, the import-linter drift check, `lint-imports`, the boundary checker, pytest and pip-audit; CI runs the same gate in `.github/workflows/python.yml` (SHA-pinned actions, read-only permissions).

## Alternatives considered
| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| Poetry or pip-tools | Mature | Slower; workspaces are weaker; a second tool next to uv, which is already installed | uv gives workspaces, a lock file and interpreter pinning in one tool |
| Python 3.15 (installed) | Newest | LinkML and pySHACL do not support it yet | The app depends on both |
| pyright instead of mypy | Faster | Needs Node for the CLI, so Python checks would depend on the JS toolchain | mypy is pure Python |
| bandit as a separate hook | Full bandit output | Duplicates ruff's `S` rules | One linter, one config |
| Only import-linter for boundaries | One tool | Cannot express "only through the public entry point" or cycles between components across levels | Added a small grimp checker for those two rules |
| Only a grimp checker, no import-linter | One tool, no generated config | Loses the established, well-reported contract types the playbook names | Both, with import-linter config generated so nothing is maintained by hand |
| `C901` at 10 in ruff | Strict | Turns the metrics warn band (11–15) into failures, which changes a threshold without an ADR (ADR-0005) | Fail at 15, report 11–15 |

## Consequences
- **Positive:** one command per check for every Python app and library; boundaries follow `components.json` automatically; the metrics of `/arch-metrics` come from the same graph as the boundary check.
- **Negative / trade-offs:** two boundary tools; pre-commit runs the Python tests, which makes commits slower as the suite grows; Python 3.14+ waits for LinkML.
- **Follow-up:** `tools/quality/languages.json` entry; root `pyproject.toml`, `.python-version`, `uv.lock`; `.pre-commit-config.yaml`; `.claude/settings.json` PostToolUse hook; `.github/workflows/python.yml` and the Python hooks skipped in `security.yml`; `.github/dependabot.yml`; root `CLAUDE.md` Conventions and `apps/ontology-builder/CLAUDE.md` commands; a baseline `/arch-metrics` snapshot.
