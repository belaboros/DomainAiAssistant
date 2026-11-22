"""Creating an ontology (plan 0002, T5: AC-1).

The scope-record guard of ingestion is tested where ingestion applies it:
``test_ingestion_estimate.py::test_refused_while_scope_record_is_empty``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from ontology_builder.governance import Actor, GovernanceRefusedError, create_ontology
from ontology_builder.model import FixedClock, Role, UlidMinter
from ontology_builder.store import DatasetStore

AT = datetime(2026, 11, 21, 10, 0, tzinfo=UTC)
ADMIN = Actor("bela", Role.domain_admin)
USER = Actor("sam", Role.user)
NAME = "pets-and-house-rules"


def _scope(scope_record: dict[str, Any]) -> dict[str, Any]:
    data = dict(scope_record)
    del data["base_iri"], data["name"]
    return data


def _store(tmp_path: Path, name: str = NAME) -> DatasetStore:
    clock = FixedClock(AT)
    return DatasetStore(tmp_path, name, clock=clock, minter=UlidMinter(clock, random_bytes=bytes))


def test_create_makes_layout_and_scope(tmp_path: Path, scope_record: dict[str, Any]) -> None:
    store = _store(tmp_path)
    create_ontology(store, _scope(scope_record), ADMIN)
    root = tmp_path / "ontology-pets-and-house-rules"
    for folder in ["00_sources", "01_model", "02_decisions", "03_release/00_raw"]:
        assert (root / folder).is_dir()
    scope = store.read().scope()
    assert scope is not None
    assert scope.name == NAME
    assert scope.purpose == scope_record["purpose"]
    assert scope.base_iri == "urn:domain-ai-assistant:ontology:pets-and-house-rules:"
    [decision] = store.read().decisions()
    assert (decision.action, decision.user, decision.role) == ("create", "bela", "domain_admin")
    assert decision.at == AT


def test_create_keeps_a_given_base_iri(tmp_path: Path, scope_record: dict[str, Any]) -> None:
    store = _store(tmp_path)
    create_ontology(store, _scope(scope_record) | {"base_iri": "https://example.org/pets#"}, ADMIN)
    scope = store.read().scope()
    assert scope is not None
    assert scope.base_iri == "https://example.org/pets#"


def test_only_a_domain_admin_creates(tmp_path: Path, scope_record: dict[str, Any]) -> None:
    store = _store(tmp_path)
    with pytest.raises(GovernanceRefusedError, match="domain admin"):
        create_ontology(store, _scope(scope_record), USER)
    assert not tmp_path.joinpath("ontology-pets-and-house-rules").exists()


@pytest.mark.parametrize("name", ["Pets", "pets_rules", "pets--rules", "-pets", "pets-", ""])
def test_name_must_be_kebab_case(tmp_path: Path, scope_record: dict[str, Any], name: str) -> None:
    with pytest.raises(GovernanceRefusedError, match="kebab-case"):
        create_ontology(_store(tmp_path, name), _scope(scope_record), ADMIN)
    assert list(tmp_path.iterdir()) == []


def test_name_already_present_is_refused(tmp_path: Path, scope_record: dict[str, Any]) -> None:
    create_ontology(_store(tmp_path), _scope(scope_record), ADMIN)
    before = _store(tmp_path).tree_hash()
    with pytest.raises(GovernanceRefusedError, match="already exists"):
        create_ontology(_store(tmp_path), _scope(scope_record), ADMIN)
    assert _store(tmp_path).tree_hash() == before


def test_scope_name_must_match(tmp_path: Path, scope_record: dict[str, Any]) -> None:
    with pytest.raises(GovernanceRefusedError, match="name"):
        create_ontology(_store(tmp_path), _scope(scope_record) | {"name": "other"}, ADMIN)


@pytest.mark.parametrize("field", ["purpose", "readers", "level_guidance", "ignorable_examples"])
def test_incomplete_scope_is_refused_with_the_field(
    tmp_path: Path, scope_record: dict[str, Any], field: str
) -> None:
    scope = _scope(scope_record)
    del scope[field]
    with pytest.raises(GovernanceRefusedError, match=field):
        create_ontology(_store(tmp_path), scope, ADMIN)
    assert list(tmp_path.iterdir()) == []
