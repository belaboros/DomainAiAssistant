"""The pass 2 prompt: every candidate term with its mentions, and the concepts (plan 0002).

Concepts are shown as ``[C<n>]`` and units as ``[U<n>]``, aliases unique in the prompt (Q38);
``TermPrompt`` keeps the maps back to the ``cn_`` and ``su_`` IDs. New concepts come first, in
element order, then the concepts already in the ontology. Terms with the same label (ignoring
case) are shown once, with all their mentions. The answer is JSON in the schema of
``TermResolutionOutput`` (ADR-0006).
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from ontology_builder.llm import LlmRequest
from ontology_builder.model import Concept, Element, SourceUnit, Term, TermResolutionOutput
from ontology_builder.model import tool_input_schema as output_schema

PASS2_MAX_TOKENS = 32_000
"""Output cap of the pass 2 call; it lists groups and splits, not whole records."""

_SYSTEM = """\
You resolve the terms of a domain ontology after its documents were read one by one.

Each document gave its own concepts and the terms (words) that name them, so the same thing may \
appear as several concepts, and one word may name different things in different documents.

# Synonym groups
Give one synonym group for every concept that is named by more than one term or found in more \
than one document:
- concept: the alias of the concept to keep. Prefer a concept already in the ontology.
- preferred_label: the label a glossary would use, singular.
- terms: the labels of every term that names this concept.
- merge: the aliases of the other new concepts that are the same thing; they are merged into \
concept. Never list a concept already in the ontology here.
Only group what the text shows to be the same thing. A broader or narrower concept (a puppy is a \
dog) is not a synonym.

# Sense splits
When one term names different things in different units (a homonym), give a sense split:
- term: the term label.
- senses: at least two; each has the alias of the concept the term names there, a short \
scope_note that tells this sense apart from the others, and the aliases (U1, U2, ...) of the \
units where the term has this sense.

Cite concepts and units only by the aliases shown. Leave out every concept and term that needs \
no change.
"""


@dataclass(frozen=True)
class TermInput:
    """What pass 2 resolves: the new elements of a run and the concepts already in the ontology.

    ``existing_terms`` are not shown to the LLM; a run's term with one of their labels extends it.
    """

    elements: Sequence[Element]
    units: Mapping[str, SourceUnit]
    existing: Sequence[Concept] = ()
    existing_terms: Sequence[Term] = ()


@dataclass
class TermPrompt:
    """The pass 2 request and the aliases it shows."""

    request: LlmRequest
    concepts: dict[str, str] = field(default_factory=dict)
    """Concept alias (``C1``) to concept ID."""
    units: dict[str, str] = field(default_factory=dict)
    """Unit alias (``U1``) to unit ID."""


def label_key(label: str) -> str:
    """The form under which term labels count as the same."""
    return " ".join(label.casefold().split())


def terms_by_label(elements: Sequence[Element]) -> dict[str, list[Term]]:
    """The terms of a run grouped by label (ignoring case), in order of first appearance."""
    grouped: dict[str, list[Term]] = {}
    for element in elements:
        if isinstance(element, Term):
            grouped.setdefault(label_key(element.label), []).append(element)
    return grouped


def _where(found: TermInput, element: Element) -> str:
    paths = []
    for evidence in element.evidence:
        unit = found.units.get(evidence.unit)
        if unit is not None and unit.location is not None:
            paths.append(unit.location.path)
    return ", ".join(dict.fromkeys(paths))


def _concept_line(alias: str, concept: Concept, found: TermInput, existing: bool) -> str:
    text = f"[{alias}] {concept.label}"
    if concept.definition:
        text += f": {concept.definition}"
    where = "already in the ontology" if existing else _where(found, concept)
    return f"{text} ({where})" if where else text


def _concepts(found: TermInput, prompt: TermPrompt) -> list[str]:
    new = [e for e in found.elements if isinstance(e, Concept)]
    lines = []
    for number, concept in enumerate([*new, *found.existing], start=1):
        alias = f"C{number}"
        prompt.concepts[alias] = concept.id
        lines.append(_concept_line(alias, concept, found, number > len(new)))
    return lines


def _unit_alias(prompt: TermPrompt, unit_id: str) -> str:
    for alias, known in prompt.units.items():
        if known == unit_id:
            return alias
    alias = f"U{len(prompt.units) + 1}"
    prompt.units[alias] = unit_id
    return alias


def _mention_line(found: TermInput, prompt: TermPrompt, unit_id: str, concept_id: str) -> str:
    concept = {cid: alias for alias, cid in prompt.concepts.items()}.get(concept_id, "?")
    unit = found.units.get(unit_id)
    path = unit.location.path if unit is not None and unit.location else "?"
    text = " ".join(unit.text.split()) if unit is not None else ""
    return f"  [{_unit_alias(prompt, unit_id)}] {path} · names {concept}: {text}"


def _terms(found: TermInput, prompt: TermPrompt) -> list[str]:
    lines = []
    for terms in terms_by_label(found.elements).values():
        lines.append(f'- "{terms[0].label}"')
        mentions = [m for term in terms for m in term.mentions or []]
        lines += [_mention_line(found, prompt, m.unit, m.concept) for m in mentions]
        if not mentions:
            lines.append("  (no mentions)")
    return lines


def terms_request(found: TermInput) -> TermPrompt:
    """The pass 2 request for a run, with the aliases it uses."""
    prompt = TermPrompt(LlmRequest("", "", {}, PASS2_MAX_TOKENS))
    concepts = _concepts(found, prompt)
    terms = _terms(found, prompt)
    body = (
        "Concepts (alias, label: definition, where found):\n"
        + ("\n".join(concepts) or "(none)")
        + "\n\nTerms and their mentions (unit, document, the concept it names there, text):\n"
        + ("\n".join(terms) or "(none)")
        + "\n"
    )
    prompt.request = LlmRequest(
        system=_SYSTEM,
        prompt=body,
        schema=output_schema(TermResolutionOutput),
        max_tokens=PASS2_MAX_TOKENS,
    )
    return prompt


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
        "these items (a synonym group keeps its concept, a sense split its term); leave the "
        f"other items out:\n{listed}\n"
    )
    return LlmRequest(request.system, request.prompt + note, request.schema, request.max_tokens)
