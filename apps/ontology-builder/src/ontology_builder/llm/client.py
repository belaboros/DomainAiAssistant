"""The client port: one request in, schema-shaped JSON out (ontology-builder/ADR-0005, ADR-0006).

A request is a system prompt, one user prompt and the JSON Schema of the expected output. The
schema is sent as structured output (``output_config.format``) after ``anthropic.transform_schema``
has removed the keywords the API does not support; the caller still validates the full schema.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Protocol

from anthropic import transform_schema

DEFAULT_MAX_TOKENS = 64_000
"""Output cap per call. Calls are streamed, so a large cap does not hit HTTP timeouts."""

FALLBACK_MODELS = frozenset(
    {
        "claude-fable-5-2",
        "claude-fable-5-1",
        "claude-opus-5-5",
        "claude-opus-5",
        "claude-sonnet-5-5",
    }
)
"""Models that get the API's server-side refusal fallback (``fallbacks: "default"``)."""

FALLBACK_BETA = "server-side-fallback-2026-07-01"


class LlmError(Exception):
    """Base class of every llm failure."""


class LlmUnavailableError(LlmError):
    """No key, a rejected key, or the API cannot be reached; nothing was produced."""


class LlmCallError(LlmError):
    """The API rejected the request (a bug on our side, e.g. an invalid schema)."""


class LlmRefusedError(LlmError):
    """The model declined the request."""


class LlmTruncatedError(LlmError):
    """The output hit ``max_tokens`` before the JSON was complete."""


class LlmOutputError(LlmError):
    """The output is not a JSON object."""


@dataclass(frozen=True)
class LlmRequest:
    """One structured-output call."""

    system: str
    prompt: str
    schema: dict[str, Any]
    max_tokens: int = DEFAULT_MAX_TOKENS
    effort: str | None = None


@dataclass(frozen=True)
class LlmResponse:
    """The parsed JSON object, the tokens used and the model that answered."""

    data: dict[str, Any]
    input_tokens: int
    output_tokens: int
    model: str


class LlmClient(Protocol):
    """What extraction and ingestion depend on; live, record and replay all implement it."""

    @property
    def model(self) -> str: ...

    def complete(self, request: LlmRequest) -> LlmResponse: ...

    def count_tokens(self, request: LlmRequest) -> int: ...


def output_config(request: LlmRequest) -> dict[str, Any]:
    """The ``output_config`` of a request: the JSON-schema format, plus the effort if set."""
    config: dict[str, Any] = {
        "format": {"type": "json_schema", "schema": transform_schema(request.schema)}
    }
    if request.effort is not None:
        config["effort"] = request.effort
    return config


def request_body(request: LlmRequest, model: str) -> dict[str, Any]:
    """The Messages API body for a request, as sent and as hashed."""
    return {
        "model": model,
        "max_tokens": request.max_tokens,
        "system": request.system,
        "messages": [{"role": "user", "content": request.prompt}],
        "output_config": output_config(request),
    }


def canonical_json(value: Any) -> str:
    """Key-sorted, compact JSON: equal values give equal text."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def body_hash(body: dict[str, Any]) -> str:
    """SHA-256 (hex) of the canonical JSON of a request body; the replay fixture key."""
    return hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()


def request_hash(request: LlmRequest, model: str) -> str:
    """The fixture key of a request for a model."""
    return body_hash(request_body(request, model))
