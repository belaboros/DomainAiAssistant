"""Recorded responses: the fixture store and the record and replay clients (ADR-0005).

A fixture is ``<dir>/<sha256 of the canonical request body>.json`` holding the request as sent and
the response. The response part may be curated by hand; the request part may not, and a fixture
whose request no longer hashes to its file name is refused, so stale fixtures fail loudly.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from ontology_builder.llm.client import (
    LlmClient,
    LlmError,
    LlmRequest,
    LlmResponse,
    body_hash,
    canonical_json,
    request_body,
)

CHARS_PER_TOKEN = 3.5
"""Characters per token of the offline token estimate (plan 0002, LLM)."""


class FixtureMissingError(LlmError):
    """Replay found no fixture for a request: record it, or the prompt changed."""


class FixtureMismatchError(LlmError):
    """A fixture's stored request does not hash to its file name (its request was edited)."""


def heuristic_tokens(request: LlmRequest) -> int:
    """Offline token estimate: the characters of system, prompt and schema over 3.5."""
    chars = (
        len(request.system) + len(request.prompt) + len(json.dumps(request.schema, sort_keys=True))
    )
    return math.ceil(chars / CHARS_PER_TOKEN)


class FixtureStore:
    """A folder of recorded request/response pairs keyed by request hash."""

    def __init__(self, folder: Path) -> None:
        self.folder = folder

    def path(self, key: str) -> Path:
        return self.folder / f"{key}.json"

    def save(self, body: dict[str, Any], response: dict[str, Any]) -> Path:
        """Write a fixture, readable for curation (sorted keys, two-space indent)."""
        path = self.path(body_hash(body))
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps({"request": body, "response": response}, sort_keys=True, indent=2)
        path.write_text(text + "\n", encoding="utf-8")
        return path

    def load(self, body: dict[str, Any]) -> dict[str, Any]:
        """The recorded response for a request body, or raise."""
        key = body_hash(body)
        path = self.path(key)
        if not path.is_file():
            raise FixtureMissingError(
                f"no recorded response {key}.json in {self.folder}; record it with "
                "ONTOLOGY_BUILDER_LLM_MODE=record (the prompt or schema may have changed)"
            )
        stored = json.loads(path.read_text(encoding="utf-8"))
        if canonical_json(stored["request"]) != canonical_json(body):
            raise FixtureMismatchError(f"{path.name}: its request was edited; re-record it")
        response: dict[str, Any] = stored["response"]
        return response


def _to_fixture(response: LlmResponse) -> dict[str, Any]:
    return {
        "data": response.data,
        "input_tokens": response.input_tokens,
        "output_tokens": response.output_tokens,
        "model": response.model,
    }


class ReplayClient:
    """Answers from recorded fixtures only; never touches the network."""

    def __init__(self, model: str, store: FixtureStore) -> None:
        self._model = model
        self._store = store

    @property
    def model(self) -> str:
        return self._model

    def complete(self, request: LlmRequest) -> LlmResponse:
        recorded = self._store.load(request_body(request, self._model))
        return LlmResponse(
            data=recorded["data"],
            input_tokens=int(recorded["input_tokens"]),
            output_tokens=int(recorded["output_tokens"]),
            model=str(recorded["model"]),
        )

    def count_tokens(self, request: LlmRequest) -> int:
        return heuristic_tokens(request)


class RecordingClient:
    """Calls another client and saves every response as a fixture."""

    def __init__(self, inner: LlmClient, store: FixtureStore) -> None:
        self._inner = inner
        self._store = store

    @property
    def model(self) -> str:
        return self._inner.model

    def complete(self, request: LlmRequest) -> LlmResponse:
        response = self._inner.complete(request)
        self._store.save(request_body(request, self._inner.model), _to_fixture(response))
        return response

    def count_tokens(self, request: LlmRequest) -> int:
        return self._inner.count_tokens(request)
