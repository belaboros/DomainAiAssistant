"""Split Markdown into block source units (plan 0002, Approach 3; ontology-builder/ADR-0003).

One unit per paragraph, list item, blockquote or table row, parsed with markdown-it-py. A list
item holds its own paragraphs; a nested list gives units of its own. A blockquote is one unit
with everything inside it. Code blocks and raw HTML blocks are not units. Headings are not units;
they make the heading path, and each heading starts a new section for ``index_in_section``.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from dataclasses import dataclass, field

from markdown_it import MarkdownIt
from markdown_it.token import Token

from ontology_builder.model import (
    SourceUnit,
    UlidMinter,
    UnitKind,
    content_hash,
    normalise,
    validate_record,
)

_PARSER = MarkdownIt("commonmark", {"html": False}).enable("table")


@dataclass
class Block:
    """One block of a document, before it gets its minted ID."""

    kind: UnitKind
    heading_path: tuple[str, ...]
    section: int
    parts: list[str] = field(default_factory=list)
    line_start: int = 0
    line_end: int = 0
    index_in_section: int = 0

    @property
    def text(self) -> str:
        return normalise(" ".join(self.parts))

    def add(self, text: str, token: Token) -> None:
        self.parts.append(text)
        if token.map is not None:
            start, end = token.map
            self.line_start = self.line_start or start + 1
            self.line_end = max(self.line_end, end)

    def to_unit(self, document_id: str, path: str, minter: UlidMinter) -> SourceUnit:
        """The validated source unit with a newly minted ``su_`` ID."""
        text = self.text
        location = {
            "path": path,
            "heading_path": list(self.heading_path),
            "index_in_section": self.index_in_section,
            "line_start": self.line_start,
            "line_end": self.line_end,
        }
        data = {
            "id": minter.new("source_unit"),
            "document_id": document_id,
            "kind": self.kind,
            "location": location,
            "content_hash": content_hash(text),
            "text": text,
        }
        return validate_record(SourceUnit, data)


class _Splitter:
    """Walks the markdown-it token stream once and collects the blocks in document order."""

    def __init__(self) -> None:
        self.blocks: list[Block] = []
        self.headings: list[tuple[int, str]] = []
        self.section = 0
        self.items: list[Block] = []
        self.quote: Block | None = None
        self.quote_depth = 0
        self.header: list[str] = []
        self.in_head = False
        self.row_block: Block | None = None
        self.target: Callable[[Token], None] | None = None
        self.handlers: dict[str, Callable[[Token], None]] = {
            "heading_open": self._heading_open,
            "paragraph_open": self._paragraph_open,
            "list_item_open": self._item_open,
            "list_item_close": self._item_close,
            "blockquote_open": self._quote_open,
            "blockquote_close": self._quote_close,
            "tr_open": self._row_open,
            "tr_close": self._row_close,
            "th_open": self._cell_open,
            "td_open": self._cell_open,
            "thead_open": self._thead_open,
            "thead_close": self._thead_close,
            "inline": self._inline,
        }

    def run(self, tokens: list[Token]) -> list[Block]:
        for token in tokens:
            handler = self.handlers.get(token.type)
            if handler is not None:
                handler(token)
        return _indexed([b for b in self.blocks if b.text])

    def _new_block(self, kind: UnitKind) -> Block:
        heading_path = tuple(text for _, text in self.headings)
        block = Block(kind=kind, heading_path=heading_path, section=self.section)
        self.blocks.append(block)
        return block

    def _inline(self, token: Token) -> None:
        if self.target is not None:
            self.target(token)
            self.target = None

    def _heading_open(self, token: Token) -> None:
        level = int(token.tag[1:])

        def take(inline: Token) -> None:
            while self.headings and self.headings[-1][0] >= level:
                self.headings.pop()
            self.headings.append((level, normalise(inline.content)))
            self.section += 1

        self.target = take

    def _paragraph_open(self, token: Token) -> None:
        holder = self.quote or (self.items[-1] if self.items else None)
        if holder is None:
            holder = self._new_block(UnitKind.paragraph)
        block = holder
        self.target = lambda inline: block.add(inline.content, inline)

    def _item_open(self, token: Token) -> None:
        if self.quote is None:
            self.items.append(self._new_block(UnitKind.list_item))

    def _item_close(self, token: Token) -> None:
        if self.quote is None:
            self.items.pop()

    def _quote_open(self, token: Token) -> None:
        self.quote_depth += 1
        if self.quote is None:
            self.quote = self._new_block(UnitKind.blockquote)

    def _quote_close(self, token: Token) -> None:
        self.quote_depth -= 1
        if self.quote_depth == 0:
            self.quote = None

    def _thead_open(self, token: Token) -> None:
        self.header = []
        self.in_head = True

    def _thead_close(self, token: Token) -> None:
        self.in_head = False

    def _row_open(self, token: Token) -> None:
        in_body = not self.in_head and self.quote is None
        self.row_block = self._new_block(UnitKind.table_row) if in_body else None

    def _row_close(self, token: Token) -> None:
        if self.row_block is not None and self.row_block.parts:
            self.row_block.parts = [_row_text(self.header, self.row_block.parts)]
        self.row_block = None

    def _cell_open(self, token: Token) -> None:
        def take(inline: Token) -> None:
            text = normalise(inline.content)
            if self.in_head:
                self.header.append(text)
            else:
                (self.row_block or self.quote or Block(UnitKind.table_row, (), 0)).add(text, inline)

        self.target = take


def _row_text(header: list[str], cells: list[str]) -> str:
    if len(header) != len(cells):
        return " | ".join(cells)
    return " | ".join(f"{name}: {cell}" for name, cell in zip(header, cells, strict=True))


def _indexed(blocks: list[Block]) -> list[Block]:
    counts: dict[int, int] = {}
    for block in blocks:
        block.index_in_section = counts.get(block.section, 0)
        counts[block.section] = block.index_in_section + 1
    return blocks


def split_markdown(markdown: str) -> list[Block]:
    """The non-empty blocks of a Markdown document, in document order."""
    return _Splitter().run(_PARSER.parse(markdown))


def first_heading(markdown: str) -> str | None:
    """The text of the first heading, if the document has one."""
    tokens = _PARSER.parse(markdown)
    for previous, token in itertools.pairwise(tokens):
        if previous.type == "heading_open" and token.type == "inline":
            return normalise(token.content)
    return None
