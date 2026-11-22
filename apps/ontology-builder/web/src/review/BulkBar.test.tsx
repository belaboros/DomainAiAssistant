// The bulk bar (FR-18, AC-17): include, exclude and set the level of every selected element in
// one step; a domain admin can also approve and reject them. Results come back per ID.
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, test, vi } from "vitest";
import type { ActionResult, Role } from "../api";
import { BulkBar, type BulkAct } from "./BulkBar";

const TWENTY = Array.from({ length: 20 }, (_, n) => `cn_${String(n).padStart(2, "0")}`);

function allOk(_action: string, ids: readonly string[]): Promise<ActionResult[]> {
  return Promise.resolve(ids.map((id) => ({ element_id: id, ok: true, message: "done" })));
}

function setup(options: { role?: Role; writer?: boolean; selected?: string[]; act?: BulkAct }) {
  const act = vi.fn(options.act ?? allOk);
  const onClear = vi.fn();
  render(
    <BulkBar
      selected={options.selected ?? TWENTY}
      role={options.role ?? "user"}
      writer={options.writer ?? true}
      act={act}
      onClear={onClear}
    />,
  );
  return { act, onClear, user: userEvent.setup() };
}

describe("BulkBar", () => {
  test("sets_level_3_on_20_selected_in_one_step", async () => {
    const { act, user } = setup({});
    expect(screen.getByText("20 selected")).toBeInTheDocument();
    await user.selectOptions(screen.getByLabelText(/set level to/i), "level-3");
    await user.click(screen.getByRole("button", { name: "Set level" }));
    expect(act).toHaveBeenCalledOnce();
    expect(act).toHaveBeenCalledWith("level", TWENTY, { level: "level-3" });
    expect(await screen.findByRole("status")).toHaveTextContent("20 changed");
  });

  test("include_all_selected", async () => {
    const { act, user } = setup({});
    await user.click(screen.getByRole("button", { name: "Include" }));
    expect(act).toHaveBeenCalledWith("include", TWENTY, {});
  });

  test("user_cannot_bulk_approve_or_reject", () => {
    setup({ role: "user" });
    expect(screen.queryByRole("button", { name: /approve/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reject/i })).not.toBeInTheDocument();
  });

  test("admin_can_bulk_approve", async () => {
    const { act, user } = setup({ role: "domain_admin" });
    await user.click(screen.getByRole("button", { name: "Approve" }));
    expect(act).toHaveBeenCalledWith("approve", TWENTY, {});
    expect(await screen.findByRole("status")).toHaveTextContent("20 changed");
  });

  test("exclude_needs_a_reason", async () => {
    const { act, user } = setup({});
    await user.click(screen.getByRole("button", { name: "Exclude…" }));
    const confirm = screen.getByRole("button", { name: "Exclude 20" });
    expect(confirm).toBeDisabled();
    await user.type(screen.getByLabelText(/reason for excluding/i), "an anecdote");
    await user.click(confirm);
    expect(act).toHaveBeenCalledWith("exclude", TWENTY, { reason: "an anecdote" });
  });

  test("admin_reject_needs_a_reason", async () => {
    const { act, user } = setup({ role: "domain_admin" });
    await user.click(screen.getByRole("button", { name: "Reject…" }));
    await user.type(screen.getByLabelText(/reason for rejecting/i), "out of scope");
    await user.click(screen.getByRole("button", { name: "Reject 20" }));
    expect(act).toHaveBeenCalledWith("reject", TWENTY, { reason: "out of scope" });
  });

  test("reason_can_be_cancelled", async () => {
    const { act, user } = setup({});
    await user.click(screen.getByRole("button", { name: "Exclude…" }));
    await user.click(screen.getByRole("button", { name: "Cancel" }));
    expect(screen.queryByLabelText(/reason for excluding/i)).not.toBeInTheDocument();
    expect(act).not.toHaveBeenCalled();
  });

  test("refused_ids_are_listed_with_the_server_message", async () => {
    const act: BulkAct = (_action, ids) =>
      Promise.resolve(
        ids.map((id, n) =>
          n < 2
            ? { element_id: id, ok: false, message: `${id} is excluded: refused` }
            : { element_id: id, ok: true, message: "done" },
        ),
      );
    const { user } = setup({ act });
    await user.click(screen.getByRole("button", { name: "Include" }));
    const result = await screen.findByRole("status");
    expect(result).toHaveTextContent("18 changed, 2 refused");
    expect(result).toHaveTextContent("cn_00 is excluded: refused");
    expect(result).toHaveTextContent("cn_01 is excluded: refused");
  });

  test("server_refusal_is_shown", async () => {
    const act: BulkAct = () => Promise.reject(new Error("only a domain admin can approve"));
    const { user } = setup({ role: "domain_admin", act });
    await user.click(screen.getByRole("button", { name: "Approve" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("only a domain admin can approve");
  });

  test("read_only_session_cannot_act", () => {
    setup({ writer: false, role: "domain_admin" });
    for (const name of ["Include", "Exclude…", "Set level", "Approve", "Reject…"]) {
      expect(screen.getByRole("button", { name })).toBeDisabled();
    }
  });

  test("nothing_selected_disables_actions", () => {
    setup({ selected: [] });
    expect(screen.getByText("0 selected")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Include" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Set level" })).toBeDisabled();
  });

  test("clear_selection", async () => {
    const { onClear, user } = setup({});
    await user.click(screen.getByRole("button", { name: "Clear selection" }));
    expect(onClear).toHaveBeenCalledOnce();
  });
});
