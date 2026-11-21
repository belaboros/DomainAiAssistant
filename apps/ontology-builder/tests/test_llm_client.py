"""The llm component: live, record and replay clients, estimate and pricing (T7, AC-6 half).

Structured output goes through ``output_config.format`` (ontology-builder/ADR-0006). No test calls
the network: the live client is driven through a fake SDK client.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import anthropic
import httpx2
import pytest
from ontology_builder.llm import (
    CHARS_PER_TOKEN,
    OUTPUT_RATIO,
    FixtureMismatchError,
    FixtureMissingError,
    FixtureStore,
    LiveClient,
    LlmCallError,
    LlmOutputError,
    LlmRefusedError,
    LlmRequest,
    LlmTruncatedError,
    LlmUnavailableError,
    Pricing,
    RecordingClient,
    ReplayClient,
    estimate,
    heuristic_tokens,
    make_client,
    request_body,
    request_hash,
    settings_from_env,
)
from ontology_builder.model import ExtractionOutput, tool_input_schema

MODEL = "claude-opus-5-5"
REPO = Path(__file__).resolve().parents[3]

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "unit": {"type": "string", "pattern": "^su_[0-9A-Z]{26}$"},
        "count": {"type": "integer", "minimum": 0},
    },
    "required": ["unit"],
}


def _request(prompt: str = "Extract the rules.") -> LlmRequest:
    return LlmRequest(system="You extract ontology candidates.", prompt=prompt, schema=SCHEMA)


# ---------- a fake of the parts of anthropic.Anthropic the live client uses ----------


def _message(
    text: str = '{"unit": "su_X"}', stop_reason: str = "end_turn", model: str = MODEL
) -> SimpleNamespace:
    usage = SimpleNamespace(
        input_tokens=120,
        output_tokens=30,
        cache_creation_input_tokens=0,
        cache_read_input_tokens=None,
    )
    blocks = [
        SimpleNamespace(type="thinking", thinking=""),
        SimpleNamespace(type="text", text=text),
    ]
    return SimpleNamespace(content=blocks, stop_reason=stop_reason, usage=usage, model=model)


@dataclass
class _Stream:
    message: SimpleNamespace

    def get_final_message(self) -> SimpleNamespace:
        return self.message


@dataclass
class _Messages:
    reply: SimpleNamespace | Exception
    calls: list[dict[str, Any]] = field(default_factory=list)
    counted: list[dict[str, Any]] = field(default_factory=list)

    @contextmanager
    def stream(self, **kwargs: Any) -> Iterator[_Stream]:
        self.calls.append(kwargs)
        if isinstance(self.reply, Exception):
            raise self.reply
        yield _Stream(self.reply)

    def count_tokens(self, **kwargs: Any) -> SimpleNamespace:
        self.counted.append(kwargs)
        return SimpleNamespace(input_tokens=777)


class _FakeSdk:
    def __init__(self, reply: SimpleNamespace | Exception) -> None:
        self.messages = _Messages(reply)
        self.beta = SimpleNamespace(messages=self.messages)


def _live(reply: SimpleNamespace | Exception, model: str = MODEL) -> tuple[LiveClient, _FakeSdk]:
    sdk = _FakeSdk(reply)
    return LiveClient(model, cast(anthropic.Anthropic, sdk)), sdk


def _api_error(cls: type[anthropic.APIStatusError], status: int) -> anthropic.APIStatusError:
    request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
    response = httpx2.Response(status, request=request)
    return cls("boom", response=response, body=None)


# ---------- the request ----------


def test_request_uses_structured_output_not_a_tool() -> None:
    body = request_body(_request(), MODEL)
    assert "tools" not in body
    assert "tool_choice" not in body
    fmt = body["output_config"]["format"]
    assert fmt["type"] == "json_schema"
    schema = fmt["schema"]
    assert schema["additionalProperties"] is False
    assert "pattern" not in schema["properties"]["unit"]
    assert "minimum" not in schema["properties"]["count"]
    assert body["messages"] == [{"role": "user", "content": "Extract the rules."}]


def test_extraction_output_schema_is_accepted_by_the_transform() -> None:
    request = LlmRequest(system="s", prompt="p", schema=tool_input_schema(ExtractionOutput))
    text = json.dumps(request_body(request, MODEL))
    assert '"pattern"' not in text


def test_hash_is_stable_and_ignores_key_order() -> None:
    reordered = LlmRequest(
        system="You extract ontology candidates.",
        prompt="Extract the rules.",
        schema={"required": ["unit"], "properties": SCHEMA["properties"], "type": "object"},
    )
    assert request_hash(_request(), MODEL) == request_hash(reordered, MODEL)
    assert re.fullmatch(r"[0-9a-f]{64}", request_hash(_request(), MODEL))


def test_hash_changes_with_prompt_schema_or_model() -> None:
    base = request_hash(_request(), MODEL)
    assert request_hash(_request("Other prompt."), MODEL) != base
    other_schema = LlmRequest(system="s", prompt="Extract the rules.", schema={"type": "object"})
    assert request_hash(other_schema, MODEL) != base
    assert request_hash(_request(), "claude-sonnet-5-5") != base


# ---------- replay and record ----------


def test_replay_returns_the_recorded_response(tmp_path: Path) -> None:
    store = FixtureStore(tmp_path)
    store.save(
        request_body(_request(), MODEL),
        {"data": {"unit": "su_A"}, "input_tokens": 5, "output_tokens": 2, "model": MODEL},
    )
    response = ReplayClient(MODEL, store).complete(_request())
    assert response.data == {"unit": "su_A"}
    assert (response.input_tokens, response.output_tokens, response.model) == (5, 2, MODEL)


def test_replay_of_an_unknown_request_fails_loudly(tmp_path: Path) -> None:
    client = ReplayClient(MODEL, FixtureStore(tmp_path))
    with pytest.raises(FixtureMissingError, match=request_hash(_request(), MODEL)):
        client.complete(_request())


def test_fixture_whose_request_was_edited_is_refused(tmp_path: Path) -> None:
    store = FixtureStore(tmp_path)
    path = store.save(
        request_body(_request(), MODEL),
        {"data": {}, "input_tokens": 1, "output_tokens": 1, "model": MODEL},
    )
    stored = json.loads(path.read_text(encoding="utf-8"))
    stored["request"]["system"] = "edited by hand"
    path.write_text(json.dumps(stored), encoding="utf-8")
    with pytest.raises(FixtureMismatchError):
        ReplayClient(MODEL, store).complete(_request())


def test_record_calls_live_once_and_saves_a_replayable_fixture(tmp_path: Path) -> None:
    live, sdk = _live(_message())
    store = FixtureStore(tmp_path)
    recorded = RecordingClient(live, store).complete(_request())
    assert len(sdk.messages.calls) == 1
    replayed = ReplayClient(MODEL, store).complete(_request())
    assert replayed == recorded
    files = list(tmp_path.glob("*.json"))
    assert [f.stem for f in files] == [request_hash(_request(), MODEL)]
    text = files[0].read_text(encoding="utf-8")
    assert text.endswith("\n") and '\n  "request"' in text  # readable, so it can be curated


def test_replay_counts_tokens_without_network(tmp_path: Path) -> None:
    client = ReplayClient(MODEL, FixtureStore(tmp_path))
    assert client.count_tokens(_request()) == heuristic_tokens(_request())


# ---------- live ----------


def test_live_parses_json_text_and_reports_usage() -> None:
    client, sdk = _live(_message('{"unit": "su_B"}'))
    response = client.complete(_request())
    assert response.data == {"unit": "su_B"}
    assert (response.input_tokens, response.output_tokens) == (120, 30)
    sent = sdk.messages.calls[0]
    assert sent["model"] == MODEL
    assert sent["output_config"]["format"]["type"] == "json_schema"
    assert sent["fallbacks"] == "default"
    assert "tool_choice" not in sent


def test_live_without_server_side_fallback_for_other_models() -> None:
    client, sdk = _live(_message(), model="claude-haiku-5-5")
    client.complete(_request())
    assert "fallbacks" not in sdk.messages.calls[0]
    assert "betas" not in sdk.messages.calls[0]


def test_live_reports_the_model_that_served_a_fallback() -> None:
    client, _ = _live(_message(model="claude-opus-5"))
    assert client.complete(_request()).model == "claude-opus-5"


@pytest.mark.parametrize(
    ("reply", "error"),
    [
        (_message(stop_reason="refusal"), LlmRefusedError),
        (_message('{"unit": "su_', stop_reason="max_tokens"), LlmTruncatedError),
        (_message("not json"), LlmOutputError),
        (_message("[1, 2]"), LlmOutputError),
    ],
)
def test_live_bad_replies_raise(reply: SimpleNamespace, error: type[Exception]) -> None:
    client, _ = _live(reply)
    with pytest.raises(error):
        client.complete(_request())


def test_live_unreachable_or_rejected_key_is_unavailable() -> None:
    request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
    for failure in (
        anthropic.APIConnectionError(request=request),
        _api_error(anthropic.AuthenticationError, 401),
        _api_error(anthropic.InternalServerError, 500),
    ):
        client, _ = _live(failure)
        with pytest.raises(LlmUnavailableError):
            client.complete(_request())


def test_live_bad_request_is_a_call_error() -> None:
    client, _ = _live(_api_error(anthropic.BadRequestError, 400))
    with pytest.raises(LlmCallError):
        client.complete(_request())


def test_live_counts_tokens_with_the_api() -> None:
    client, sdk = _live(_message())
    assert client.count_tokens(_request()) == 777
    counted = sdk.messages.counted[0]
    assert counted["model"] == MODEL
    assert counted["output_config"]["format"]["type"] == "json_schema"


# ---------- configuration ----------


def test_no_key_is_a_clear_error_before_any_call(tmp_path: Path) -> None:
    for mode in ("live", "record"):
        with pytest.raises(LlmUnavailableError, match="ANTHROPIC_API_KEY"):
            make_client(mode, MODEL, fixtures_dir=tmp_path, api_key="")


def test_replay_needs_no_key(tmp_path: Path) -> None:
    assert isinstance(
        make_client("replay", MODEL, fixtures_dir=tmp_path, api_key=None), ReplayClient
    )


def test_unknown_mode_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="ONTOLOGY_BUILDER_LLM_MODE"):
        make_client("dry-run", MODEL, fixtures_dir=tmp_path, api_key="k")


def test_settings_from_env() -> None:
    settings = settings_from_env(
        {"ONTOLOGY_BUILDER_LLM_MODE": "replay", "CLAUDE_MODEL": MODEL, "ANTHROPIC_API_KEY": ""}
    )
    assert (settings.mode, settings.model, settings.api_key) == ("replay", MODEL, None)
    assert settings_from_env({"CLAUDE_MODEL": MODEL}).mode == "live"
    with pytest.raises(LlmUnavailableError, match="CLAUDE_MODEL"):
        settings_from_env({"ONTOLOGY_BUILDER_LLM_MODE": "live"})


# ---------- estimate and pricing ----------


def test_heuristic_is_characters_over_3_5() -> None:
    request = _request()
    chars = len(request.system) + len(request.prompt) + len(json.dumps(SCHEMA, sort_keys=True))
    assert CHARS_PER_TOKEN == 3.5
    assert heuristic_tokens(request) == math.ceil(chars / 3.5)


def test_estimate_sums_requests_with_output_ratio_and_cost() -> None:
    pricing = Pricing.load()
    requests = [_request(), _request("Second document.")]
    result = estimate(requests, MODEL, counter=lambda _r: 1000, pricing=pricing)
    assert (result.requests, result.input_tokens) == (2, 2000)
    assert OUTPUT_RATIO == 0.6
    assert result.output_tokens == 1200
    assert result.cost_usd == pytest.approx(2000 * 4 / 1e6 + 1200 * 20 / 1e6)
    assert result.model == MODEL


def test_estimate_for_unknown_model_shows_tokens_only() -> None:
    result = estimate([_request()], "claude-unknown", counter=lambda _r: 10, pricing=Pricing.load())
    assert result.input_tokens == 10
    assert result.cost_usd is None


def test_long_prompt_tier_applies_per_request() -> None:
    pricing = Pricing.load()
    assert pricing.cost("claude-haiku-5-5", 100_000, 0) == pytest.approx(0.01)
    assert pricing.cost("claude-haiku-5-5", 200_000, 0) == pytest.approx(0.10)


def test_pricing_file_is_dated_and_covers_the_default_model() -> None:
    pricing = Pricing.load()
    assert isinstance(pricing.checked_at, date)
    default = re.search(r"^CLAUDE_MODEL=(\S+)$", (REPO / ".env.example").read_text(), re.M)
    assert default is not None
    assert pricing.cost(default.group(1), 1, 1) is not None
