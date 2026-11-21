"""cli component.

Exposes the use cases as ontology-builder commands.

``ontology-builder create | ingest | build | serve | eval`` (plan 0002, CLI). The environment is the
layered one of ``tools/env/with-env.sh ontology-builder`` (ADR-0012). Publishing is GUI-only: it
needs a signed-in domain admin.
"""

from __future__ import annotations

from ontology_builder.cli.commands import main, make_app

__all__ = ["main", "make_app"]
