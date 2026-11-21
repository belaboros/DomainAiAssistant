"""The element routes: the index and its filters, detail, actions, authoring, save, publish and
ingestion (T19: AC-18 on the server; AC-16 and AC-6 through the API)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from ontology_builder.model import Element


def _index(kit: Any, **filters: str) -> list[dict[str, Any]]:
    response = kit.client.get(kit.url("/elements"), params=filters)
    assert response.status_code == 200, response.text
    elements: list[dict[str, Any]] = response.json()["elements"]
    return elements


def _building_rules(kit: Any) -> dict[str, Any]:
    corpora = kit.client.get(kit.url("/elements")).json()["corpora"]
    [found] = [c for c in corpora if c["folder"].endswith("building-and-house-rules")]
    return dict(found)


def _cites_corpus(element: Element, units: dict[str, Any], folder: str) -> bool:
    return any(units.get(e.unit) == folder for e in element.evidence)


def test_filter_rule_level1_building_rules(pet_api_kit: Any, pet_extraction: Any) -> None:
    pet_api_kit.sign_in()
    rules = _building_rules(pet_api_kit)
    corpus_of = {
        unit.id: corpus.folder for corpus in pet_extraction.corpora for unit in corpus.units
    }
    expected = {
        e.id
        for e in pet_extraction.elements
        if e.id.startswith("ru_")
        and e.level == "level-1"
        and _cites_corpus(e, corpus_of, rules["folder"])
    }
    assert expected, "the pet fixture has level-1 rules from the building rules"

    found = _index(pet_api_kit, type="rule", level="level-1", corpus=rules["folder"])
    assert {e["id"] for e in found} == expected

    document = rules["documents"][0]["id"]
    in_document = _index(pet_api_kit, type="rule", document=document)
    assert in_document and all(document in e["documents"] for e in in_document)


def test_search_lead_matches_label_definition_evidence(
    pet_api_kit: Any, pet_extraction: Any
) -> None:
    pet_api_kit.sign_in()
    texts = pet_extraction.units

    def mentions_lead(element: Element) -> bool:
        parts = [element.label, getattr(element, "definition", None) or ""]
        parts += [getattr(element, "text", "") or ""]
        parts += [e.quote or "" for e in element.evidence]
        parts += [texts[e.unit].text for e in element.evidence if e.unit in texts]
        return any("lead" in part.casefold() for part in parts)

    expected = {e.id for e in pet_extraction.elements if mentions_lead(e)}
    found = {e["id"] for e in _index(pet_api_kit, q="Lead")}
    assert expected and found == expected
    by_label = [e for e in pet_extraction.elements if "lead" in e.label.casefold()]
    assert by_label and {e.id for e in by_label} <= found


def test_detail_shows_evidence_before_the_proposal(pet_api_kit: Any, pet_extraction: Any) -> None:
    pet_api_kit.sign_in()
    element = next(e for e in pet_extraction.elements if e.id.startswith("ru_"))
    detail = pet_api_kit.client.get(pet_api_kit.url(f"/elements/{element.id}")).json()
    assert list(detail)[:2] == ["id", "type"]
    assert list(detail).index("evidence") < list(detail).index("record")
    assert detail["evidence"][0]["unit"] == element.evidence[0].unit
    assert detail["evidence"][0]["text"] == pet_extraction.units[element.evidence[0].unit].text
    assert detail["record"]["level_reason"] == element.level_reason
    unknown = pet_api_kit.client.get(pet_api_kit.url("/elements/cn_01JDK7F3Q8ZX5N6M2W4R9T0ZZZ"))
    assert unknown.status_code == 404


def test_bulk_action_returns_a_result_per_id(api_kit: Any, review_kit: Any) -> None:
    ids = review_kit.seed([review_kit.concept(), review_kit.concept("rejected")])
    api_kit.sign_in()
    body = {"action": "level", "ids": ids, "payload": {"level": "level-3", "reason": "detail"}}
    results = api_kit.client.post(api_kit.url("/actions"), json=body).json()["results"]
    assert [(r["element_id"], r["ok"]) for r in results] == [(ids[0], True), (ids[1], False)]
    assert results[1]["message"]
    assert api_kit.session.pending == 1


def test_unknown_action_is_rejected(api_kit: Any, review_kit: Any) -> None:
    ids = review_kit.seed([review_kit.concept()])
    api_kit.sign_in()
    body = {"action": "delete", "ids": ids, "payload": {}}
    assert api_kit.client.post(api_kit.url("/actions"), json=body).status_code == 422


def test_statement_revision_and_authored_element(api_kit: Any, review_kit: Any) -> None:
    api_kit.sign_in()
    created = api_kit.client.post(
        api_kit.url("/statements"), json={"text": "A dog and a cat must be introduced gradually."}
    )
    assert created.status_code == 200, created.text
    unit = created.json()["id"]
    revised = api_kit.client.put(
        api_kit.url(f"/statements/{unit}"), json={"text": "Dogs and cats meet gradually."}
    )
    assert revised.json()["id"] == unit

    fields = {"label": "gradual introduction", "level": "level-2", "evidence": [{"unit": unit}]}
    authored = api_kit.client.post(
        api_kit.url("/elements"), json={"type": "concept", "fields": fields}
    )
    assert authored.status_code == 200, authored.text
    [entry] = _index(api_kit)
    assert (entry["id"], entry["status"]) == (authored.json()["id"], "included")
    assert entry["corpora"] == ["90_user_statements"]

    no_evidence = {"type": "concept", "fields": {"label": "x", "level": "level-2"}}
    refused = api_kit.client.post(api_kit.url("/elements"), json=no_evidence)
    assert refused.status_code == 403 and "evidence" in refused.json()["detail"]


def test_save_returns_the_commit_or_the_hook_output(api_kit: Any, review_kit: Any) -> None:
    [concept] = review_kit.seed([review_kit.concept()])
    api_kit.sign_in()
    body = {"action": "include", "ids": [concept], "payload": {}}
    api_kit.client.post(api_kit.url("/actions"), json=body)
    commits = api_kit.commits()

    api_kit.hook_fails()
    failed = api_kit.client.post(api_kit.url("/save")).json()
    assert not failed["ok"] and failed["sha"] is None
    assert "detect-secrets: a secret was found" in failed["output"]
    assert api_kit.commits() == commits and api_kit.session.pending == 1

    api_kit.hook_fails(False)
    saved = api_kit.client.post(api_kit.url("/save")).json()
    assert saved["ok"] and saved["sha"]
    assert api_kit.commits() == commits + 1


def test_publish_lists_offenders_or_the_version(api_kit: Any, review_kit: Any) -> None:
    concept = review_kit.concept("proposed")
    relation = review_kit.element(
        "relation", "approved", snapshot=True, subject=concept["id"], object=concept["id"]
    )
    review_kit.seed([concept, relation])
    api_kit.sign_in("dora", "domain_admin")

    blocked = api_kit.client.post(api_kit.url("/publish"), json={"version": "1.0.0"}).json()
    assert blocked["version"] is None
    assert [(o["element_id"], o["target_id"]) for o in blocked["offenders"]] == [
        (relation["id"], concept["id"])
    ]

    body = {"action": "approve", "ids": [concept["id"]], "payload": {}}
    api_kit.client.post(api_kit.url("/actions"), json=body)
    refused = api_kit.client.post(api_kit.url("/publish"), json={"version": "1.0.0"})
    assert refused.status_code == 409 and "save" in refused.json()["detail"]
    api_kit.client.post(api_kit.url("/save"))
    published = api_kit.client.post(api_kit.url("/publish"), json={"version": "1.0.0"}).json()
    assert published["version"] == "1.0.0" and published["commit"]["ok"]
    assert "1.0.0" in published["changelog"]


@pytest.fixture
def ingest_kit(review_kit: Any, tmp_path: Path, pet_kit: Any, api_factory: Any) -> Any:
    clients: list[Any] = []

    def llm() -> Any:
        clients.append(pet_kit.client())
        return clients[-1]

    kit = api_factory(tmp_path, review_kit.store, llm, sources_root=pet_kit.manuals_root)
    kit.clients = clients
    yield kit
    kit.close()


DOG = "user-manuals-pets-and-house-rules/dog-owners-manual"


def test_ingestion_estimates_then_runs_only_after_confirm(ingest_kit: Any) -> None:
    ingest_kit.sign_in()
    estimate = ingest_kit.client.post(ingest_kit.url("/ingestions/estimate"), json={"folder": DOG})
    assert estimate.status_code == 200, estimate.text
    shown = estimate.json()
    assert shown["documents"] > 0 and shown["units"] > 0 and shown["input_tokens"] > 0
    assert "cost_usd" in shown and shown["model"]

    unconfirmed = ingest_kit.client.post(ingest_kit.url("/ingestions"), json={"folder": DOG})
    assert unconfirmed.status_code == 409
    assert all(client.calls == 0 for client in ingest_kit.clients), "no LLM call yet"

    body = {"folder": DOG, "confirm": True}
    ran = ingest_kit.client.post(ingest_kit.url("/ingestions"), json=body)
    assert ran.status_code == 200, ran.text
    outcome = ran.json()
    assert outcome["status"] == "completed" and outcome["commit"]["ok"]
    run = ingest_kit.client.get(ingest_kit.url(f"/runs/{outcome['run_id']}")).json()
    assert run["model"] and run["input_tokens"] > 0 and run["ended_at"]
    assert _index(ingest_kit), "the ingested elements are listed"

    again = ingest_kit.client.post(ingest_kit.url("/ingestions/estimate"), json={"folder": DOG})
    assert again.status_code == 409 and "already" in again.json()["detail"]
