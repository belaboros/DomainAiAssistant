"""The local-only guards of the API (T19: NFR local only; edge case "two GUI windows"), the
built front end, and the exported OpenAPI schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from ontology_builder.api import OPENAPI_PATH, create_app, openapi_schema, server_config


def test_binds_localhost_rejects_foreign_host_and_missing_header(
    api_kit: Any, review_kit: Any
) -> None:
    [concept] = review_kit.seed([review_kit.concept()])
    config = server_config(api_kit.app, port=8765)
    assert (config.host, config.port) == ("127.0.0.1", 8765)
    api_kit.sign_in()
    for host in ("evil.example:8765", "127.0.0.1:9999", "localhost.evil.example:8765"):
        refused = api_kit.client.get("/api/session", headers={"Host": host})
        assert refused.status_code == 400, host
    assert api_kit.client.get("/api/session", headers={"Host": "localhost:8765"}).status_code == 200

    body = {"action": "include", "ids": [concept], "payload": {}}
    bare = TestClient(api_kit.app, base_url="http://127.0.0.1:8765", cookies=api_kit.client.cookies)
    missing = bare.post(api_kit.url("/actions"), json=body)
    assert missing.status_code == 403 and "X-Ontology-Builder" in missing.json()["detail"]
    foreign = api_kit.client.post(
        api_kit.url("/actions"), json=body, headers={"Origin": "http://evil.example"}
    )
    assert foreign.status_code == 403
    assert api_kit.session.pending == 0, "no refused write changed anything"


def test_second_session_is_read_only(api_kit: Any, review_kit: Any) -> None:
    [concept] = review_kit.seed([review_kit.concept()])
    assert api_kit.sign_in("alice")["writer"] is True
    second = api_kit.new_client()
    assert api_kit.sign_in("bob", client=second)["writer"] is False

    assert second.get(api_kit.url("/elements")).status_code == 200
    body = {"action": "include", "ids": [concept], "payload": {}}
    refused = second.post(api_kit.url("/actions"), json=body)
    assert refused.status_code == 403 and "read-only" in refused.json()["detail"]

    api_kit.client.delete("/api/session")
    third = api_kit.new_client()
    assert api_kit.sign_in("carol", client=third)["writer"] is True


def test_serves_the_built_front_end(api_kit: Any, tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("<!doctype html><title>OntologyBuilder</title>", "utf-8")
    app = create_app(api_kit.session, port=8765, web_dist=dist)
    with TestClient(app, base_url="http://127.0.0.1:8765") as client:
        assert "OntologyBuilder" in client.get("/").text
        api = client.get("/api/session")
        assert (api.status_code, api.json()) == (401, {"detail": "sign in first"}), "API first"


def test_without_a_build_the_root_says_how_to_build(api_kit: Any, tmp_path: Path) -> None:
    app = create_app(api_kit.session, port=8765, web_dist=tmp_path / "missing")
    with TestClient(app, base_url="http://127.0.0.1:8765") as client:
        assert "npm --prefix apps/ontology-builder/web run build" in client.get("/").text


def test_openapi_json_matches_the_app() -> None:
    """``web/openapi.json`` is what the TypeScript client is generated from (drift check).
    Regenerate it with ``uv run python apps/ontology-builder/tools/export_openapi.py``."""
    committed = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    assert committed == openapi_schema()


@pytest.mark.parametrize("path", ["/api/session", "/api/ontologies"])
def test_openapi_lists_the_routes(path: str) -> None:
    assert path in openapi_schema()["paths"]
