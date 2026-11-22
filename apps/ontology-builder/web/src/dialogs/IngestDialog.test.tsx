// Ingesting a folder (FR-6, AC-6 in the GUI): the estimate first (documents, units, tokens,
// cost), the LLM runs only after the confirmation, then the running state and the run record.
import { screen } from "@testing-library/react";
import { describe, expect, test, vi } from "vitest";
import type { IngestOut } from "../api";
import { dialog, renderBar } from "./setup";

const FOLDER = "user-manuals-pets-and-house-rules/dog-owners-manual";

async function estimated(options: Parameters<typeof renderBar>[0] = {}) {
  const kit = renderBar(options);
  await kit.user.click(screen.getByRole("button", { name: "Ingest folder…" }));
  await kit.user.type(dialog().getByLabelText("Folder"), FOLDER);
  await kit.user.click(dialog().getByRole("button", { name: "Estimate" }));
  await dialog().findByText(/estimated cost/i);
  return kit;
}

describe("ingest_dialog", () => {
  test("shows_counts_tokens_cost", async () => {
    const { api } = await estimated();
    expect(api.estimate).toHaveBeenCalledWith("pets", { folder: FOLDER });
    const shown = screen.getByRole("dialog");
    expect(shown).toHaveTextContent("3 documents");
    expect(shown).toHaveTextContent("412 source units");
    expect(shown).toHaveTextContent("198,000 input tokens");
    expect(shown).toHaveTextContent("118,800 output tokens");
    expect(shown).toHaveTextContent("$3.18");
    expect(shown).toHaveTextContent("claude-opus-5-5");
    expect(api.ingest).not.toHaveBeenCalled();
  });

  test("unknown_price_shows_tokens_only", async () => {
    const unpriced = () =>
      Promise.resolve({
        model: "claude-x",
        documents: 1,
        units: 2,
        input_tokens: 10,
        output_tokens: 6,
        cost_usd: null,
      });
    await estimated({ api: { estimate: unpriced } });
    expect(screen.getByRole("dialog")).toHaveTextContent(/no price is known for claude-x/i);
  });

  test("runs_after_confirm_then_shows_the_run_record", async () => {
    let finish: (out: IngestOut) => void = () => undefined;
    const pending = new Promise<IngestOut>((resolve) => {
      finish = resolve;
    });
    const { api, onChanged, user } = await estimated({ api: { ingest: vi.fn(() => pending) } });
    await user.click(dialog().getByRole("button", { name: /run for about \$3\.18/i }));
    expect(api.ingest).toHaveBeenCalledWith("pets", { folder: FOLDER });
    expect(await dialog().findByText(/running/i)).toBeInTheDocument();
    finish({
      run_id: "run_01",
      status: "completed",
      commit: { ok: true, sha: "0123456789abcdef", output: "" },
    });
    expect(await dialog().findByText("completed")).toBeInTheDocument();
    expect(api.runRecord).toHaveBeenCalledWith("pets", "run_01");
    const shown = screen.getByRole("dialog");
    expect(shown).toHaveTextContent("190,123 input tokens");
    expect(shown).toHaveTextContent("80,456 output tokens");
    expect(shown).toHaveTextContent("2026-11-22T10:04:00Z");
    expect(shown).toHaveTextContent("cites an unknown unit");
    expect(shown).toHaveTextContent("0123456");
    expect(onChanged).toHaveBeenCalled();
  });

  test("failing_hook_after_the_run_is_shown", async () => {
    const hooked = () =>
      Promise.resolve({
        run_id: "run_01",
        status: "completed",
        commit: { ok: false, sha: null, output: "gitleaks: leak found" },
      });
    const { user } = await estimated({ api: { ingest: hooked } });
    await user.click(dialog().getByRole("button", { name: /run for about/i }));
    expect(await dialog().findByText("gitleaks: leak found")).toBeInTheDocument();
  });

  test("refused_estimate_is_shown", async () => {
    const refused = () => Promise.reject(new Error("the folder was already ingested"));
    const { user } = renderBar({ api: { estimate: refused } });
    await user.click(screen.getByRole("button", { name: "Ingest folder…" }));
    await user.type(dialog().getByLabelText("Folder"), FOLDER);
    await user.click(dialog().getByRole("button", { name: "Estimate" }));
    expect(await dialog().findByRole("alert")).toHaveTextContent("already ingested");
  });
});
