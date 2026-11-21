# ADR-0004: Hold changes in a pending change set; save them atomically as one git commit

- **Status:** accepted
- **Scope:** app `ontology-builder`
- **Date:** 2026-11-21
- **Related:** [spec 0002](../../../../../docs/specs/0002-ontology-builder/spec.md) FR-8, FR-26 to FR-29, edge cases "git unavailable", "two GUI windows", "governed build fails"; [idea 0002](../../../../../docs/ideas/0002-ontology-builder.md) Q15

## Context

Each save in the GUI must create exactly one git commit that touches only that ontology's dataset, runs the repo's hooks, and never pushes (FR-27). If a hook fails, nothing is committed. If git is unavailable or the branch has conflicts, saving is refused and "nothing is written outside a commit". An interrupted ingestion must leave no partial records (FR-8). A failed governed build must leave the previous release untouched. One person uses the GUI at a time.

## Decision

We will:
- **Keep a pending change set.** Review and authoring actions change an in-memory copy of the ontology and add to a pending change set (the changes plus their decisions). The change set is journaled in the git-ignored work folder (`ONTOLOGY_BUILDER_WORK_DIR`), so a crash or restart loses nothing.
- **Save in this order** (`workflows`):
  1. Check that the dataset's tree hash still equals the one loaded.
  2. Validate every changed record.
  3. Write the records and decisions into a staging copy `data/.<dataset>.staging/`.
  4. Rebuild the raw release there.
  5. Swap the folders by rename, keeping the old one as `data/.<dataset>.previous/`.
  6. Run `git add` and then `git commit -- data/<dataset>/` with hooks.

  Only after the commit succeeds is `.previous` removed. On any failure the old folder is swapped back and the hook output or error is returned. No code path pushes.
- **Write ingestion runs the same way.** LLM responses are cached per batch in the work folder, so an interrupted run resumes with `--resume <run-id>` and gives the same result. The records are written in one swap at the end. The governed build also writes to a staging folder and swaps only on success.
- **Allow one server process per dataset:** a lock file in the work folder. A second browser session on the same server is read-only.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
| Write every action to disk at once; commit on Save | Simple; survives crashes without a journal | Files sit on disk outside a commit; a failing hook leaves a half-saved dataset | Breaks "nothing is written outside a commit" |
| Commit after every action | No pending state | Hundreds of tiny commits, and the hooks run every time (slow) | FR-27 commits per save, not per action |
| `git restore` + `git clean` to roll back | No staging copy | Depends on git, so not usable for the evaluation's throw-away ontology; `git clean` in a pathspec is risky | The swap works with and without git |

## Consequences

- **Positive:** the dataset is always either the last commit or the new commit. Failures are visible and safe. The evaluation uses the same code without git.
- **Negative / trade-offs:** each save copies the dataset folder (fine up to the 5,000-element target). Staging folders appear in `data/` for a moment, so `.gitignore` gets `/data/.*.staging/` and `/data/.*.previous/`. Pending changes live outside git until saved; the journal mitigates that.
- **Follow-up:** the `store`, `vcs` and `workflows` components; `ONTOLOGY_BUILDER_WORK_DIR` in `.env.example`; `.gitignore` lines (T4); T10, T17, T18.
