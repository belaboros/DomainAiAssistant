// Cyclomatic complexity of every JS/TS function, by ESLint's own `complexity` count (ADR-0021).
// ESLint has one threshold per rule (it fails above 15), so this report shows the warn band
// (CC 11-15) and fails above 15. The metrics collector uses `measure` too.
//
// Usage: node tools/quality/js-ts/cc_report.ts [paths...]   (default: the whole repo)
import { relative } from "node:path";

import { ESLint } from "eslint";

import { ROOT } from "./archgraph.ts";

export const WARN = 10;
export const FAIL = 15;

export interface FunctionCc {
  file: string;
  function: string;
  cc: number;
}

const COUNT = /^(?<name>.*?) has a complexity of (?<cc>\d+)\./;

/** CC of every function in `patterns` (relative to the repo root), sorted by file and line. */
export async function measure(patterns: string[] = ["."]): Promise<FunctionCc[]> {
  const eslint = new ESLint({
    cwd: ROOT,
    overrideConfig: { rules: { complexity: ["warn", 0] } },
    ruleFilter: ({ ruleId }) => ruleId === "complexity",
    warnIgnored: false,
  });
  const results = await eslint.lintFiles(patterns);
  const found: FunctionCc[] = [];
  for (const result of results) {
    for (const message of result.messages) {
      const match = COUNT.exec(message.message);
      if (message.ruleId !== "complexity" || match?.groups === undefined) continue;
      const name = match.groups.name ?? "function";
      found.push({
        file: relative(ROOT, result.filePath),
        function: `${name} (line ${String(message.line)})`,
        cc: Number(match.groups.cc),
      });
    }
  }
  return found;
}

async function main(): Promise<number> {
  const args = process.argv.slice(2);
  const measured = await measure(args.length > 0 ? args : ["."]);
  const over = measured.filter((f) => f.cc > WARN).sort((a, b) => b.cc - a.cc);
  for (const f of over) {
    const kind = f.cc > FAIL ? "FAIL" : "warn";
    console.log(`${kind} CC ${String(f.cc)} ${f.file}::${f.function}`);
  }
  console.log(
    `${String(measured.length)} functions, ${String(over.length)} over CC ${String(WARN)}`,
  );
  return over.some((f) => f.cc > FAIL) ? 1 : 0;
}

if (import.meta.main) process.exitCode = await main();
