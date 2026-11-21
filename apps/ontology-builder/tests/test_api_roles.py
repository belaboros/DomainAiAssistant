"""Role checks on every governing route (T19: AC-3 through the back-end API)."""

from __future__ import annotations

from typing import Any

import pytest

SCOPE_EDIT = {
    "purpose": "A new purpose.",
    "readers": "Residents.",
    "level_guidance": {"level_1": "Core.", "level_2": "Everyday.", "level_3": "Special cases."},
    "ignorable_examples": ["Quotes"],
}


def _request(kit: Any, what: str, ids: list[str]) -> Any:
    client = kit.client
    if what == "scope":
        return client.put(kit.url("/scope"), json=SCOPE_EDIT)
    if what == "publish":
        return client.post(kit.url("/publish"), json={})
    payload = {"reason": "not in scope"} if what in {"reject", "deprecate"} else {}
    return client.post(kit.url("/actions"), json={"action": what, "ids": ids, "payload": payload})


@pytest.mark.parametrize("what", ["approve", "reject", "deprecate", "scope", "publish"])
def test_user_refused(api_kit: Any, review_kit: Any, what: str) -> None:
    ids = review_kit.seed([review_kit.concept("included"), review_kit.concept("approved")])
    api_kit.sign_in("alice", "user")
    tree, commits = review_kit.store.tree_hash(), api_kit.commits()

    response = _request(api_kit, what, ids)

    assert response.status_code == 403, response.text
    assert "domain admin" in response.json()["detail"]
    assert review_kit.store.tree_hash() == tree, "the dataset is unchanged"
    assert api_kit.commits() == commits
    assert api_kit.session.pending == 0, "nothing is pending either"
    statuses = [
        e["status"] for e in api_kit.client.get(api_kit.url("/elements")).json()["elements"]
    ]
    assert sorted(statuses) == ["approved", "included"]


def test_admin_approves_and_edits_the_scope(api_kit: Any, review_kit: Any) -> None:
    [concept] = review_kit.seed([review_kit.concept("included")])
    api_kit.sign_in("dora", "domain_admin")
    approved = api_kit.client.post(
        api_kit.url("/actions"), json={"action": "approve", "ids": [concept], "payload": {}}
    )
    assert approved.json()["results"] == [{"element_id": concept, "ok": True, "message": ""}]
    assert api_kit.client.post(api_kit.url("/save")).json()["ok"]

    commits = api_kit.commits()
    edited = api_kit.client.put(api_kit.url("/scope"), json=SCOPE_EDIT)
    assert edited.status_code == 200, edited.text
    assert edited.json()["ok"]
    assert api_kit.commits() == commits + 1
    assert api_kit.client.get(api_kit.url("/scope")).json()["purpose"] == "A new purpose."
    [decision] = [d for d in review_kit.store.read().decisions() if d.action == "edit_scope"]
    assert (decision.user, decision.role) == ("dora", "domain_admin")


def test_user_may_not_create_an_ontology(api_kit: Any) -> None:
    api_kit.sign_in("alice", "user")
    body = {"name": "other-domain", "scope": SCOPE_EDIT}
    assert api_kit.client.post("/api/ontologies", json=body).status_code == 403
    assert api_kit.client.get("/api/ontologies").json() == ["pets-and-house-rules"]
