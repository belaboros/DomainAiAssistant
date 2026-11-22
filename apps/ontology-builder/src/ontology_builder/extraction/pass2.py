"""Pass 2 for one ingestion: term resolution across documents (plan 0002, Approach 4 and 5).

One call gets every candidate term with its mentions and contexts, the new concepts and the
concepts already in the ontology, and returns synonym groups and sense splits. The answer is
validated item by item and retried once, like pass 1; what stays invalid or cites an unknown alias
is reported in the run record and left out. Without a usable answer the elements stay as pass 1
gave them. An unavailable API is not retried: the error reaches the caller, before any write.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ontology_builder.extraction.parse import UnusableOutputError
from ontology_builder.extraction.terms_apply import apply_answer
from ontology_builder.extraction.terms_parse import (
    WHERE,
    TermAnswer,
    merge_retry,
    parse_terms,
    report_invalid,
)
from ontology_builder.extraction.terms_prompt import (
    TermInput,
    retry_invalid,
    retry_unusable,
    terms_request,
)
from ontology_builder.llm import (
    LlmClient,
    LlmOutputError,
    LlmRefusedError,
    LlmRequest,
    LlmTruncatedError,
)
from ontology_builder.model import Concept, Element, SkippedItem, Term

_RETRYABLE = (LlmOutputError, LlmTruncatedError, LlmRefusedError, UnusableOutputError)


@dataclass
class TermResolution:
    """The result of pass 2: the run's elements after it, and what it changed or left out."""

    elements: list[Element]
    merged: dict[str, str] = field(default_factory=dict)
    """Merged concept ID to the ID of the concept it was merged into."""
    skipped: list[SkippedItem] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    extended: list[Element] = field(default_factory=list)
    """Concepts and terms already in the ontology that the run added to (ADR-0012)."""


class _Caller:
    def __init__(self, client: LlmClient) -> None:
        self.client = client
        self.input_tokens = 0
        self.output_tokens = 0
        self.failures: list[str] = []

    def answer(self, request: LlmRequest) -> TermAnswer:
        try:
            response = self.client.complete(request)
            self.input_tokens += response.input_tokens
            self.output_tokens += response.output_tokens
            return parse_terms(response.data)
        except _RETRYABLE as error:
            self.failures.append(str(error))
            raise


def _ask(caller: _Caller, request: LlmRequest) -> tuple[TermAnswer | None, list[SkippedItem]]:
    """The validated answer after at most one retry, and the items reported on the way."""
    try:
        first = caller.answer(request)
    except _RETRYABLE as error:
        try:
            answer = caller.answer(retry_unusable(request, str(error)))
        except _RETRYABLE:
            return None, []
        return answer, report_invalid(answer, "and not retried again")
    if not first.invalid:
        return first, []
    try:
        retry = caller.answer(retry_invalid(request, [i.for_retry() for i in first.invalid]))
    except _RETRYABLE as error:
        return first, report_invalid(first, f"and the retry failed ({error})")
    merged = merge_retry(first, retry)
    return merged, report_invalid(merged, "after one retry")


def _has_work(found: TermInput) -> bool:
    return any(isinstance(e, Concept | Term) for e in found.elements)


def resolve_terms(client: LlmClient, found: TermInput) -> TermResolution:
    """Pass 2: merge synonyms and split senses in the new elements of one run."""
    result = TermResolution(list(found.elements))
    if not _has_work(found):
        return result
    prompt = terms_request(found)
    caller = _Caller(client)
    answer, reported = _ask(caller, prompt.request)
    result.input_tokens, result.output_tokens = caller.input_tokens, caller.output_tokens
    if answer is None:
        reason = "no usable answer after one retry: " + caller.failures[-1]
        result.skipped = [SkippedItem(where=WHERE, item="term resolution", reason=reason)]
        return result
    existing = [*found.existing, *found.existing_terms]
    applied = apply_answer(prompt, found.elements, existing, answer)
    result.elements, result.merged = applied.elements, applied.merged
    result.extended = applied.extended
    result.skipped = reported + applied.skipped
    return result
