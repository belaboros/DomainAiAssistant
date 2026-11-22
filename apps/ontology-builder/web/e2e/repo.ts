// The temporary git repository of the end-to-end fixture (tools/e2e_server.py): read its state
// with git, and switch its pre-commit hook between passing and failing.
import { execFileSync } from "node:child_process";
import { join } from "node:path";

const root = process.env.ONTOLOGY_BUILDER_E2E_DIR;
if (root === undefined) throw new Error("ONTOLOGY_BUILDER_E2E_DIR is set by playwright.config.ts");

export const REPO = join(root, "repo");
export const REMOTE = join(root, "remote.git");
export const DATASET = "data/ontology-e2e-house-rules/";

function git(cwd: string, ...args: string[]): string {
  return execFileSync("git", ["-C", cwd, ...args], { encoding: "utf8" }).trimEnd();
}

/** The number of commits on the current branch. */
export function commitCount(): number {
  return Number(git(REPO, "rev-list", "--count", "HEAD"));
}

export function headSha(): string {
  return git(REPO, "rev-parse", "HEAD");
}

export function headSubject(): string {
  return git(REPO, "log", "-1", "--format=%s");
}

/** The paths the last commit touched. */
export function headFiles(): string[] {
  return git(REPO, "show", "--name-only", "--format=", "HEAD").split("\n").filter(Boolean);
}

/** `git status --porcelain`, one line per changed path. */
export function workingChanges(): string[] {
  return git(REPO, "status", "--porcelain").split("\n").filter(Boolean);
}

/** The commit of `main` on the bare remote. */
export function remoteMain(): string {
  return git(REMOTE, "rev-parse", "main");
}

/** While on (git config `e2e.hookfails`), the pre-commit hook fails with a detect-secrets
 * message. */
export function hookFails(on: boolean): void {
  git(REPO, "config", "e2e.hookfails", on ? "true" : "false");
}
