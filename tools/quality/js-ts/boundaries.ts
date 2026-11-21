// Check JS/TS imports against every components.json, at system and app level (ADR-0021).
// dependency-cruiser enforces the generated rules module by module; this adds what it cannot
// express: cycles between components. It also reports undeclared edges, app-to-app imports and
// imports past `public` entry points, in the same words as tools/quality/python/boundaries.py.
//
// Usage: node tools/quality/js-ts/boundaries.ts
import { relative } from "node:path";

import {
  appComponentsFiles,
  cruise,
  cycles,
  edges,
  loadLevel,
  pairsOf,
  ROOT,
  ROOT_COMPONENTS,
  violations,
  type CruisedModule,
  type Level,
} from "./archgraph.ts";

function problemsOf(level: Level, modules: CruisedModule[]): string[] {
  const found = edges(modules, level.units);
  const problems = violations(level, found).map((v) => v.detail);
  return [...problems, ...cycles(pairsOf(found)).map((cycle) => `cycle: ${cycle.join(" -> ")}`)];
}

function main(): number {
  const modules = cruise();
  const files = [ROOT_COMPONENTS, ...appComponentsFiles()];
  let failed = false;
  for (const file of files) {
    const problems = problemsOf(loadLevel(file), modules);
    for (const problem of problems) console.error(`${relative(ROOT, file)}: ${problem}`);
    if (problems.length > 0) failed = true;
  }
  if (!failed) console.log(`JS/TS boundaries: ok (${String(files.length)} components files)`);
  return failed ? 1 : 0;
}

process.exitCode = main();
