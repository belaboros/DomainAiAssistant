// The API wrapper: the write header on every request, the server's message on a refusal, and
// "nobody signed in" for a 401 on the session.
import { afterEach, describe, expect, test, vi } from "vitest";
import {
  act,
  type ActionIn,
  addStatement,
  ApiError,
  author,
  currentSession,
  elementDetail,
  elementIndex,
  estimate,
  ingest,
  publish,
  reviseStatement,
  runRecord,
  save,
  signIn,
  units,
} from ".";

function reply(status: number, body: unknown) {
  const fetch = vi.fn<(request: Request) => Promise<Response>>(() =>
    Promise.resolve(
      new Response(JSON.stringify(body), {
        status,
        headers: { "Content-Type": "application/json" },
      }),
    ),
  );
  vi.stubGlobal("fetch", fetch);
  return fetch;
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("api", () => {
  test("sign_in_posts_with_the_write_header", async () => {
    const fetch = reply(200, { user: "alice", role: "user", writer: true, ontology: "pets" });
    await expect(signIn({ user: "alice", role: "user" })).resolves.toMatchObject({
      user: "alice",
    });
    const request = fetch.mock.calls[0]?.[0];
    expect(request?.method).toBe("POST");
    expect(new URL(request?.url ?? "").pathname).toBe("/api/session");
    expect(request?.headers.get("X-Ontology-Builder")).toBe("1");
    expect(await request?.json()).toEqual({ user: "alice", role: "user" });
  });

  test("refusal_carries_the_server_message", async () => {
    reply(403, { detail: "only a domain admin can publish" });
    const refusal = signIn({ user: "alice", role: "user" });
    await expect(refusal).rejects.toThrow(ApiError);
    await expect(refusal).rejects.toMatchObject({
      message: "only a domain admin can publish",
      status: 403,
    });
  });

  test("no_session_is_null", async () => {
    reply(401, { detail: "sign in first" });
    await expect(currentSession()).resolves.toBeNull();
  });

  test("unreachable_server_is_reported", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.reject(new TypeError("fetch failed"))),
    );
    await expect(currentSession()).rejects.toThrow("the server is not reachable");
  });

  test("element_index_reads_the_open_ontology", async () => {
    const fetch = reply(200, { elements: [], corpora: [], pending: 0 });
    await expect(elementIndex("pets-and-house-rules")).resolves.toEqual({
      elements: [],
      corpora: [],
      pending: 0,
    });
    const request = fetch.mock.calls[0]?.[0];
    expect(request?.method).toBe("GET");
    expect(new URL(request?.url ?? "").pathname).toBe(
      "/api/ontologies/pets-and-house-rules/elements",
    );
  });

  test("element_detail_reads_one_element", async () => {
    const fetch = reply(200, { id: "cn_1", type: "concept" });
    await expect(elementDetail("pets", "cn_1")).resolves.toMatchObject({ id: "cn_1" });
    const request = fetch.mock.calls[0]?.[0];
    expect(request?.method).toBe("GET");
    expect(new URL(request?.url ?? "").pathname).toBe("/api/ontologies/pets/elements/cn_1");
  });

  test("act_posts_the_action_ids_and_payload", async () => {
    const results = [{ element_id: "cn_1", ok: true, message: "level-3" }];
    const fetch = reply(200, { results, pending: 1 });
    const body: ActionIn = { action: "level", ids: ["cn_1"], payload: { level: "level-3" } };
    await expect(act("pets", body)).resolves.toEqual({ results, pending: 1 });
    const request = fetch.mock.calls[0]?.[0];
    expect(request?.method).toBe("POST");
    expect(new URL(request?.url ?? "").pathname).toBe("/api/ontologies/pets/actions");
    expect(request?.headers.get("X-Ontology-Builder")).toBe("1");
    expect(await request?.json()).toEqual(body);
  });
});

describe("api writes of the work bar", () => {
  test("estimate_never_confirms_and_ingest_always_does", async () => {
    const fetch = reply(200, {});
    await estimate("pets", { folder: "manuals/dog" });
    await ingest("pets", { units: ["su_1"] });
    const [first, second] = fetch.mock.calls.map((call) => call[0]);
    expect(new URL(first?.url ?? "").pathname).toBe("/api/ontologies/pets/ingestions/estimate");
    expect(await first?.json()).toEqual({ folder: "manuals/dog", confirm: false });
    expect(new URL(second?.url ?? "").pathname).toBe("/api/ontologies/pets/ingestions");
    expect(await second?.json()).toEqual({ units: ["su_1"], confirm: true });
  });

  test("statements_authoring_units_and_runs_use_their_routes", async () => {
    const fetch = reply(200, { id: "su_1" });
    await expect(addStatement("pets", "Cats nap.")).resolves.toBe("su_1");
    await reviseStatement("pets", "su_1", "Cats nap a lot.");
    await author("pets", { type: "concept", fields: { label: "nap" } });
    await units("pets");
    await runRecord("pets", "run_01");
    const calls = fetch.mock.calls.map((call) => call[0]);
    expect(calls.map((r) => `${r.method} ${new URL(r.url).pathname}`)).toEqual([
      "POST /api/ontologies/pets/statements",
      "PUT /api/ontologies/pets/statements/su_1",
      "POST /api/ontologies/pets/elements",
      "GET /api/ontologies/pets/units",
      "GET /api/ontologies/pets/runs/run_01",
    ]);
    expect(await calls[1]?.json()).toEqual({ text: "Cats nap a lot." });
  });

  test("save_and_publish_post_with_the_write_header", async () => {
    const fetch = reply(200, { ok: true, sha: "abc", output: "" });
    await save("pets");
    await publish("pets", null);
    const [saved, published] = fetch.mock.calls.map((call) => call[0]);
    expect(new URL(saved?.url ?? "").pathname).toBe("/api/ontologies/pets/save");
    expect(saved?.headers.get("X-Ontology-Builder")).toBe("1");
    expect(new URL(published?.url ?? "").pathname).toBe("/api/ontologies/pets/publish");
    expect(await published?.json()).toEqual({ version: null });
  });
});
