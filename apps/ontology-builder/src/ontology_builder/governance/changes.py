"""The pending change set: an in-memory copy of the elements and user statements, plus the
decisions made on it.

Review actions change this copy only (plan 0002, Approach 6; ontology-builder/ADR-0004). A save
writes the changed records and the decisions inside one store transaction and then calls
``mark_saved``. Nothing here removes a record: a record can only be replaced by a new version.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

from ontology_builder.governance.actors import GovernanceRefusedError
from ontology_builder.model import (
    ID_PREFIXES,
    Decision,
    Element,
    SourceUnit,
    validate_element,
    validate_record,
)
from ontology_builder.store import DatasetFiles, DatasetStore

_ELEMENTS, _STATEMENTS = "elements", "statements"
_TYPE_OF_PREFIX = {prefix: name for name, prefix in ID_PREFIXES.items()}


def _data(record: Any) -> Any:
    return record.model_dump(mode="json", exclude_none=True)


class ChangeSet:
    """One ontology as the reviewer sees it, and what changed since loading."""

    def __init__(
        self,
        store: DatasetStore,
        elements: Mapping[str, Element],
        statements: Mapping[str, SourceUnit] | None = None,
    ) -> None:
        self.store = store
        self.elements: dict[str, Element] = dict(elements)
        self.statements: dict[str, SourceUnit] = dict(statements or {})
        self.decisions: list[Decision] = []
        self._changed: dict[str, set[str]] = {_ELEMENTS: set(), _STATEMENTS: set()}
        self._undo: dict[tuple[str, str], Any] | None = None
        self._corpus_units: set[str] | None = None

    @classmethod
    def load(cls, store: DatasetStore) -> ChangeSet:
        files = store.read()
        statements = {unit.id: unit for unit in files.user_statements()}
        return cls(store, files.elements(), statements)

    # ---- reading ----

    def get(self, element_id: str) -> Element:
        element = self.elements.get(element_id)
        if element is None:
            raise GovernanceRefusedError(f"unknown element {element_id!r}")
        return element

    def statement(self, unit_id: str) -> SourceUnit:
        unit = self.statements.get(unit_id)
        if unit is None:
            raise GovernanceRefusedError(f"unknown user statement {unit_id!r}")
        return unit

    def has_unit(self, unit_id: str) -> bool:
        """Whether a corpus unit or a user statement with this ID exists."""
        if unit_id in self.statements:
            return True
        if self._corpus_units is None:
            files = self.store.read()
            self._corpus_units = {
                unit.id
                for folder in files.corpora()
                for document in files.documents(folder)
                for unit in files.units(folder, document.id)
            }
        return unit_id in self._corpus_units

    # ---- changing ----

    def put(self, element: Element, decisions: list[Decision]) -> None:
        """Add the element or replace it by its new version, with the decisions that led to it."""
        self._replace(_ELEMENTS, element.id, element)
        self.decisions.extend(decisions)

    def put_statement(self, unit: SourceUnit, decisions: list[Decision]) -> None:
        """Add a user statement or replace it by its new revision, with its decisions."""
        self._replace(_STATEMENTS, unit.id, unit)
        self.decisions.extend(decisions)

    def _replace(self, table: str, key: str, record: Any) -> None:
        records: dict[str, Any] = getattr(self, table)
        if self._undo is not None and (table, key) not in self._undo:
            self._undo[(table, key)] = records.get(key)
        records[key] = record
        self._changed[table].add(key)

    @contextmanager
    def atomic(self) -> Iterator[None]:
        """Undo every change made inside the block if it raises, so an action applies whole or
        not at all. Nested blocks belong to the outermost one."""
        if self._undo is not None:
            yield
            return
        self._undo = {}
        decisions = len(self.decisions)
        changed = {table: set(keys) for table, keys in self._changed.items()}
        try:
            yield
        except BaseException:
            self._roll_back(self._undo)
            self.decisions = self.decisions[:decisions]
            self._changed = changed
            raise
        finally:
            self._undo = None

    def _roll_back(self, undo: Mapping[tuple[str, str], Any]) -> None:
        for (table, key), before in undo.items():
            records: dict[str, Any] = getattr(self, table)
            if before is None:
                records.pop(key)  # added in this block: not yet a record
            else:
                records[key] = before

    # ---- saving ----

    def changed_ids(self) -> list[str]:
        """IDs of the changed elements."""
        return sorted(self._changed[_ELEMENTS])

    def changed_statement_ids(self) -> list[str]:
        return sorted(self._changed[_STATEMENTS])

    def write(self, files: DatasetFiles) -> None:
        """Write the changed records (validated by the store) and append the decisions."""
        for element_id in self.changed_ids():
            files.write_element(self.elements[element_id])
        for unit_id in self.changed_statement_ids():
            files.write_user_statement(self.statements[unit_id])
        files.append_decisions(self.decisions)

    def mark_saved(self) -> None:
        """Forget the pending changes once the save that wrote them has succeeded."""
        for keys in self._changed.values():
            keys.clear()
        self.decisions = []

    # ---- journal ----

    @property
    def pending(self) -> int:
        """How many records (elements and user statements) changed since loading or saving."""
        return sum(len(keys) for keys in self._changed.values())

    def journal(self) -> dict[str, Any]:
        """The pending changes as plain data, to be kept until they are saved (crash safety)."""
        return {
            _ELEMENTS: [_data(self.elements[key]) for key in self.changed_ids()],
            _STATEMENTS: [_data(self.statements[key]) for key in self.changed_statement_ids()],
            "decisions": [_data(decision) for decision in self.decisions],
        }

    def restore(self, journal: Mapping[str, Any]) -> None:
        """Re-apply the pending changes of ``journal()``, each record validated again."""
        for data in journal.get(_ELEMENTS, []):
            element_type = _TYPE_OF_PREFIX.get(str(data.get("id", "")).split("_")[0], "")
            self._replace(_ELEMENTS, data["id"], validate_element(element_type, data))
        for data in journal.get(_STATEMENTS, []):
            self._replace(_STATEMENTS, data["id"], validate_record(SourceUnit, data))
        self.decisions.extend(validate_record(Decision, d) for d in journal.get("decisions", []))
