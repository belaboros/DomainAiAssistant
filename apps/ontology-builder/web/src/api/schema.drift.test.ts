// @vitest-environment node
// The API types must match openapi.json (plan 0002, T23): a fresh rendering of
// scripts/gen-api.ts must equal the committed src/api/schema.gen.ts.
import { expect, test } from "vitest";
import { render } from "../../scripts/gen-api";
import committed from "./schema.gen.ts?raw";

test("generated_types_match_openapi_json", async () => {
  const hint = "src/api/schema.gen.ts is stale: run `npm run gen:api` in apps/ontology-builder/web";
  expect(committed, hint).toBe(await render());
});
