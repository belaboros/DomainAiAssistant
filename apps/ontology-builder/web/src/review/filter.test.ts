// The client filter of the element list (FR-19, AC-18): the same cases as the server's
// test_api_elements.py, on part of the pet fixture's index with the server's answers
// (fixtures/pet-index.json, kept in step by test_api_elements.py::test_gui_pet_index_fixture_matches).
import { describe, expect, test } from "vitest";
import type { Corpus, IndexEntry } from "../api";
import { documentsOf, filterIndex, type IndexFilters } from "./filter";
import petIndex from "./fixtures/pet-index.json";

interface PetFixture {
  elements: IndexEntry[];
  corpora: Corpus[];
  cases: { filters: IndexFilters; expected: string[] }[];
}

// The JSON's own type has plain strings where the API has enums.
const PETS = petIndex as unknown as PetFixture;

const BUILDING_RULES = PETS.corpora.find((c) => c.folder.endsWith("building-and-house-rules"));

function ids(found: IndexEntry[]): string[] {
  return found.map((entry) => entry.id);
}

describe("filterIndex", () => {
  test.each(PETS.cases)("matches_the_server_for_%o", ({ filters, expected }) => {
    expect(ids(filterIndex(PETS.elements, filters))).toEqual(expected);
  });

  test("rule_level1_building_rules_returns_exactly_the_matching_records", () => {
    const folder = BUILDING_RULES?.folder ?? "";
    const found = filterIndex(PETS.elements, { type: "rule", level: "level-1", corpus: folder });
    const expected = PETS.elements.filter(
      (e) => e.type === "rule" && e.level === "level-1" && e.corpora.includes(folder),
    );
    expect(found.length).toBeGreaterThan(0);
    expect(ids(found)).toEqual(ids(expected));
  });

  test("document_filter_keeps_only_elements_citing_that_document", () => {
    const document = BUILDING_RULES?.documents[0]?.id ?? "";
    const found = filterIndex(PETS.elements, { type: "rule", document });
    expect(found.length).toBeGreaterThan(0);
    expect(found.every((e) => e.documents.includes(document))).toBe(true);
  });

  test("search_lead_is_case_insensitive_over_labels_definitions_and_evidence", () => {
    const found = filterIndex(PETS.elements, { q: "LeAd" });
    expect(ids(found)).toEqual(ids(PETS.elements.filter((e) => e.search.includes("lead"))));
    const byLabel = PETS.elements.filter((e) => e.label.toLowerCase().includes("lead"));
    expect(byLabel.length).toBeGreaterThan(0);
    expect(ids(found)).toEqual(expect.arrayContaining(ids(byLabel)));
  });

  test("empty_filters_are_ignored", () => {
    const found = filterIndex(PETS.elements, { type: "", q: "  " });
    expect(found).toHaveLength(PETS.elements.length);
  });

  test("documents_of_a_corpus_or_of_every_corpus", () => {
    const all = documentsOf(PETS.corpora, "");
    const inRules = documentsOf(PETS.corpora, BUILDING_RULES?.folder ?? "");
    expect(inRules.length).toBeGreaterThan(0);
    expect(inRules.length).toBeLessThan(all.length);
    expect(all).toEqual(expect.arrayContaining(inRules));
  });
});
