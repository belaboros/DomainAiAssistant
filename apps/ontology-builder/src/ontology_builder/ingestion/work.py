"""The work folder of one run: its plan, its run record and the cached answer of each batch (FR-8).

``<work dir>/ontology-<name>/runs/<run-id>/`` holds ``plan.yaml``, ``run.yaml`` (status
``running`` or ``failed``) and one file per finished batch under ``pass1/`` plus ``pass2.yaml``.
The work folder is git-ignored; the dataset is written only at the end of a run, in one swap.
A resumed run reads the plan and the finished batches back and asks only for the rest.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from ontology_builder.extraction import DocumentExtraction, TermResolution
from ontology_builder.ingestion.plan import Batch, IngestionRefusedError, RunPlan
from ontology_builder.model import (
    ELEMENT_TYPES,
    Corpus,
    Document,
    Element,
    Estimate,
    IgnorableVerdict,
    Role,
    Run,
    RunKind,
    SkippedItem,
    SourceUnit,
    validate_element,
    validate_record,
)
from ontology_builder.store import dump_yaml, load_yaml

_TYPE_OF_CLASS = {record_class: name for name, record_class in ELEMENT_TYPES.items()}


def _dump(record: Any) -> Any:
    return record.model_dump(mode="json", exclude_none=True)


def _elements_data(elements: list[Element]) -> list[dict[str, Any]]:
    return [{"type": _TYPE_OF_CLASS[type(e)], "record": _dump(e)} for e in elements]


def _elements(data: list[dict[str, Any]]) -> list[Element]:
    return [validate_element(item["type"], item["record"]) for item in data]


def _skipped(data: list[Any]) -> list[SkippedItem]:
    return [validate_record(SkippedItem, item) for item in data]


def _plan_data(plan: RunPlan) -> dict[str, Any]:
    return {
        "ontology": plan.ontology,
        "run_id": plan.run_id,
        "kind": str(plan.kind),
        "user": plan.user,
        "role": str(plan.role),
        "model": plan.model,
        "estimate": _dump(plan.estimate),
        "corpus": _dump(plan.corpus) if plan.corpus else None,
        "source_path": plan.source_path,
        "not_ignorable": list(plan.not_ignorable),
        "batches": [
            {
                "folder": batch.folder,
                "document": _dump(batch.document),
                "units": [_dump(unit) for unit in batch.units],
            }
            for batch in plan.batches
        ],
    }


def _plan(data: dict[str, Any]) -> RunPlan:
    batches = [
        Batch(
            folder=item["folder"],
            document=validate_record(Document, item["document"]),
            units=[validate_record(SourceUnit, unit) for unit in item["units"]],
        )
        for item in data["batches"]
    ]
    return RunPlan(
        ontology=data["ontology"],
        run_id=data["run_id"],
        kind=RunKind(data["kind"]),
        user=data["user"],
        role=Role(data["role"]),
        model=data["model"],
        estimate=validate_record(Estimate, data["estimate"]),
        batches=batches,
        corpus=validate_record(Corpus, data["corpus"]) if data.get("corpus") else None,
        source_path=data.get("source_path"),
        not_ignorable=list(data.get("not_ignorable") or []),
    )


class RunFolder:
    """The work folder of one run."""

    def __init__(self, path: Path) -> None:
        self.path = path

    @staticmethod
    def runs_dir(work_dir: Path, ontology: str) -> Path:
        return work_dir / f"ontology-{ontology}" / "runs"

    @classmethod
    def of(cls, work_dir: Path, ontology: str, run_id: str) -> RunFolder:
        return cls(cls.runs_dir(work_dir, ontology) / run_id)

    @classmethod
    def unfinished(cls, work_dir: Path, ontology: str) -> list[RunFolder]:
        """Every run of the ontology that has a work folder (running, failed or interrupted)."""
        folder = cls.runs_dir(work_dir, ontology)
        found = sorted(p for p in folder.iterdir() if p.is_dir()) if folder.is_dir() else []
        return [cls(path) for path in found if (path / "plan.yaml").is_file()]

    def exists(self) -> bool:
        return (self.path / "plan.yaml").is_file()

    def _write(self, name: str, data: Any) -> None:
        target = self.path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        partial = target.with_name(target.name + ".partial")
        partial.write_text(dump_yaml(data), encoding="utf-8")
        partial.replace(target)  # a crash never leaves half a file behind

    def _read(self, name: str) -> Any:
        return load_yaml((self.path / name).read_text(encoding="utf-8"))

    # ---- plan and run record ----

    def start(self, plan: RunPlan, run: Run) -> None:
        if self.exists():
            raise IngestionRefusedError(f"run {plan.run_id} was already started; resume it")
        self._write("plan.yaml", _plan_data(plan))
        self.write_run(run)

    def plan(self) -> RunPlan:
        if not self.exists():
            raise IngestionRefusedError(f"no unfinished run {self.path.name} to resume")
        return _plan(self._read("plan.yaml"))

    def write_run(self, run: Run) -> None:
        self._write("run.yaml", _dump(validate_record(Run, _dump(run))))

    def run(self) -> Run:
        return validate_record(Run, self._read("run.yaml"))

    def remove(self) -> None:
        shutil.rmtree(self.path, ignore_errors=True)

    # ---- pass 1 per batch ----

    def _pass1_name(self, document_id: str) -> str:
        return f"pass1/{document_id}.yaml"

    def pass1(self, document_id: str) -> DocumentExtraction | None:
        """The cached pass 1 answer of a document, or ``None`` when it has not run yet."""
        name = self._pass1_name(document_id)
        if not (self.path / name).is_file():
            return None
        data = self._read(name)
        return DocumentExtraction(
            document_id=data["document_id"],
            verdicts={
                unit: validate_record(IgnorableVerdict, verdict)
                for unit, verdict in data["verdicts"].items()
            },
            elements=_elements(data["elements"]),
            skipped=_skipped(data["skipped"]),
            input_tokens=data["input_tokens"],
            output_tokens=data["output_tokens"],
        )

    def save_pass1(self, result: DocumentExtraction) -> None:
        self._write(
            self._pass1_name(result.document_id),
            {
                "document_id": result.document_id,
                "verdicts": {unit: _dump(v) for unit, v in result.verdicts.items()},
                "elements": _elements_data(result.elements),
                "skipped": [_dump(item) for item in result.skipped],
                "input_tokens": result.input_tokens,
                "output_tokens": result.output_tokens,
            },
        )

    # ---- pass 2 ----

    def pass2(self) -> TermResolution | None:
        if not (self.path / "pass2.yaml").is_file():
            return None
        data = self._read("pass2.yaml")
        return TermResolution(
            elements=_elements(data["elements"]),
            merged=dict(data["merged"]),
            skipped=_skipped(data["skipped"]),
            input_tokens=data["input_tokens"],
            output_tokens=data["output_tokens"],
            extended=_elements(data.get("extended", [])),
        )

    def save_pass2(self, result: TermResolution) -> None:
        self._write(
            "pass2.yaml",
            {
                "elements": _elements_data(result.elements),
                "merged": dict(result.merged),
                "skipped": [_dump(item) for item in result.skipped],
                "input_tokens": result.input_tokens,
                "output_tokens": result.output_tokens,
                "extended": _elements_data(result.extended),
            },
        )
