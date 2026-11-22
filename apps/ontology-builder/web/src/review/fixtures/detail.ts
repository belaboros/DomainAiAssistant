// Element details as GET …/elements/{id} returns them, for the detail and action tests (T25).
import type { Corpus, ElementDetail, IndexEntry } from "../../api";

const ORIGIN = { kind: "llm", run_id: "run_01", created_at: "2026-11-20T10:00:00Z" };

export const CONCEPT: ElementDetail = {
  id: "cn_leash",
  type: "concept",
  evidence: [
    {
      unit: "su_one",
      quote: "on a leash",
      text: "Dogs must be kept on a leash in the stairwell.",
      corpus: "02_rules",
      document: "doc_house",
    },
    { unit: "su_gone", quote: null, text: null, corpus: null, document: null },
  ],
  record: {
    label: "leash",
    definition: "A strap to hold a dog.",
    level: "level-1",
    level_reason: "Every resident with a dog needs it.",
    status: "proposed",
    origin: ORIGIN,
    scope_note: "Also called a lead.",
    parents: ["cn_equipment"],
  },
  decisions: [
    {
      id: "dc_1",
      at: "2026-11-21T09:30:00Z",
      user: "alice",
      role: "user",
      action: "level",
      field: "level",
      old: "level-2",
      new: "level-1",
      reason: "core to the house rules",
    },
  ],
  pending: true,
};

export const TERM: ElementDetail = {
  id: "tm_lead",
  type: "term",
  evidence: [
    {
      unit: "su_one",
      text: "Dogs must be kept on a lead in the stairwell.",
      corpus: "02_rules",
      document: "doc_house",
    },
    {
      unit: "su_two",
      text: "Use a lead of at most 2 m.",
      corpus: "00_dogs",
      document: "doc_dogs",
    },
  ],
  record: {
    label: "lead",
    level: "level-2",
    level_reason: "A synonym of leash.",
    status: "included",
    origin: { kind: "user", author: "bob", created_at: "2026-11-20T11:00:00Z" },
    mentions: [
      { unit: "su_one", concept: "cn_lead" },
      { unit: "su_two", concept: "cn_lead" },
    ],
  },
  decisions: [],
  pending: false,
};

function entry(id: string, type: IndexEntry["type"], label: string): IndexEntry {
  return {
    id,
    type,
    label,
    status: "proposed",
    level: "level-2",
    definition: "",
    corpora: [],
    documents: [],
    search: label,
  };
}

export const ELEMENTS: readonly IndexEntry[] = [
  entry("cn_leash", "concept", "leash"),
  entry("cn_lead", "concept", "lead"),
  entry("tm_lead", "term", "lead"),
];

export const CORPORA: readonly Corpus[] = [
  {
    folder: "02_rules",
    source_path: "rules",
    documents: [{ id: "doc_house", path: "rules/house.md", title: "House rules" }],
  },
];
