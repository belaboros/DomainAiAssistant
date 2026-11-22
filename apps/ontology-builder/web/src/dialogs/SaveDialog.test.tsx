// Save (FR-27, AC-25 in the GUI): one commit, shown by its SHA, or the hook's output when a hook
// fails (nothing committed).
import { screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";
import { dialog, renderBar } from "./setup";

describe("save_dialog", () => {
  test("shows_the_commit_sha", async () => {
    const { api, onChanged, user } = renderBar();
    await user.click(screen.getByRole("button", { name: "Save" }));
    expect(api.save).toHaveBeenCalledWith("pets");
    expect(await dialog().findByText(/saved as commit/i)).toHaveTextContent("abcdef0");
    expect(onChanged).toHaveBeenCalled();
    await user.click(dialog().getByRole("button", { name: "Close" }));
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  test("shows_the_hook_output", async () => {
    const failed = () =>
      Promise.resolve({ ok: false, sha: null, output: "check yaml....Failed\nbad indent" });
    const { user } = renderBar({ api: { save: failed } });
    await user.click(screen.getByRole("button", { name: "Save" }));
    expect(await dialog().findByRole("alert")).toHaveTextContent(/nothing was committed/i);
    expect(dialog().getByText(/bad indent/)).toBeInTheDocument();
  });

  test("nothing_to_save", async () => {
    const idle = () => Promise.resolve({ ok: true, sha: null, output: "nothing to save" });
    const { user } = renderBar({ api: { save: idle } });
    await user.click(screen.getByRole("button", { name: "Save" }));
    expect(await dialog().findByText(/nothing to save/i)).toBeInTheDocument();
  });

  test("read_only_session_cannot_write", () => {
    renderBar({ writer: false });
    for (const name of ["New statement…", "Author element…", "Ingest folder…", "Save"]) {
      expect(screen.getByRole("button", { name })).toBeDisabled();
    }
  });
});
