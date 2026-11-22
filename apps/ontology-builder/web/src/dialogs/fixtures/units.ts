// Source units as GET …/units returns them, and a fake of the dialogs' API calls (T26).
import { vi } from "vitest";
import type { IndexEntry, Unit } from "../../api";
import type { WorkApi } from "../workApi";

export const LEASH_RULE: Unit = {
  id: "su_leash",
  kind: "paragraph",
  corpus: "01_rules",
  document: "doc_house",
  text: "Dogs must be kept on a lead of at most 2 m in the stairwell.",
  ignorable: null,
  author: null,
  revisions: 0,
};

export const BODZA: Unit = {
  id: "su_bodza",
  kind: "paragraph",
  corpus: "00_dog",
  document: "doc_dog",
  text: "Our dog Bodza once ate a whole cake.",
  ignorable: {
    proposed: true,
    category: "instance_or_anecdote",
    reason: "A story about one dog.",
    status: "proposed",
  },
  author: null,
  revisions: 0,
};

export const CICERO: Unit = {
  id: "su_cicero",
  kind: "blockquote",
  corpus: "01_rules",
  document: "doc_house",
  text: "A room without books is like a body without a soul.",
  ignorable: {
    proposed: true,
    category: "quote_or_motivational",
    reason: "A quote.",
    status: "proposed",
  },
  author: null,
  revisions: 0,
};

export const RESCUED: Unit = {
  ...CICERO,
  id: "su_rescued",
  text: "Feed a cat twice a day.",
  ignorable: {
    proposed: true,
    category: "procedure",
    reason: "A step list.",
    status: "rejected",
  },
};

export const STATEMENT: Unit = {
  id: "su_intro",
  kind: "user_statement",
  corpus: "90_user_statements",
  document: null,
  text: "A dog and a cat must be introduced gradually.",
  ignorable: null,
  author: "alice",
  revisions: 1,
};

export const UNITS: readonly Unit[] = [LEASH_RULE, BODZA, CICERO, RESCUED, STATEMENT];

function entry(id: string, type: IndexEntry["type"], label: string): IndexEntry {
  return {
    id,
    type,
    label,
    status: "included",
    level: "level-1",
    definition: "",
    corpora: [],
    documents: [],
    search: label,
  };
}

export const ELEMENTS: readonly IndexEntry[] = [
  entry("cn_dog", "concept", "dog"),
  entry("cn_cat", "concept", "cat"),
  entry("ru_lead", "rule", "lead in the stairwell"),
];

/** Every call of the dialogs answered with a plausible value; override what a test needs. */
export function fakeWork(overrides: Partial<WorkApi> = {}) {
  const api = {
    units: vi.fn(() => Promise.resolve([...UNITS])),
    addStatement: vi.fn(() => Promise.resolve("su_new")),
    reviseStatement: vi.fn((_: string, id: string) => Promise.resolve(id)),
    author: vi.fn(() => Promise.resolve("cn_new")),
    estimate: vi.fn(() =>
      Promise.resolve({
        model: "claude-opus-5-5",
        documents: 3,
        units: 412,
        input_tokens: 198_000,
        output_tokens: 118_800,
        cost_usd: 3.18,
      }),
    ),
    ingest: vi.fn(() =>
      Promise.resolve({
        run_id: "run_01",
        status: "completed",
        commit: { ok: true, sha: "0123456789abcdef", output: "" },
      }),
    ),
    runRecord: vi.fn(() =>
      Promise.resolve({
        id: "run_01",
        kind: "ingestion" as const,
        user: "alice",
        model: "claude-opus-5-5",
        source_path: "user-manuals/dog",
        started_at: "2026-11-22T10:00:00Z",
        ended_at: "2026-11-22T10:04:00Z",
        status: "completed" as const,
        input_tokens: 190_123,
        output_tokens: 80_456,
        skipped: [{ where: "doc_dog", item: "a relation", reason: "cites an unknown unit" }],
      }),
    ),
    save: vi.fn(() => Promise.resolve({ ok: true, sha: "abcdef0123456789", output: "" })),
    publish: vi.fn(() =>
      Promise.resolve({
        version: "1.1.0",
        changelog: "# 1.1.0\n\n## Added\n- dog",
        offenders: [],
        warnings: [],
        commit: { ok: true, sha: "fedcba9876543210", output: "" },
      }),
    ),
    ...overrides,
  };
  return api satisfies WorkApi;
}
