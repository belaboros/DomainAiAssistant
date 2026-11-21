"""Generate the Pydantic models of ontology_builder.model from its LinkML schema (plan 0002, T3).

Run: uv run python apps/ontology-builder/tools/gen_model.py [--check]
The output is formatted with ruff, so it passes the quality gate unchanged. --check exits 1
when the committed file differs from a fresh generation.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
MODEL = APP / "src" / "ontology_builder" / "model"
SCHEMA = MODEL / "schema" / "ontology_builder.yaml"
TARGET = MODEL / "_generated.py"
TEMPLATES = APP / "tools" / "linkml-templates"


def generate() -> str:
    """Return the formatted Pydantic module for the current schema."""
    raw = subprocess.run(  # noqa: S603
        [
            str(Path(sys.executable).parent / "gen-pydantic"),
            "--meta",
            "None",
            "--extra-fields",
            "forbid",
            "--template-dir",
            str(TEMPLATES),
            str(SCHEMA),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "_generated.py"
        path.write_text(raw, encoding="utf-8")
        ruff = [sys.executable, "-m", "ruff"]
        config = ["--config", str(APP.parents[1] / "pyproject.toml")]
        fmt = [*ruff, "format", "-q", *config, str(path)]
        fix = [*ruff, "check", "--fix", "--unsafe-fixes", "-q", *config, str(path)]
        for command in (fmt, fix, fmt):
            subprocess.run(command, check=True)  # noqa: S603 - the repo's own ruff, fixed arguments
        return path.read_text(encoding="utf-8")


def main(argv: list[str]) -> int:
    fresh = generate()
    if "--check" in argv:
        if TARGET.read_text(encoding="utf-8") != fresh:
            print(f"{TARGET} is out of date; run {Path(__file__).name}", file=sys.stderr)
            return 1
        return 0
    TARGET.write_text(fresh, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
