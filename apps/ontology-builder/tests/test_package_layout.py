"""The package layout matches the app's components.json (plan 0002, rule 5)."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
COMPONENTS = APP / "docs" / "architecture" / "components.json"


def _python_components() -> list[str]:
    data = json.loads(COMPONENTS.read_text(encoding="utf-8"))
    return [
        c["name"]
        for c in data["components"]
        if any("/src/ontology_builder/" in p for p in c["paths"])
    ]


def test_every_python_component_is_an_importable_package() -> None:
    names = _python_components()
    assert names, "components.json lists no Python components"
    for name in names:
        module = importlib.import_module(f"ontology_builder.{name}")
        assert module.__doc__, (
            f"ontology_builder.{name} needs a docstring naming its responsibility"
        )
