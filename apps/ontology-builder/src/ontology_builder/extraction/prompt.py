"""The pass 1 prompt: scope record, level rubric and one document's units by alias (plan 0002).

Each unit is shown as ``[U<n>]`` (Q38); ``aliases`` gives the map back to the ``su_`` IDs. The
system prompt depends only on the scope record, so it is the same for every document of an
ontology. Pass 1 is two calls per document (ontology-builder/ADR-0007): ``concepts_request``
(call A, ``ConceptsOutput``) and ``rules_request`` (call B, ``RulesOutput``), each answered as JSON
in the schema of its output class (ADR-0006).
"""

from __future__ import annotations

import json
from collections.abc import Collection, Sequence
from dataclasses import dataclass
from typing import Any

from ontology_builder.llm import LlmRequest
from ontology_builder.model import (
    ConceptsOutput,
    Document,
    RulesOutput,
    ScopeRecord,
    SourceUnit,
)
from ontology_builder.model import tool_input_schema as output_schema

PASS1_MAX_TOKENS = 16_000
"""Output cap of one pass 1 call; one document's candidates stay far below it."""

_CALL_A = (
    "\nGive the unit verdicts and the statements, terms, concepts and relations now. Rules and "
    "properties are asked for in a second step, which can refer to your keys.\n"
)
_CALL_B = (
    "\nThe first step gave the verdicts and the candidates below. Now give only the rules and "
    "properties of this document. Refer to these candidates by key, or to keys of other rules and "
    "properties you define now; leave every other list out.\n"
)

_SYSTEM = """\
You extract the building blocks of a domain ontology from one document of a manual.

# The ontology
Name: {name}
Purpose: {purpose}
Intended readers: {readers}

# Levels
Propose a level for every candidate, with a short reason:
- level-1: the core concepts, actors, processes, relations and rules that show what the domain \
is about, quick to grasp without prior knowledge. Here: {level_1}
- level-2: what someone taking part in the domain needs for the normal, happy-path case. \
Here: {level_2}
- level-3: detail for special cases and error scenarios. Here: {level_3}
- ignorable: not knowledge about the domain.

# Step 1: one verdict per source unit
Give every unit a verdict. A unit is ignorable when it holds no general knowledge about the \
domain. Categories:
- instance_or_anecdote: about one particular person, animal or event (names, places, memories).
- generic_or_historical_story: background or history that says nothing about the domain today.
- quote_or_motivational: quotes, slogans and value statements that create no obligation, actor \
or relation.
- procedure: step-by-step instructions or commands for one specific tool or task.
- other: anything else that is not domain knowledge (say why).
Examples of ignorable content in this ontology:
{ignorable_examples}
Judge each unit on its own: a unit next to an ignorable one may hold real content. Extract \
nothing from an ignorable unit and never cite it as evidence, even when it seems to confirm a \
fact stated elsewhere.

# Step 2: candidates from the other units
- statements: atomic claims, one fact each, in plain words (label: a short name; text: the claim).
- concepts: things, roles, places and events of the domain. Label: a singular noun phrase as in \
a glossary. definition: only when the text gives one. parents: keys of broader concepts the text \
states (a puppy is a dog).
- terms: the words the text uses to name concepts. Each term lists its mentions: the unit and the \
key of the concept the word names there. When one word names different things in different \
units, its mentions point to different concepts.
- relations: a link between two concepts (subject and object are concept keys); the label is the \
predicate ("is registered with"). Give a cardinality only when the text states a number.
- rules: who (actor) must, must_not or may do what (action), under which condition. A numeric \
limit becomes limit {{comparator: lt|le|eq|ge|gt, value, unit}}; "a lead of at most 2 m" is \
limit le 2 m. A limit on how many things one may have becomes a cardinality on a relation. \
refers_to: keys of the concepts and relations the rule is about.
- properties: a value of a concept or another candidate (of: its key), such as a lifespan of \
10 to 15 years: name, value, unit.

# Keys, evidence, faithfulness
- Every candidate has a key, unique in your answer, made of letters, digits and _ . : - \
(for example c.leash, r.lead-limit). Refer to other candidates only by keys defined in your answer.
- evidence lists the aliases (U1, U2, ...) of every unit the candidate comes from, exactly as \
shown. Never cite an ignorable unit.
- Stay close to the text: no abstractions, generalisations or facts it does not state.
"""


def system_prompt(scope: ScopeRecord) -> str:
    """The pass 1 system prompt for an ontology's scope record."""
    examples = "\n".join(f"- {example}" for example in scope.ignorable_examples)
    guidance = scope.level_guidance
    return _SYSTEM.format(
        name=scope.name,
        purpose=scope.purpose,
        readers=scope.readers,
        level_1=guidance.level_1,
        level_2=guidance.level_2,
        level_3=guidance.level_3,
        ignorable_examples=examples,
    )


def aliases(units: Sequence[SourceUnit]) -> dict[str, str]:
    """``U1``, ``U2``, ... in unit order, mapped to the units' IDs."""
    return {f"U{number}": unit.id for number, unit in enumerate(units, start=1)}


def _unit_block(alias: str, unit: SourceUnit) -> str:
    headings = " > ".join(unit.location.heading_path or []) if unit.location else ""
    where = f"{unit.kind} · {headings}" if headings else str(unit.kind)
    return f"[{alias}] {where}\n{unit.text}"


def document_prompt(document: Document, units: Sequence[SourceUnit]) -> str:
    """The user prompt: the document and its units, each under its alias."""
    blocks = [_unit_block(alias, unit) for alias, unit in zip(aliases(units), units, strict=True)]
    body = "\n\n".join(blocks) if blocks else "(this document has no source units)"
    return f"Document: {document.path}\nTitle: {document.title}\n\nSource units:\n\n{body}\n"


def _kept_note(units: Sequence[SourceUnit], not_ignorable: Collection[str]) -> str:
    """The note on units a person marked not ignorable (FR-14); empty when there are none."""
    kept = [alias for alias, uid in aliases(units).items() if uid in not_ignorable]
    if not kept:
        return ""
    return (
        f"A person has marked these units as not ignorable: {', '.join(kept)}. Give each of them "
        "the verdict not ignorable and extract from them like from any other unit.\n"
    )


def concepts_request(
    document: Document,
    units: Sequence[SourceUnit],
    scope: ScopeRecord,
    not_ignorable: Collection[str] = (),
) -> LlmRequest:
    """Pass 1, call A for one document: unit verdicts, statements, terms, concepts, relations.

    ``not_ignorable`` holds the IDs of units a person marked not ignorable (on-demand extraction).
    """
    return LlmRequest(
        system=system_prompt(scope),
        prompt=document_prompt(document, units) + _CALL_A + _kept_note(units, not_ignorable),
        schema=output_schema(ConceptsOutput),
        max_tokens=PASS1_MAX_TOKENS,
    )


@dataclass(frozen=True)
class Found:
    """A candidate of call A, as call B sees it."""

    kind: str
    key: str
    label: str


def rules_request(
    document: Document,
    units: Sequence[SourceUnit],
    scope: ScopeRecord,
    found: Sequence[Found],
    ignorable: Sequence[str],
) -> LlmRequest:
    """Pass 1, call B for one document: rules and properties that refer to ``found`` by key."""
    listed = "\n".join(f"- {f.kind} {f.key}: {f.label}" for f in found) or "- (none)"
    skipped = ", ".join(ignorable) or "none"
    context = f"\nCandidates (kind, key: label):\n{listed}\n\nIgnorable units: {skipped}\n"
    return LlmRequest(
        system=system_prompt(scope),
        prompt=document_prompt(document, units) + _CALL_B + context,
        schema=output_schema(RulesOutput),
        max_tokens=PASS1_MAX_TOKENS,
    )


def pass1_requests(
    document: Document,
    units: Sequence[SourceUnit],
    scope: ScopeRecord,
    not_ignorable: Collection[str] = (),
) -> list[LlmRequest]:
    """The two requests of one document as the cost estimate counts them (call B without the
    candidates of call A, which are not known yet)."""
    return [
        concepts_request(document, units, scope, not_ignorable),
        rules_request(document, units, scope, [], []),
    ]


def retry_unusable(request: LlmRequest, error: str) -> LlmRequest:
    """The one retry after an answer that could not be used at all."""
    note = (
        f"\n\nYour previous answer could not be used: {error}\n"
        "Answer again with the complete output in the required format."
    )
    return LlmRequest(request.system, request.prompt + note, request.schema, request.max_tokens)


def retry_invalid(request: LlmRequest, invalid: Sequence[dict[str, Any]]) -> LlmRequest:
    """The one retry for invalid items: only corrected versions of those items are asked for."""
    listed = json.dumps(list(invalid), indent=2, ensure_ascii=False, sort_keys=True)
    note = (
        "\n\nSome items of your previous answer are invalid. Return corrected versions of only "
        "these items, with the same keys, in the same format (unit_verdicts, where the format has "
        f"it, holds only corrected verdicts; leave other lists empty):\n{listed}\n"
    )
    return LlmRequest(request.system, request.prompt + note, request.schema, request.max_tokens)
