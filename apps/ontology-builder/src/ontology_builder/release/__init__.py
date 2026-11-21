"""release component.

Builds the raw and governed release files from the records.

``build_turtle`` maps the elements of one release to ``ontology.ttl`` (OWL 2 + SKOS + SHACL and
the ``dai:`` vocabulary of the shared contract ``libs/contracts/ontology/``);
``build_level_files`` writes ``level-1.md`` to ``level-3.md`` (Jinja2 templates with Mermaid).
``save_raw`` rebuilds the raw release on every save; ``publish`` also builds the governed one,
unless the FR-35 check finds offenders. Both write through a ``DatasetFiles`` of a transaction.
"""

from __future__ import annotations

from ontology_builder.release.build import (
    BuildInfo,
    Release,
    build_raw,
    load_units,
    raw_elements,
    save_raw,
    write_release,
)
from ontology_builder.release.changelog import Changes, diff
from ontology_builder.release.governed import (
    FIRST_VERSION,
    GovernedBuild,
    GovernedBuildError,
    PublishResult,
    Reference,
    ReleaseVersionError,
    build_governed,
    governed_version,
    publish,
    references,
    resolve_version,
)
from ontology_builder.release.labels import LEVELS, level_elements, term_labels
from ontology_builder.release.markdown import BADGES, build_level_files, render_level
from ontology_builder.release.mermaid import MAX_NODES, mermaid_label
from ontology_builder.release.rdf import (
    DAI,
    VARIANTS,
    ReleaseInput,
    build_graph,
    build_turtle,
    ontology_iri,
)

__all__ = [
    "BADGES",
    "DAI",
    "FIRST_VERSION",
    "LEVELS",
    "MAX_NODES",
    "VARIANTS",
    "BuildInfo",
    "Changes",
    "GovernedBuild",
    "GovernedBuildError",
    "PublishResult",
    "Reference",
    "Release",
    "ReleaseInput",
    "ReleaseVersionError",
    "build_governed",
    "build_graph",
    "build_level_files",
    "build_raw",
    "build_turtle",
    "diff",
    "governed_version",
    "level_elements",
    "load_units",
    "mermaid_label",
    "ontology_iri",
    "publish",
    "raw_elements",
    "references",
    "render_level",
    "resolve_version",
    "save_raw",
    "term_labels",
    "write_release",
]
