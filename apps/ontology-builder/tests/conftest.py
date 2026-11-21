"""Shared fixtures for the ontology-builder tests."""

from __future__ import annotations

import copy
import re
import shutil
import subprocess
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from ontology_builder.api import create_app
from ontology_builder.extraction import (
    DocumentExtraction,
    ExtractionContext,
    TermInput,
    TermResolution,
    extract_document,
    pass1_requests,
    resolve_terms,
    terms_request,
)
from ontology_builder.llm import (
    FixtureMissingError,
    FixtureStore,
    LlmClient,
    LlmRequest,
    LlmResponse,
    LlmUnavailableError,
    ReplayClient,
    heuristic_tokens,
)
from ontology_builder.model import (
    ID_PREFIXES,
    Element,
    FixedClock,
    IgnorableVerdict,
    ScopeRecord,
    SourceUnit,
    UlidMinter,
    validate_element,
    validate_record,
)
from ontology_builder.sources import CorpusSource, read_corpus
from ontology_builder.store import DatasetStore
from ontology_builder.workflows import OpenOntology, Workspace, open_ontology

ULID = "01JDK7F3Q8ZX5N6M2W4R9T0BCD"
ULID2 = "01JDK7F3Q8ZX5N6M2W4R9T0BCE"
UNIT = f"su_{ULID}"
CONCEPT = f"cn_{ULID}"
CONCEPT2 = f"cn_{ULID2}"
RELATION = f"rl_{ULID}"
AT = "2026-11-21T10:00:00Z"
HASH = "sha256:" + "a" * 64

_COMMON: dict[str, Any] = {
    "label": "leash",
    "level": "level-1",
    "level_reason": "Walking a dog on a leash is everyday knowledge.",
    "status": "proposed",
    "evidence": [{"unit": UNIT, "quote": "on a lead of at most 2 m"}],
    "origin": {"kind": "llm", "run_id": f"run_{ULID}", "created_at": AT},
}

_BY_TYPE: dict[str, dict[str, Any]] = {
    "statement": {"id": f"st_{ULID}", "text": "A dog is kept on a lead of at most 2 m."},
    "term": {"id": f"tm_{ULID}", "mentions": [{"unit": UNIT, "concept": CONCEPT}]},
    "concept": {"id": CONCEPT, "definition": "A rope or strap to lead a dog.", "parents": []},
    "relation": {
        "id": RELATION,
        "subject": CONCEPT,
        "object": CONCEPT2,
        "predicate_label": "keeps",
        "cardinality": {"max": 2},
    },
    "rule": {
        "id": f"ru_{ULID}",
        "modality": "must",
        "actor": "dog owner",
        "action": "keep the dog on a lead",
        "condition": "in the stairwell",
        "limit": {"comparator": "le", "value": 2.0, "unit": "m"},
        "refers_to": [CONCEPT],
    },
    "property": {"id": f"pr_{ULID}", "of": CONCEPT, "name": "length", "value": "2", "unit": "m"},
}

ElementFactory = Callable[[str], dict[str, Any]]


def _element_record(element_type: str) -> dict[str, Any]:
    return copy.deepcopy(_COMMON | _BY_TYPE[element_type])


@pytest.fixture
def make_element() -> ElementFactory:
    """Return a factory of valid element records by type, as they would be read from YAML."""
    return _element_record


class ReviewKit:
    """Helpers for the governance tests: a dataset with concepts in chosen statuses."""

    at = datetime(2026, 11, 21, 10, 0, tzinfo=UTC)

    def __init__(self, data_dir: Path, scope: dict[str, Any]) -> None:
        clock = FixedClock(self.at)
        self.store = DatasetStore(
            data_dir, "pets-and-house-rules", clock=clock, minter=UlidMinter(clock, bytes)
        )
        self.store.create(validate_record(ScopeRecord, scope))

    def element(
        self, element_type: str, status: str = "proposed", *, snapshot: bool = False, **fields: Any
    ) -> dict[str, Any]:
        """A record of the type with a fresh ID; ``snapshot`` adds an approved snapshot."""
        record = _element_record(element_type) | fields
        record |= {"id": self.store.minter.new(element_type), "status": status}
        if snapshot:
            record["approved_snapshot"] = record | {"status": "approved"}
        return record

    def concept(self, status: str = "proposed", *, snapshot: bool = False) -> dict[str, Any]:
        return self.element("concept", status, snapshot=snapshot)

    def unit(self) -> str:
        return self.store.minter.new("source_unit")

    def seed(self, records: list[dict[str, Any]]) -> list[str]:
        """Write the records into the live dataset and return their IDs."""
        types = {prefix: name for name, prefix in ID_PREFIXES.items()}
        with self.store.transaction() as files:
            for record in records:
                element_type = types[record["id"].split("_")[0]]
                files.write_element(validate_element(element_type, record))
        return [record["id"] for record in records]


@pytest.fixture
def review_kit(tmp_path: Path, scope_record: dict[str, Any]) -> ReviewKit:
    return ReviewKit(tmp_path, scope_record)


@pytest.fixture
def scope_record() -> dict[str, Any]:
    return {
        "name": "pets-and-house-rules",
        "purpose": "Help residents keep pets in line with the house rules.",
        "readers": "Residents, newcomers, the building manager.",
        "level_guidance": {
            "level_1": "What every pet owner in the building must know.",
            "level_2": "Everyday care and the common rules.",
            "level_3": "Special cases and error scenarios.",
        },
        "ignorable_examples": ["Anecdotes about one dog", "Quotes"],
        "base_iri": "urn:domain-ai-assistant:ontology:pets-and-house-rules:",
    }


@pytest.fixture
def corpus_unit() -> dict[str, Any]:
    return {
        "id": UNIT,
        "document_id": f"doc_{ULID}",
        "kind": "paragraph",
        "location": {"path": "rules/01.md", "heading_path": ["Pets"], "index_in_section": 0},
        "content_hash": HASH,
        "text": "Keep the dog on a lead of at most 2 m in the stairwell.",
    }


# ---------- the pet manuals as deterministic corpora, for the replayed LLM fixtures ----------
# The request hash of every recorded LLM call covers the prompt, which holds the unit IDs and the
# scope record. Both must therefore be identical on every run: the minter below has a fixed clock
# and fixed "random" bytes, and PET_SCOPE is frozen. Changing either invalidates the fixtures.

REPO = Path(__file__).resolve().parents[3]
PET_MANUALS = REPO / "data" / "user-manuals-pets-and-house-rules"
PET_CORPORA = ("dog-owners-manual", "cat-owners-manual", "building-and-house-rules")
LLM_FIXTURES = Path(__file__).parent / "fixtures" / "llm"
FIXTURE_MODEL = "claude-opus-5-5"
PET_RUN = "run_01JDK7F3Q8ZX5N6M2W4R9T0RNA"
PET_AT = datetime(2026, 11, 21, 12, 0, tzinfo=UTC)

PET_SCOPE: dict[str, Any] = {
    "name": "pets-and-house-rules",
    "purpose": (
        "Explain what it takes to own a dog or a cat in a residential complex, and which house"
        " rules apply to pets and their owners."
    ),
    "readers": (
        "People who consider getting a dog or a cat, pet owners living in the complex, and the"
        " house management."
    ),
    "level_guidance": {
        "level_1": (
            "The core of the domain: dog, cat, owner, resident, house management, and the rules"
            " every pet owner in the complex must know (registration, the lead, waste)."
        ),
        "level_2": (
            "What an owner needs on a normal day: feeding, walks, vaccination, grooming, leaving"
            " the pet alone, the shared spaces."
        ),
        "level_3": (
            "Special cases and error scenarios: puppies and kittens, dangerous breeds, moving"
            " house, travel, complaints and enforcement."
        ),
    },
    "ignorable_examples": [
        "Stories about one particular dog, cat or owner (names, places, memories)",
        "History or folklore about animals",
        "Quotes and motivational paragraphs that state no rule",
    ],
    "base_iri": "urn:domain-ai-assistant:ontology:pets-and-house-rules:",
}


def pet_minter() -> UlidMinter:
    """A minter whose IDs are the same on every run (fixed clock, fixed bytes)."""
    return UlidMinter(FixedClock(PET_AT), random_bytes=lambda n: b"\x5a" * n)


def read_pet_corpora(minter: UlidMinter) -> list[CorpusSource]:
    """The three pet manuals as corpora 00, 01 and 02, in a fixed order."""
    return [
        read_corpus(
            PET_MANUALS / name,
            source_path=f"user-manuals-pets-and-house-rules/{name}",
            number=number,
            run_id=PET_RUN,
            minter=minter,
        )
        for number, name in enumerate(PET_CORPORA)
    ]


@pytest.fixture(scope="session")
def pet_corpora() -> list[CorpusSource]:
    return read_pet_corpora(pet_minter())


@dataclass(frozen=True)
class PetExtraction:
    """Pass 1 over the three pet manuals: the corpora and one result per document."""

    corpora: list[CorpusSource]
    documents: list[DocumentExtraction]

    @property
    def units(self) -> dict[str, SourceUnit]:
        return {unit.id: unit for corpus in self.corpora for unit in corpus.units}

    @property
    def elements(self) -> list[Element]:
        return [element for document in self.documents for element in document.elements]

    @property
    def verdicts(self) -> dict[str, IgnorableVerdict]:
        return {u: v for document in self.documents for u, v in document.verdicts.items()}

    def path_of(self, unit_id: str) -> str:
        location = self.units[unit_id].location
        return location.path if location else ""


def pet_requests() -> list[LlmRequest]:
    """The pass 1 requests (calls A and B) of every pet document, as the estimate counts them."""
    scope = validate_record(ScopeRecord, PET_SCOPE)
    return [
        request
        for corpus in read_pet_corpora(pet_minter())
        for item in corpus.documents
        for request in pass1_requests(item.document, item.units, scope)
    ]


def extract_pets(client: LlmClient) -> PetExtraction:
    """Run pass 1 on every pet document with ``client``; IDs are the same on every run."""
    minter = pet_minter()
    corpora = read_pet_corpora(minter)
    context = ExtractionContext(
        scope=validate_record(ScopeRecord, PET_SCOPE),
        run_id=PET_RUN,
        clock=FixedClock(PET_AT),
        minter=minter,
    )
    documents = [
        extract_document(client, item.document, item.units, context)
        for corpus in corpora
        for item in corpus.documents
    ]
    return PetExtraction(corpora, documents)


@pytest.fixture(scope="session")
def pet_extraction() -> PetExtraction:
    """Pass 1 over the pet manuals, replayed from the curated fixtures."""
    return extract_pets(pet_replay())


def pet_term_input(extraction: PetExtraction) -> TermInput:
    """What pass 2 gets for the pet manuals: every element of pass 1; no ontology yet."""
    return TermInput(elements=extraction.elements, units=extraction.units)


def resolve_pets(client: LlmClient, extraction: PetExtraction) -> TermResolution:
    """Run pass 2 on the result of pass 1 over the pet manuals."""
    return resolve_terms(client, pet_term_input(extraction))


def pet_terms_request(extraction: PetExtraction) -> LlmRequest:
    return terms_request(pet_term_input(extraction)).request


def pet_replay() -> ReplayClient:
    return ReplayClient(FIXTURE_MODEL, FixtureStore(LLM_FIXTURES))


_ALIAS = re.compile(r"^\[U(\d+)\]", re.MULTILINE)


def _scripted_candidate(kind: str, number: str) -> dict[str, Any]:
    return {
        "key": f"{kind}.u{number}",
        "label": f"{kind} of U{number}",
        "evidence": [f"U{number}"],
        "level": "level-2",
        "level_reason": "scripted",
    }


def scripted_answer(request: LlmRequest) -> dict[str, Any]:
    """A valid answer to a request no fixture covers: one statement and concept per unit."""
    title = request.schema.get("title")
    if title == "TermResolutionOutput":
        return {"synonym_groups": [], "sense_splits": []}
    if title == "RulesOutput":
        return {"rules": [], "properties": []}
    numbers = _ALIAS.findall(request.prompt)
    return {
        "unit_verdicts": [{"unit": f"U{n}", "ignorable": False} for n in numbers],
        "statements": [
            _scripted_candidate("s", n) | {"text": f"What unit U{n} states."} for n in numbers
        ],
        "concepts": [_scripted_candidate("c", n) for n in numbers],
    }


class PetClient:
    """Replays the pet fixtures; a request without a fixture gets ``scripted_answer``.

    Ingesting one manual makes the pass 1 requests the fixtures were recorded for, but its pass 2
    request (one corpus, not three) and on-demand requests have no fixture. ``fail_after`` makes
    the client raise ``LlmUnavailableError`` from that call on, as a dropped connection would.
    """

    def __init__(self, fail_after: int | None = None) -> None:
        self.replay = pet_replay()
        self.fail_after = fail_after
        self.calls = 0
        self.scripted: list[LlmRequest] = []

    @property
    def model(self) -> str:
        return FIXTURE_MODEL

    def complete(self, request: LlmRequest) -> LlmResponse:
        if self.fail_after is not None and self.calls >= self.fail_after:
            raise LlmUnavailableError("the Claude API is not available: connection dropped")
        self.calls += 1
        try:
            return self.replay.complete(request)
        except FixtureMissingError:
            self.scripted.append(request)
            return LlmResponse(scripted_answer(request), 100, 50, FIXTURE_MODEL)

    def count_tokens(self, request: LlmRequest) -> int:
        return heuristic_tokens(request)


def pet_store(data_dir: Path) -> DatasetStore:
    """A new pets-and-house-rules dataset in ``data_dir`` with ``PET_SCOPE`` and fixed IDs."""
    store = DatasetStore(
        data_dir, "pets-and-house-rules", clock=FixedClock(PET_AT), minter=pet_minter()
    )
    store.create(validate_record(ScopeRecord, PET_SCOPE))
    return store


class PetKit:
    """The pet helpers for test modules (conftest cannot be imported under importlib mode)."""

    model = FIXTURE_MODEL
    fixtures = LLM_FIXTURES
    scope = PET_SCOPE
    extract = staticmethod(extract_pets)
    requests = staticmethod(pet_requests)
    resolve = staticmethod(resolve_pets)
    terms_request = staticmethod(pet_terms_request)
    replay = staticmethod(pet_replay)
    client = PetClient
    store = staticmethod(pet_store)
    manuals = PET_MANUALS
    manuals_root = PET_MANUALS.parent


@pytest.fixture(scope="session")
def pet_kit() -> PetKit:
    return PetKit()


# ---------- the HTTP API on a dataset in a temporary git repository (T19) ----------

API_PORT = 8765
API_BASE = f"http://127.0.0.1:{API_PORT}"
API_HEADERS = {"X-Ontology-Builder": "1"}
FAILING_HOOK = """#!/bin/sh
if [ -f .hook-fails ]; then
  echo "detect-secrets: a secret was found in the dataset"
  exit 1
fi
"""


def git(repo: Path, *args: str) -> str:
    found = shutil.which("git")
    assert found is not None
    done = subprocess.run(  # noqa: S603 - git with fixed arguments in a temp repo
        [found, "-C", str(repo), *args], check=True, capture_output=True, text=True
    )
    return done.stdout.strip()


def init_git_repo(path: Path) -> None:
    """A git repository at ``path`` whose pre-commit hook fails while ``.hook-fails`` exists;
    everything already in ``path`` (but the work folder) is committed."""
    git(path, "init", "-q", "-b", "main")
    for key, value in (
        ("user.name", "test"),
        ("user.email", "test@example.invalid"),
        ("commit.gpgsign", "false"),
        ("core.hooksPath", ".git/hooks"),
    ):
        git(path, "config", key, value)
    hook = path / ".git" / "hooks" / "pre-commit"
    hook.write_text(FAILING_HOOK, encoding="utf-8")
    hook.chmod(0o755)
    (path / ".gitignore").write_text("/work/\n/.hook-fails\n", encoding="utf-8")
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "start")


class ApiKit:
    """A served ontology: the app on an open session, a signed-out client, and git helpers.

    Nothing starts until first used, so a test can seed the dataset first: then the dataset is
    committed to a new git repository at ``path``, opened, and served.
    """

    def __init__(self, path: Path, store: DatasetStore, workspace: Workspace) -> None:
        self.path = path
        self.store = store
        self.workspace = workspace
        self._served: tuple[OpenOntology, FastAPI, TestClient] | None = None

    def _serve(self) -> tuple[OpenOntology, FastAPI, TestClient]:
        if self._served is None:
            init_git_repo(self.path)
            session = open_ontology(self.workspace, self.store.name)
            app = create_app(session, port=API_PORT)
            self._served = (session, app, TestClient(app, base_url=API_BASE, headers=API_HEADERS))
        return self._served

    @property
    def session(self) -> OpenOntology:
        return self._serve()[0]

    @property
    def app(self) -> FastAPI:
        return self._serve()[1]

    @property
    def client(self) -> TestClient:
        return self._serve()[2]

    def new_client(self) -> TestClient:
        return TestClient(self.app, base_url=API_BASE, headers=API_HEADERS)

    def sign_in(self, user: str = "alice", role: str = "user", client: Any = None) -> Any:
        response = (client or self.client).post("/api/session", json={"user": user, "role": role})
        assert response.status_code == 200, response.text
        return response.json()

    def url(self, rest: str = "") -> str:
        return f"/api/ontologies/{self.store.name}{rest}"

    def commits(self) -> int:
        return int(git(self.path, "rev-list", "--count", "HEAD"))

    def hook_fails(self, fails: bool = True) -> None:
        switch = self.path / ".hook-fails"
        if fails:
            switch.write_text("", encoding="utf-8")
        else:
            switch.unlink()

    def close(self) -> None:
        if self._served is not None:
            self._served[2].close()
            self._served[0].close()


def _no_llm() -> Any:
    pytest.fail("no LLM call expected")


def make_api_kit(
    path: Path,
    store: DatasetStore,
    llm: Callable[[], Any] = _no_llm,
    sources_root: Path | None = None,
) -> ApiKit:
    """Serve ``store`` (in ``path``) once first used, committed to a new git repository."""
    workspace = Workspace(
        data_dir=path,
        work_dir=path / "work",
        llm=llm,
        sources_root=sources_root,
        open_store=lambda _data_dir, _name: store,
    )
    return ApiKit(path, store, workspace)


@pytest.fixture
def api_kit(review_kit: ReviewKit, tmp_path: Path) -> Iterator[ApiKit]:
    """The review kit's dataset, served; seed it with ``review_kit.seed`` before signing in."""
    kit = make_api_kit(tmp_path, review_kit.store)
    yield kit
    kit.close()


def seed_pets(store: DatasetStore, extraction: PetExtraction) -> None:
    """Write the replayed pass 1 of the pet manuals (corpora, units, elements) into ``store``."""
    with store.transaction() as files:
        for corpus in extraction.corpora:
            files.write_corpus(corpus.folder, corpus.corpus)
            for item in corpus.documents:
                files.write_document(corpus.folder, item.document)
                files.write_units(corpus.folder, item.document.id, item.units)
        for element in extraction.elements:
            files.write_element(element)


@pytest.fixture
def pet_api_kit(
    review_kit: ReviewKit, tmp_path: Path, pet_extraction: PetExtraction
) -> Iterator[ApiKit]:
    """The pet manuals' pass 1 (fixture) as a served dataset."""
    seed_pets(review_kit.store, pet_extraction)
    kit = make_api_kit(tmp_path, review_kit.store)
    yield kit
    kit.close()


@pytest.fixture
def api_factory() -> Callable[..., ApiKit]:
    """``make_api_kit`` for tests that need their own LLM client or sources root."""
    return make_api_kit


@pytest.fixture
def git_init() -> Callable[[Path], None]:
    """``init_git_repo``: commit what is in a folder to a new repo with the failing-hook switch."""
    return init_git_repo
