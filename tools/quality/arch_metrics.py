"""Shared merge and render step of /arch-metrics, for every language (ADR-0005, ADR-0020).

For each level in scope it runs the ``metrics`` command of every language in
tools/quality/languages.json, merges the snapshots, and writes:
``history/<date>.json``, ``latest.md`` and the coupling block of ``architecture.md``.

Usage: uv run python tools/quality/arch_metrics.py [all | system | <app>]
"""

from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "tools" / "quality" / "languages.json"
CE_WARN, CE_FAIL, D_WARN = 4, 7, 0.5
BEGIN = "<!-- coupling:begin (generated, do not edit) -->"
END = "<!-- coupling:end -->"

Snapshot = dict[str, Any]


@dataclass(frozen=True)
class Level:
    """One level to measure: the system, or one app."""

    name: str
    components: Path
    metrics_dir: Path
    architecture: Path


def levels(scope: str) -> list[Level]:
    system = Level(
        "system",
        ROOT / "docs/architecture/components.json",
        ROOT / "docs/architecture/metrics",
        ROOT / "docs/architecture/architecture.md",
    )
    apps = [
        Level(p.parts[-4], p, p.parent / "metrics", p.parent / "architecture.md")
        for p in sorted(ROOT.glob("apps/*/docs/architecture/components.json"))
    ]
    if scope == "all":
        return [system, *apps]
    if scope == "system":
        return [system]
    chosen = [a for a in apps if a.name == scope]
    if not chosen:
        raise SystemExit(f"unknown scope {scope!r}: use all, system or an app name")
    return chosen


def run_language(command: str, components: Path) -> Snapshot:
    argv = [components.as_posix() if a == "<components.json>" else a for a in shlex.split(command)]
    out = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, check=True)  # noqa: S603
    snapshot: Snapshot = json.loads(out.stdout)
    return snapshot


def _merged_deps(snapshots: list[Snapshot]) -> list[dict[str, Any]]:
    deps: dict[tuple[str, str], int] = {}
    for snap in snapshots:
        for d in snap["dependencies"]:
            key = (d["from"], d["to"])
            deps[key] = deps.get(key, 0) + d["count"]
    return [{"from": a, "to": b, "count": n} for (a, b), n in sorted(deps.items())]


def _merged_functions(snapshots: list[Snapshot]) -> dict[str, Any]:
    funcs = [s["functions"] for s in snapshots]
    count = sum(f["count"] for f in funcs)
    weighted = sum(f["ccAvg"] * f["count"] for f in funcs)
    return {
        "count": count,
        "ccAvg": round(weighted / count, 2) if count else 0,
        "ccMax": max(f["ccMax"] for f in funcs),
        "overWarn": [w for f in funcs for w in f["overWarn"]],
    }


def merge(snapshots: list[Snapshot]) -> Snapshot:
    """Sum per component, union the edges; I, cycles and SDP are recomputed by finish()."""
    if len(snapshots) == 1:
        return snapshots[0]
    kept = [v for s in snapshots for v in s["violations"] if v["kind"] in {"boundary", "cc"}]
    return {
        **snapshots[0],
        "languages": sorted({lang for s in snapshots for lang in s["languages"]}),
        "functions": _merged_functions(snapshots),
        "dependencies": _merged_deps(snapshots),
        "violations": kept,
    }


def find_cycles(pairs: set[tuple[str, str]]) -> list[list[str]]:
    succ: dict[str, set[str]] = {}
    for a, b in pairs:
        succ.setdefault(a, set()).add(b)
    found: list[list[str]] = []

    def walk(start: str, node: str, path: list[str]) -> None:
        for nxt in sorted(succ.get(node, set())):
            if nxt == start:
                found.append([*path, start])
            elif nxt > start and nxt not in path:
                walk(start, nxt, [*path, nxt])

    for start in sorted(succ):
        walk(start, start, [start])
    return found


def _update_component(comp: dict[str, Any], pairs: set[tuple[str, str]]) -> None:
    comp["ca"] = sum(1 for _, b in pairs if b == comp["name"])
    comp["ce"] = sum(1 for a, _ in pairs if a == comp["name"])
    total = comp["ca"] + comp["ce"]
    comp["instability"] = round(comp["ce"] / total, 3) if total else 0.0
    a = comp["abstractness"]
    comp["distance"] = round(abs(a + comp["instability"] - 1), 3) if a is not None else None


def _sdp(snap: Snapshot, pairs: set[tuple[str, str]]) -> list[dict[str, str]]:
    inst = {c["name"]: c["instability"] for c in snap["components"]}
    return [
        {"kind": "sdp", "detail": f"{a} -> {b}: I({b})={inst[b]} > I({a})={inst[a]}"}
        for a, b in sorted(pairs)
        if inst.get(b, 0) > inst.get(a, 0)
    ]


def finish(snap: Snapshot) -> Snapshot:
    """Recompute Ca, Ce, I, D, cycles, SDP violations and the result on the merged graph."""
    pairs = {(d["from"], d["to"]) for d in snap["dependencies"]}
    for comp in snap["components"]:
        _update_component(comp, pairs)
    snap["cycles"] = find_cycles(pairs)
    kept = [v for v in snap["violations"] if v["kind"] in {"boundary", "cc"}]
    kept += [{"kind": "cycle", "detail": " -> ".join(c)} for c in snap["cycles"]]
    snap["violations"] = kept + _sdp(snap, pairs)
    snap["result"] = result_of(snap)
    return snap


def result_of(snap: Snapshot) -> str:
    kinds = {v["kind"] for v in snap["violations"]}
    comps = snap["components"]
    max_ce = max((c["ce"] for c in comps), default=0)
    if kinds & {"boundary", "cycle", "cc"} or max_ce > CE_FAIL:
        return "fail"
    warnings = [
        "sdp" in kinds,
        bool(snap["functions"]["overWarn"]),
        max_ce > CE_WARN,
        any((c["distance"] or 0) > D_WARN for c in comps),
    ]
    return "warn" if any(warnings) else "pass"


def previous(history: Path, today: str) -> Snapshot | None:
    older = sorted(p for p in history.glob("*.json") if p.stem < today)
    return json.loads(older[-1].read_text(encoding="utf-8")) if older else None


def status_of(comp: dict[str, Any]) -> str:
    if comp["ce"] > CE_FAIL:
        return "fail"
    far = comp["distance"] is not None and comp["distance"] > D_WARN
    return "warn" if comp["ce"] > CE_WARN or far else "pass"


def _fmt(value: Any) -> str:
    return "n/a" if value is None else str(value)


def component_table(snap: Snapshot) -> list[str]:
    lines = [
        "| Component | Ca | Ce | I | H | A | D | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for c in snap["components"]:
        cells = [c["name"], c["ca"], c["ce"], c["instability"], c["relationalCohesion"]]
        cells += [c["abstractness"], c["distance"], status_of(c)]
        lines.append("| " + " | ".join(_fmt(x) for x in cells) + " |")
    return lines


def _ce_changes(snap: Snapshot, prev: Snapshot) -> list[str]:
    old_ce = {c["name"]: c["ce"] for c in prev["components"]}
    return [
        f"- Ce of {c['name']}: {old_ce[c['name']]} → {c['ce']}."
        for c in snap["components"]
        if old_ce.get(c["name"], c["ce"]) != c["ce"]
    ]


def changes(snap: Snapshot, prev: Snapshot | None) -> list[str]:
    if prev is None:
        return ["- First snapshot (baseline)."]
    old = {v["detail"] for v in prev["violations"]}
    new = [f"- New violation: {v['detail']}" for v in snap["violations"] if v["detail"] not in old]
    head = [
        f"- Compared with {prev['date']} ({prev['commit'][:7]}).",
        f"- CC max: {prev['functions']['ccMax']} → {snap['functions']['ccMax']}.",
    ]
    return head + _ce_changes(snap, prev) + (new or ["- No new violations."])


def render_latest(level: Level, snap: Snapshot, prev: Snapshot | None) -> str:
    title = (
        "Latest modularity metrics"
        if level.name == "system"
        else (f"{level.name} · Latest modularity metrics")
    )
    funcs = snap["functions"]
    lines = [
        f"# {title}",
        "",
        "_Generated by `/arch-metrics` (`tools/quality/arch_metrics.py`). Do not edit._",
        "",
        f"- **Result:** `{snap['result']}`",
        f"- **Date:** {snap['date']} · **Commit:** `{snap['commit'][:7]}`"
        f" · **Languages:** {', '.join(snap['languages'])}",
        f"- **Functions:** {funcs['count']} · CC avg {funcs['ccAvg']} · CC max {funcs['ccMax']}",
        "",
        "## Components",
        "",
        *component_table(snap),
        "",
        "## Functions over CC 10",
        "",
        *(
            [f"- `{w['file']}::{w['function']}`: CC {w['cc']}" for w in funcs["overWarn"]]
            or ["None."]
        ),
        "",
        "## Violations",
        "",
        *([f"- **{v['kind']}**: {v['detail']}" for v in snap["violations"]] or ["None."]),
        "",
        "## Change since the previous snapshot",
        "",
        *changes(snap, prev),
        "",
    ]
    return "\n".join(lines)


def _node_id(name: str) -> str:
    return re.sub(r"\W", "_", name)


def render_coupling(snap: Snapshot) -> str:
    bad = {
        tuple(v["detail"].split(":")[0].split(" -> ")[:2])
        for v in snap["violations"]
        if v["kind"] == "boundary"
    }
    cyc = {(c[i], c[i + 1]) for c in snap["cycles"] for i in range(len(c) - 1)}
    lines = ["```mermaid", "flowchart TD"]
    for c in snap["components"]:
        label = f"{c['name']}<br/>{c['ca']}·{c['ce']}·{c['instability']}"
        lines.append(f'  {_node_id(c["name"])}["{label}"]')
    red: list[int] = []
    for i, d in enumerate(snap["dependencies"]):
        lines.append(f"  {_node_id(d['from'])} -->|{d['count']}| {_node_id(d['to'])}")
        if (d["from"], d["to"]) in bad | cyc:
            red.append(i)
    if red:
        lines.append(f"  linkStyle {','.join(map(str, red))} stroke:#d00,stroke-width:2px")
    lines.append("```")
    legend = "_Nodes: name, Ca·Ce·I. Edges: number of import statements. Red: violation._"
    if not snap["dependencies"]:
        legend = "_No dependencies between components measured yet._ " + legend
    return "\n".join([legend, "", *lines])


def write_coupling(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    start, end = text.index(BEGIN) + len(BEGIN), text.index(END)
    path.write_text(text[:start] + "\n" + block + "\n" + text[end:], encoding="utf-8")


def drift(level: Level, snap: Snapshot) -> list[str]:
    """Declared edges that no import uses (undeclared ones are boundary violations)."""
    data = json.loads(level.components.read_text(encoding="utf-8"))
    measured = {(d["from"], d["to"]) for d in snap["dependencies"]}
    return [
        f"declared, not used yet: {c['name']} -> {dep}"
        for c in data["components"]
        for dep in c.get("mayDependOn", [])
        if (c["name"], dep) not in measured
    ]


def measure(level: Level, languages: list[dict[str, Any]]) -> Snapshot:
    snap = finish(merge([run_language(lang["metrics"], level.components) for lang in languages]))
    history = level.metrics_dir / "history"
    history.mkdir(parents=True, exist_ok=True)
    prev = previous(history, snap["date"])
    (history / f"{snap['date']}.json").write_text(json.dumps(snap, indent=2) + "\n", "utf-8")
    (level.metrics_dir / "latest.md").write_text(render_latest(level, snap, prev), "utf-8")
    write_coupling(level.architecture, render_coupling(snap))
    return snap


def main() -> int:
    scope = sys.argv[1] if len(sys.argv) > 1 else "all"
    languages = json.loads(REGISTRY.read_text(encoding="utf-8"))["languages"]
    if not languages:
        print("No language is registered: nothing to measure.")
        return 0
    worst = 0
    for level in levels(scope):
        snap = measure(level, languages)
        print(f"{level.name}: {snap['result']} ({len(snap['violations'])} violations)")
        for line in drift(level, snap):
            print(f"  {line}")
        worst = max(worst, ["pass", "warn", "fail"].index(snap["result"]))
    return 1 if worst == 2 else 0  # noqa: PLR2004


if __name__ == "__main__":
    sys.exit(main())
