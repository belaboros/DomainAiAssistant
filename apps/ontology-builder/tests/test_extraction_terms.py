"""Pass 2, term resolution: synonym groups and sense splits (T9: AC-11, FR-11, FR-12).

The pet test replays the curated fixture of pass 2 on top of the replayed pass 1. The other tests
drive ``resolve_terms`` with a scripted client, so each case states exactly what the LLM returns.
"""

from __future__ import annotations

from typing import Any

import pytest
from ontology_builder.extraction import TermInput, resolve_terms, terms_request
from ontology_builder.llm import LlmOutputError, LlmRequest, LlmResponse
from ontology_builder.model import (
    Concept,
    Element,
    Relation,
    Rule,
    SourceUnit,
    Term,
    validate_element,
    validate_record,
)

AT = "2026-11-21T10:00:00Z"
RUN = "run_01JDK7F3Q8ZX5N6M2W4R9T0BCD"
HASH = "sha256:" + "c" * 64


def _ulid(n: int) -> str:
    return f"01JDK7F3Q8ZX5N6M2W4R9T0{n:03d}"


def _id(prefix: str, n: int) -> str:
    return f"{prefix}_{_ulid(n)}"


U = {n: _id("su", n) for n in range(1, 6)}
TEXTS = {
    1: "Choose a sturdy leash for your dog.",  # dog manual, leash
    2: "Keep the leash short near roads.",  # dog manual, leash
    3: "Be a calm and consistent lead for your dog.",  # dog manual, lead = the owner's role
    4: "A dog must be on a lead of at most 2 m in the stairwell.",  # building rules, lead = leash
    5: "Every dog in the complex is registered.",
}
PATHS = {1: "dog/05.md", 2: "dog/05.md", 3: "dog/06.md", 4: "rules/04-pets/02-dogs.md", 5: "r.md"}


def _units() -> dict[str, SourceUnit]:
    return {
        U[n]: validate_record(
            SourceUnit,
            {
                "id": U[n],
                "document_id": _id("doc", n),
                "kind": "paragraph",
                "location": {"path": PATHS[n], "index_in_section": 0},
                "content_hash": HASH,
                "text": text,
            },
        )
        for n, text in TEXTS.items()
    }


def _common(label: str, *units: int) -> dict[str, Any]:
    return {
        "label": label,
        "level": "level-2",
        "level_reason": "everyday",
        "status": "proposed",
        "evidence": [{"unit": U[n]} for n in units],
        "origin": {"kind": "llm", "run_id": RUN, "created_at": AT},
    }


def _concept(n: int, label: str, *units: int, **extra: Any) -> Element:
    return validate_element("concept", _common(label, *units) | {"id": _id("cn", n)} | extra)


def _term(n: int, label: str, mentions: list[tuple[int, int]]) -> Element:
    data = _common(label, *[unit for unit, _ in mentions]) | {
        "id": _id("tm", n),
        "mentions": [{"unit": U[unit], "concept": _id("cn", c)} for unit, c in mentions],
    }
    return validate_element("term", data)


# Pass 1 found one "leash" concept per dog document, "lead (leader)" in dog 6 and "lead" in the
# building rules, and the 2 m rule refers to the rules' "lead".
DOG = _concept(1, "dog", 5)
LEASH_A = _concept(2, "leash", 1, level="level-3", level_reason="detail")
LEASH_B = _concept(3, "leash", 2, level="level-1", level_reason="core", definition="A strap.")
LEADER = _concept(4, "lead (leader of the dog)", 3)
LEAD = _concept(5, "lead", 4, parents=[_id("cn", 3)])
TERMS = [
    _term(1, "leash", [(1, 2)]),
    _term(2, "Leash", [(2, 3)]),
    _term(3, "lead", [(3, 4), (4, 5)]),
]
RELATION = validate_element(
    "relation",
    _common("is kept on", 4)
    | {"id": _id("rl", 1), "subject": DOG.id, "object": LEAD.id, "predicate_label": "is kept on"},
)
RULE = validate_element(
    "rule",
    _common("lead at most 2 m", 4)
    | {
        "id": _id("ru", 1),
        "modality": "must",
        "actor": "dog owner",
        "action": "keep the dog on a lead",
        "limit": {"comparator": "le", "value": 2.0, "unit": "m"},
        "refers_to": [LEAD.id, DOG.id],
    },
)
ELEMENTS = [DOG, LEASH_A, LEASH_B, LEADER, LEAD, *TERMS, RELATION, RULE]
EXISTING_DOG = _concept(9, "dog", 5)

# The aliases follow the prompt: candidate concepts in element order, then the existing ones;
# units in the order the terms mention them.
C_DOG, C_LEASH_A, C_LEASH_B, C_LEADER, C_LEAD, C_EXISTING = "C1", "C2", "C3", "C4", "C5", "C6"


def _leash_group(**extra: Any) -> dict[str, Any]:
    return {
        "concept": C_LEASH_B,
        "preferred_label": "leash",
        "terms": ["leash", "lead"],
        "merge": [C_LEASH_A, C_LEAD],
    } | extra


def _lead_split() -> dict[str, Any]:
    return {
        "term": "lead",
        "senses": [
            {"concept": C_LEASH_B, "scope_note": "The rope or strap.", "mentions": ["U4"]},
            {"concept": C_LEADER, "scope_note": "The owner as leader.", "mentions": ["U3"]},
        ],
    }


def _answer() -> dict[str, Any]:
    return {"synonym_groups": [_leash_group()], "sense_splits": [_lead_split()]}


Reply = dict[str, Any] | Exception


class ScriptedClient:
    """Returns the scripted replies in order and keeps every request."""

    def __init__(self, *replies: Reply) -> None:
        self.replies = list(replies)
        self.requests: list[LlmRequest] = []

    @property
    def model(self) -> str:
        return "claude-test"

    def complete(self, request: LlmRequest) -> LlmResponse:
        self.requests.append(request)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return LlmResponse(data=reply, input_tokens=300, output_tokens=40, model="claude-test")

    def count_tokens(self, request: LlmRequest) -> int:
        return 1


def _input(existing: list[Element] | None = None) -> TermInput:
    concepts = [c for c in existing or [] if isinstance(c, Concept)]
    return TermInput(elements=ELEMENTS, units=_units(), existing=concepts)


def _run(*replies: Reply, existing: list[Element] | None = None) -> tuple[Any, ScriptedClient]:
    client = ScriptedClient(*replies)
    return resolve_terms(client, _input(existing)), client


def _get(result: Any, element_id: str) -> Any:
    [element] = [e for e in result.elements if e.id == element_id]
    return element


def _mentions(term: Any) -> list[tuple[str, str]]:
    return [(m.unit, m.concept) for m in term.mentions]


# ---------- the prompt ----------


def test_prompt_shows_concepts_terms_and_units_by_alias() -> None:
    request = terms_request(_input([EXISTING_DOG])).request
    prompt = request.prompt
    assert "[C2] leash" in prompt and "[C3] leash: A strap." in prompt
    assert "[C6] dog" in prompt and "already in the ontology" in prompt
    assert '"lead"' in prompt and "[U3]" in prompt and TEXTS[4] in prompt
    assert "dog/06.md" in prompt
    assert "su_" not in prompt and "cn_" not in prompt  # Q38: aliases only
    assert request.schema["title"] == "TermResolutionOutput"


def test_terms_with_one_label_are_shown_once() -> None:
    prompt = terms_request(_input()).request.prompt
    assert prompt.lower().count('- "leash"') == 1


# ---------- applying the answer ----------


def test_synonym_group_merges_concepts_and_rewires_references() -> None:
    result, client = _run(_answer())
    assert len(client.requests) == 1
    assert result.skipped == []
    assert (result.input_tokens, result.output_tokens) == (300, 40)
    ids = {e.id for e in result.elements}
    assert LEASH_A.id not in ids and LEAD.id not in ids
    assert result.merged == {LEASH_A.id: LEASH_B.id, LEAD.id: LEASH_B.id}
    leash = _get(result, LEASH_B.id)
    assert leash.label == "leash"
    assert [e.unit for e in leash.evidence] == [U[2], U[1], U[4]]
    assert (leash.level, leash.definition) == ("level-1", "A strap.")
    assert leash.parents in (None, [])  # LEAD's parent was LEASH_B itself
    assert _get(result, RELATION.id).object == LEASH_B.id
    assert _get(result, RULE.id).refers_to == [LEASH_B.id, DOG.id]


def test_terms_with_one_label_become_one_term() -> None:
    result, _ = _run(_answer())
    terms = [e for e in result.elements if isinstance(e, Term)]
    assert sorted(t.label for t in terms) == ["lead", "leash"]
    leash = next(t for t in terms if t.label == "leash")
    assert leash.id == TERMS[0].id
    assert _mentions(leash) == [(U[1], LEASH_B.id), (U[2], LEASH_B.id)]


def test_sense_split_resolves_each_mention_and_writes_scope_notes() -> None:
    result, _ = _run(_answer())
    lead = next(e for e in result.elements if isinstance(e, Term) and e.label == "lead")
    assert _mentions(lead) == [(U[3], LEADER.id), (U[4], LEASH_B.id)]
    assert _get(result, LEADER.id).scope_note == "The owner as leader."
    assert _get(result, LEASH_B.id).scope_note == "The rope or strap."


def test_new_concept_merges_into_an_existing_concept() -> None:
    group = {"concept": C_EXISTING, "preferred_label": "dog", "terms": ["dog"], "merge": [C_DOG]}
    result, _ = _run({"synonym_groups": [group]}, existing=[EXISTING_DOG])
    ids = {e.id for e in result.elements}
    assert DOG.id not in ids and EXISTING_DOG.id not in ids  # the existing record is not touched
    assert result.merged == {DOG.id: EXISTING_DOG.id}
    assert _get(result, RELATION.id).subject == EXISTING_DOG.id
    assert [s.reason for s in result.skipped] == ["no term with the label 'dog'"]


def test_existing_concept_is_never_merged_away() -> None:
    group = {"concept": C_DOG, "preferred_label": "dog", "terms": ["leash"], "merge": [C_EXISTING]}
    result, _ = _run({"synonym_groups": [group]}, existing=[EXISTING_DOG])
    assert result.merged == {}
    assert len(result.skipped) == 1
    assert "already in the ontology" in result.skipped[0].reason


def test_unknown_aliases_are_reported_and_dropped() -> None:
    answer = {
        "synonym_groups": [_leash_group(concept="C99")],
        "sense_splits": [
            _lead_split() | {"senses": [*_lead_split()["senses"][:1], _sense("C4", "U77")]}
        ],
    }
    result, _ = _run(answer)
    assert result.merged == {}
    reasons = sorted(s.reason for s in result.skipped)
    assert reasons == ["cites unknown concept C99", "cites unknown unit U77"]
    assert {e.id for e in result.elements} == {e.id for e in ELEMENTS if e.id != TERMS[1].id}


def _sense(concept: str, *mentions: str) -> dict[str, Any]:
    return {"concept": concept, "scope_note": "a sense", "mentions": list(mentions)}


def test_invalid_item_is_retried_once_then_reported() -> None:
    broken = {"term": "lead", "senses": [_sense(C_LEADER, "U3")]}  # one sense only
    retry_fixed = {"sense_splits": [_lead_split()]}
    result, client = _run(
        {"synonym_groups": [_leash_group()], "sense_splits": [broken]}, retry_fixed
    )
    assert len(client.requests) == 2
    assert "invalid" in client.requests[1].prompt and '"lead"' in client.requests[1].prompt
    assert result.skipped == []
    assert _get(result, LEADER.id).scope_note == "The owner as leader."

    still_broken = {"sense_splits": [broken]}
    result, client = _run({"sense_splits": [broken]}, still_broken)
    assert len(client.requests) == 2
    [skipped] = result.skipped
    assert skipped.reason.startswith("invalid after one retry")


def test_no_usable_answer_leaves_the_elements_unchanged_and_is_reported() -> None:
    result, client = _run(LlmOutputError("not JSON"), {"synonym_groups": "nope"})
    assert len(client.requests) == 2
    assert result.elements == ELEMENTS
    [skipped] = result.skipped
    assert skipped.where == "term resolution"
    assert "no usable answer" in skipped.reason


def test_nothing_to_resolve_makes_no_call() -> None:
    client = ScriptedClient()
    result = resolve_terms(client, TermInput(elements=[RULE], units=_units()))
    assert client.requests == []
    assert result.elements == [RULE]


# ---------- the pet manuals (AC-11, fixture) ----------


def _evidence_paths(pet_extraction: Any, element: Element) -> set[str]:
    return {pet_extraction.path_of(e.unit) for e in element.evidence}


@pytest.fixture(scope="session")
def pet_terms(pet_extraction: Any, pet_kit: Any) -> Any:
    return pet_kit.resolve(pet_kit.replay(), pet_extraction)


def test_leash_lead_synonym_and_lead_senses(pet_extraction: Any, pet_terms: Any) -> None:
    elements = {e.id: e for e in pet_terms.elements}
    terms = [e for e in elements.values() if isinstance(e, Term)]
    [lead] = [t for t in terms if t.label.lower() == "lead"]
    by_path = {pet_extraction.path_of(m.unit): m.concept for m in lead.mentions or []}
    leash = elements[by_path["04-pets/02-dogs.md"]]  # the building rules: lead = the leash
    role = elements[by_path["06-being-a-good-lead-for-your-dog.md"]]  # dog 6: the owner's role
    assert isinstance(leash, Concept) and isinstance(role, Concept) and leash.id != role.id
    leash_labels = {leash.label.lower()} | {
        t.label.lower() for t in terms if any(m.concept == leash.id for m in t.mentions or [])
    }
    assert {"leash", "lead"} <= leash_labels
    assert leash.scope_note and role.scope_note
    role_labels = {role.label.lower()} | {
        t.label.lower() for t in terms if any(m.concept == role.id for m in t.mentions or [])
    }
    assert "leash" not in role_labels  # the owner's role is a sense of "lead", not a leash
    rules = [
        e
        for e in elements.values()
        if isinstance(e, Rule) and e.limit is not None and e.limit.unit == "m"
    ]
    assert any(leash.id in (rule.refers_to or []) for rule in rules)
    assert all(role.id not in (rule.refers_to or []) for rule in rules)


def test_pet_resolution_merges_duplicates_and_keeps_references(pet_terms: Any) -> None:
    assert pet_terms.skipped == []
    ids = {e.id for e in pet_terms.elements}
    assert pet_terms.merged and not set(pet_terms.merged) & ids
    assert set(pet_terms.merged.values()) <= ids
    concepts = [e for e in pet_terms.elements if isinstance(e, Concept)]
    leashes = [c for c in concepts if c.label.lower() == "leash"]
    assert len(leashes) == 1
    for element in pet_terms.elements:
        if isinstance(element, Relation):
            assert {element.subject, element.object} <= ids
        if isinstance(element, Term):
            assert {m.concept for m in element.mentions or []} <= ids
