"""NFR responsiveness: with 5,000 elements, listing, search and one review action each answer
within 1 second."""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

ELEMENTS = 5000
LIMIT_S = 1.0


def _timed[T](call: Callable[[], T]) -> tuple[T, float]:
    started = time.perf_counter()
    result = call()
    return result, time.perf_counter() - started


def test_5000_elements_list_and_action_under_1s(
    review_kit: Any, tmp_path: Path, api_factory: Any
) -> None:
    records = [review_kit.concept() for _ in range(ELEMENTS)]
    for number, record in enumerate(records):
        record["label"] = f"concept {number}"
    ids = review_kit.seed(records)
    kit = api_factory(tmp_path, review_kit.store)
    try:
        kit.sign_in()
        listed, listing = _timed(lambda: kit.client.get(kit.url("/elements")))
        assert len(listed.json()["elements"]) == ELEMENTS

        query = {"q": "concept 4999"}
        found, searching = _timed(lambda: kit.client.get(kit.url("/elements"), params=query))
        assert [e["label"] for e in found.json()["elements"]] == ["concept 4999"]

        body = {"action": "include", "ids": [ids[17]], "payload": {}}
        acted, acting = _timed(lambda: kit.client.post(kit.url("/actions"), json=body))
        assert acted.json()["results"][0]["ok"]
    finally:
        kit.close()

    assert max(listing, searching, acting) < LIMIT_S, (listing, searching, acting)
