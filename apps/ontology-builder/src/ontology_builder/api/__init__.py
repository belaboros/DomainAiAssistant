"""api component.

Exposes the use cases as a localhost JSON API and serves the built front end.

``create_app(ontology, port=...)`` builds the FastAPI app on an ontology opened with
``workflows.open_ontology``; ``serve`` runs it on 127.0.0.1 only. The OpenAPI schema is exported
to ``web/openapi.json`` (``export_openapi``), from which the TypeScript client is generated.
"""

from __future__ import annotations

from ontology_builder.api.app import (
    DEFAULT_PORT,
    OPENAPI_PATH,
    WEB_DIST,
    create_app,
    export_openapi,
    openapi_schema,
    serve,
    server_config,
)

__all__ = [
    "DEFAULT_PORT",
    "OPENAPI_PATH",
    "WEB_DIST",
    "create_app",
    "export_openapi",
    "openapi_schema",
    "serve",
    "server_config",
]
