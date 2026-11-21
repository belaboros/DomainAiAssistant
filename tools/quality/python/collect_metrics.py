"""Emit the metrics snapshot (docs/architecture/metrics/README.md) for the Python code of one level.

Usage: uv run python tools/quality/python/collect_metrics.py <components.json>
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

import archgraph
import cc_report
import grimp

CE_WARN, CE_FAIL, D_WARN = 4, 7, 0.5
ABSTRACT_BASES = {"ABC", "Protocol"}


def package_dir(package: str) -> Path | None:
    """Folder (or file) of a dotted package under one of the src/ folders."""
    rel = Path(*package.split("."))
    for src in archgraph.src_dirs():
        for candidate in (src / rel, src / rel.with_suffix(".py")):
            if candidate.exists():
                return candidate
    return None


def unit_files(unit: archgraph.Unit) -> list[Path]:
    paths = [p for pkg in unit.packages if (p := package_dir(pkg)) is not None]
    return cc_report.python_files(paths)


def abstractness(files: list[Path]) -> float | None:
    """Share of classes that are ABCs or Protocols; None when there are no classes."""
    total = abstract = 0
    for path in files:
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ClassDef):
                total += 1
                bases = {
                    b.id if isinstance(b, ast.Name) else getattr(b, "attr", "") for b in node.bases
                }
                abstract += bool(bases & ABSTRACT_BASES)
    return round(abstract / total, 3) if total else None


def _base_names(node: ast.ClassDef) -> set[str]:
    return {b.id if isinstance(b, ast.Name) else getattr(b, "attr", "") for b in node.bases}


def internal_refs(graph: grimp.ImportGraph, modules: list[str]) -> int:
    inside = set(modules)
    return sum(len(graph.find_modules_directly_imported_by(m) & inside) for m in modules)


def externals(graph: grimp.ImportGraph, modules: list[str]) -> list[str]:
    found = {
        imported
        for m in modules
        for imported in graph.find_modules_directly_imported_by(m)
        if graph.is_module_squashed(imported)
    }
    return sorted(found)


def component_row(unit: archgraph.Unit, ctx: dict[str, Any], ca: int, ce: int) -> dict[str, Any]:
    graph: grimp.ImportGraph = ctx["graph"]
    modules = sorted(m for m, u in ctx["owners"].items() if u.name == unit.name)
    instability = round(ce / (ca + ce), 3) if ca + ce else 0.0
    a = abstractness(unit_files(unit))
    return {
        "name": unit.name,
        "ca": ca,
        "ce": ce,
        "instability": instability,
        "relationalCohesion": round((internal_refs(graph, modules) + 1) / len(modules), 3)
        if modules
        else None,
        "abstractness": a,
        "distance": round(abs(a + instability - 1), 3) if a is not None else None,
        "externalDeps": externals(graph, modules),
    }


def sdp_violations(
    rows: list[dict[str, Any]], pairs: list[tuple[str, str]]
) -> list[dict[str, str]]:
    inst = {r["name"]: r["instability"] for r in rows}
    return [
        {"kind": "sdp", "detail": f"{a} -> {b}: I({b})={inst[b]} > I({a})={inst[a]}"}
        for a, b in pairs
        if inst[b] > inst[a]
    ]


def result_of(snapshot: dict[str, Any]) -> str:
    kinds = {v["kind"] for v in snapshot["violations"]}
    comps = snapshot["components"]
    max_ce = max((c["ce"] for c in comps), default=0)
    if kinds & {"boundary", "cycle", "cc"} or max_ce > CE_FAIL:
        return "fail"
    warnings = [
        "sdp" in kinds,
        bool(snapshot["functions"]["overWarn"]),
        max_ce > CE_WARN,
        any((c["distance"] or 0) > D_WARN for c in comps),
    ]
    return "warn" if any(warnings) else "pass"


def functions_block(units: list[archgraph.Unit]) -> dict[str, Any]:
    files = sorted({f for u in units for f in unit_files(u)})
    measured = cc_report.measure(files)
    ccs = [f.cc for f in measured]
    over = [
        {"file": f.file, "function": f.function, "cc": f.cc}
        for f in sorted(measured, key=lambda f: -f.cc)
        if f.cc > cc_report.WARN
    ]
    return {
        "count": len(ccs),
        "ccAvg": round(sum(ccs) / len(ccs), 2) if ccs else 0.0,
        "ccMax": max(ccs, default=0),
        "overWarn": over,
    }


def all_violations(
    is_system: bool, units: list[archgraph.Unit], ctx: dict[str, Any]
) -> list[dict[str, str]]:
    found = ctx["edges"]
    out = archgraph.violations(is_system, units, found)
    out += [{"kind": "cycle", "detail": " -> ".join(c)} for c in ctx["cycles"]]
    out += sdp_violations(ctx["rows"], sorted(found))
    over = ctx["functions"]["overWarn"]
    fails = [f for f in over if f["cc"] > cc_report.FAIL]
    return out + [
        {"kind": "cc", "detail": f"{f['file']}::{f['function']} CC {f['cc']}"} for f in fails
    ]


def collect(components_json: Path) -> dict[str, Any]:
    is_system, units = archgraph.load_units(components_json)
    graph = archgraph.build_graph()
    owners = archgraph.first_party(graph, units)
    found = archgraph.edges(graph, owners)
    pairs = sorted(found)
    ctx: dict[str, Any] = {"graph": graph, "owners": owners, "edges": found}
    ca = {u.name: sum(1 for _, b in pairs if b == u.name) for u in units}
    ce = {u.name: sum(1 for a, _ in pairs if a == u.name) for u in units}
    ctx["rows"] = [component_row(u, ctx, ca[u.name], ce[u.name]) for u in units]
    ctx["functions"] = functions_block(units)
    ctx["cycles"] = archgraph.cycles([u.name for u in units], set(pairs))
    snapshot: dict[str, Any] = {
        "date": date.today().isoformat(),
        "commit": git_sha(),
        "languages": ["python"],
        "functions": ctx["functions"],
        "components": ctx["rows"],
        "dependencies": [{"from": a, "to": b, "count": found[(a, b)].count} for a, b in pairs],
        "cycles": ctx["cycles"],
        "violations": all_violations(is_system, units, ctx),
    }
    snapshot["result"] = result_of(snapshot)
    return snapshot


def git_sha() -> str:
    out = subprocess.run(
        ["git", "rev-parse", "HEAD"],  # noqa: S607
        cwd=archgraph.ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return out.stdout.strip()


def main() -> int:
    if len(sys.argv) != 2:  # noqa: PLR2004
        print(__doc__, file=sys.stderr)
        return 2
    print(json.dumps(collect(Path(sys.argv[1]).resolve()), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
