"""Serve a small fixture ontology in a new temporary git repository, for the Playwright tests (T27).

Run by ``web/playwright.config.ts`` as its web server, from the repository root:
``uv run --package ontology-builder python apps/ontology-builder/tools/e2e_server.py <dir>
--port <port>``.

``<dir>`` is emptied, then gets ``repo/`` (a git working copy with the dataset, an unrelated
uncommitted change, and a pre-commit hook that fails while the git config ``e2e.hookfails`` is
``true``) and ``remote.git`` (a bare remote that ``main`` was pushed to once at setup; the app
never pushes).
The dataset has three proposed concepts, a statement, and an approved rule that refers to the
proposed concept "lead", so a governed build is blocked by FR-35 until "lead" is approved.
No LLM is needed: review, save and publish never call it.
"""

from __future__ import annotations

import argparse
import shutil
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any

from ontology_builder.api import serve
from ontology_builder.model import ScopeRecord, validate_element, validate_record
from ontology_builder.sources import CorpusSource, read_corpus
from ontology_builder.store import DatasetStore
from ontology_builder.workflows import Workspace, open_ontology

NAME = "e2e-house-rules"
RUN = "run_01JDK7F3Q8ZX5N6M2W4R9T0E2E"
AT = "2026-11-22T10:00:00Z"

SCOPE: dict[str, Any] = {
    "name": NAME,
    "purpose": "Fixture ontology of the end-to-end tests: dogs in a residential building.",
    "readers": "The Playwright tests.",
    "level_guidance": {
        "level_1": "What every dog owner in the building must know.",
        "level_2": "Everyday care.",
        "level_3": "Special cases.",
    },
    "ignorable_examples": ["Stories about one dog"],
    "base_iri": f"urn:domain-ai-assistant:ontology:{NAME}:",
}

RULES_MD = """# House rules for dogs

A dog is a pet that lives with its owner in the building.

In the stairwell, keep the dog on a lead.

The stairwell connects the floors of the building.
"""

FAILING_HOOK = """#!/bin/sh
if [ "$(git config --get e2e.hookfails)" = "true" ]; then
  echo "detect-secrets: a secret was found in the dataset"
  exit 1
fi
"""


def git(repo: Path, *args: str) -> None:
    found = shutil.which("git")
    if found is None:
        raise SystemExit("git is not available")
    subprocess.run([found, "-C", str(repo), *args], check=True, capture_output=True)  # noqa: S603


def _common(label: str, unit: str, status: str = "proposed") -> dict[str, Any]:
    return {
        "label": label,
        "level": "level-2",
        "level_reason": "Fixture element of the end-to-end tests.",
        "status": status,
        "evidence": [{"unit": unit}],
        "origin": {"kind": "llm", "run_id": RUN, "created_at": AT},
    }


def _elements(store: DatasetStore, units: list[str]) -> list[tuple[str, dict[str, Any]]]:
    dog_unit, lead_unit, stair_unit = units
    new = store.minter.new
    lead = new("concept")
    rule: dict[str, Any] = _common("keep the dog on a lead", lead_unit, "approved") | {
        "id": new("rule"),
        "modality": "must",
        "actor": "dog owner",
        "action": "keep the dog on a lead",
        "condition": "in the stairwell",
        "refers_to": [lead],
    }
    rule["approved_snapshot"] = dict(rule)
    return [
        ("concept", _common("dog", dog_unit) | {"id": new("concept"), "parents": []}),
        ("concept", _common("lead", lead_unit) | {"id": lead, "parents": []}),
        ("concept", _common("stairwell", stair_unit) | {"id": new("concept"), "parents": []}),
        (
            "statement",
            _common("dog on a lead", lead_unit)
            | {"id": new("statement"), "text": "In the stairwell, keep the dog on a lead."},
        ),
        ("rule", rule),
    ]


def _write(store: DatasetStore, corpus: CorpusSource) -> None:
    with store.transaction() as files:
        files.write_corpus(corpus.folder, corpus.corpus)
        for item in corpus.documents:
            files.write_document(corpus.folder, item.document)
            files.write_units(corpus.folder, item.document.id, item.units)
        units = [unit.id for unit in corpus.units]
        for element_type, record in _elements(store, units):
            files.write_element(validate_element(element_type, record))


def seed_dataset(repo: Path) -> DatasetStore:
    """The fixture dataset in ``repo/data/``, from the Markdown file ``data/manuals/rules.md``."""
    manuals = repo / "data" / "manuals"
    manuals.mkdir(parents=True)
    (manuals / "rules.md").write_text(RULES_MD, encoding="utf-8")
    store = DatasetStore(repo / "data", NAME)
    store.create(validate_record(ScopeRecord, SCOPE))
    corpus = read_corpus(manuals, source_path="manuals", number=0, run_id=RUN, minter=store.minter)
    _write(store, corpus)
    return store


def init_repo(root: Path) -> Path:
    """``root/repo`` with a switchable failing hook, pushed once to ``root/remote.git``."""
    repo, remote = root / "repo", root / "remote.git"
    repo.mkdir()
    git(root, "init", "-q", "--bare", str(remote))
    git(repo, "init", "-q", "-b", "main")
    for key, value in (
        ("user.name", "e2e"),
        ("user.email", "e2e@example.invalid"),
        ("commit.gpgsign", "false"),
        ("core.hooksPath", ".git/hooks"),
    ):
        git(repo, "config", key, value)
    hook = repo / ".git" / "hooks" / "pre-commit"
    hook.write_text(FAILING_HOOK, encoding="utf-8")
    hook.chmod(0o755)
    return repo


def commit_start(repo: Path) -> None:
    """Commit everything, push ``main`` once, then leave an unrelated change uncommitted."""
    (repo / ".gitignore").write_text("/work/\n", encoding="utf-8")
    (repo / "notes.md").write_text("Unrelated notes.\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "start")
    git(repo, "remote", "add", "origin", str(repo.parent / "remote.git"))
    git(repo, "push", "-q", "origin", "main")
    (repo / "notes.md").write_text("Unrelated notes, changed and not saved.\n", encoding="utf-8")


def _no_llm() -> Any:
    raise SystemExit("the end-to-end fixture has no LLM")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("dir", type=Path)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    root: Path = args.dir.resolve()
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    repo = init_repo(root)
    store = seed_dataset(repo)
    commit_start(repo)
    workspace = Workspace(data_dir=repo / "data", work_dir=repo / "work", llm=_no_llm)
    # uvicorn re-raises SIGTERM after its shutdown; exiting normally lets ``finally`` run.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    try:
        with open_ontology(workspace, store.name) as session:
            print(f"serving {NAME} from {repo} on http://127.0.0.1:{args.port}", flush=True)
            serve(session, args.port)
    finally:
        shutil.rmtree(root, ignore_errors=True)  # Playwright stops the server after the tests


if __name__ == "__main__":
    main()
