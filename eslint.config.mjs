// ESLint flat config of the repo-wide JS/TS quality gate (ADR-0021).
// Limits follow docs/architecture/metrics/README.md: CC fails above 15 (11-15 is the warn band,
// reported by tools/quality/js-ts/cc_report.ts), plus nesting, argument and size limits.
import js from "@eslint/js";
import { defineConfig } from "eslint/config";
import security from "eslint-plugin-security";
import globals from "globals";
import tseslint from "typescript-eslint";

/** @type {import("eslint").Linter.RulesRecord} */
export const LIMITS = {
  complexity: ["error", 15],
  "max-depth": ["error", 4],
  "max-params": ["error", 6],
  "max-statements": ["error", 50],
  "max-lines-per-function": ["error", { max: 100, skipBlankLines: true, skipComments: true }],
};

export default defineConfig(
  {
    ignores: [
      ".venv/",
      "**/.*_cache/",
      "**/__pycache__/",
      "**/node_modules/",
      "**/dist/",
      "**/coverage/",
      "**/playwright-report/",
      "**/test-results/",
      "data/",
      "docs/",
      "apps/*/.work/",
    ],
  },
  js.configs.recommended,
  tseslint.configs.strictTypeChecked,
  security.configs.recommended,
  {
    languageOptions: {
      globals: { ...globals.node },
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: LIMITS,
  },
  {
    // The gate's own tools read repo files and build regexes from components.json by design;
    // their inputs are the repo itself, never user input. App and library code keeps these rules.
    files: ["tools/**"],
    rules: {
      "security/detect-non-literal-fs-filename": "off",
      "security/detect-non-literal-regexp": "off",
      "security/detect-object-injection": "off",
    },
  },
  {
    files: ["apps/*/web/src/**"],
    languageOptions: { globals: { ...globals.browser } },
  },
);
