"""One ontology dataset and its atomic swap (plan 0002, Approach 6; ontology-builder/ADR-0004).

Every change is made in a staging copy ``data/.ontology-<name>.staging/``. The swap renames the
live folder to ``.ontology-<name>.previous/`` and the staging copy to the live name. A step after
the swap (the git commit) can still fail; then the previous folder is swapped back.
"""

from __future__ import annotations

import hashlib
import shutil
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

from ontology_builder.model import Clock, Decision, ScopeRecord, SystemClock, UlidMinter
from ontology_builder.store.files import DatasetFiles
from ontology_builder.store.yaml_io import to_data


class DatasetExistsError(FileExistsError):
    """An ontology with this name already exists."""


class DatasetStore:
    """The dataset ``ontology-<name>`` under ``data_dir`` (the shared data folder)."""

    def __init__(
        self,
        data_dir: Path,
        name: str,
        *,
        clock: Clock | None = None,
        minter: UlidMinter | None = None,
    ) -> None:
        self.name = name
        self.root = data_dir / f"ontology-{name}"
        self.staging_dir = data_dir / f".ontology-{name}.staging"
        self.previous_dir = data_dir / f".ontology-{name}.previous"
        self.clock = clock or SystemClock()
        self.minter = minter or UlidMinter(self.clock)

    def exists(self) -> bool:
        return self.root.is_dir()

    def read(self) -> DatasetFiles:
        """A read-only view of the live dataset."""
        return DatasetFiles(self.root, writable=False)

    def create(self, scope: ScopeRecord, decisions: list[Decision] | None = None) -> None:
        """Make the layout of FR-30 with the scope record and any decisions, in one rename."""
        to_data(scope)  # validate before anything is written
        if self.exists() or self.previous_dir.exists():
            raise DatasetExistsError(f"ontology {self.name!r} already exists")
        self._refuse_stale_staging()
        files = DatasetFiles(self.staging_dir, writable=True)
        try:
            files.make_layout()
            files.write_scope(scope)
            files.append_decisions(decisions or [])
        except BaseException:
            shutil.rmtree(self.staging_dir, ignore_errors=True)
            raise
        self.staging_dir.rename(self.root)

    @contextmanager
    def transaction(self, after_swap: Callable[[], None] | None = None) -> Iterator[DatasetFiles]:
        """Yield a writable staging copy; swap it in on success, then run ``after_swap``.

        If the body raises, the staging copy is dropped. If ``after_swap`` raises, the previous
        folder is swapped back. Either way the live dataset is as it was, and the error is raised.
        """
        self._refuse_stale_staging()
        if not self.exists():
            raise FileNotFoundError(f"ontology {self.name!r} does not exist")
        shutil.copytree(self.root, self.staging_dir)
        try:
            yield DatasetFiles(self.staging_dir, writable=True)
        except BaseException:
            shutil.rmtree(self.staging_dir, ignore_errors=True)
            raise
        self.root.rename(self.previous_dir)
        self.staging_dir.rename(self.root)
        try:
            if after_swap is not None:
                after_swap()
        except BaseException:
            self._swap_back()
            raise
        shutil.rmtree(self.previous_dir)

    def recover(self) -> None:
        """Undo an interrupted transaction: restore the previous folder, drop the staging copy."""
        if self.previous_dir.exists():
            self._swap_back()
        if self.staging_dir.exists():
            shutil.rmtree(self.staging_dir)

    def tree_hash(self) -> str:
        """SHA-256 over every file path and its bytes; changes when anything in the dataset does."""
        digest = hashlib.sha256()
        for path in sorted(p for p in self.root.rglob("*") if p.is_file()):
            digest.update(path.relative_to(self.root).as_posix().encode("utf-8") + b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
        return "sha256:" + digest.hexdigest()

    def _swap_back(self) -> None:
        if self.root.exists():
            shutil.rmtree(self.root)
        self.previous_dir.rename(self.root)

    def _refuse_stale_staging(self) -> None:
        if self.staging_dir.exists() or self.previous_dir.exists():
            raise RuntimeError(
                f"an interrupted change of ontology {self.name!r} was found; run recover() first"
            )
