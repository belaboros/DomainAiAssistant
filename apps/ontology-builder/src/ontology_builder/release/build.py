"""Assembling one release folder: files, manifest and checksums (FR-28, FR-31, FR-36).

The raw release holds every element except excluded, rejected and ignorable ones, each in its
current version and with its status. ``built_at`` is the only value that changes between two
builds of the same records.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime

from ontology_builder.model import ELEMENT_TYPES, Element, ScopeRecord, SourceUnit
from ontology_builder.release.labels import LEVELS
from ontology_builder.release.markdown import build_level_files
from ontology_builder.release.rdf import ReleaseInput, build_jsonld, build_turtle
from ontology_builder.store import DatasetFiles

RAW_STATUSES = ("approved", "deprecated", "included", "proposed")
GOVERNED_STATUSES = ("approved", "deprecated")
_TYPE_OF_CLASS = {record_class: name for name, record_class in ELEMENT_TYPES.items()}


@dataclass(frozen=True)
class BuildInfo:
    """Where a build comes from: the git commit of the records, and when it was made."""

    source_commit: str
    built_at: datetime


@dataclass(frozen=True)
class Release:
    """The files of one release folder, by name, as text."""

    variant: str
    version: str
    elements: tuple[Element, ...]
    files: dict[str, str]


def load_units(files: DatasetFiles) -> dict[str, SourceUnit]:
    """Every source unit of the dataset (corpus units and user statements), by ID."""
    units = {unit.id: unit for unit in files.user_statements()}
    for folder in files.corpora():
        for document in files.documents(folder):
            units.update((unit.id, unit) for unit in files.units(folder, document.id))
    return units


def raw_elements(elements: Iterable[Element]) -> list[Element]:
    """The elements of the raw release (FR-28)."""
    return [
        element
        for element in elements
        if element.status not in {"excluded", "rejected"} and element.level != "ignorable"
    ]


def _count(values: Iterable[str], keys: Iterable[str]) -> dict[str, int]:
    found = dict.fromkeys(keys, 0)
    for value in values:
        found[value] = found.get(value, 0) + 1
    return found


def _counts(elements: list[Element], statuses: tuple[str, ...]) -> dict[str, dict[str, int]]:
    return {
        "by_type": _count((_TYPE_OF_CLASS[type(e)] for e in elements), sorted(ELEMENT_TYPES)),
        "by_status": _count((str(e.status) for e in elements), statuses),
        "by_level": _count((str(e.level) for e in elements), LEVELS),
    }


def _timestamp(moment: datetime) -> str:
    return moment.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _manifest(release: Release, name: str, info: BuildInfo) -> str:
    statuses = RAW_STATUSES if release.variant == "raw" else GOVERNED_STATUSES
    data = {
        "ontology": name,
        "variant": release.variant,
        "version": release.version,
        "built_at": _timestamp(info.built_at),
        "source_commit": info.source_commit,
        "counts": _counts(list(release.elements), statuses),
        "files": {
            file_name: "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
            for file_name, text in sorted(release.files.items())
        },
    }
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def assemble(
    release_input: ReleaseInput, info: BuildInfo, extra: Mapping[str, str] | None = None
) -> Release:
    """``ontology.ttl`` and its JSON-LD twin, ``level-N.md``, any ``extra`` files, and the
    manifest of all of them."""
    content = {
        "ontology.ttl": build_turtle(release_input),
        "ontology.jsonld": build_jsonld(release_input),
        **build_level_files(release_input),
    }
    content.update(extra or {})
    release = Release(
        release_input.variant, release_input.version, tuple(release_input.elements), content
    )
    content["manifest.json"] = _manifest(release, release_input.scope.name, info)
    return release


def _scope(files: DatasetFiles) -> ScopeRecord:
    scope = files.scope()
    if scope is None:
        raise ValueError("the ontology has no scope record; create it first")
    return scope


def release_input(
    files: DatasetFiles, elements: list[Element], variant: str, version: str
) -> ReleaseInput:
    """What a release of ``elements`` is built from, with the dataset's scope and units."""
    ordered = sorted(elements, key=lambda element: element.id)
    return ReleaseInput(_scope(files), ordered, load_units(files), variant, version)


def build_raw(files: DatasetFiles, info: BuildInfo) -> Release:
    """The raw release of the records in ``files`` (not written)."""
    elements = raw_elements(files.elements().values())
    version = f"raw+{info.source_commit[:7]}"
    return assemble(release_input(files, elements, "raw", version), info)


def write_release(files: DatasetFiles, release: Release) -> None:
    """Replace the release folder with ``release`` in one folder swap."""
    files.replace_release(release.variant, release.files)


def save_raw(files: DatasetFiles, info: BuildInfo) -> Release:
    """Build the raw release and write it (every save, FR-28)."""
    release = build_raw(files, info)
    write_release(files, release)
    return release
