// Playwright: the end-to-end tests of the review GUI in e2e/ (ADR-0021). T27 adds the server
// (`ontology-builder serve` on a fixture dataset in a temporary git repository).
import { defineConfig, devices } from "@playwright/test";

const port = process.env.ONTOLOGY_BUILDER_PORT ?? "8765";

export default defineConfig({
  testDir: "e2e",
  forbidOnly: process.env.CI !== undefined,
  reporter: "list",
  use: { baseURL: `http://127.0.0.1:${port}` },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
