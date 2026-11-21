"""The machine-readable answer key of the pet manuals (FR-38).

Only this component may refer to ``docs/research/notes/pet-manuals-corpus/`` (AC-33). The key is
loaded by ``load_answer_key`` after the ingestion has finished; nothing else reads it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[5]
ANSWER_KEY = REPO_ROOT / "docs" / "research" / "notes" / "pet-manuals-corpus" / "answer-key.yaml"

Keywords = tuple[tuple[str, ...], ...]
"""Groups of keywords: every group must have at least one keyword in the text."""


class AnswerKeyError(ValueError):
    """The answer key file does not have the expected shape."""


@dataclass(frozen=True)
class Place:
    """A document of a corpus (``dog``, ``cat``, ``rules``) and, for a passage, a piece of text."""

    corpus: str
    document: str
    contains: str = ""


@dataclass(frozen=True)
class Passage:
    id: str
    place: Place
    category: str = ""


@dataclass(frozen=True)
class ConceptItem:
    id: str
    labels: tuple[str, ...]


@dataclass(frozen=True)
class RuleItem:
    id: str
    all: Keywords


@dataclass(frozen=True)
class LeashLead:
    term: str
    leash_labels: tuple[str, ...]
    rope_mention: Place
    role_mention: Place
    rule: Keywords


@dataclass(frozen=True)
class Trap:
    id: str
    no_concept_label_contains: tuple[str, ...] = ()
    no_rule: Keywords = ()
    no_element_text: tuple[str, ...] = ()
    no_citation_of: str = ""


@dataclass(frozen=True)
class AnswerKey:
    version: int
    corpora: dict[str, str]
    """Corpus key → source folder name, e.g. ``dog`` → ``dog-owners-manual``."""
    ignorable: tuple[Passage, ...]
    kept: tuple[Passage, ...]
    leash_lead: LeashLead
    concepts: tuple[ConceptItem, ...]
    rules: tuple[RuleItem, ...]
    traps: tuple[Trap, ...]

    def passage(self, passage_id: str) -> Passage:
        for passage in (*self.ignorable, *self.kept):
            if passage.id == passage_id:
                return passage
        raise AnswerKeyError(f"no passage {passage_id!r} in the answer key")


def _strings(value: Any) -> tuple[str, ...]:
    return tuple(str(item) for item in value or ())


def _keywords(value: Any) -> Keywords:
    groups = (value or {}).get("all", ())
    return tuple(_strings(group) for group in groups)


def _place(data: dict[str, Any]) -> Place:
    return Place(str(data["corpus"]), str(data["document"]), str(data.get("contains", "")))


def _passages(items: Any) -> tuple[Passage, ...]:
    return tuple(
        Passage(str(item["id"]), _place(item), str(item.get("category", ""))) for item in items
    )


def _trap(item: dict[str, Any]) -> Trap:
    return Trap(
        id=str(item["id"]),
        no_concept_label_contains=_strings(item.get("no_concept_label_contains")),
        no_rule=_keywords(item.get("no_rule")),
        no_element_text=_strings(item.get("no_element_text")),
        no_citation_of=str(item.get("no_citation_of", "")),
    )


def _leash_lead(data: dict[str, Any]) -> LeashLead:
    return LeashLead(
        term=str(data["term"]),
        leash_labels=_strings(data["leash_labels"]),
        rope_mention=_place(data["rope_mention"]),
        role_mention=_place(data["role_mention"]),
        rule=_keywords(data["rule"]),
    )


def parse_answer_key(data: dict[str, Any]) -> AnswerKey:
    """The answer key of the parsed YAML; a missing field raises ``AnswerKeyError``."""
    try:
        return AnswerKey(
            version=int(data["version"]),
            corpora={str(k): str(v) for k, v in data["corpora"].items()},
            ignorable=_passages(data["ignorable"]),
            kept=_passages(data["kept"]),
            leash_lead=_leash_lead(data["leash_lead"]),
            concepts=tuple(
                ConceptItem(str(c["id"]), _strings(c["labels"])) for c in data["concepts"]
            ),
            rules=tuple(RuleItem(str(r["id"]), _keywords(r)) for r in data["rules"]),
            traps=tuple(_trap(t) for t in data["traps"]),
        )
    except (KeyError, TypeError, AttributeError, ValueError) as error:
        raise AnswerKeyError(f"the answer key is malformed: {error!r}") from None


def load_answer_key(path: Path = ANSWER_KEY) -> AnswerKey:
    """Read and parse the answer key file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AnswerKeyError(f"{path} holds no mapping")
    return parse_answer_key(data)
