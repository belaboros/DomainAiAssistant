"""The text rule of every source unit: normalisation and content hash (contract ``ontology``).

It lives in ``model`` because both the Markdown splitter (``sources``) and user statements
(``governance``) must hash text the same way.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata

_WHITESPACE = re.compile(r"\s+")


def normalise(text: str) -> str:
    """Unicode NFC, runs of whitespace as one space, no leading or trailing whitespace."""
    return _WHITESPACE.sub(" ", unicodedata.normalize("NFC", text)).strip()


def content_hash(text: str) -> str:
    """``sha256:`` + hex SHA-256 of the normalised text (contract ``ontology``, source unit)."""
    return "sha256:" + hashlib.sha256(normalise(text).encode("utf-8")).hexdigest()
