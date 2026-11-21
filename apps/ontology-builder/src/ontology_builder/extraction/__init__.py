"""extraction component.

Turns source units into validated proposed elements with evidence and levels.

Pass 1 (``extract_document``) runs per document as two calls (ontology-builder/ADR-0007). The LLM
gets the scope record, the level rubric and the document's units under short aliases (Q38). Call A
(``concepts_request``) returns a verdict per unit and candidate statements, terms, concepts and
relations; call B (``rules_request``) returns the rules and properties that refer to them.
``pass1_requests`` gives both requests for the cost estimate. The answer is
validated item by item, invalid items are retried once, and what stays invalid, cites an unknown
unit or refers to a dropped candidate is reported and left out (FR-10). Ignorable units are never
evidence (FR-14). The result holds proposed records with minted IDs, ready to be written.

Pass 2 (``resolve_terms``) runs once per ingestion over the new elements of every document and
the concepts already in the ontology (``TermInput``). It merges concepts that are the same thing
(synonym groups, FR-11) and points each mention of a homonym to the concept it names there, with a
scope note per sense (FR-12). ``terms_request`` gives its request for the cost estimate.
"""

from __future__ import annotations

from ontology_builder.extraction.pass1 import (
    DocumentExtraction,
    ExtractionContext,
    extract_document,
)
from ontology_builder.extraction.pass2 import TermResolution, resolve_terms
from ontology_builder.extraction.prompt import (
    PASS1_MAX_TOKENS,
    aliases,
    concepts_request,
    pass1_requests,
    rules_request,
)
from ontology_builder.extraction.terms_prompt import (
    PASS2_MAX_TOKENS,
    TermInput,
    TermPrompt,
    terms_request,
)

__all__ = [
    "PASS1_MAX_TOKENS",
    "PASS2_MAX_TOKENS",
    "DocumentExtraction",
    "ExtractionContext",
    "TermInput",
    "TermPrompt",
    "TermResolution",
    "aliases",
    "concepts_request",
    "extract_document",
    "pass1_requests",
    "resolve_terms",
    "rules_request",
    "terms_request",
]
