// New and edited user statements (FR-21, AC-20 in the GUI): a new one is posted, an edit is a
// new revision of the chosen statement, under the same ID.
import { screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";
import { STATEMENT } from "./fixtures/units";
import { dialog, renderBar } from "./setup";

describe("statement_dialogs", () => {
  test("new_statement_is_posted", async () => {
    const { api, onChanged, user } = renderBar();
    await user.click(screen.getByRole("button", { name: "New statement…" }));
    expect(dialog().getByRole("button", { name: "Add statement" })).toBeDisabled();
    await user.type(dialog().getByLabelText("Statement"), "Cats nap a lot.");
    await user.click(dialog().getByRole("button", { name: "Add statement" }));
    expect(api.addStatement).toHaveBeenCalledWith("pets", "Cats nap a lot.");
    expect(onChanged).toHaveBeenCalled();
    expect(screen.queryByRole("dialog")).toBeNull();
    expect(await screen.findByRole("status")).toHaveTextContent("su_new");
  });

  test("edit_makes_a_revision_of_the_chosen_statement", async () => {
    const { api, user } = renderBar();
    await user.click(screen.getByRole("button", { name: "Edit statement…" }));
    const text = await dialog().findByLabelText("Statement");
    expect(dialog().getByLabelText("User statement")).toHaveValue(STATEMENT.id);
    expect(text).toHaveValue(STATEMENT.text);
    await user.clear(text);
    await user.type(text, "Dogs and cats meet gradually.");
    await user.click(dialog().getByRole("button", { name: "Save revision" }));
    expect(api.reviseStatement).toHaveBeenCalledWith(
      "pets",
      STATEMENT.id,
      "Dogs and cats meet gradually.",
    );
  });

  test("edit_without_statements_says_so", async () => {
    const { user } = renderBar({ api: { units: () => Promise.resolve([]) } });
    await user.click(screen.getByRole("button", { name: "Edit statement…" }));
    expect(await dialog().findByText(/no user statements yet/i)).toBeInTheDocument();
  });

  test("refusal_is_shown_in_the_dialog", async () => {
    const refused = () => Promise.reject(new Error("the statement is empty"));
    const { user } = renderBar({ api: { addStatement: refused } });
    await user.click(screen.getByRole("button", { name: "New statement…" }));
    await user.type(dialog().getByLabelText("Statement"), "x");
    await user.click(dialog().getByRole("button", { name: "Add statement" }));
    expect(await dialog().findByRole("alert")).toHaveTextContent("the statement is empty");
  });
});
