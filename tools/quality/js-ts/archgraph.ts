// The JS/TS module graph mapped to the components of one level (ADR-0021).
// Shared by gen_depcruise.ts, boundaries.ts and collect_metrics.ts.
import { spawnSync } from "node:child_process";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";

export const ROOT = resolve(import.meta.dirname, "..", "..", "..");
export const ROOT_COMPONENTS = join(ROOT, "docs", "architecture", "components.json");
export const DEPCRUISE_CONFIG = join(ROOT, ".dependency-cruiser.json");
export const CRUISE_DIRS = ["apps", "libs", "tools"];
export const SOURCE_EXTENSIONS = ["ts", "tsx", "mts", "cts", "js", "jsx", "mjs", "cjs"];

export interface Unit {
  name: string;
  kind: "app" | "lib" | "component";
  paths: string[];
  mayDependOn: string[];
  public: string[];
}

export interface Level {
  name: string;
  isSystem: boolean;
  units: Unit[];
}

interface RawUnit {
  name: string;
  kind?: string;
  paths?: string[];
  mayDependOn?: string[];
  public?: string[];
}

export function loadLevel(componentsPath: string): Level {
  const file = resolve(componentsPath);
  const data = JSON.parse(readFileSync(file, "utf-8")) as { components: RawUnit[] };
  const isSystem = file === ROOT_COMPONENTS;
  const units = data.components.map((raw): Unit => ({
    name: raw.name,
    kind: raw.kind === "app" || raw.kind === "lib" ? raw.kind : "component",
    paths: raw.paths ?? [],
    mayDependOn: raw.mayDependOn ?? [],
    public: raw.public ?? [],
  }));
  const name = isSystem ? "system" : (relative(ROOT, file).split("/")[1] ?? "app");
  return { name, isSystem, units };
}

export function appComponentsFiles(): string[] {
  const apps = join(ROOT, "apps");
  if (!existsSync(apps)) return [];
  return readdirSync(apps, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => join(apps, entry.name, "docs", "architecture", "components.json"))
    .filter((path) => existsSync(path))
    .sort();
}

export function allLevels(): Level[] {
  return [ROOT_COMPONENTS, ...appComponentsFiles()].map(loadLevel);
}

const REGEX_SPECIAL = /[.+^${}()|[\]\\]/g;

/** A `paths` glob of components.json as a regex body: `**` spans folders, `*` does not. */
export function globToRegex(glob: string): string {
  const escaped = glob.replace(REGEX_SPECIAL, "\\$&");
  return escaped
    .replace(/\*\*\//g, "\u0000")
    .replace(/\*\*/g, "\u0001")
    .replace(/\*/g, "[^/]*")
    .replace(/\?/g, "[^/]")
    .replaceAll("\u0000", "(?:.+/)?")
    .replaceAll("\u0001", ".*");
}

export function pathsRegex(globs: string[]): string {
  return `^(?:${globs.map(globToRegex).join("|")})$`;
}

export function owner(path: string, units: Unit[]): Unit | undefined {
  return units.find((unit) => unit.paths.some((glob) => new RegExp(pathsRegex([glob])).test(path)));
}

export interface CruisedDependency {
  resolved: string;
  module: string;
  dependencyTypes: string[];
  couldNotResolve: boolean;
}

export interface CruisedModule {
  source: string;
  dependencies: CruisedDependency[];
}

/** Every JS/TS module under apps/, libs/ and tools/, with its resolved dependencies. */
export function cruise(): CruisedModule[] {
  const bin = join(ROOT, "node_modules", ".bin", "depcruise");
  const dirs = CRUISE_DIRS.filter((dir) => existsSync(join(ROOT, dir)));
  const args = ["--config", DEPCRUISE_CONFIG, "--output-type", "json", ...dirs];
  const done = spawnSync(bin, args, { cwd: ROOT, encoding: "utf-8", maxBuffer: 1 << 28 });
  if (done.error !== undefined) throw done.error;
  if (!done.stdout.trim()) throw new Error(`depcruise produced no output: ${done.stderr}`);
  const result = JSON.parse(done.stdout) as { modules: CruisedModule[] };
  return result.modules;
}

export function isFirstParty(dependency: CruisedDependency): boolean {
  return dependency.dependencyTypes.some((type) => type === "local");
}

export interface Edge {
  from: string;
  to: string;
  count: number;
  files: string[];
}

/** Dependencies between different units of the level, with the target files they reach. */
export function edges(modules: CruisedModule[], units: Unit[]): Map<string, Edge> {
  const found = new Map<string, Edge>();
  for (const module of modules) {
    const from = owner(module.source, units);
    if (from === undefined) continue;
    for (const dependency of module.dependencies.filter(isFirstParty)) {
      const to = owner(dependency.resolved, units);
      if (to === undefined || to.name === from.name) continue;
      const key = `${from.name}\u0000${to.name}`;
      const edge = found.get(key) ?? { from: from.name, to: to.name, count: 0, files: [] };
      edge.count += 1;
      edge.files.push(dependency.resolved);
      found.set(key, edge);
    }
  }
  return found;
}

/** Elementary cycles of the component graph, each starting at its smallest name. */
export function cycles(pairs: [string, string][]): string[][] {
  const next = new Map<string, string[]>();
  for (const [from, to] of pairs) next.set(from, [...(next.get(from) ?? []), to].sort());
  const found: string[][] = [];
  const walk = (start: string, node: string, path: string[]): void => {
    for (const target of next.get(node) ?? []) {
      if (target === start) found.push([...path, start]);
      else if (target > start && !path.includes(target)) walk(start, target, [...path, target]);
    }
  };
  for (const start of [...next.keys()].sort()) walk(start, start, [start]);
  return found;
}

export interface Violation {
  kind: "boundary" | "cycle" | "sdp" | "cc";
  detail: string;
}

function privateImports(edge: Edge, target: Unit): Violation[] {
  if (target.public.length === 0) return [];
  const entry = new RegExp(pathsRegex(target.public));
  return [...new Set(edge.files)]
    .filter((file) => !entry.test(file))
    .sort()
    .map((file) => ({
      kind: "boundary",
      detail: `${edge.from} -> ${edge.to}: ${file} is not a public entry point of ${target.name}`,
    }));
}

/** Boundary violations: undeclared edges, app-to-app edges, imports past `public` entries. */
export function violations(level: Level, found: Map<string, Edge>): Violation[] {
  const byName = new Map(level.units.map((unit) => [unit.name, unit]));
  const out: Violation[] = [];
  for (const edge of [...found.values()].sort((a, b) =>
    `${a.from}${a.to}`.localeCompare(`${b.from}${b.to}`),
  )) {
    const source = byName.get(edge.from);
    const target = byName.get(edge.to);
    if (source === undefined || target === undefined) continue;
    if (level.isSystem && target.kind === "app") {
      out.push({
        kind: "boundary",
        detail: `${edge.from} -> ${edge.to}: an app never imports an app`,
      });
    } else if (!source.mayDependOn.includes(edge.to)) {
      out.push({
        kind: "boundary",
        detail: `${edge.from} -> ${edge.to}: not in mayDependOn of ${edge.from}`,
      });
    }
    out.push(...privateImports(edge, target));
  }
  return out;
}

export function pairsOf(found: Map<string, Edge>): [string, string][] {
  return [...found.values()].map((edge): [string, string] => [edge.from, edge.to]).sort();
}
