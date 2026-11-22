// The API wrapper: the write header on every request, the server's message on a refusal, and
// "nobody signed in" for a 401 on the session.
import { afterEach, describe, expect, test, vi } from "vitest";
import { act, type ActionIn, ApiError, currentSession, elementIndex, signIn } from ".";

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
