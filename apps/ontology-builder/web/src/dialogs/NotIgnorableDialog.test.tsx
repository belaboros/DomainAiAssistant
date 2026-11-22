// Marking passages not ignorable (FR-14, AC-13 in the GUI): the units proposed ignorable, with
// their category and reason; extraction on the chosen ones runs only after the cost confirmation.
import { screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";
import { BODZA, CICERO, RESCUED } from "./fixtures/units";
import { containing, dialog, renderBar } from "./setup";

describe("not_ignorable_dialog", () => {
  test("lists_proposed_ignorable_units_with_their_category", async () => {
    const { user } = renderBar();
    await user.click(screen.getByRole("button", { name: "Mark not ignorable…" }));
    const boxes = await dialog().findAllByRole("checkbox");
    expect(boxes).toHaveLength(2);
    expect(dialog().getByText(BODZA.text)).toBeInTheDocument();
    expect(dialog().getByText(/instance or anecdote/i)).toBeInTheDocument();
    expect(dialog().getByText(/quote or motivational/i)).toBeInTheDocument();
    expect(dialog().queryByText(RESCUED.text)).toBeNull();
  });

  test("extraction_runs_after_the_cost_confirmation", async () => {
    const { api, user } = renderBar();
    await user.click(screen.getByRole("button", { name: "Mark not ignorable…" }));
    await user.click(await dialog().findByRole("checkbox", { name: containing(CICERO.text) }));
    await user.click(dialog().getByRole("button", { name: "Estimate" }));
    await dialog().findByText(/estimated cost/i);
    expect(api.estimate).toHaveBeenCalledWith("pets", { units: [CICERO.id] });
    expect(api.ingest).not.toHaveBeenCalled();
    await user.click(dialog().getByRole("button", { name: /run for about/i }));
    expect(api.ingest).toHaveBeenCalledWith("pets", { units: [CICERO.id] });
    expect(await dialog().findByText("completed")).toBeInTheDocument();
  });

  test("estimate_needs_a_chosen_unit", async () => {
    const { user } = renderBar();
    await user.click(screen.getByRole("button", { name: "Mark not ignorable…" }));
    await dialog().findAllByRole("checkbox");
    expect(dialog().getByRole("button", { name: "Estimate" })).toBeDisabled();
  });
});
