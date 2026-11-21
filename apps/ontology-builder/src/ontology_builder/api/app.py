"""The FastAPI app: routes, the local-only guards, error mapping and the built front end.

Guards (plan 0002, HTTP API): the server binds to 127.0.0.1 only (``server_config``); any Host
other than ``127.0.0.1:<port>`` or ``localhost:<port>`` is rejected (DNS rebinding); every write
needs the header ``X-Ontology-Builder: 1`` and, when the browser sends an Origin, a local one.
"""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from ontology_builder.api import routes_review, routes_session, routes_writes
from ontology_builder.api.state import ServerState
from ontology_builder.workflows import (
    GovernanceRefusedError,
    IngestionFailedError,
    IngestionRefusedError,
    LlmError,
    NotFoundError,
    OpenOntology,
    WorkflowRefusedError,
)

WEB_DIR = Path(__file__).resolve().parents[3] / "web"
WEB_DIST = WEB_DIR / "dist"
OPENAPI_PATH = WEB_DIR / "openapi.json"
"""The exported schema the TypeScript client is generated from (drift-tested)."""
DEFAULT_PORT = 8765
WRITE_HEADER = "X-Ontology-Builder"
BUILD_HINT = (
    "The GUI is not built yet. Build it with: npm --prefix apps/ontology-builder/web run build\n"
)
_SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})

_STATUS: tuple[tuple[type[Exception], int], ...] = (
    (NotFoundError, 404),
    (GovernanceRefusedError, 403),
    (WorkflowRefusedError, 409),
    (IngestionRefusedError, 409),
    (IngestionFailedError, 502),
    (LlmError, 503),
)
"""Refusals of the use cases and the HTTP status each one gets; the message is the detail."""

Next = Callable[[Request], Awaitable[Response]]


def _refusal(state: ServerState, request: Request) -> JSONResponse | None:
    if request.headers.get("host", "") not in state.allowed_hosts():
        return JSONResponse({"detail": "unknown Host: this server is local only"}, 400)
    if request.method in _SAFE_METHODS:
        return None
    if request.headers.get(WRITE_HEADER) != "1":
        return JSONResponse({"detail": f"a write needs the header {WRITE_HEADER}: 1"}, 403)
    origin = request.headers.get("origin")
    if origin is not None and origin not in state.allowed_origins():
        return JSONResponse({"detail": "a write must come from this server's own page"}, 403)
    return None


def _add_guards(app: FastAPI, state: ServerState) -> None:
    @app.middleware("http")
    async def guard(request: Request, call_next: Next) -> Response:
        refused = _refusal(state, request)
        return refused if refused is not None else await call_next(request)


def _add_error_mapping(app: FastAPI) -> None:
    for error, status in _STATUS:

        def handler(_request: Request, exc: Exception, status: int = status) -> JSONResponse:
            return JSONResponse({"detail": str(exc)}, status)

        app.add_exception_handler(error, handler)


def _add_front_end(app: FastAPI, web_dist: Path) -> None:
    if (web_dist / "index.html").is_file():
        app.mount("/", StaticFiles(directory=web_dist, html=True), name="web")
        return

    @app.get("/", include_in_schema=False)
    def build_hint() -> PlainTextResponse:
        return PlainTextResponse(BUILD_HINT)


def create_app(
    ontology: OpenOntology | None, *, port: int = DEFAULT_PORT, web_dist: Path = WEB_DIST
) -> FastAPI:
    """The API on ``ontology`` (opened, and so locked, by the caller), served on ``port``."""
    app = FastAPI(
        title="OntologyBuilder",
        version="0.1.0",
        description="Local API of the ontology-builder review GUI (spec 0002).",
    )
    state = ServerState(ontology, port)
    app.state.server = state
    _add_guards(app, state)
    _add_error_mapping(app)
    for router in (routes_session.router, routes_review.router, routes_writes.router):
        app.include_router(router)
    _add_front_end(app, web_dist)
    return app


def openapi_schema() -> dict[str, Any]:
    """The OpenAPI schema of the app (no ontology needed)."""
    schema: dict[str, Any] = create_app(None).openapi()
    return schema


def export_openapi(path: Path = OPENAPI_PATH) -> None:
    """Write ``web/openapi.json``, sorted and indented, so its diffs are readable."""
    text = json.dumps(openapi_schema(), indent=2, sort_keys=True, ensure_ascii=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


def server_config(app: FastAPI, port: int = DEFAULT_PORT) -> uvicorn.Config:
    """The server binds to 127.0.0.1 only (NFR local only)."""
    return uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")


def serve(ontology: OpenOntology, port: int = DEFAULT_PORT) -> None:
    """Serve the API and the GUI on ``http://127.0.0.1:<port>`` until stopped."""
    uvicorn.Server(server_config(create_app(ontology, port=port), port)).run()
