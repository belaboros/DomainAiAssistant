// Vitest: the unit and component tests of the review GUI, next to the code in src/ (ADR-0021).
// Components render in happy-dom; src/test/setup.ts adds the Testing Library matchers.
// styles.css is processed (not stubbed), so the badge test can read the status colours.
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    include: ["src/**/*.test.{ts,tsx}"],
    environment: "happy-dom",
    setupFiles: ["src/test/setup.ts"],
    css: { include: [/src\/styles\.css/] },
  },
});
