"""Records the LLM fixtures of the pet manuals (live; costs money; never part of the gate).

Run it only after the cost estimate was shown and confirmed (FR-6, plan 0002 T8 and T9):

    tools/env/with-env.sh ontology-builder -- uv run pytest -m live \
        apps/ontology-builder/tests/test_record_llm_fixtures.py -s

A request that already has a fixture is replayed, never re-recorded, so curated fixtures stay as
they are. Only missing fixtures (a new document, or a prompt change) call Claude. Fixtures are
recorded for the kit's fixture model, whatever ``CLAUDE_MODEL`` says, so request hashes are stable.
"""

from __future__ import annotations

import os
from typing import Any

import pytest
from ontology_builder.llm import (
    FixtureMissingError,
    FixtureStore,
    LlmRequest,
    LlmResponse,
    Pricing,
    RecordingClient,
    ReplayClient,
    estimate,
    heuristic_tokens,
    make_client,
)

pytestmark = pytest.mark.live


class ReplayOrRecord:
    """Replays a request that has a fixture; records one that has not."""

    def __init__(self, replay: ReplayClient, record: RecordingClient) -> None:
        self._replay = replay
        self._record = record
        self.recorded = 0

    @property
    def model(self) -> str:
        return self._replay.model

    def complete(self, request: LlmRequest) -> LlmResponse:
        try:
            return self._replay.complete(request)
        except FixtureMissingError:
            self.recorded += 1
            return self._record.complete(request)

    def count_tokens(self, request: LlmRequest) -> int:
        return self._replay.count_tokens(request)


def test_record_pass1_fixtures(pet_kit: Any) -> None:
    replay = ReplayClient(pet_kit.model, FixtureStore(pet_kit.fixtures))
    key = os.environ.get("ANTHROPIC_API_KEY")
    record = make_client("record", pet_kit.model, pet_kit.fixtures, key)
    assert isinstance(record, RecordingClient)
    print(estimate(pet_kit.requests(), pet_kit.model, heuristic_tokens, Pricing.load()))
    client = ReplayOrRecord(replay, record)
    result = pet_kit.extract(client)
    used_in = sum(d.input_tokens for d in result.documents)
    used_out = sum(d.output_tokens for d in result.documents)
    print(f"recorded {client.recorded} calls; tokens in {used_in}, out {used_out}")
    for document in result.documents:
        for item in document.skipped:
            print(f"skipped in {item.where}: {item.item}: {item.reason}")


def test_record_pass2_fixture(pet_kit: Any) -> None:
    """Pass 2 on the replayed pass 1 (record pass 1 first; its fixtures must all exist)."""
    replay = ReplayClient(pet_kit.model, FixtureStore(pet_kit.fixtures))
    key = os.environ.get("ANTHROPIC_API_KEY")
    record = make_client("record", pet_kit.model, pet_kit.fixtures, key)
    assert isinstance(record, RecordingClient)
    extraction = pet_kit.extract(replay)
    request = pet_kit.terms_request(extraction)
    print(estimate([request], pet_kit.model, heuristic_tokens, Pricing.load()))
    client = ReplayOrRecord(replay, record)
    result = pet_kit.resolve(client, extraction)
    tokens = f"tokens in {result.input_tokens}, out {result.output_tokens}"
    print(f"recorded {client.recorded} calls; {tokens}")
    print(f"merged {len(result.merged)} concepts")
    for item in result.skipped:
        print(f"skipped in {item.where}: {item.item}: {item.reason}")
