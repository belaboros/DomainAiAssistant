"""The journal of the pending change set in the work folder, so a crash loses nothing.

It is rewritten after every action and removed by a successful save. It records the tree hash
of the dataset it was made on: a journal of a dataset that changed since is not applied.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from ontology_builder.governance import ChangeSet


class Journal:
    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> dict[str, Any] | None:
        if not self.path.is_file():
            return None
        data: dict[str, Any] = json.loads(self.path.read_text(encoding="utf-8"))
        return data

    def write(self, tree_hash: str, changes: ChangeSet) -> None:
        if not changes.pending and not changes.decisions:
            self.clear()
            return
        data = {"tree_hash": tree_hash, "changes": changes.journal()}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fresh = self.path.with_name(f".{self.path.name}.new")
        fresh.write_text(json.dumps(data, sort_keys=True, ensure_ascii=False), encoding="utf-8")
        os.replace(fresh, self.path)

    def clear(self) -> None:
        self.path.unlink(missing_ok=True)
