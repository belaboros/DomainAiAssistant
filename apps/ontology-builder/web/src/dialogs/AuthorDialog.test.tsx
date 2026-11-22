// Authoring an element (FR-22, AC-21 in the GUI): the fields of its type, a level, and evidence
// picked from the source units (corpus passages and user statements); without evidence the
// dialog cannot be sent.
import { screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";
import { LEASH_RULE, STATEMENT } from "./fixtures/units";
import { containing, dialog, renderBar } from "./setup";

async function openAuthor() {
  const kit = renderBar();
  await kit.user.click(screen.getByRole("button", { name: "Author element…" }));
  await dialog().findByLabelText("Find a passage");
  return kit;
}

describe("author_dialog", () => {
  test("concept_without_definition_from_a_statement", async () => {
    const { api, onChanged, user } = await openAuthor();
    await user.type(dialog().getByLabelText("Label"), "gradual introduction");
    await user.selectOptions(dialog().getByLabelText("Level"), "level-2");
    const submit = dialog().getByRole("button", { name: "Author" });
    expect(submit).toBeDisabled();
    await user.click(dialog().getByRole("checkbox", { name: containing(STATEMENT.text) }));
    await user.click(submit);
    expect(api.author).toHaveBeenCalledWith("pets", {
      type: "concept",
      fields: {
        label: "gradual introduction",
        level: "level-2",
        evidence: [{ unit: STATEMENT.id }],
      },
    });
    expect(onChanged).toHaveBeenCalled();
    expect(await screen.findByRole("status")).toHaveTextContent("cn_new");
  });

  test("evidence_is_required", async () => {
    const { user } = await openAuthor();
    await user.type(dialog().getByLabelText("Label"), "x");
    expect(dialog().getByRole("button", { name: "Author" })).toBeDisabled();
    expect(dialog().getByText(/pick at least one passage/i)).toBeInTheDocument();
  });

  test("picker_searches_passages", async () => {
    const { user } = await openAuthor();
    await user.type(dialog().getByLabelText("Find a passage"), "stairwell");
    const boxes = dialog().getAllByRole("checkbox");
    expect(boxes).toHaveLength(1);
    expect(boxes[0]?.closest("label")).toHaveTextContent(LEASH_RULE.text);
  });

  test("relation_asks_for_subject_predicate_and_object", async () => {
    const { api, user } = await openAuthor();
    await user.selectOptions(dialog().getByLabelText("Type"), "relation");
    await user.type(dialog().getByLabelText("Label"), "dog meets cat");
    await user.selectOptions(dialog().getByLabelText("Subject"), "cn_dog");
    await user.type(dialog().getByLabelText("Predicate label"), "meets");
    await user.selectOptions(dialog().getByLabelText("Object"), "cn_cat");
    await user.click(dialog().getByRole("checkbox", { name: containing(STATEMENT.text) }));
    await user.click(dialog().getByRole("button", { name: "Author" }));
    expect(api.author).toHaveBeenCalledWith("pets", {
      type: "relation",
      fields: {
        label: "dog meets cat",
        level: "level-1",
        subject: "cn_dog",
        predicate_label: "meets",
        object: "cn_cat",
        evidence: [{ unit: STATEMENT.id }],
      },
    });
  });

  test("rule_asks_for_modality_actor_and_action", async () => {
    const { api, user } = await openAuthor();
    await user.selectOptions(dialog().getByLabelText("Type"), "rule");
    await user.type(dialog().getByLabelText("Label"), "lead in the stairwell");
    await user.selectOptions(dialog().getByLabelText("Modality"), "must");
    await user.type(dialog().getByLabelText("Actor"), "dog owner");
    await user.type(dialog().getByLabelText("Action"), "keep the dog on a lead");
    await user.click(dialog().getByRole("checkbox", { name: containing(LEASH_RULE.text) }));
    await user.click(dialog().getByRole("button", { name: "Author" }));
    expect(api.author).toHaveBeenCalledWith("pets", {
      type: "rule",
      fields: {
        label: "lead in the stairwell",
        level: "level-1",
        modality: "must",
        actor: "dog owner",
        action: "keep the dog on a lead",
        evidence: [{ unit: LEASH_RULE.id }],
      },
    });
  });
});
