"""One process per dataset: a lock file in the work folder (plan 0002, HTTP API guards).

The lock file holds the process ID of its holder. A lock left behind by a process that is no
longer running is taken over, so a crash never blocks the ontology for good.
"""

from __future__ import annotations

import os
from pathlib import Path

from ontology_builder.workflows.errors import WorkflowRefusedError


def _alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except (ProcessLookupError, OverflowError):
        return False
    except PermissionError:
        return True  # running, but owned by someone else
    return True


class ProcessLock:
    """An exclusive lock on one ontology, held by this process until ``release``."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._held = False

    def _holder(self) -> int | None:
        try:
            return int(self.path.read_text(encoding="utf-8").strip())
        except (FileNotFoundError, ValueError):
            return None

    def acquire(self) -> None:
        """Take the lock, or refuse while another live process (or this one) holds it."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _attempt in range(2):
            try:
                handle = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                holder = self._holder()
                if holder is not None and _alive(holder):
                    raise WorkflowRefusedError(
                        f"the ontology is already open in process {holder}; "
                        "close that server first (one server per dataset)"
                    ) from None
                self.path.unlink(missing_ok=True)  # left behind by a process that ended
                continue
            with os.fdopen(handle, "w", encoding="utf-8") as file:
                file.write(f"{os.getpid()}\n")
            self._held = True
            return
        raise WorkflowRefusedError(f"could not take the lock {self.path}")

    def release(self) -> None:
        if self._held and self._holder() == os.getpid():
            self.path.unlink(missing_ok=True)
        self._held = False
