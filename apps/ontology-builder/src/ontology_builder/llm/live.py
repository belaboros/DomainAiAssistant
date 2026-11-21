"""The live client: calls Claude through the ``anthropic`` SDK (ontology-builder/ADR-0006).

The body carries the JSON-schema output format and no tools. Calls are streamed. Models in
``FALLBACK_MODELS`` get the server-side refusal fallback; the model that answered is reported.
"""

from __future__ import annotations

import json
from typing import Any

import anthropic

from ontology_builder.llm.client import (
    FALLBACK_BETA,
    FALLBACK_MODELS,
    LlmCallError,
    LlmOutputError,
    LlmRefusedError,
    LlmRequest,
    LlmResponse,
    LlmTruncatedError,
    LlmUnavailableError,
    output_config,
    request_body,
)

_UNAVAILABLE = (
    anthropic.APIConnectionError,
    anthropic.AuthenticationError,
    anthropic.PermissionDeniedError,
    anthropic.RateLimitError,
    anthropic.InternalServerError,
)


def _text(message: Any) -> str:
    return "".join(block.text for block in message.content if block.type == "text")


def _input_tokens(usage: Any) -> int:
    cached = (usage.cache_creation_input_tokens or 0) + (usage.cache_read_input_tokens or 0)
    return int(usage.input_tokens) + cached


def parse_message(message: Any) -> LlmResponse:
    """Turn a final SDK message into a response, or raise for a refusal, truncation or non-JSON."""
    if message.stop_reason == "refusal":
        raise LlmRefusedError("the model declined the request")
    if message.stop_reason == "max_tokens":
        raise LlmTruncatedError("the output hit max_tokens before the JSON was complete")
    try:
        data = json.loads(_text(message))
    except json.JSONDecodeError as error:
        raise LlmOutputError(f"the output is not JSON: {error}") from None
    if not isinstance(data, dict):
        raise LlmOutputError("the output is JSON but not an object")
    return LlmResponse(
        data=data,
        input_tokens=_input_tokens(message.usage),
        output_tokens=int(message.usage.output_tokens),
        model=str(message.model),
    )


class LiveClient:
    """Calls the Messages API with the configured model."""

    def __init__(self, model: str, sdk: anthropic.Anthropic) -> None:
        self._model = model
        self._sdk = sdk

    @property
    def model(self) -> str:
        return self._model

    def _stream(self, body: dict[str, Any]) -> Any:
        if self._model in FALLBACK_MODELS:
            return self._sdk.beta.messages.stream(
                **body, betas=[FALLBACK_BETA], fallbacks="default"
            )
        return self._sdk.messages.stream(**body)

    def complete(self, request: LlmRequest) -> LlmResponse:
        body = request_body(request, self._model)
        try:
            with self._stream(body) as stream:
                message = stream.get_final_message()
        except _UNAVAILABLE as error:
            raise LlmUnavailableError(f"the Claude API is not available: {error}") from None
        except anthropic.APIStatusError as error:
            raise LlmCallError(f"the Claude API rejected the request: {error}") from None
        return parse_message(message)

    def count_tokens(self, request: LlmRequest) -> int:
        try:
            counted = self._sdk.messages.count_tokens(
                model=self._model,
                system=request.system,
                messages=[{"role": "user", "content": request.prompt}],
                output_config=output_config(request),  # type: ignore[arg-type]
            )
        except _UNAVAILABLE as error:
            raise LlmUnavailableError(f"the Claude API is not available: {error}") from None
        except anthropic.APIStatusError as error:
            raise LlmCallError(f"the Claude API rejected the request: {error}") from None
        return int(counted.input_tokens)
