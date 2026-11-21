"""store component.

Reads and writes the files of one ontology dataset, atomically.

``DatasetStore`` is one dataset ``data/ontology-<name>/``: ``read()`` gives a read-only view and
``transaction()`` a writable staging copy that is swapped in as a whole (plan 0002, Approach 6).
Every record is validated before it is written, and every file is deterministic (FR-36).
"""

from __future__ import annotations

from ontology_builder.store.dataset import DatasetExistsError, DatasetStore
from ontology_builder.store.files import (
    LAYOUT_FOLDERS,
    RELEASE_VARIANTS,
    DatasetFiles,
    ReadOnlyError,
)
from ontology_builder.store.yaml_io import dump_json_line, dump_yaml, load_yaml

__all__ = [
    "LAYOUT_FOLDERS",
    "RELEASE_VARIANTS",
    "DatasetExistsError",
    "DatasetFiles",
    "DatasetStore",
    "ReadOnlyError",
    "dump_json_line",
    "dump_yaml",
    "load_yaml",
]
