"""Cyclomatic complexity of every first-party Python function (ADR-0020, thresholds ADR-0005).

Ruff fails above 15 (C901). This report adds the warn band: it lists functions with CC 11-15,
which need a one-line justification in review, and never fails on them.

Usage: uv run python tools/quality/python/cc_report.py [paths...]
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from radon.complexity import cc_visit

ROOT = Path(__file__).resolve().parents[3]
WARN = 10
FAIL = 15
SKIP_PARTS = {".venv", "node_modules", ".work"}


@dataclass(frozen=True)
class FunctionCC:
    """Complexity of one function or method."""

    file: str
    function: str
    cc: int


def python_files(paths: list[Path]) -> list[Path]:
    """The first-party .py files under the given paths."""
    files: list[Path] = []
    for base in paths:
        candidates = [base] if base.is_file() else sorted(base.rglob("*.py"))
        files.extend(f for f in candidates if not SKIP_PARTS & set(f.parts))
    return files


def measure(files: list[Path]) -> list[FunctionCC]:
    """CC of every function and method in the files."""
    result: list[FunctionCC] = []
    for path in files:
        for block in cc_visit(path.read_text(encoding="utf-8")):
            if block.letter == "C":  # a class: its methods are reported on their own
                continue
            rel = path.resolve().relative_to(ROOT).as_posix()
            result.append(FunctionCC(rel, block.fullname, block.complexity))
    return result


def default_paths() -> list[Path]:
    """Every src/ folder in apps/ and libs/, and tools/."""
    return [*sorted(ROOT.glob("apps/*/src")), *sorted(ROOT.glob("libs/*/src")), ROOT / "tools"]


def main() -> int:
    paths = [Path(a) for a in sys.argv[1:]] or default_paths()
    functions = measure(python_files(paths))
    over = sorted((f for f in functions if f.cc > WARN), key=lambda f: -f.cc)
    for f in over:
        band = "FAIL" if f.cc > FAIL else "warn"
        print(f"{band} CC {f.cc:>2} {f.file}::{f.function}")
    print(f"{len(functions)} functions, {len(over)} over CC {WARN}")
    return 1 if any(f.cc > FAIL for f in over) else 0


if __name__ == "__main__":
    sys.exit(main())
