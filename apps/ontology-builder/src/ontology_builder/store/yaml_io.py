"""Deterministic YAML and JSON for every record the store writes (FR-36)."""

from __future__ import annotations

import json
from typing import Any

import yaml
from pydantic import BaseModel

from ontology_builder.model import validate_record

_NO_WRAP = 1_000_000


def dump_yaml(data: Any) -> str:
    """YAML with sorted keys, block style, Unicode kept and no line wrapping."""
    return yaml.safe_dump(
        data,
        sort_keys=True,
        allow_unicode=True,
        default_flow_style=False,
        width=_NO_WRAP,
        indent=2,
    )


def load_yaml(text: str) -> Any:
    return yaml.safe_load(text)


def dump_json_line(data: Any) -> str:
    """One compact JSON line with sorted keys, ending in a newline."""
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"


def to_data(record: BaseModel) -> Any:
    """The record as plain data, validated again first so nothing invalid is ever written."""
    data = record.model_dump(mode="json", exclude_none=True)
    validate_record(type(record), data)
    return data
