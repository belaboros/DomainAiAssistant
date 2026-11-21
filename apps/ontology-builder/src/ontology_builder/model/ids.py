"""Minted IDs and the clock, both injectable so tests are deterministic (plan 0002, Decision).

An ID is a type prefix from ``ID_PREFIXES`` plus ``_`` plus a ULID: 48 bits of milliseconds and
80 random bits in Crockford base32. It never comes from a unit's text or position (FR-5).
"""

from __future__ import annotations

import os
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Protocol

ID_PREFIXES: dict[str, str] = {
    "statement": "st",
    "term": "tm",
    "concept": "cn",
    "relation": "rl",
    "rule": "ru",
    "property": "pr",
    "source_unit": "su",
    "document": "doc",
    "corpus": "co",
    "run": "run",
    "decision": "dc",
}
"""Prefix of each minted ID (prefix + ``_`` + ULID)."""

_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
_RANDOM_BITS = 80


class Clock(Protocol):
    """Gives the current time, always timezone-aware UTC."""

    def now(self) -> datetime: ...


class SystemClock:
    """The real clock."""

    def now(self) -> datetime:
        return datetime.now(UTC)


class FixedClock:
    """A clock that always gives the same time (for tests)."""

    def __init__(self, at: datetime) -> None:
        self._at = at

    def now(self) -> datetime:
        return self._at


def _encode(value: int, length: int) -> str:
    chars = []
    for _ in range(length):
        value, digit = divmod(value, 32)
        chars.append(_CROCKFORD[digit])
    return "".join(reversed(chars))


class UlidMinter:
    """Mints prefixed ULIDs; IDs minted in the same millisecond stay unique and ordered."""

    def __init__(
        self,
        clock: Clock | None = None,
        random_bytes: Callable[[int], bytes] = os.urandom,
    ) -> None:
        self._clock = clock or SystemClock()
        self._random_bytes = random_bytes
        self._last: tuple[int, int] = (-1, 0)

    def ulid(self) -> str:
        millis = int(self._clock.now().timestamp() * 1000)
        last_millis, last_random = self._last
        if millis <= last_millis:
            millis, random = last_millis, last_random + 1
        else:
            random = int.from_bytes(self._random_bytes(_RANDOM_BITS // 8), "big")
        self._last = (millis, random)
        return _encode(millis, 10) + _encode(random % (1 << _RANDOM_BITS), 16)

    def new(self, kind: str) -> str:
        """A new ID for a record kind of ``ID_PREFIXES`` (``concept``, ``source_unit``, ...)."""
        return f"{ID_PREFIXES[kind]}_{self.ulid()}"
