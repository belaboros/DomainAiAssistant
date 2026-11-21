// Emit the metrics snapshot (docs/architecture/metrics/README.md) for the JS/TS code of one level.
// tools/quality/arch_metrics.py merges it with the other languages' snapshots (ADR-0021).
//
// Usage: node tools/quality/js-ts/collect_metrics.ts <components.json>
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { join } from "node:path";

import ts from "typescript";

import {
  cruise,
  cycles,
  edges,
  isFirstParty,
  loadLevel,
  owner,
  pairsOf,
  ROOT,
  violations,
  type CruisedModule,
  type Level,
  type Unit,
  type Violation,
} from "./archgraph.ts";
import { FAIL, measure, WARN, type FunctionCc } from "./cc_report.ts";

const CE_WARN = 4;
const CE_FAIL = 7;
const D_WARN = 0.5;

interface Row {
  name: string;
  ca: number;
  ce: number;
  instability: number;
  relationalCohesion: number | null;
  abstractness: number | null;
  distance: number | null;
  externalDeps: string[];
}

const round = (value: number, digits = 3): number => Number(value.toFixed(digits));

/** Interfaces and abstract classes among all interfaces and classes; null without any. */
export function abstractness(files: string[]): number | null {
  let total = 0;
  let abstract = 0;
  const visit = (node: ts.Node): void => {
    if (ts.isInterfaceDeclaration(node)) {
      total += 1;
      abstract += 1;
    } else if (ts.isClassDeclaration(node) || ts.isClassExpression(node)) {
      total += 1;
      const modifiers = ts.canHaveModifiers(node) ? ts.getModifiers(node) : undefined;
      if (modifiers?.some((m) => m.kind === ts.SyntaxKind.AbstractKeyword)) abstract += 1;
    }
    ts.forEachChild(node, visit);
  };
  for (const file of files) {
    const text = readFileSync(join(ROOT, file), "utf-8");
    visit(ts.createSourceFile(file, text, ts.ScriptTarget.Latest, true));
  }
  return total > 0 ? round(abstract / total) : null;
}

function packageName(module: string): string {
  const parts = module.split("/");
  return module.startsWith("@") ? parts.slice(0, 2).join("/") : (parts[0] ?? module);
}

interface Context {
  level: Level;
  modules: CruisedModule[];
  pairs: [string, string][];
}

function row(unit: Unit, ctx: Context): Row {
  const own = ctx.modules.filter((m) => owner(m.source, ctx.level.units)?.name === unit.name);
  const sources = new Set(own.map((m) => m.source));
  const deps = own.flatMap((m) => m.dependencies);
  const internal = deps.filter((d) => isFirstParty(d) && sources.has(d.resolved)).length;
  const external = deps.filter((d) => d.dependencyTypes.some((t) => t.startsWith("npm")));
  const ca = ctx.pairs.filter(([, to]) => to === unit.name).length;
  const ce = ctx.pairs.filter(([from]) => from === unit.name).length;
  const instability = ca + ce > 0 ? round(ce / (ca + ce)) : 0;
  const a = abstractness([...sources]);
  return {
    name: unit.name,
    ca,
    ce,
    instability,
    relationalCohesion: own.length > 0 ? round((internal + 1) / own.length) : null,
    abstractness: a,
    distance: a === null ? null : round(Math.abs(a + instability - 1)),
    externalDeps: [...new Set(external.map((d) => packageName(d.module)))].sort(),
  };
}

function functionsBlock(measured: FunctionCc[]): Record<string, unknown> {
  const ccs = measured.map((f) => f.cc);
  const sum = ccs.reduce((a, b) => a + b, 0);
  return {
    count: ccs.length,
    ccAvg: ccs.length > 0 ? round(sum / ccs.length, 2) : 0,
    ccMax: Math.max(0, ...ccs),
    overWarn: measured.filter((f) => f.cc > WARN).sort((a, b) => b.cc - a.cc),
  };
}

function sdp(rows: Row[], pairs: [string, string][]): Violation[] {
  const inst = new Map(rows.map((r) => [r.name, r.instability]));
  return pairs
    .filter(([from, to]) => (inst.get(to) ?? 0) > (inst.get(from) ?? 0))
    .map(([from, to]) => ({
      kind: "sdp",
      detail: `${from} -> ${to}: I(${to})=${String(inst.get(to))} > I(${from})=${String(inst.get(from))}`,
    }));
}

function resultOf(found: Violation[], rows: Row[], overWarn: boolean): "pass" | "warn" | "fail" {
  const kinds = new Set(found.map((v) => v.kind));
  const maxCe = Math.max(0, ...rows.map((r) => r.ce));
  if (kinds.has("boundary") || kinds.has("cycle") || kinds.has("cc") || maxCe > CE_FAIL) {
    return "fail";
  }
  const warnings = [
    kinds.has("sdp"),
    overWarn,
    maxCe > CE_WARN,
    rows.some((r) => (r.distance ?? 0) > D_WARN),
  ];
  return warnings.some(Boolean) ? "warn" : "pass";
}

function gitSha(): string {
  try {
    return execFileSync("git", ["rev-parse", "HEAD"], { cwd: ROOT, encoding: "utf-8" }).trim();
  } catch {
    return "";
  }
}

export async function collect(componentsPath: string): Promise<Record<string, unknown>> {
  const level = loadLevel(componentsPath);
  const modules = cruise();
  const found = edges(modules, level.units);
  const pairs = pairsOf(found);
  const ctx: Context = { level, modules, pairs };
  const rows = level.units.map((unit) => row(unit, ctx));
  const owned = new Set(
    modules.filter((m) => owner(m.source, level.units) !== undefined).map((m) => m.source),
  );
  const measured = owned.size > 0 ? await measure([...owned].sort()) : [];
  const loops = cycles(pairs);
  const cc: Violation[] = measured
    .filter((f) => f.cc > FAIL)
    .map((f) => ({ kind: "cc", detail: `${f.file}::${f.function} CC ${String(f.cc)}` }));
  const all: Violation[] = [
    ...violations(level, found),
    ...loops.map((loop): Violation => ({ kind: "cycle", detail: loop.join(" -> ") })),
    ...sdp(rows, pairs),
    ...cc,
  ];
  return {
    date: new Date().toISOString().slice(0, 10),
    commit: gitSha(),
    languages: ["js-ts"],
    functions: functionsBlock(measured),
    components: rows,
    dependencies: [...found.values()].map((e) => ({ from: e.from, to: e.to, count: e.count })),
    cycles: loops,
    violations: all,
    result: resultOf(
      all,
      rows,
      measured.some((f) => f.cc > WARN),
    ),
  };
}

async function main(): Promise<number> {
  const [path] = process.argv.slice(2);
  if (path === undefined) {
    console.error("usage: node tools/quality/js-ts/collect_metrics.ts <components.json>");
    return 2;
  }
  console.log(JSON.stringify(await collect(path), null, 2));
  return 0;
}

process.exitCode = await main();
