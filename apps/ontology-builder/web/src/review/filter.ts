// The filters of the element list (FR-19), applied in the browser to the compact index. Same
// rules as the server's filter_index: type, status and level are exact, corpus and document
// match any of the element's evidence, q is a case-insensitive substring of the search text
// (labels, definitions, statement text, quotes and evidence text). Empty filters are ignored.
import type { Corpus, IndexEntry } from "../api";

export interface IndexFilters {
  type?: string;
  status?: string;
  level?: string;
  corpus?: string;
  document?: string;
  q?: string;
}

export interface DocumentOption {
  id: string;
  label: string;
}

type Test = (entry: IndexEntry) => boolean;

function given(value: string | undefined): string | null {
  const trimmed = value?.trim() ?? "";
  return trimmed === "" ? null : trimmed;
}

/** One test per given filter; an entry matches when it passes all of them. */
function testsOf(filters: IndexFilters): Test[] {
  const tests: Test[] = [];
  const { type, status, level, corpus, document, q } = filters;
  const exact = given(type);
  if (exact !== null) tests.push((e) => e.type === exact);
  const wantedStatus = given(status);
  if (wantedStatus !== null) tests.push((e) => e.status === wantedStatus);
  const wantedLevel = given(level);
  if (wantedLevel !== null) tests.push((e) => e.level === wantedLevel);
  const wantedCorpus = given(corpus);
  if (wantedCorpus !== null) tests.push((e) => e.corpora.includes(wantedCorpus));
  const wantedDocument = given(document);
  if (wantedDocument !== null) tests.push((e) => e.documents.includes(wantedDocument));
  const text = given(q)?.toLowerCase() ?? null;
  if (text !== null) tests.push((e) => e.search.includes(text));
  return tests;
}

/** The entries that match every given filter, in index order. */
export function filterIndex(entries: readonly IndexEntry[], filters: IndexFilters): IndexEntry[] {
  const tests = testsOf(filters);
  if (tests.length === 0) return [...entries];
  return entries.filter((entry) => tests.every((test) => test(entry)));
}

/** The documents of one corpus, or of every corpus when none is chosen, for the filter. */
export function documentsOf(corpora: readonly Corpus[], corpus: string): DocumentOption[] {
  const chosen = corpus === "" ? corpora : corpora.filter((c) => c.folder === corpus);
  return chosen.flatMap((c) => c.documents.map((d) => ({ id: d.id, label: d.title ?? d.path })));
}
