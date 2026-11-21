// Vitest: the unit and component tests of the review GUI, next to the code in src/ (ADR-0021).
// T23 adds the browser-like environment and the React setup.
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["src/**/*.test.{ts,tsx}"],
  },
});
