"""What one server holds: the open ontology, the browser sessions and the write lock.

The first signed-in browser session is the writer; any other session is read-only until the
writer signs out (plan 0002, HTTP API guards: single user, FR-27).
"""

from __future__ import annotations

import re
import secrets
import threading
from collections.abc import Iterator
from dataclasses import dataclass, field

from ontology_builder.workflows import Actor, OpenOntology

COOKIE = "ontology_builder_session"
_EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
EMAIL_WARNING = (
    "This looks like an email address. The dataset is public: use a handle, not a real name "
    "or email address."
)


def name_warning(user: str) -> str | None:
    """The FR-2 warning for a user name that looks like an email address."""
    return EMAIL_WARNING if _EMAIL.search(user) else None


@dataclass
class Sessions:
    """Browser sessions by cookie token, and which one may write."""

    actors: dict[str, Actor] = field(default_factory=dict)
    writer: str | None = None

    def sign_in(self, token: str | None, actor: Actor) -> str:
        """Sign in (again, when ``token`` is known); returns the session's token."""
        if token is None or token not in self.actors:
            token = secrets.token_urlsafe(32)
        self.actors[token] = actor
        if self.writer is None:
            self.writer = token
        return token

    def sign_out(self, token: str | None) -> None:
        if token is None:
            return
        self.actors.pop(token, None)
        if self.writer == token:
            self.writer = None

    def actor(self, token: str | None) -> Actor | None:
        return self.actors.get(token) if token else None

    def is_writer(self, token: str | None) -> bool:
        return token is not None and token == self.writer


@dataclass
class ServerState:
    """``ontology`` is ``None`` only for the schema export (no dataset open)."""

    ontology: OpenOntology | None
    port: int
    sessions: Sessions = field(default_factory=Sessions)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def allowed_hosts(self) -> frozenset[str]:
        return frozenset({f"127.0.0.1:{self.port}", f"localhost:{self.port}"})

    def allowed_origins(self) -> frozenset[str]:
        return frozenset(f"http://{host}" for host in self.allowed_hosts())

    def held(self) -> Iterator[OpenOntology]:
        """The open ontology under the lock (one request at a time changes or reads it)."""
        if self.ontology is None:
            raise LookupError("no ontology is open")
        with self.lock:
            yield self.ontology
