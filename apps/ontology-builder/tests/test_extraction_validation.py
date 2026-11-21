"""Pass 1 output handling: validation, one retry, dropped and reported items (T8, edge cases).

These tests drive extraction with a scripted client, so each case states exactly what the LLM
returns. The pet-manual fixtures are tested in ``test_extraction_pets.py``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest
from ontology_builder.extraction import ExtractionContext, extract_document, pass1_requests
from ontology_builder.llm import LlmOutputError, LlmRequest, LlmResponse
from ontology_builder.model import (
    Concept,
    Document,
    FixedClock,
    Property,
    Relation,
    Rule,
    ScopeRecord,
    SourceUnit,
    Statement,
    Term,
    UlidMinter,
    validate_record,
)

AT = datetime(2026, 11, 21, 10, 0, tzinfo=UTC)
RUN = "run_01JDK7F3Q8ZX5N6M2W4R9T0BCD"
DOC = "doc_01JDK7F3Q8ZX5N6M2W4R9T0BCD"
CORPUS = "co_01JDK7F3Q8ZX5N6M2W4R9T0BCD"
U1 = "su_01JDK7F3Q8ZX5N6M2W4R9T0BC1"
U2 = "su_01JDK7F3Q8ZX5N6M2W4R9T0BC2"
U3 = "su_01JDK7F3Q8ZX5N6M2W4R9T0BC3"
HASH = "sha256:" + "b" * 64
TEXTS = {
    U1: "Rex, my first dog, loved the park.",
    U2: "A dog lives 10 to 15 years.",
    U3: "Dogs must be kept on a lead of at most 2 metres in the stairwell.",
}

Reply = dict[str, Any] | Exception


class ScriptedClient:
    """Returns the scripted replies of call A and call B in order, and keeps every request.

    A request is call B when its output format is ``RulesOutput`` (ontology-builder/ADR-0007).
    """

    def __init__(self, a: list[Reply], b: list[Reply]) -> None:
        self.replies = {"a": list(a), "b": list(b)}
        self.requests: dict[str, list[LlmRequest]] = {"a": [], "b": []}

    @property
    def model(self) -> str:
        return "claude-test"

    def complete(self, request: LlmRequest) -> LlmResponse:
        call = "b" if request.schema.get("title") == "RulesOutput" else "a"
        self.requests[call].append(request)
        reply = self.replies[call].pop(0)
        if isinstance(reply, Exception):
            raise reply
        return LlmResponse(data=reply, input_tokens=100, output_tokens=50, model="claude-test")

    def count_tokens(self, request: LlmRequest) -> int:
        return 1


def _units() -> list[SourceUnit]:
    return [
        validate_record(
            SourceUnit,
            {
                "id": uid,
                "document_id": DOC,
                "kind": "paragraph",
                "location": {"path": "dogs.md", "heading_path": ["Dogs"], "index_in_section": i},
                "content_hash": HASH,
                "text": text,
            },
        )
        for i, (uid, text) in enumerate(TEXTS.items())
    ]


def _document() -> Document:
    return validate_record(
        Document,
        {"id": DOC, "corpus_id": CORPUS, "path": "dogs.md", "title": "Dogs", "content_hash": HASH},
    )


def _context(scope_record: dict[str, Any]) -> ExtractionContext:
    return ExtractionContext(
        scope=validate_record(ScopeRecord, scope_record),
        run_id=RUN,
        clock=FixedClock(AT),
        minter=UlidMinter(FixedClock(AT)),
    )


def _candidate(key: str, label: str, *evidence: str) -> dict[str, Any]:
    return {
        "key": key,
        "label": label,
        "evidence": list(evidence),
        "level": "level-1",
        "level_reason": "core",
    }


def _verdicts() -> list[dict[str, Any]]:
    return [
        {
            "unit": "U1",
            "ignorable": True,
            "category": "instance_or_anecdote",
            "reason": "one dog",
        },
        {"unit": "U2", "ignorable": False},
        {"unit": "U3", "ignorable": False},
    ]


def _full_output() -> dict[str, Any]:
    return {
        "unit_verdicts": _verdicts(),
        "statements": [
            _candidate("s.life", "dog lifespan", "U2") | {"text": "A dog lives 10 to 15 years."}
        ],
        "terms": [
            _candidate("t.lead", "lead", "U3") | {"mentions": [{"unit": "U3", "concept": "c.lead"}]}
        ],
        "concepts": [
            _candidate("c.dog", "dog", "U2", "U3"),
            _candidate("c.lead", "lead", "U3") | {"definition": "A rope to lead a dog."},
            _candidate("c.stair", "stairwell", "U3"),
        ],
        "relations": [
            _candidate("r.on", "is kept on", "U3")
            | {"subject": "c.dog", "object": "c.lead", "cardinality": {"max": 1}}
        ],
        "rules": [
            _candidate("u.lead", "dog on a lead in the stairwell", "U3")
            | {
                "modality": "must",
                "actor": "dog owner",
                "action": "keep the dog on a lead",
                "condition": "in the stairwell",
                "limit": {"comparator": "le", "value": 2, "unit": "m"},
                "cardinality": {"relation": "r.on", "max": 1},
                "refers_to": ["c.dog", "c.lead", "c.stair"],
            }
        ],
        "properties": [
            _candidate("p.life", "lifespan", "U2")
            | {"of": "c.dog", "name": "lifespan", "value": "10-15", "unit": "years"}
        ],
    }


def _split(reply: Reply) -> tuple[Reply, dict[str, Any]]:
    """A full answer as the answers of call A and call B."""
    if not isinstance(reply, dict):
        return reply, {}
    a = {k: v for k, v in reply.items() if k not in {"rules", "properties"}}
    return a, {k: v for k, v in reply.items() if k in {"rules", "properties"}}


def _run(
    scope_record: dict[str, Any], *replies: Reply, rules: list[Reply] | None = None
) -> tuple[Any, ScriptedClient]:
    """Run pass 1 on the scripted replies of call A. Call B answers ``rules`` or, by default, the
    rules and properties of the first full reply of call A."""
    a_replies: list[Reply] = []
    b_replies: list[Reply] = list(rules or [])
    for reply in replies:
        a, b = _split(reply)
        a_replies.append(a)
        if b and rules is None and not b_replies:
            b_replies.append(b)
    client = ScriptedClient(a_replies, b_replies or [{}])
    result = extract_document(client, _document(), _units(), _context(scope_record))
    return result, client


def _by_label(elements: list[Any]) -> dict[str, Any]:
    return {element.label: element for element in elements}


def test_prompt_shows_units_by_alias_with_scope(scope_record: dict[str, Any]) -> None:
    scope = validate_record(ScopeRecord, scope_record)
    for request in pass1_requests(_document(), _units(), scope):
        assert "[U1]" in request.prompt and "[U3]" in request.prompt
        assert TEXTS[U3] in request.prompt
        assert "su_" not in request.prompt
        assert scope_record["purpose"] in request.system
        assert scope_record["level_guidance"]["level_1"] in request.system
        assert request.schema["type"] == "object"
    a, b = pass1_requests(_document(), _units(), scope)
    assert set(a.schema["properties"]) == {
        "unit_verdicts",
        "statements",
        "terms",
        "concepts",
        "relations",
    }
    assert set(b.schema["properties"]) == {"rules", "properties"}
    assert a.system == b.system


def test_call_b_lists_the_keys_of_call_a_and_the_ignorable_units(
    scope_record: dict[str, Any],
) -> None:
    _, client = _run(scope_record, _full_output())
    [b] = client.requests["b"]
    assert "- concept c.dog: dog" in b.prompt
    assert "- relation r.on: is kept on" in b.prompt
    assert "- term t.lead: lead" in b.prompt
    assert "Ignorable units: U1" in b.prompt


def test_valid_output_becomes_proposed_records_with_real_ids(
    scope_record: dict[str, Any],
) -> None:
    result, client = _run(scope_record, _full_output())
    assert (len(client.requests["a"]), len(client.requests["b"])) == (1, 1)
    assert result.skipped == []
    assert (result.input_tokens, result.output_tokens) == (200, 100)
    types = {type(element) for element in result.elements}
    assert types == {Statement, Term, Concept, Relation, Rule, Property}
    for element in result.elements:
        assert element.status == "proposed"
        assert element.origin.kind == "llm" and element.origin.run_id == RUN
        assert element.origin.created_at == AT
        assert {e.unit for e in element.evidence} <= {U2, U3}
    named = _by_label(result.elements)
    dog, lead = named["dog"], named["lead"]
    assert [e.unit for e in dog.evidence] == [U2, U3]
    rule = named["dog on a lead in the stairwell"]
    assert rule.limit.value == 2.0 and rule.limit.unit == "m"
    assert set(rule.refers_to) == {dog.id, lead.id, named["stairwell"].id}
    assert rule.cardinality.relation == named["is kept on"].id
    assert rule.scope == [CORPUS]
    relation = named["is kept on"]
    assert (relation.subject, relation.predicate_label) == (dog.id, "is kept on")
    [term] = [e for e in result.elements if isinstance(e, Term)]
    assert term.mentions is not None
    assert term.mentions[0].unit == U3
    assert term.mentions[0].concept in {c.id for c in result.elements if isinstance(c, Concept)}
    assert named["lifespan"].of == dog.id


def test_ignorable_verdicts_are_kept_per_unit(scope_record: dict[str, Any]) -> None:
    result, _ = _run(scope_record, _full_output())
    assert set(result.verdicts) == {U1}
    verdict = result.verdicts[U1]
    assert verdict.proposed is True
    assert (verdict.category, verdict.status) == ("instance_or_anecdote", "proposed")


def test_ignorable_unit_is_never_evidence(scope_record: dict[str, Any]) -> None:
    output = _full_output()
    output["properties"][0]["evidence"] = ["U2", "U1"]
    output["concepts"].append(_candidate("c.rex", "Rex", "U1"))
    result, _ = _run(scope_record, output)
    named = _by_label(result.elements)
    assert [e.unit for e in named["lifespan"].evidence] == [U2]
    assert "Rex" not in named
    assert any("ignorable" in s.reason and "Rex" in s.item for s in result.skipped)


def test_unknown_unit_alias_drops_item_without_retry(scope_record: dict[str, Any]) -> None:
    output = _full_output()
    output["concepts"].append(_candidate("c.cat", "cat", "U9"))
    result, client = _run(scope_record, output)
    assert len(client.requests["a"]) == 1
    assert "cat" not in _by_label(result.elements)
    [skipped] = result.skipped
    assert "U9" in skipped.reason and "cat" in skipped.item and skipped.where == "dogs.md"


def test_dangling_reference_is_dropped_and_cascades(scope_record: dict[str, Any]) -> None:
    output = _full_output()
    output["concepts"] = [c for c in output["concepts"] if c["key"] != "c.lead"]
    output["terms"] = []
    result, _ = _run(scope_record, output)
    named = _by_label(result.elements)
    assert "is kept on" not in named
    assert "dog on a lead in the stairwell" not in named
    reasons = " ".join(s.reason for s in result.skipped)
    assert "c.lead" in reasons and "r.on" in reasons


def test_invalid_item_retried_once_and_fixed(scope_record: dict[str, Any]) -> None:
    output = _full_output()
    output["concepts"][2]["level"] = "important"
    fixed = {"unit_verdicts": [], "concepts": [_candidate("c.stair", "stairwell", "U3")]}
    result, client = _run(scope_record, output, fixed)
    assert len(client.requests["a"]) == 2
    retry = client.requests["a"][1]
    assert "important" in retry.prompt and "c.stair" in retry.prompt
    assert retry.schema == client.requests["a"][0].schema
    assert result.skipped == []
    assert "stairwell" in _by_label(result.elements)
    assert (result.input_tokens, result.output_tokens) == (300, 150)


def test_invalid_item_still_invalid_after_retry_is_reported(
    scope_record: dict[str, Any],
) -> None:
    output = _full_output()
    output["concepts"][2]["level"] = "important"
    still = {"unit_verdicts": [], "concepts": [output["concepts"][2]]}
    result, client = _run(scope_record, output, still)
    assert len(client.requests["a"]) == 2
    named = _by_label(result.elements)
    assert "stairwell" not in named
    assert "dog on a lead in the stairwell" not in named  # it referred to c.stair
    assert any("level" in s.reason and "stairwell" in s.item for s in result.skipped)


def test_verdict_without_category_is_invalid(scope_record: dict[str, Any]) -> None:
    output = _full_output()
    del output["unit_verdicts"][0]["category"]
    fixed = {"unit_verdicts": _verdicts()[:1]}
    result, client = _run(scope_record, output, fixed)
    assert len(client.requests["a"]) == 2
    assert "category" in client.requests["a"][1].prompt
    assert result.verdicts[U1].category == "instance_or_anecdote"


def test_unusable_output_is_retried_once(scope_record: dict[str, Any]) -> None:
    result, client = _run(scope_record, LlmOutputError("not JSON"), _full_output())
    assert len(client.requests["a"]) == 2
    assert "not JSON" in client.requests["a"][1].prompt
    assert len(result.elements) == 8


def test_unusable_twice_reports_the_document(scope_record: dict[str, Any]) -> None:
    result, client = _run(scope_record, {"statements": []}, LlmOutputError("cut off"))
    assert len(client.requests["a"]) == 2
    assert client.requests["b"] == []  # no call B without a usable call A
    assert result.elements == [] and result.verdicts == {}
    [skipped] = result.skipped
    assert skipped.where == "dogs.md" and "cut off" in skipped.reason


def test_duplicate_key_in_retry_is_skipped(scope_record: dict[str, Any]) -> None:
    output = _full_output()
    output["concepts"][2]["level"] = "important"
    fixed = {
        "unit_verdicts": [],
        "concepts": [_candidate("c.stair", "stairwell", "U3"), _candidate("c.dog", "dog 2", "U2")],
    }
    result, _ = _run(scope_record, output, fixed)
    named = _by_label(result.elements)
    assert "dog 2" not in named and "stairwell" in named
    assert any("duplicate key c.dog" in s.reason for s in result.skipped)


@pytest.mark.parametrize("field", ["evidence", "level_reason"])
def test_required_candidate_fields(scope_record: dict[str, Any], field: str) -> None:
    output = _full_output()
    del output["statements"][0][field]
    result, _ = _run(scope_record, output, {"unit_verdicts": []})
    assert "dog lifespan" not in _by_label(result.elements)
    assert any(field in s.reason for s in result.skipped)


# ---------- call B (rules and properties; ontology-builder/ADR-0007) ----------


def _rules_part() -> dict[str, Any]:
    return _split(_full_output())[1]


def test_call_b_unusable_twice_keeps_call_a(scope_record: dict[str, Any]) -> None:
    failures: list[Reply] = [LlmOutputError("not JSON"), LlmOutputError("cut off")]
    result, client = _run(scope_record, _full_output(), rules=failures)
    assert len(client.requests["b"]) == 2
    named = _by_label(result.elements)
    assert {"dog", "lead", "is kept on", "dog lifespan"} <= set(named)
    assert not any(isinstance(e, Rule | Property) for e in result.elements)
    [skipped] = result.skipped
    assert skipped.item == "rules and properties of dogs.md" and "cut off" in skipped.reason


def test_call_b_invalid_rule_is_retried_within_call_b(scope_record: dict[str, Any]) -> None:
    broken = _rules_part()
    broken["rules"][0]["modality"] = "should"
    fixed = {"rules": [_rules_part()["rules"][0]]}
    result, client = _run(scope_record, _full_output(), rules=[broken, fixed])
    assert (len(client.requests["a"]), len(client.requests["b"])) == (1, 2)
    retry = client.requests["b"][1]
    assert "should" in retry.prompt and retry.schema["title"] == "RulesOutput"
    assert result.skipped == []
    assert "dog on a lead in the stairwell" in _by_label(result.elements)


def test_call_b_reusing_a_key_of_call_a_is_skipped(scope_record: dict[str, Any]) -> None:
    part = _rules_part()
    part["properties"][0]["key"] = "c.dog"
    result, _ = _run(scope_record, _full_output(), rules=[part])
    assert "lifespan" not in _by_label(result.elements)
    assert any("duplicate key c.dog" in s.reason for s in result.skipped)


def test_no_call_b_when_every_unit_is_ignorable(scope_record: dict[str, Any]) -> None:
    verdict = {"ignorable": True, "category": "instance_or_anecdote", "reason": "a story"}
    only_stories = {"unit_verdicts": [{"unit": f"U{n}"} | verdict for n in (1, 2, 3)]}
    result, client = _run(scope_record, only_stories, rules=[])
    assert client.requests["b"] == []
    assert result.elements == [] and set(result.verdicts) == {U1, U2, U3}


def test_unit_marked_not_ignorable_is_kept_and_named_in_the_prompt(
    scope_record: dict[str, Any],
) -> None:
    """On-demand extraction (FR-14): a unit a person marked not ignorable stays evidence, even when
    the LLM proposes it ignorable again, and the prompt tells the LLM so."""
    context = _context(scope_record)
    context = ExtractionContext(
        context.scope, context.run_id, context.clock, context.minter, not_ignorable={U1}
    )
    a, b = _split(_full_output())
    assert isinstance(a, dict)
    a["concepts"] = [*a["concepts"], _candidate("c.rex", "first dog", "U1")]
    client = ScriptedClient([a], [b])
    result = extract_document(client, _document(), _units(), context)
    assert result.verdicts == {}
    assert "first dog" in _by_label(result.elements)
    [request] = client.requests["a"]
    assert "marked these units as not ignorable: U1." in request.prompt
    plain = pass1_requests(_document(), _units(), context.scope)[0]
    assert "not ignorable:" not in plain.prompt, "the usual prompt (and its fixtures) is unchanged"
    kept = pass1_requests(_document(), _units(), context.scope, not_ignorable={U1})[0]
    assert kept.prompt == request.prompt, "the estimate counts the prompt that is sent"
