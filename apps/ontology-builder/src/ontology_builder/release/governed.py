"""The governed release and publishing (FR-24, FR-29, FR-35; plan 0002, Approach 8).

The governed release holds approved and deprecated elements only, each in its approved version:
the approved snapshot when the element has one, so an edit after approval does not reach the
governed release until it is approved again. A publish fails, listing the offenders, when an
element of it refers to an element that is not in it; the raw release is built regardless.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from typing import Any

from rdflib import Graph

from ontology_builder.model import Concept, Element, Mention, Property, Relation, Rule, Term
from ontology_builder.release.build import (
    BuildInfo,
    Release,
    assemble,
    release_input,
    save_raw,
    write_release,
)
from ontology_builder.release.changelog import changelog, diff
from ontology_builder.release.rdf import build_graph
from ontology_builder.store import DatasetFiles

_SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
FIRST_VERSION = "1.0.0"


class ReleaseVersionError(ValueError):
    """The version asked for is not a semantic version newer than the published one."""


@dataclass(frozen=True)
class Reference:
    """``element_id`` refers to ``target_id``, which has ``target_status`` (FR-35)."""

    element_id: str
    element_label: str
    target_id: str
    target_label: str
    target_status: str


class GovernedBuildError(RuntimeError):
    """An element of the governed release refers to an element that is not approved."""

    def __init__(self, offenders: list[Reference]) -> None:
        self.offenders = offenders
        listed = "; ".join(
            f"{o.element_id} ({o.element_label}) refers to {o.target_id} ({o.target_label}), "
            f"which is {o.target_status}"
            for o in offenders
        )
        super().__init__(f"the governed release cannot be built: {listed}")


@dataclass(frozen=True)
class GovernedBuild:
    release: Release
    warnings: list[Reference]


@dataclass(frozen=True)
class PublishResult:
    """The raw release (always built) and the governed one, or the offenders that blocked it."""

    raw: Release
    governed: Release | None
    offenders: list[Reference] = field(default_factory=list)
    warnings: list[Reference] = field(default_factory=list)


def governed_version(element: Element) -> Element | None:
    """The version of ``element`` that belongs in the governed release, if any (FR-24)."""
    snapshot = getattr(element, "approved_snapshot", None)
    if element.status in {"excluded", "rejected"}:
        return None
    if element.status == "deprecated":
        base = snapshot if isinstance(snapshot, Element) else element
        update: dict[str, Any] = {"status": "deprecated", "replaced_by": element.replaced_by}
        version = base.model_copy(update=update)
    elif isinstance(snapshot, Element):
        version = snapshot.model_copy(update={"status": "approved"})
    elif element.status == "approved":
        version = element
    else:
        return None
    return version if version.level != "ignorable" else None


def _listed(values: list[str] | None) -> list[str]:
    return values if values is not None else []


def references(element: Element) -> Iterator[str]:
    """Every element ID that ``element`` refers to."""
    match element:
        case Concept():
            yield from _listed(element.parents)
        case Term():
            yield from (mention.concept for mention in _listed_mentions(element))
        case Relation():
            yield from (element.subject, element.object)
        case Rule():
            yield from _listed(element.refers_to)
            yield from [element.cardinality.relation] if element.cardinality else []
        case Property():
            yield element.of


def _listed_mentions(term: Term) -> list[Mention]:
    return term.mentions if term.mentions is not None else []


def _by_ids(reference: Reference) -> tuple[str, str]:
    return reference.element_id, reference.target_id


def check_references(
    governed: Mapping[str, Element], current: Mapping[str, Element]
) -> tuple[list[Reference], list[Reference]]:
    """Offenders (a reference to an element not in the release) and warnings (to a deprecated
    one). Deprecated elements are not checked: they are kept for readers, not used."""
    offenders, warnings = [], []
    for element in governed.values():
        if element.status == "deprecated":
            continue
        for target_id in sorted(set(references(element))):
            target = governed.get(target_id) or current.get(target_id)
            status = str(target.status) if target is not None else "missing"
            label = target.label if target is not None else ""
            found = Reference(element.id, element.label, target_id, label, status)
            if target_id not in governed:
                offenders.append(found)
            elif status == "deprecated":
                warnings.append(found)
    return sorted(offenders, key=_by_ids), sorted(warnings, key=_by_ids)


def _parse(version: str) -> tuple[int, int, int]:
    match = _SEMVER.match(version)
    if match is None:
        raise ReleaseVersionError(f"{version!r} is not a semantic version like 1.2.0")
    major, minor, patch = (int(part) for part in match.groups())
    return major, minor, patch


def resolve_version(previous: str | None, asked: str | None) -> str:
    """The version to publish: ``asked``, or the next minor after ``previous`` (FR-29)."""
    if asked is None:
        if previous is None:
            return FIRST_VERSION
        major, minor, _ = _parse(previous)
        return f"{major}.{minor + 1}.0"
    if previous is not None and _parse(asked) <= _parse(previous):
        raise ReleaseVersionError(f"version {asked} is not newer than the published {previous}")
    _parse(asked)
    return asked


@dataclass(frozen=True)
class _Previous:
    version: str | None
    graph: Graph | None
    changelog: str


def _previous(files: DatasetFiles) -> _Previous:
    found = files.release_files("governed")
    if "manifest.json" not in found:
        return _Previous(None, None, "")
    version = str(json.loads(found["manifest.json"])["version"])
    graph = Graph().parse(data=found["ontology.ttl"].decode("utf-8"), format="turtle")
    return _Previous(version, graph, found.get("CHANGELOG.md", b"").decode("utf-8"))


def build_governed(
    files: DatasetFiles, info: BuildInfo, version: str | None = None
) -> GovernedBuild:
    """The governed release of the records in ``files`` (not written), or raise
    ``GovernedBuildError`` listing the offenders, or ``ReleaseVersionError``."""
    current = files.elements()
    governed = {
        element_id: version_of
        for element_id, element in current.items()
        if (version_of := governed_version(element)) is not None
    }
    offenders, warnings = check_references(governed, current)
    if offenders:
        raise GovernedBuildError(offenders)
    previous = _previous(files)
    number = resolve_version(previous.version, version)
    source = release_input(files, list(governed.values()), "governed", number)
    changes = diff(previous.graph, build_graph(source), source.scope.base_iri)
    log = changelog(source.scope.name, number, previous.version, changes, previous.changelog)
    return GovernedBuild(assemble(source, info, {"CHANGELOG.md": log}), warnings)


def publish(files: DatasetFiles, info: BuildInfo, version: str | None = None) -> PublishResult:
    """Rebuild the raw release, then build and write the governed one if nothing blocks it.

    A version that is not newer than the published one raises before anything is written; an
    offender leaves the governed folder as it was.
    """
    resolve_version(_previous(files).version, version)
    raw = save_raw(files, info)
    try:
        build = build_governed(files, info, version)
    except GovernedBuildError as error:
        return PublishResult(raw, None, error.offenders)
    write_release(files, build.release)
    return PublishResult(raw, build.release, [], build.warnings)
