// The review screen (FR-18, FR-19, FR-20): the element list with its filters, badges and
// multi-select, and the bulk bar acting on the selected elements that are shown.
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, test, vi } from "vitest";
import type { ActionIn, ElementsOut, IndexEntry, SessionOut } from "../api";
import { ReviewScreen, type ReviewApi } from "./ReviewScreen";

function entry(id: string, fields: Partial<IndexEntry>): IndexEntry {
  return {
    id,
    type: "concept",
    label: id,
    status: "proposed",
    level: "level-2",
    definition: "",
    corpora: ["00_dogs"],
    documents: ["doc_dogs"],
    search: id,
    ...fields,
  };
}

const INDEX: ElementsOut = {
  elements: [
    entry("cn_leash", { label: "leash", level: "level-1", search: "leash a lead of 2 m" }),
    entry("ru_stairs", {
      type: "rule",
      label: "dog on a lead in the stairwell",
      level: "level-1",
      corpora: ["02_rules"],
      documents: ["doc_house"],
      search: "dog on a lead in the stairwell",
    }),
    entry("ru_noise", {
      type: "rule",
      label: "quiet hours",
      status: "approved",
      corpora: ["02_rules"],
      documents: ["doc_noise"],
      search: "quiet hours after 22:00",
    }),
    entry("tm_cat", { type: "term", label: "cat", level: "level-3", status: "excluded" }),
  ],
  corpora: [
    {
      folder: "00_dogs",
      source_path: "dogs",
      documents: [{ id: "doc_dogs", path: "dogs/care.md", title: "Dog care" }],
    },
    {
      folder: "02_rules",
      source_path: "rules",
      documents: [
        { id: "doc_house", path: "rules/house.md", title: "House rules" },
        { id: "doc_noise", path: "rules/noise.md", title: null },
      ],
    },
  ],
  pending: 0,
};

const ALICE: SessionOut = { user: "alice", role: "user", writer: true, ontology: "pets" };

/** A server that accepts every action and counts the unsaved changes. */
function fakeApi(): ReviewApi {
  let pending = 0;
  return {
    elementIndex: vi.fn(() => Promise.resolve({ ...INDEX, pending })),
    act: vi.fn((_name: string, body: ActionIn) => {
      pending += body.ids.length;
      return Promise.resolve({
        results: body.ids.map((id) => ({ element_id: id, ok: true, message: "done" })),
        pending,
      });
    }),
  };
}

function setup(session: SessionOut = ALICE, api: ReviewApi = fakeApi()) {
  render(<ReviewScreen session={session} api={api} />);
  return { api, user: userEvent.setup() };
}

function rows(): HTMLElement[] {
  return within(screen.getByRole("table")).getAllByRole("row").slice(1);
}

describe("ReviewScreen", () => {
  test("lists_every_element_with_status_and_level_badges", async () => {
    const { api } = setup();
    expect(await screen.findByText("leash")).toBeInTheDocument();
    expect(api.elementIndex).toHaveBeenCalledWith("pets");
    expect(rows()).toHaveLength(4);
    const noise = rows().find((row) => row.textContent.includes("quiet hours"));
    expect(noise).toBeDefined();
    expect(within(noise as HTMLElement).getByTestId("status-badge")).toHaveTextContent("Approved");
    expect(within(noise as HTMLElement).getByTestId("level-badge")).toHaveTextContent("L2");
    expect(screen.getByText("4 of 4 elements")).toBeInTheDocument();
  });

  test("filters_by_type_level_and_document", async () => {
    const { user } = setup();
    await screen.findByText("leash");
    await user.selectOptions(screen.getByLabelText("Type"), "rule");
    await user.selectOptions(screen.getByLabelText("Level"), "level-1");
    expect(rows().map((r) => r.textContent)).toEqual([
      expect.stringContaining("dog on a lead in the stairwell"),
    ]);
    await user.selectOptions(screen.getByLabelText("Level"), "");
    await user.selectOptions(screen.getByLabelText("Document"), "doc_noise");
    expect(rows()).toHaveLength(1);
    expect(rows()[0]).toHaveTextContent("quiet hours");
  });

  test("filters_by_status_and_corpus", async () => {
    const { user } = setup();
    await screen.findByText("leash");
    await user.selectOptions(screen.getByLabelText("Status"), "excluded");
    expect(rows()).toHaveLength(1);
    expect(rows()[0]).toHaveTextContent("cat");
    await user.selectOptions(screen.getByLabelText("Status"), "");
    await user.selectOptions(screen.getByLabelText("Corpus"), "02_rules");
    expect(rows()).toHaveLength(2);
  });

  test("documents_follow_the_chosen_corpus", async () => {
    const { user } = setup();
    await screen.findByText("leash");
    const documents = () =>
      within(screen.getByLabelText("Document"))
        .getAllByRole("option")
        .map((o) => o.textContent);
    expect(documents()).toEqual(["All documents", "Dog care", "House rules", "rules/noise.md"]);
    await user.selectOptions(screen.getByLabelText("Corpus"), "02_rules");
    expect(documents()).toEqual(["All documents", "House rules", "rules/noise.md"]);
  });

  test("search_lead_matches_labels_and_evidence", async () => {
    const { user } = setup();
    await screen.findByText("leash");
    await user.type(screen.getByLabelText("Search"), "LEAD");
    expect(rows()).toHaveLength(2);
    expect(screen.getByText("2 of 4 elements")).toBeInTheDocument();
  });

  test("select_shown_then_bulk_level_acts_on_them_and_reloads", async () => {
    const { api, user } = setup();
    await screen.findByText("leash");
    await user.selectOptions(screen.getByLabelText("Type"), "rule");
    await user.click(screen.getByLabelText("Select every element shown"));
    expect(screen.getByText("2 selected")).toBeInTheDocument();
    await user.selectOptions(screen.getByLabelText(/set level to/i), "level-3");
    await user.click(screen.getByRole("button", { name: "Set level" }));
    expect(api.act).toHaveBeenCalledWith("pets", {
      action: "level",
      ids: ["ru_stairs", "ru_noise"],
      payload: { level: "level-3" },
    });
    expect(await screen.findByRole("status")).toHaveTextContent("2 changed");
    expect(api.elementIndex).toHaveBeenCalledTimes(2);
    expect(await screen.findByText("2 unsaved changes")).toBeInTheDocument();
  });

  test("bulk_acts_only_on_selected_elements_that_are_shown", async () => {
    const { api, user } = setup();
    await screen.findByText("leash");
    await user.click(screen.getByLabelText("Select leash"));
    await user.click(screen.getByLabelText("Select cat"));
    await user.selectOptions(screen.getByLabelText("Type"), "term");
    expect(screen.getByText("1 selected")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Include" }));
    expect(api.act).toHaveBeenCalledWith("pets", {
      action: "include",
      ids: ["tm_cat"],
      payload: {},
    });
  });

  test("admin_gets_approve_and_reject", async () => {
    setup({ ...ALICE, role: "domain_admin" });
    await screen.findByText("leash");
    expect(screen.getByRole("button", { name: "Approve" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Reject…" })).toBeInTheDocument();
  });

  test("shows_when_the_index_cannot_be_loaded", async () => {
    const api = fakeApi();
    api.elementIndex = () => Promise.reject(new Error("the server is not reachable"));
    setup(ALICE, api);
    expect(await screen.findByRole("alert")).toHaveTextContent("the server is not reachable");
  });
});
