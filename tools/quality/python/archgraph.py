"""Python import graph mapped onto the components of a components.json (ADR-0020).

Shared by the boundary checker, the import-linter generator and the metrics collector.
A components.json is either the root one (units: apps and libraries, ``kind`` set) or an
app one (units: the app's internal components). Paths are globs relative to the repo root.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import grimp

ROOT = Path(__file__).resolve().parents[3]
ROOT_COMPONENTS = ROOT / "docs" / "architecture" / "components.json"


@dataclass
class Unit:
    """One component (app, library or in-app component) and its Python modules."""

    name: str
    kind: str
    may_depend_on: set[str]
    public: set[str]
    packages: list[str] = field(default_factory=list)


@dataclass
class Edge:
    """Imports from one unit to another."""

    source: str
    target: str
    count: int = 0
    modules: set[tuple[str, str]] = field(default_factory=set)


def src_dirs() -> list[Path]:
    """Every src/ folder that holds Python packages, in apps/ and libs/."""
    return sorted(p for p in ROOT.glob("*/*/src") if p.parts[-3] in {"apps", "libs"})


def top_packages() -> list[str]:
    """Top-level Python packages found under the src/ folders."""
    return sorted(init.parent.name for src in src_dirs() for init in src.glob("*/__init__.py"))


def module_of(path: str) -> str | None:
    """Turn a repo-relative path under a src/ folder into a dotted module name."""
    parts = Path(path.removesuffix("/**").removesuffix("/__init__.py")).parts
    if "src" not in parts:
        return None
    dotted = parts[parts.index("src") + 1 :]
    if dotted and dotted[-1].endswith(".py"):
        dotted = (*dotted[:-1], dotted[-1].removesuffix(".py"))
    return ".".join(dotted) or None


def _packages_of(path_glob: str) -> list[str]:
    module = module_of(path_glob)
    if module is not None:
        return [module]
    base = ROOT / path_glob.removesuffix("/**")
    return sorted(init.parent.name for init in (base / "src").glob("*/__init__.py"))


def load_units(components_json: Path) -> tuple[bool, list[Unit]]:
    """Read a components.json; return (is_system_level, units)."""
    data = json.loads(components_json.read_text(encoding="utf-8"))
    units: list[Unit] = []
    is_system = any("kind" in c for c in data["components"])
    for comp in data["components"]:
        public = {m for p in comp.get("public", []) if (m := module_of(p))}
        unit = Unit(
            name=comp["name"],
            kind=comp.get("kind", "component"),
            may_depend_on=set(comp.get("mayDependOn", [])),
            public=public,
        )
        for glob in comp["paths"]:
            unit.packages.extend(_packages_of(glob))
        units.append(unit)
    return is_system, units


def app_components_files() -> list[Path]:
    """Every app-level components.json."""
    return sorted(ROOT.glob("apps/*/docs/architecture/components.json"))


def build_graph() -> grimp.ImportGraph:
    """Import graph of every first-party package, with external packages as leaves."""
    for src in src_dirs():
        if str(src) not in sys.path:
            sys.path.insert(0, str(src))
    packages = top_packages()
    if not packages:
        raise SystemExit("No Python packages found under apps/*/src or libs/*/src.")
    return grimp.build_graph(*packages, include_external_packages=True)


def owner_of(module: str, units: list[Unit]) -> Unit | None:
    """The unit whose package is the longest prefix of the module."""
    best: tuple[int, Unit] | None = None
    for unit in units:
        for pkg in unit.packages:
            if (module == pkg or module.startswith(pkg + ".")) and (
                best is None or len(pkg) > best[0]
            ):
                best = (len(pkg), unit)
    return best[1] if best else None


def first_party(graph: grimp.ImportGraph, units: list[Unit]) -> dict[str, Unit]:
    """Map each first-party module of the graph to its unit."""
    owners: dict[str, Unit] = {}
    for module in graph.modules:
        if graph.is_module_squashed(module):
            continue
        unit = owner_of(module, units)
        if unit is not None:
            owners[module] = unit
    return owners


def edges(graph: grimp.ImportGraph, owners: dict[str, Unit]) -> dict[tuple[str, str], Edge]:
    """Cross-unit import edges, with the number of import statements behind each."""
    result: dict[tuple[str, str], Edge] = {}
    for importer, src_unit in owners.items():
        for imported in graph.find_modules_directly_imported_by(importer):
            dst_unit = owners.get(imported)
            if dst_unit is None or dst_unit.name == src_unit.name:
                continue
            key = (src_unit.name, dst_unit.name)
            edge = result.setdefault(key, Edge(src_unit.name, dst_unit.name))
            lines = graph.get_import_details(importer=importer, imported=imported)
            edge.count += max(1, len(lines))
            edge.modules.add((importer, imported))
    return result


def cycles(names: list[str], pairs: set[tuple[str, str]]) -> list[list[str]]:
    """Elementary cycles of the unit graph, each reported once (smallest name first)."""
    succ: dict[str, set[str]] = defaultdict(set)
    for a, b in pairs:
        succ[a].add(b)
    found: list[list[str]] = []
    for start in sorted(names):
        _walk(start, start, [start], succ, found)
    return found


def _walk(
    start: str, node: str, path: list[str], succ: dict[str, set[str]], found: list[list[str]]
) -> None:
    for nxt in sorted(succ[node]):
        if nxt == start:
            found.append([*path, start])
        elif nxt > start and nxt not in path:
            _walk(start, nxt, [*path, nxt], succ, found)


def violations(
    is_system: bool, units: list[Unit], found: dict[tuple[str, str], Edge]
) -> list[dict[str, str]]:
    """Boundary violations: undeclared edges, app-to-app edges, non-public entry points."""
    by_name = {u.name: u for u in units}
    out: list[dict[str, str]] = []
    for (a, b), edge in sorted(found.items()):
        src, dst = by_name[a], by_name[b]
        if is_system and dst.kind == "app":
            out.append({"kind": "boundary", "detail": f"{a} -> {b}: an app never imports an app"})
        elif b not in src.may_depend_on:
            out.append({"kind": "boundary", "detail": f"{a} -> {b}: not in mayDependOn of {a}"})
        out.extend(_private_imports(edge, dst))
    return out


def _private_imports(edge: Edge, dst: Unit) -> list[dict[str, str]]:
    if not dst.public:
        return []
    return [
        {
            "kind": "boundary",
            "detail": f"{edge.source} -> {edge.target}: {importer} imports {imported},"
            f" which is not a public entry point of {dst.name}",
        }
        for importer, imported in sorted(edge.modules)
        if imported not in dst.public
    ]
