"""The cost estimate shown before every LLM run (FR-6), and the price list ``pricing.yaml``.

Input tokens are counted per request; the expected output is ``OUTPUT_RATIO`` of the input. The
price of each request is looked up per model in ``pricing.yaml``; an unknown model shows tokens
only. A model may have a long-prompt tier that applies per request above a token threshold.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from ontology_builder.llm.client import LlmRequest

OUTPUT_RATIO = 0.6
"""Expected output tokens per input token (plan 0002, LLM)."""

PRICING_PATH = Path(__file__).parent / "pricing.yaml"
_PER_TOKEN = 1 / 1_000_000


@dataclass(frozen=True)
class Price:
    """USD per million tokens, with an optional higher price above a prompt size."""

    input: float
    output: float
    long_above: int | None = None
    long_input: float | None = None
    long_output: float | None = None

    def cost(self, input_tokens: int, output_tokens: int) -> float:
        rate_in, rate_out = self.input, self.output
        if self.long_above is not None and input_tokens > self.long_above:
            rate_in = self.long_input if self.long_input is not None else rate_in
            rate_out = self.long_output if self.long_output is not None else rate_out
        return (input_tokens * rate_in + output_tokens * rate_out) * _PER_TOKEN


def _price(entry: Mapping[str, Any]) -> Price:
    long = entry.get("long_prompt") or {}
    return Price(
        input=float(entry["input"]),
        output=float(entry["output"]),
        long_above=int(long["above_input_tokens"]) if long else None,
        long_input=float(long["input"]) if long else None,
        long_output=float(long["output"]) if long else None,
    )


@dataclass(frozen=True)
class Pricing:
    """The price list and the date it was checked against Anthropic's pricing page."""

    checked_at: date
    source: str
    prices: Mapping[str, Price]

    @classmethod
    def load(cls, path: Path = PRICING_PATH) -> Pricing:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(
            checked_at=data["checked_at"],
            source=str(data["source"]),
            prices={name: _price(entry) for name, entry in data["models"].items()},
        )

    def cost(self, model: str, input_tokens: int, output_tokens: int) -> float | None:
        """USD for one request, or ``None`` for a model not in the list."""
        price = self.prices.get(model)
        return None if price is None else price.cost(input_tokens, output_tokens)


@dataclass(frozen=True)
class TokenEstimate:
    """What a run will cost: requests, tokens in and out, and USD when the model is priced."""

    model: str
    requests: int
    input_tokens: int
    output_tokens: int
    cost_usd: float | None


def estimate(
    requests: Iterable[LlmRequest],
    model: str,
    counter: Callable[[LlmRequest], int],
    pricing: Pricing,
) -> TokenEstimate:
    """Count every request with ``counter`` and price it for ``model``."""
    count = total_in = total_out = 0
    cost: float | None = 0.0
    for request in requests:
        tokens_in = counter(request)
        tokens_out = math.ceil(tokens_in * OUTPUT_RATIO)
        count, total_in, total_out = count + 1, total_in + tokens_in, total_out + tokens_out
        request_cost = pricing.cost(model, tokens_in, tokens_out)
        cost = None if cost is None or request_cost is None else cost + request_cost
    return TokenEstimate(model, count, total_in, total_out, cost)
