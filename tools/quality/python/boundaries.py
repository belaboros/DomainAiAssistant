"""Check Python imports against every components.json, at system and app level (ADR-0020).

Fails on: an import between units that is not in ``mayDependOn``; any app-to-app import;
an import into another unit that bypasses its ``public`` entry points; a cycle between units.

Usage: uv run python tools/quality/python/boundaries.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import archgraph
import grimp


def check(components_json: Path, graph: grimp.ImportGraph) -> list[str]:
    """Return the problems found for one components.json."""
    is_system, units = archgraph.load_units(components_json)
    owners = archgraph.first_party(graph, units)
    found = archgraph.edges(graph, owners)
    problems = [v["detail"] for v in archgraph.violations(is_system, units, found)]
    for cycle in archgraph.cycles([u.name for u in units], set(found)):
        problems.append("cycle: " + " -> ".join(cycle))
    return problems


def main() -> int:
    graph = archgraph.build_graph()
    files = [archgraph.ROOT_COMPONENTS, *archgraph.app_components_files()]
    failed = False
    for path in files:
        problems = check(path, graph)
        rel = path.relative_to(archgraph.ROOT)
        for problem in problems:
            print(f"{rel}: {problem}", file=sys.stderr)
        failed = failed or bool(problems)
    if not failed:
        print(f"Python boundaries: ok ({len(files)} components files)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
