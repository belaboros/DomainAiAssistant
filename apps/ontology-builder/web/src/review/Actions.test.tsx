// The actions on one element (FR-17, AC-16 in the GUI; AC-3 in the GUI): a button for every
// action, a dialog for those that need more (a reason, a field, a target), admin-only actions
// disabled for a user with a refusal message, and the keyboard shortcuts x, i, e, 1–3 and a.
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, test, vi } from "vitest";
import type { ActionResult, ElementDetail, IndexEntry, Role } from "../api";
import { Actions, type DetailAct } from "./Actions";
import { CONCEPT, ELEMENTS, TERM } from "./fixtures/detail";

function allOk(): Promise<ActionResult[]> {
  return Promise.resolve([{ element_id: "x", ok: true, message: "done" }]);
}

interface Options {
  detail?: ElementDetail;
  role?: Role;
  writer?: boolean;
  act?: DetailAct;
  elements?: readonly IndexEntry[];
}

function setup(options: Options = {}) {
  const act = vi.fn(options.act ?? allOk);
  render(
    <Actions
      detail={options.detail ?? CONCEPT}
      elements={options.elements ?? ELEMENTS}
      role={options.role ?? "user"}
      writer={options.writer ?? true}
      act={act}
    />,
  );
  return { act, user: userEvent.setup() };
}

function dialog() {
  return within(screen.getByRole("dialog"));
}

describe("each_action_calls_api", () => {
  test("include", async () => {
    const { act, user } = setup();
    await user.click(screen.getByRole("button", { name: "Include" }));
    expect(act).toHaveBeenLastCalledWith("include", {});
  });

  test("exclude_with_a_reason", async () => {
    const { act, user } = setup();
    await user.click(screen.getByRole("button", { name: "Exclude…" }));
    expect(dialog().getByRole("button", { name: "Exclude" })).toBeDisabled();
    await user.type(dialog().getByLabelText("Reason"), "an anecdote");
    await user.click(dialog().getByRole("button", { name: "Exclude" }));
    expect(act).toHaveBeenLastCalledWith("exclude", { reason: "an anecdote" });
  });

  test("correct_a_field", async () => {
    const { act, user } = setup();
    await user.click(screen.getByRole("button", { name: "Correct…" }));
    await user.selectOptions(dialog().getByLabelText("Field"), "definition");
    const value = dialog().getByLabelText("New value");
    expect(value).toHaveValue("A strap to hold a dog.");
    await user.clear(value);
    await user.type(value, "A strap or cord to walk a dog.");
    await user.type(dialog().getByLabelText("Reason"), "clearer");
    await user.click(dialog().getByRole("button", { name: "Correct" }));
    expect(act).toHaveBeenLastCalledWith("correct", {
      field: "definition",
      value: "A strap or cord to walk a dog.",
      reason: "clearer",
    });
  });

  test("override_the_level", async () => {
    const { act, user } = setup();
    await user.click(screen.getByRole("button", { name: "Set level…" }));
    await user.selectOptions(dialog().getByLabelText("Level"), "level-3");
    await user.type(dialog().getByLabelText("Reason"), "a detail");
    await user.click(dialog().getByRole("button", { name: "Set level" }));
    expect(act).toHaveBeenLastCalledWith("level", { level: "level-3", reason: "a detail" });
  });

  test("merge_as_synonym_offers_other_concepts_only", async () => {
    const { act, user } = setup();
    expect(screen.queryByRole("button", { name: "Split senses…" })).not.toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Merge into…" }));
    const keep = dialog().getByLabelText("Keep concept");
    expect(within(keep).queryByRole("option", { name: /^leash/ })).not.toBeInTheDocument();
    expect(within(keep).queryByRole("option", { name: /lead \(term\)/ })).not.toBeInTheDocument();
    await user.selectOptions(keep, "cn_lead");
    await user.click(dialog().getByRole("button", { name: "Merge" }));
    expect(act).toHaveBeenLastCalledWith("merge", { into: "cn_lead" });
  });

  test("split_senses_of_a_term", async () => {
    const { act, user } = setup({ detail: TERM });
    expect(screen.queryByRole("button", { name: "Merge into…" })).not.toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Split senses…" }));
    await user.click(dialog().getByRole("checkbox", { name: /a lead of at most 2 m/ }));
    await user.type(dialog().getByLabelText("Label of the new sense"), "lead (electric)");
    await user.type(dialog().getByLabelText("Scope note of the new sense"), "a cable");
    await user.click(dialog().getByRole("button", { name: "Split" }));
    expect(act).toHaveBeenLastCalledWith("split", {
      units: ["su_two"],
      label: "lead (electric)",
      scope_note: "a cable",
    });
  });

  test("reassign_a_mention", async () => {
    const { act, user } = setup({ detail: TERM });
    await user.click(screen.getByRole("button", { name: "Reassign mention…" }));
    await user.selectOptions(dialog().getByLabelText("Mention"), "su_two");
    await user.selectOptions(dialog().getByLabelText("Move to concept"), "cn_leash");
    await user.click(dialog().getByRole("button", { name: "Reassign" }));
    expect(act).toHaveBeenLastCalledWith("reassign", { unit: "su_two", concept: "cn_leash" });
  });
});

describe("Actions", () => {
  test("admin_actions_disabled_for_user", async () => {
    const { act, user } = setup({ role: "user" });
    for (const name of ["Approve", "Reject…", "Deprecate…"]) {
      expect(screen.getByRole("button", { name })).toBeDisabled();
    }
    expect(screen.getByText(/only a domain admin can approve, reject or deprecate/i)).toBeVisible();
    await user.keyboard("a");
    expect(await screen.findByRole("alert")).toHaveTextContent("Only a domain admin can approve.");
    expect(act).not.toHaveBeenCalled();
  });

  test("admin_approves_rejects_and_deprecates", async () => {
    const { act, user } = setup({ role: "domain_admin" });
    await user.click(screen.getByRole("button", { name: "Approve" }));
    expect(act).toHaveBeenLastCalledWith("approve", {});

    await user.click(screen.getByRole("button", { name: "Reject…" }));
    await user.type(dialog().getByLabelText("Reason"), "out of scope");
    await user.click(dialog().getByRole("button", { name: "Reject" }));
    expect(act).toHaveBeenLastCalledWith("reject", { reason: "out of scope" });

    await user.click(screen.getByRole("button", { name: "Deprecate…" }));
    await user.selectOptions(dialog().getByLabelText("Replaced by"), "cn_lead");
    await user.click(dialog().getByRole("button", { name: "Deprecate" }));
    expect(act).toHaveBeenLastCalledWith("deprecate", { replacement: "cn_lead" });
  });

  test("dialog_can_be_cancelled_with_escape", async () => {
    const { act, user } = setup();
    await user.click(screen.getByRole("button", { name: "Exclude…" }));
    await user.keyboard("{Escape}");
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(act).not.toHaveBeenCalled();
  });

  test("refusal_is_shown_with_the_server_message", async () => {
    const act: DetailAct = () =>
      Promise.resolve([{ element_id: "cn_leash", ok: false, message: "cn_leash is excluded" }]);
    const { user } = setup({ act });
    await user.click(screen.getByRole("button", { name: "Include" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("cn_leash is excluded");
  });

  test("failure_is_shown", async () => {
    const act: DetailAct = () => Promise.reject(new Error("the server is not reachable"));
    const { user } = setup({ act });
    await user.click(screen.getByRole("button", { name: "Include" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("the server is not reachable");
  });

  test("read_only_session_cannot_act", async () => {
    const { act, user } = setup({ writer: false, role: "domain_admin" });
    for (const name of ["Include", "Exclude…", "Correct…", "Set level…", "Approve"]) {
      expect(screen.getByRole("button", { name })).toBeDisabled();
    }
    await user.keyboard("i");
    expect(act).not.toHaveBeenCalled();
  });

  test("keyboard_shortcuts", async () => {
    const { act, user } = setup({ role: "domain_admin" });
    await user.keyboard("i");
    expect(act).toHaveBeenLastCalledWith("include", {});
    await user.keyboard("2");
    expect(act).toHaveBeenLastCalledWith("level", { level: "level-2" });
    await user.keyboard("a");
    expect(act).toHaveBeenLastCalledWith("approve", {});

    await user.keyboard("x");
    expect(screen.getByRole("dialog", { name: /exclude/i })).toBeInTheDocument();
    // typing in the dialog is not a shortcut
    await user.type(dialog().getByLabelText("Reason"), "i1a");
    expect(act).toHaveBeenCalledTimes(3);
    await user.keyboard("{Escape}");

    await user.keyboard("e");
    expect(screen.getByRole("dialog", { name: /correct/i })).toBeInTheDocument();
  });
});
