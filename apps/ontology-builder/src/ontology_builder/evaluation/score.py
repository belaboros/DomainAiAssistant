"""Score the findings of an ingestion against the answer key, one score per item (AC-33)."""

from __future__ import annotations

from dataclasses import dataclass

from ontology_builder.evaluation.answer_key import (
    AnswerKey,
    ConceptItem,
    Keywords,
    LeashLead,
    Passage,
    Place,
    RuleItem,
    Trap,
)
from ontology_builder.evaluation.findings import (
    Findings,
    Item,
    Unit,
    contains_all,
    normalise_label,
    read_findings,
)
from ontology_builder.store import DatasetFiles

SECTIONS = {
    "ignorable": "Ignorable passages",
    "kept": "Content kept next to them",
    "leash_lead": "Leash and lead: synonym and senses",
    "concepts": "Expected concepts",
    "rules": "Expected rules",
    "traps": "Traps",
}


@dataclass(frozen=True)
class Score:
    section: str
    item: str
    passed: bool
    detail: str


def _labels(items: list[Item], limit: int = 3) -> str:
    shown = ", ".join(f'"{item.label}"' for item in items[:limit])
    return shown + (f" and {len(items) - limit} more" if len(items) > limit else "")


def _units(key: AnswerKey, findings: Findings, place: Place) -> list[Unit]:
    corpus = key.corpora.get(place.corpus, place.corpus)
    return findings.find_units(corpus, place.document, place.contains)


def _ignorable(key: AnswerKey, findings: Findings, passage: Passage) -> Score:
    units = _units(key, findings, passage.place)
    if not units:
        return Score("ignorable", passage.id, False, "passage not found in the sources")
    unit = units[0]
    problems = []
    if not unit.ignorable:
        problems.append("not proposed ignorable")
    elif unit.category != passage.category:
        problems.append(f"category {unit.category}, expected {passage.category}")
    citing = findings.citing(unit.id)
    if citing:
        problems.append(f"cited by {_labels(citing)}")
    detail = "; ".join(problems) or f"ignorable as {unit.category}; cited by no element"
    return Score("ignorable", passage.id, not problems, detail)


def _kept(key: AnswerKey, findings: Findings, passage: Passage) -> Score:
    units = _units(key, findings, passage.place)
    if not units:
        return Score("kept", passage.id, False, "passage not found in the sources")
    unit = units[0]
    citing = findings.citing(unit.id)
    if unit.ignorable:
        return Score("kept", passage.id, False, f"proposed ignorable as {unit.category}")
    if not citing:
        return Score("kept", passage.id, False, "not ignorable, but no element cites it")
    return Score("kept", passage.id, True, f"cited by {_labels(citing)}")


def _concept(findings: Findings, item: ConceptItem) -> Score:
    wanted = {normalise_label(label) for label in item.labels}
    found = [c for c in findings.of_type("concept") if findings.labels(c.id) & wanted]
    if not found:
        return Score("concepts", item.id, False, "no concept with these labels")
    return Score("concepts", item.id, True, f"found as {_labels(found)}")


def _matching_rules(findings: Findings, groups: Keywords) -> list[Item]:
    return [rule for rule in findings.of_type("rule") if contains_all(rule.text, groups)]


def _rule(findings: Findings, item: RuleItem) -> Score:
    found = _matching_rules(findings, item.all)
    if not found:
        return Score("rules", item.id, False, "no matching rule")
    return Score("rules", item.id, True, f"found as {_labels(found)}")


def _named_by(key: AnswerKey, findings: Findings, term: str, place: Place) -> set[str]:
    """The concepts that mentions of ``term`` in the place's document point to."""
    units = {unit.id for unit in _units(key, findings, place)}
    wanted = normalise_label(term)
    return {
        concept
        for item in findings.of_type("term")
        if normalise_label(item.label) == wanted
        for unit, concept in item.mentions
        if unit in units and concept in findings.elements
    }


def _concept_labels(findings: Findings, concepts: set[str]) -> str:
    return ", ".join(sorted(f'"{findings.elements[c].label}"' for c in concepts)) or "none"


def _referring(rules: list[Item], concepts: set[str]) -> list[Item]:
    return [rule for rule in rules if set(rule.refers_to) & concepts]


def _leash_lead(key: AnswerKey, findings: Findings, item: LeashLead) -> list[Score]:
    rope = _named_by(key, findings, item.term, item.rope_mention)
    role = _named_by(key, findings, item.term, item.role_mention)
    leash = {normalise_label(label) for label in item.leash_labels}
    synonym = any(findings.labels(c) & leash for c in rope)
    rules = _matching_rules(findings, item.rule)
    on_rope, on_role = _referring(rules, rope), _referring(rules, role)
    where = f'"{item.term}" in the building rules names {_concept_labels(findings, rope)}'
    senses = f'"{item.term}" in dog 6 names {_concept_labels(findings, role)}; {where}'
    rule_detail = f"{len(on_rope)} matching rules refer to it, {len(on_role)} to the role"
    return [
        Score("leash_lead", "leash-lead-synonym", synonym, where),
        Score("leash_lead", "lead-senses", bool(rope and role) and not rope & role, senses),
        Score("leash_lead", "lead-rule-on-leash", bool(on_rope) and not on_role, rule_detail),
    ]


def _concepts_labelled(findings: Findings, words: tuple[str, ...]) -> list[Item]:
    folded = [word.casefold() for word in words]
    return [
        concept
        for concept in findings.of_type("concept")
        if any(word in label for word in folded for label in findings.labels(concept.id))
    ]


def _with_text(findings: Findings, phrases: tuple[str, ...]) -> list[Item]:
    if not phrases:
        return []
    return [item for item in findings.elements.values() if contains_all(item.text, (phrases,))]


def _citing_passage(key: AnswerKey, findings: Findings, passage_id: str) -> list[Item]:
    if not passage_id:
        return []
    units = _units(key, findings, key.passage(passage_id).place)
    return [item for unit in units for item in findings.citing(unit.id)]


def _trap_hits(key: AnswerKey, findings: Findings, trap: Trap) -> list[Item]:
    hits = [
        *_concepts_labelled(findings, trap.no_concept_label_contains),
        *(_matching_rules(findings, trap.no_rule) if trap.no_rule else []),
        *_with_text(findings, trap.no_element_text),
        *_citing_passage(key, findings, trap.no_citation_of),
    ]
    return list({item.id: item for item in hits}.values())


def _trap(key: AnswerKey, findings: Findings, trap: Trap) -> Score:
    hits = _trap_hits(key, findings, trap)
    detail = f"fell in: {_labels(hits)}" if hits else "avoided"
    return Score("traps", trap.id, not hits, detail)


def score_findings(key: AnswerKey, findings: Findings) -> list[Score]:
    """One score per answer-key item, in the order of ``SECTIONS``."""
    return [
        *(_ignorable(key, findings, passage) for passage in key.ignorable),
        *(_kept(key, findings, passage) for passage in key.kept),
        *_leash_lead(key, findings, key.leash_lead),
        *(_concept(findings, item) for item in key.concepts),
        *(_rule(findings, item) for item in key.rules),
        *(_trap(key, findings, trap) for trap in key.traps),
    ]


def score(key: AnswerKey, files: DatasetFiles) -> list[Score]:
    """Score the dataset ``files`` of an ingestion against ``key``."""
    return score_findings(key, read_findings(files))
