"""Pass 1 for one document: ask, validate, retry once, report the rest (plan 0002, Approach 4).

Pass 1 is two calls (ontology-builder/ADR-0007): call A gives the unit verdicts, statements,
terms, concepts and relations; call B gets A's candidates by key and gives rules and properties.
Each answer is validated item by item. If any item is invalid, or the answer is unusable as a
whole, one retry is asked for; whatever is still invalid after it is reported in the run record
and dropped. An unavailable API is not retried: the error reaches the caller, before any write.
"""

from __future__ import annotations

from collections.abc import Collection, Sequence
from dataclasses import dataclass, field

from ontology_builder.extraction.parse import (
    CALL_A_LISTS,
    CALL_B_LISTS,
    KIND_OF_LIST,
    Parsed,
    UnusableOutputError,
    merge_answers,
    parse_answer,
    report_invalid,
)
from ontology_builder.extraction.prompt import (
    Found,
    aliases,
    concepts_request,
    retry_invalid,
    retry_unusable,
    rules_request,
)
from ontology_builder.extraction.resolve import Origin, build_records, ignorable_verdicts
from ontology_builder.llm import (
    LlmClient,
    LlmOutputError,
    LlmRefusedError,
    LlmRequest,
    LlmTruncatedError,
)
from ontology_builder.model import (
    Clock,
    Document,
    Element,
    IgnorableVerdict,
    ScopeRecord,
    SkippedItem,
    SourceUnit,
    UlidMinter,
)

_RETRYABLE = (LlmOutputError, LlmTruncatedError, LlmRefusedError, UnusableOutputError)


@dataclass(frozen=True)
class ExtractionContext:
    """What every extraction of one run shares."""

    scope: ScopeRecord
    run_id: str
    clock: Clock
    minter: UlidMinter
    not_ignorable: Collection[str] = frozenset()
    """IDs of units a person marked not ignorable: never proposed ignorable again (FR-14)."""


@dataclass
class DocumentExtraction:
    """The result of pass 1 for one document."""

    document_id: str
    verdicts: dict[str, IgnorableVerdict] = field(default_factory=dict)
    """Units proposed ignorable, by unit ID."""
    elements: list[Element] = field(default_factory=list)
    skipped: list[SkippedItem] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass(frozen=True)
class _Call:
    """One of the two calls of pass 1: its request and what its answer may hold."""

    request: LlmRequest
    lists: tuple[str, ...]
    verdicts: bool

    def again(self, request: LlmRequest) -> _Call:
        return _Call(request, self.lists, self.verdicts)


class _Caller:
    """Calls the client, adds up the tokens of every call and keeps each retryable failure."""

    def __init__(self, client: LlmClient) -> None:
        self.client = client
        self.input_tokens = 0
        self.output_tokens = 0
        self.failures: list[str] = []

    def answer(self, call: _Call) -> Parsed:
        try:
            response = self.client.complete(call.request)
            self.input_tokens += response.input_tokens
            self.output_tokens += response.output_tokens
            return parse_answer(response.data, call.lists, call.verdicts)
        except _RETRYABLE as error:
            self.failures.append(str(error))
            raise


def _ask(caller: _Caller, call: _Call, where: str) -> Parsed | None:
    """The validated answer after at most one retry, or ``None`` if none was usable."""
    try:
        first = caller.answer(call)
    except _RETRYABLE as error:
        try:
            parsed = caller.answer(call.again(retry_unusable(call.request, str(error))))
        except _RETRYABLE:
            return None
        report_invalid(parsed, where, "and not retried again")
        return parsed
    if not first.invalid:
        return first
    invalid = [item.for_retry() for item in first.invalid]
    try:
        retry = caller.answer(call.again(retry_invalid(call.request, invalid)))
    except _RETRYABLE as error:
        report_invalid(first, where, f"and the retry failed ({error})")
        return first
    merged = merge_answers(first, retry, where)
    report_invalid(merged, where, "after one retry")
    return merged


def _found(parsed: Parsed) -> list[Found]:
    return [
        Found(KIND_OF_LIST[name], candidate.key, candidate.label)
        for name in CALL_A_LISTS
        for candidate in parsed.candidates[name]
    ]


def _rules_call(
    document: Document, units: Sequence[SourceUnit], scope: ScopeRecord, first: Parsed
) -> _Call | None:
    """Call B for the answer of call A, or ``None`` when every unit is ignorable."""
    ignorable = sorted(alias for alias, verdict in first.verdicts.items() if verdict.ignorable)
    if len(ignorable) >= len(units):
        return None
    request = rules_request(document, units, scope, _found(first), ignorable)
    return _Call(request, CALL_B_LISTS, verdicts=False)


def _drop_kept_verdicts(
    parsed: Parsed | None, units: Sequence[SourceUnit], not_ignorable: Collection[str]
) -> None:
    """Forget the ignorable verdicts on units a person marked not ignorable."""
    if parsed is None:
        return
    for alias, unit_id in aliases(units).items():
        if unit_id in not_ignorable:
            parsed.verdicts.pop(alias, None)


def _ask_both(
    caller: _Caller, document: Document, units: Sequence[SourceUnit], context: ExtractionContext
) -> Parsed | None:
    """Calls A and B merged; ``None`` if call A gave no usable answer (ADR-0007)."""
    where, scope = document.path, context.scope
    request = concepts_request(document, units, scope, context.not_ignorable)
    first = _ask(caller, _Call(request, CALL_A_LISTS, True), where)
    _drop_kept_verdicts(first, units, context.not_ignorable)
    rules = _rules_call(document, units, scope, first) if first is not None else None
    if first is None or rules is None:
        return first
    second = _ask(caller, rules, where)
    if second is None:
        reason = "no usable answer after one retry: " + caller.failures[-1]
        first.skipped.append(
            SkippedItem(where=where, item=f"rules and properties of {where}", reason=reason)
        )
        return first
    return merge_answers(first, second, where)


def extract_document(
    client: LlmClient,
    document: Document,
    units: Sequence[SourceUnit],
    context: ExtractionContext,
) -> DocumentExtraction:
    """Pass 1 for one document: verdicts per unit and proposed records with evidence."""
    where = document.path
    caller = _Caller(client)
    parsed = _ask_both(caller, document, units, context)
    result = DocumentExtraction(document.id)
    if parsed is None:
        reason = "no usable answer after one retry: " + caller.failures[-1]
        result.skipped = [SkippedItem(where=where, item=f"document {where}", reason=reason)]
    else:
        unit_ids = aliases(units)
        result.verdicts = ignorable_verdicts(parsed, unit_ids)
        origin = Origin(context.run_id, context.clock, context.minter, document.corpus_id, where)
        result.elements, result.skipped = build_records(parsed, unit_ids, result.verdicts, origin)
    result.input_tokens, result.output_tokens = caller.input_tokens, caller.output_tokens
    return result
