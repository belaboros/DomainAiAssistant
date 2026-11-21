"""Request dependencies: who is signed in, whether they may write, and the open ontology."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, HTTPException, Request

from ontology_builder.api.state import COOKIE, ServerState
from ontology_builder.model import Role
from ontology_builder.workflows import Actor, OpenOntology


def server(request: Request) -> ServerState:
    state: ServerState = request.app.state.server
    return state


Server = Annotated[ServerState, Depends(server)]


def token(request: Request) -> str | None:
    return request.cookies.get(COOKIE)


Token = Annotated[str | None, Depends(token)]


def signed_in(state: Server, session: Token) -> Actor:
    actor = state.sessions.actor(session)
    if actor is None:
        raise HTTPException(401, "sign in first")
    return actor


Reader = Annotated[Actor, Depends(signed_in)]


def writer(state: Server, session: Token, actor: Reader) -> Actor:
    """The signed-in actor of the writing session; a second session is read-only."""
    if not state.sessions.is_writer(session):
        raise HTTPException(
            403, "this session is read-only: another session of this server is signed in"
        )
    return actor


Writer = Annotated[Actor, Depends(writer)]


def require_admin(actor: Actor, what: str) -> None:
    """Refuse a governing request of a user before it reaches the use case (FR-3, AC-3)."""
    if actor.role != Role.domain_admin:
        raise HTTPException(403, f"only a domain admin can {what}")


def ontology(name: str, state: Server) -> Iterator[OpenOntology]:
    """The ontology this server opened, under the lock; any other name is not found."""
    if state.ontology is None:
        raise HTTPException(503, "no ontology is open on this server")
    if name != state.ontology.name:
        raise HTTPException(404, f"the ontology {name!r} is not open on this server")
    yield from state.held()


Ontology = Annotated[OpenOntology, Depends(ontology)]
