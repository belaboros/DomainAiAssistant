// Renders the work bar with a fake API, for the dialog tests (T26).
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import type { IndexEntry, Role } from "../api";
import { ELEMENTS, fakeWork } from "./fixtures/units";
import { WorkBar } from "./WorkBar";
import type { WorkApi } from "./workApi";

export interface Options {
  role?: Role;
  writer?: boolean;
  api?: Partial<WorkApi>;
  elements?: readonly IndexEntry[];
}

export function renderBar(options: Options = {}) {
  const api = fakeWork(options.api);
  const onChanged = vi.fn(() => Promise.resolve());
  render(
    <WorkBar
      ontology="pets"
      role={options.role ?? "user"}
      writer={options.writer ?? true}
      elements={options.elements ?? ELEMENTS}
      api={api}
      onChanged={onChanged}
    />,
  );
  return { api, onChanged, user: userEvent.setup() };
}

export function dialog() {
  return within(screen.getByRole("dialog"));
}

/** Matches an accessible name that contains ``text``. */
export function containing(text: string) {
  return (name: string) => name.includes(text);
}
