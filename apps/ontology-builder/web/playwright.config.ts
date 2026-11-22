// Playwright: the end-to-end tests of the review GUI in e2e/ (ADR-0021, plan 0002 T27).
// The web server is `ontology-builder serve` on a fixture dataset in a new temporary git
// repository (apps/ontology-builder/tools/e2e_server.py); it serves the built GUI, so
// `npm run e2e` builds it first. The tests share one server and run in order, in one worker.
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { defineConfig, devices } from "@playwright/test";

const port = "8775"; // not 8765, so a running `serve` does not clash
// Set once in the runner process; the workers inherit it, so they see the same folder.
process.env.ONTOLOGY_BUILDER_E2E_DIR ??= mkdtempSync(join(tmpdir(), "ontology-builder-e2e-"));
const dir = process.env.ONTOLOGY_BUILDER_E2E_DIR;
const repoRoot = resolve(import.meta.dirname, "../../..");

export default defineConfig({
  testDir: "e2e",
  forbidOnly: process.env.CI !== undefined,
  fullyParallel: false,
  workers: 1,
  reporter: "list",
  use: { baseURL: `http://127.0.0.1:${port}` },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: `uv run --package ontology-builder python apps/ontology-builder/tools/e2e_server.py "${dir}" --port ${port}`,
    cwd: repoRoot,
    url: `http://127.0.0.1:${port}/`,
    reuseExistingServer: false,
    timeout: 120_000,
    stdout: "pipe",
    // SIGTERM lets the server remove its temporary folder (SIGKILL is the default).
    gracefulShutdown: { signal: "SIGTERM", timeout: 10_000 },
  },
});
