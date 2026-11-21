"""llm component.

Calls Claude or replays recorded responses, and estimates tokens and cost.

``make_client`` gives an ``LlmClient`` for a mode (``ONTOLOGY_BUILDER_LLM_MODE``): ``live`` calls
Claude, ``record`` calls Claude and saves fixtures, ``replay`` answers from fixtures only (tests).
Output is JSON shaped by ``output_config.format`` (ontology-builder/ADR-0006). ``estimate`` gives
the token count and cost shown before every run (FR-6), priced from ``pricing.yaml``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import anthropic

from ontology_builder.llm.client import (
    DEFAULT_MAX_TOKENS,
    LlmCallError,
    LlmClient,
    LlmError,
    LlmOutputError,
    LlmRefusedError,
    LlmRequest,
    LlmResponse,
    LlmTruncatedError,
    LlmUnavailableError,
    request_body,
    request_hash,
)
from ontology_builder.llm.estimate import (
    OUTPUT_RATIO,
    PRICING_PATH,
    Price,
    Pricing,
    TokenEstimate,
    estimate,
)
from ontology_builder.llm.fixtures import (
    CHARS_PER_TOKEN,
    FixtureMismatchError,
    FixtureMissingError,
    FixtureStore,
    RecordingClient,
    ReplayClient,
    heuristic_tokens,
)
from ontology_builder.llm.live import LiveClient

MODES = ("live", "record", "replay")


@dataclass(frozen=True)
class LlmSettings:
    """The llm configuration read from the layered environment (ADR-0012)."""

    mode: str
    model: str
    api_key: str | None


def settings_from_env(env: Mapping[str, str]) -> LlmSettings:
    """Read ``ONTOLOGY_BUILDER_LLM_MODE`` (default ``live``), ``CLAUDE_MODEL`` and the API key."""
    model = env.get("CLAUDE_MODEL", "").strip()
    if not model:
        raise LlmUnavailableError("CLAUDE_MODEL is not set; set it in the root .env")
    return LlmSettings(
        mode=env.get("ONTOLOGY_BUILDER_LLM_MODE", "").strip() or "live",
        model=model,
        api_key=env.get("ANTHROPIC_API_KEY", "").strip() or None,
    )


def make_client(mode: str, model: str, fixtures_dir: Path, api_key: str | None) -> LlmClient:
    """A client for the mode. Without a key, ``live`` and ``record`` fail before any call."""
    if mode not in MODES:
        raise ValueError(f"ONTOLOGY_BUILDER_LLM_MODE must be one of {', '.join(MODES)}: {mode!r}")
    store = FixtureStore(fixtures_dir)
    if mode == "replay":
        return ReplayClient(model, store)
    if not api_key:
        raise LlmUnavailableError(
            "ANTHROPIC_API_KEY is not set; set it in the root .env "
            "(check with tools/env/with-env.sh ontology-builder --check)"
        )
    live = LiveClient(model, anthropic.Anthropic(api_key=api_key))
    return live if mode == "live" else RecordingClient(live, store)


__all__ = [
    "CHARS_PER_TOKEN",
    "DEFAULT_MAX_TOKENS",
    "MODES",
    "OUTPUT_RATIO",
    "PRICING_PATH",
    "FixtureMismatchError",
    "FixtureMissingError",
    "FixtureStore",
    "LiveClient",
    "LlmCallError",
    "LlmClient",
    "LlmError",
    "LlmOutputError",
    "LlmRefusedError",
    "LlmRequest",
    "LlmResponse",
    "LlmSettings",
    "LlmTruncatedError",
    "LlmUnavailableError",
    "Price",
    "Pricing",
    "RecordingClient",
    "ReplayClient",
    "TokenEstimate",
    "estimate",
    "heuristic_tokens",
    "make_client",
    "request_body",
    "request_hash",
    "settings_from_env",
]
