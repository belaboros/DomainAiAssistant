"""Sign-in to the API: the handle and role every decision carries (T19: AC-2, server side)."""

from __future__ import annotations

from typing import Any

import pytest


def test_decisions_carry_user_and_role(api_kit: Any, review_kit: Any) -> None:
    [concept] = review_kit.seed([review_kit.concept()])
    signed = api_kit.sign_in("alice", "user")
    assert signed["user"] == "alice" and signed["role"] == "user"

    done = api_kit.client.post(
        api_kit.url("/actions"), json={"action": "include", "ids": [concept], "payload": {}}
    )
    assert done.status_code == 200, done.text
    detail = api_kit.client.get(api_kit.url(f"/elements/{concept}")).json()
    assert [(d["user"], d["role"], d["action"]) for d in detail["decisions"]] == [
        ("alice", "user", "include")
    ]

    saved = api_kit.client.post(api_kit.url("/save")).json()
    assert saved["ok"], saved
    written = [d for d in review_kit.store.read().decisions() if d.element_id == concept]
    assert [(d.user, str(d.role), str(d.action)) for d in written] == [("alice", "user", "include")]


@pytest.mark.parametrize("user", ["alice@example.com", "Alice.Smith@mail.example.org"])
def test_email_like_name_warns(api_kit: Any, user: str) -> None:
    signed = api_kit.sign_in(user, "user")
    assert signed["warning"] and "email" in signed["warning"]


def test_handle_signs_in_without_warning(api_kit: Any) -> None:
    signed = api_kit.sign_in("alice", "domain_admin")
    assert signed["warning"] is None
    assert signed["writer"] is True
    assert api_kit.client.get("/api/session").json()["user"] == "alice"


def test_session_names_the_open_ontology(api_kit: Any, review_kit: Any) -> None:
    """The GUI learns from the session which ontology its routes address."""
    signed = api_kit.sign_in("alice", "user")
    assert signed["ontology"] == review_kit.store.name
    assert api_kit.client.get("/api/session").json()["ontology"] == review_kit.store.name


def test_signed_out_requests_are_refused(api_kit: Any) -> None:
    assert api_kit.client.get(api_kit.url("/elements")).status_code == 401
    api_kit.sign_in()
    assert api_kit.client.get(api_kit.url("/elements")).status_code == 200
    assert api_kit.client.delete("/api/session").status_code == 200
    assert api_kit.client.get(api_kit.url("/elements")).status_code == 401


@pytest.mark.parametrize(
    "body", [{"user": "", "role": "user"}, {"user": "alice", "role": "root"}, {"role": "user"}]
)
def test_bad_sign_in_is_rejected(api_kit: Any, body: dict[str, str]) -> None:
    assert api_kit.client.post("/api/session", json=body).status_code == 422
