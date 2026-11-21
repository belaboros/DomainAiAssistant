"""Where the use cases work: the shared data folder, the work folder and the LLM client.

``workspace_from_env`` reads the layered environment (ADR-0012): ``SHARED_DATA_DIR``,
``ONTOLOGY_BUILDER_WORK_DIR`` and, only when an LLM client is asked for, the llm settings, so
review, authoring and releases work without an API key.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

from ontology_builder.llm import LlmClient, make_client, settings_from_env
from ontology_builder.store import DatasetStore
from ontology_builder.workflows.errors import WorkflowRefusedError

FIXTURES_DIR = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"
"""Recorded LLM responses, used by the ``replay`` and ``record`` modes."""

DEFAULT_WORK_DIR = "apps/ontology-builder/.work"


@dataclass(frozen=True)
class Workspace:
    """``data_dir`` holds the datasets (``SHARED_DATA_DIR``); ``work_dir`` is git-ignored."""

    data_dir: Path
    work_dir: Path
    llm: Callable[[], LlmClient]
    """Makes a new LLM client; called only when a use case needs one."""
    sources_root: Path | None = None
    """Where corpus folders are found; defaults to ``data_dir``."""
    open_store: Callable[[Path, str], DatasetStore] | None = None
    """Opens the dataset of an ontology; defaults to ``DatasetStore`` (tests inject a clock)."""

    def store(self, name: str) -> DatasetStore:
        return (self.open_store or DatasetStore)(self.data_dir, name)

    def sources(self) -> Path:
        return self.sources_root or self.data_dir

    def ontologies(self) -> list[str]:
        """The names of the ontologies in ``data_dir`` (folders ``ontology-<name>/``)."""
        return sorted(
            path.name.removeprefix("ontology-")
            for path in self.data_dir.glob("ontology-*")
            if path.is_dir() and self.store(path.name.removeprefix("ontology-")).exists()
        )

    def ontology_dir(self, name: str) -> Path:
        """The ontology's part of the work folder (lock, journal, runs)."""
        return self.work_dir / f"ontology-{name}"


def _path(value: str, root: Path) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else root / path


def workspace_from_env(env: Mapping[str, str], root: Path) -> Workspace:
    """The workspace of the environment; relative paths are relative to ``root`` (the repo)."""
    data = env.get("SHARED_DATA_DIR", "").strip()
    if not data:
        raise WorkflowRefusedError("SHARED_DATA_DIR is not set; set it in the root .env")
    work = env.get("ONTOLOGY_BUILDER_WORK_DIR", "").strip() or DEFAULT_WORK_DIR
    settings = dict(env)

    def llm() -> LlmClient:
        found = settings_from_env(settings)
        return make_client(found.mode, found.model, FIXTURES_DIR, found.api_key)

    return Workspace(data_dir=_path(data, root), work_dir=_path(work, root), llm=llm)
