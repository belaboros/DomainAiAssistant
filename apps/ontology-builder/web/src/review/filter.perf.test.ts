// NFR responsiveness on the client: filtering an index of 5,000 elements takes under 100 ms.
import { describe, expect, test } from "vitest";
import type { IndexEntry } from "../api";
import { filterIndex } from "./filter";

const TYPES = ["statement", "term", "concept", "relation", "rule", "property"] as const;
const LEVELS = ["level-1", "level-2", "level-3", "ignorable"] as const;

function entry(n: number): IndexEntry {
  const type = TYPES[n % TYPES.length] ?? "concept";
  const level = LEVELS[n % LEVELS.length] ?? "level-1";
  const text = `element ${String(n)} about a dog on a lead in the stairwell, kept for the house`;
  return {
    id: `cn_${String(n).padStart(26, "0")}`,
    type,
    label: `element ${String(n)}`,
    status: "proposed",
    level,
    definition: text,
    corpora: [`0${String(n % 3)}_corpus`],
    documents: [`doc_${String(n % 40)}`],
    search: `${text} ${text} ${text}`.repeat(4),
  };
}

describe("filterIndex performance", () => {
  test("filters_5000_elements_under_100_ms", () => {
    const index = Array.from({ length: 5000 }, (_, n) => entry(n));
    filterIndex(index, { q: "warm-up" });
    const started = performance.now();
    const found = filterIndex(index, { type: "rule", level: "level-1", q: "Stairwell" });
    const searched = filterIndex(index, { q: "no such text" });
    const took = performance.now() - started;
    expect(found.length).toBeGreaterThan(0);
    expect(searched).toHaveLength(0);
    expect(took).toBeLessThan(100);
  });
});
