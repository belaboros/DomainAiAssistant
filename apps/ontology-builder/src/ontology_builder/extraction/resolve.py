"""Turn valid candidates into proposed element records (FR-9, FR-10, FR-13, FR-14).

1. Aliases go back to ``su_`` IDs. A candidate that cites an alias not in the prompt is dropped.
2. Evidence from ignorable units is removed; a candidate left without evidence is dropped.
3. A candidate that refers to a key no longer present is dropped, until nothing changes.
4. Every remaining key gets a minted ID, and each record is validated as it is built.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from ontology_builder.extraction.parse import CANDIDATE_LISTS, Parsed, skip
from ontology_builder.model import (
    Candidate,
    CandidateConcept,
    CandidateProperty,
    CandidateRelation,
    CandidateRule,
    CandidateStatement,
    CandidateTerm,
    Clock,
    Element,
    IgnorableStatus,
    IgnorableVerdict,
    SkippedItem,
    UlidMinter,
    validate_element,
)

_ELEMENT_TYPE = {
    "statements": "statement",
    "terms": "term",
    "concepts": "concept",
    "relations": "relation",
    "rules": "rule",
    "properties": "property",
}


@dataclass(frozen=True)
class Origin:
    """Where the records come from: the run, the clock and the minter, and the document."""

    run_id: str
    clock: Clock
    minter: UlidMinter
    corpus_id: str
    where: str


@dataclass
class _Kept:
    list_name: str
    candidate: Candidate
    evidence: list[str]


def ignorable_verdicts(parsed: Parsed, aliases: Mapping[str, str]) -> dict[str, IgnorableVerdict]:
    """The proposed-ignorable units by ID; verdicts on unknown aliases are ignored."""
    return {
        aliases[alias]: IgnorableVerdict(
            proposed=True,
            category=verdict.category,
            reason=verdict.reason or "",
            status=IgnorableStatus.proposed,
        )
        for alias, verdict in parsed.verdicts.items()
        if verdict.ignorable and verdict.category is not None and alias in aliases
    }


def _cited_units(candidate: Candidate) -> list[str]:
    cited = list(candidate.evidence)
    if isinstance(candidate, CandidateTerm):
        cited += [mention.unit for mention in candidate.mentions or []]
    return cited


def _check_evidence(item: _Kept, aliases: Mapping[str, str], ignorable: set[str]) -> str | None:
    """Map the evidence of one candidate to IDs; return why it is dropped, if it is."""
    unknown = sorted({a for a in _cited_units(item.candidate) if a not in aliases})
    if unknown:
        return f"cites unknown unit {', '.join(unknown)}"
    evidence = [aliases[a] for a in dict.fromkeys(item.candidate.evidence)]
    item.evidence = [unit for unit in evidence if unit not in ignorable]
    if not item.evidence:
        return "cites only ignorable units"
    return None


def _rule_references(candidate: CandidateRule) -> list[str]:
    cardinality = [candidate.cardinality.relation] if candidate.cardinality else []
    return list(candidate.refers_to or []) + cardinality


_REFERENCES: dict[type[Candidate], Callable[[Any], Iterable[str]]] = {
    CandidateConcept: lambda c: c.parents or [],
    CandidateTerm: lambda c: [mention.concept for mention in c.mentions or []],
    CandidateRelation: lambda c: [c.subject, c.object],
    CandidateRule: _rule_references,
    CandidateProperty: lambda c: [c.of],
}


def _references(candidate: Candidate) -> Iterable[str]:
    """The keys of the other candidates this candidate refers to."""
    refers = _REFERENCES.get(type(candidate))
    return refers(candidate) if refers else []


def _drop_dangling(kept: list[_Kept], skipped: list[SkippedItem], where: str) -> list[_Kept]:
    """Drop candidates that refer to missing keys, repeating until nothing more is dropped."""
    changed = True
    while changed:
        changed = False
        keys = {item.candidate.key for item in kept}
        survivors = []
        for item in kept:
            missing = sorted(set(_references(item.candidate)) - keys)
            if missing:
                reason = f"refers to missing {', '.join(missing)}"
                skipped.append(skip(where, item.list_name, item.candidate, reason))
                keys.discard(item.candidate.key)
                changed = True
            else:
                survivors.append(item)
        kept = survivors
    return kept


def _specific(candidate: Candidate, ids: Mapping[str, str], origin: Origin) -> dict[str, Any]:
    """The type-specific slots of a record, with keys replaced by minted IDs."""
    if isinstance(candidate, CandidateStatement):
        return {"text": candidate.text}
    if isinstance(candidate, CandidateConcept):
        parents = [ids[key] for key in candidate.parents or []]
        return {"definition": candidate.definition, "parents": parents}
    if isinstance(candidate, CandidateRelation):
        cardinality = candidate.cardinality.model_dump() if candidate.cardinality else None
        return {
            "subject": ids[candidate.subject],
            "object": ids[candidate.object],
            "predicate_label": candidate.label,
            "cardinality": cardinality,
        }
    if isinstance(candidate, CandidateRule):
        return _rule(candidate, ids, origin)
    if isinstance(candidate, CandidateProperty):
        return {
            "of": ids[candidate.of],
            "name": candidate.name,
            "value": candidate.value,
            "unit": candidate.unit,
        }
    return {}


def _rule(candidate: CandidateRule, ids: Mapping[str, str], origin: Origin) -> dict[str, Any]:
    cardinality = None
    if candidate.cardinality is not None:
        cardinality = candidate.cardinality.model_dump() | {
            "relation": ids[candidate.cardinality.relation]
        }
    return {
        "modality": candidate.modality,
        "actor": candidate.actor,
        "action": candidate.action,
        "condition": candidate.condition,
        "limit": candidate.limit.model_dump() if candidate.limit else None,
        "cardinality": cardinality,
        "scope": [origin.corpus_id],
        "refers_to": [ids[key] for key in candidate.refers_to or []],
    }


@dataclass(frozen=True)
class _Units:
    aliases: Mapping[str, str]
    ignorable: set[str]


def _mentions(
    candidate: CandidateTerm, ids: Mapping[str, str], units: _Units
) -> list[dict[str, str]]:
    mentions = [
        {"unit": units.aliases[mention.unit], "concept": ids[mention.concept]}
        for mention in candidate.mentions or []
    ]
    return [mention for mention in mentions if mention["unit"] not in units.ignorable]


def _record(item: _Kept, ids: Mapping[str, str], units: _Units, origin: Origin) -> Element:
    candidate = item.candidate
    data: dict[str, Any] = {
        "id": ids[candidate.key],
        "label": candidate.label,
        "level": candidate.level,
        "level_reason": candidate.level_reason,
        "status": "proposed",
        "evidence": [{"unit": unit} for unit in item.evidence],
        "origin": {"kind": "llm", "run_id": origin.run_id, "created_at": origin.clock.now()},
    } | _specific(candidate, ids, origin)
    if isinstance(candidate, CandidateTerm):
        data["mentions"] = _mentions(candidate, ids, units)
    clean = {name: value for name, value in data.items() if value is not None}
    return validate_element(_ELEMENT_TYPE[item.list_name], clean)


def build_records(
    parsed: Parsed,
    aliases: Mapping[str, str],
    verdicts: Mapping[str, IgnorableVerdict],
    origin: Origin,
) -> tuple[list[Element], list[SkippedItem]]:
    """The proposed records of the valid candidates, and the candidates dropped on the way."""
    units = _Units(aliases, set(verdicts))
    skipped = list(parsed.skipped)
    kept: list[_Kept] = []
    for name in CANDIDATE_LISTS:
        for candidate in parsed.candidates[name]:
            item = _Kept(name, candidate, [])
            reason = _check_evidence(item, aliases, units.ignorable)
            if reason is None:
                kept.append(item)
            else:
                skipped.append(skip(origin.where, name, candidate, reason))
    kept = _drop_dangling(kept, skipped, origin.where)
    ids = {item.candidate.key: origin.minter.new(_ELEMENT_TYPE[item.list_name]) for item in kept}
    return [_record(item, ids, units, origin) for item in kept], skipped
