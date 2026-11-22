// The only way the GUI talks to the back end (plan 0002: web → api over HTTP, no import edge).
// A typed openapi-fetch client over the types generated from openapi.json
// (ontology-builder/ADR-0011): same-origin cookies, the write header the server's guard asks
// for, and refusals turned into errors that carry the server's message.
import createClient from "openapi-fetch";
import type { components, paths } from "./schema.gen";

type Schemas = components["schemas"];
export type Role = Schemas["Role"];
export type SessionOut = Schemas["SessionOut"];
export type SignIn = Schemas["SignIn"];
export type IndexEntry = Schemas["IndexEntryOut"];
export type Corpus = Schemas["CorpusOut"];
export type ElementsOut = Schemas["ElementsOut"];
export type ElementStatus = Schemas["ElementStatus"];
export type Level = Schemas["Level"];
export type ElementType = IndexEntry["type"];
export type ActionIn = Schemas["ActionIn"];
export type ActionName = ActionIn["action"];
export type ActionsOut = Schemas["ActionsOut"];
export type ActionResult = Schemas["ActionResultOut"];

/** Every write needs this header (the server refuses a write without it). */
export const WRITE_HEADER = { "X-Ontology-Builder": "1" } as const;

export const api = createClient<paths>({
  credentials: "same-origin",
  headers: WRITE_HEADER,
  // Looked up on each call rather than captured once, so tests can stub the global fetch.
  fetch: (request) => globalThis.fetch(request),
});

/** A refusal or failure of an API call, with the server's message and HTTP status. */
export class ApiError extends Error {
  readonly status: number | undefined;

  constructor(message: string, status: number | undefined) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function detailOf(error: unknown): string | undefined {
  if (typeof error !== "object" || error === null || !("detail" in error)) return undefined;
  const { detail } = error;
  if (typeof detail === "string") return detail;
  return Array.isArray(detail) ? "the server refused the request as invalid" : undefined;
}

interface Outcome<T> {
  data?: T;
  error?: unknown;
  response: Response;
}

/** The data of a successful call, or an ApiError with the server's message. */
export async function unwrap<T>(call: Promise<Outcome<T>>): Promise<T> {
  let outcome: Outcome<T>;
  try {
    outcome = await call;
  } catch {
    throw new ApiError("the server is not reachable", undefined);
  }
  const { data, error, response } = outcome;
  if (response.ok && data !== undefined) return data;
  const { status } = response;
  throw new ApiError(detailOf(error) ?? `the request failed (HTTP ${String(status)})`, status);
}

/** The signed-in session, or null when nobody is signed in in this browser. */
export async function currentSession(): Promise<SessionOut | null> {
  try {
    return await unwrap(api.GET("/api/session"));
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) return null;
    throw error;
  }
}

export function signIn(body: SignIn): Promise<SessionOut> {
  return unwrap(api.POST("/api/session", { body }));
}

export async function signOut(): Promise<void> {
  await unwrap(api.DELETE("/api/session"));
}

/** The compact index of every element of the open ontology, and its corpora (FR-19). */
export function elementIndex(ontology: string): Promise<ElementsOut> {
  return unwrap(
    api.GET("/api/ontologies/{name}/elements", { params: { path: { name: ontology } } }),
  );
}

/** One action on every ID; the server checks role and status per ID (FR-17, FR-18). */
export function act(ontology: string, body: ActionIn): Promise<ActionsOut> {
  return unwrap(
    api.POST("/api/ontologies/{name}/actions", { params: { path: { name: ontology } }, body }),
  );
}
