"""Sign-in and sign-out (FR-2): a handle and a role, no password, kept in a session cookie."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from ontology_builder.api.deps import Reader, Server, Token
from ontology_builder.api.schemas import Done, SessionOut, SignIn
from ontology_builder.api.state import COOKIE, ServerState, name_warning
from ontology_builder.workflows import Actor

router = APIRouter(prefix="/api/session", tags=["session"])


def _open_name(state: ServerState) -> str:
    if state.ontology is None:
        raise HTTPException(503, "no ontology is open on this server")
    return state.ontology.name


@router.post("")
def sign_in(body: SignIn, state: Server, session: Token, response: Response) -> SessionOut:
    """Sign in; the response warns when the user name looks like an email address."""
    user = body.user.strip()
    token = state.sessions.sign_in(session, Actor(user, body.role))
    response.set_cookie(COOKIE, token, httponly=True, samesite="strict")
    return SessionOut(
        user=user,
        role=body.role,
        writer=state.sessions.is_writer(token),
        ontology=_open_name(state),
        warning=name_warning(user),
    )


@router.get("")
def current(state: Server, session: Token, actor: Reader) -> SessionOut:
    return SessionOut(
        user=actor.user,
        role=actor.role,
        writer=state.sessions.is_writer(session),
        ontology=_open_name(state),
    )


@router.delete("")
def sign_out(state: Server, session: Token, response: Response) -> Done:
    state.sessions.sign_out(session)
    response.delete_cookie(COOKIE)
    return Done()
