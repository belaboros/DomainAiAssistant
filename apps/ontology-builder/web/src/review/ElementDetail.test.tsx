// The element detail (FR-16, AC-15): the evidence passages first, then the proposal (type,
// label, level, reason), the actions, and the decision history (FR-26).
import { render, screen, within } from "@testing-library/react";
import { describe, expect, test, vi } from "vitest";
import type { ElementDetail as Detail } from "../api";
import { ElementDetail } from "./ElementDetail";
import { CONCEPT, CORPORA, ELEMENTS, TERM } from "./fixtures/detail";

function setup(detail: Detail = CONCEPT) {
  render(
    <ElementDetail
      detail={detail}
      corpora={CORPORA}
      elements={ELEMENTS}
      role="user"
      writer
      act={vi.fn(() => Promise.resolve([]))}
    />,
  );
}

describe("ElementDetail", () => {
  test("evidence_rendered_before_proposal", () => {
    setup();
    const evidence = screen.getByRole("region", { name: "Evidence" });
    const proposal = screen.getByRole("region", { name: /proposal/i });
    expect(evidence.compareDocumentPosition(proposal)).toBe(Node.DOCUMENT_POSITION_FOLLOWING);
  });

  test("evidence_shows_the_passage_and_where_it_is", () => {
    setup();
    const evidence = within(screen.getByRole("region", { name: "Evidence" }));
    expect(evidence.getByText("Dogs must be kept on a leash in the stairwell.")).toBeVisible();
    expect(evidence.getByText(/House rules/)).toBeVisible();
    expect(evidence.getByText(/su_gone/)).toBeVisible();
    expect(evidence.getByText(/not found/i)).toBeVisible();
  });

  test("proposal_shows_type_label_level_and_reason", () => {
    setup();
    const proposal = within(screen.getByRole("region", { name: /proposal/i }));
    expect(proposal.getByText("concept")).toBeVisible();
    expect(proposal.getByRole("heading", { name: "leash" })).toBeVisible();
    expect(proposal.getByText("A strap to hold a dog.")).toBeVisible();
    expect(proposal.getByText("Level 1")).toBeVisible();
    expect(proposal.getByText("Every resident with a dog needs it.")).toBeVisible();
    expect(proposal.getByText("Proposed")).toBeVisible();
    expect(proposal.getByText("Also called a lead.")).toBeVisible();
    expect(screen.getByText(/unsaved changes/i)).toBeVisible();
  });

  test("an_authored_element_names_its_author", () => {
    setup(TERM);
    expect(screen.getByRole("region", { name: /authored by bob/i })).toBeVisible();
  });

  test("decision_history", () => {
    setup();
    const history = within(screen.getByRole("region", { name: "Decision history" }));
    const [row] = history.getAllByRole("row").slice(1);
    expect(row).toHaveTextContent("alice");
    expect(row).toHaveTextContent("User");
    expect(row).toHaveTextContent("level");
    expect(row).toHaveTextContent("level-2");
    expect(row).toHaveTextContent("level-1");
    expect(row).toHaveTextContent("core to the house rules");
  });

  test("no_decisions_yet", () => {
    setup(TERM);
    const history = within(screen.getByRole("region", { name: "Decision history" }));
    expect(history.getByText(/no decisions yet/i)).toBeVisible();
  });
});
