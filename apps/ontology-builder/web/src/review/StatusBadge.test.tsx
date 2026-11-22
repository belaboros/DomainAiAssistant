// Status badges (FR-20, AC-19): each status has its own colour class, with a colour of its own
// in styles.css, and its own text label and icon, so status never depends on colour alone.
import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";
import type { ElementStatus } from "../api";
import styles from "../styles.css?raw";
import { STATUS_LOOK, StatusBadge } from "./StatusBadge";

const STATUSES: readonly ElementStatus[] = [
  "proposed",
  "included",
  "excluded",
  "approved",
  "rejected",
  "deprecated",
];

/** The value of `name` in the first rule of styles.css that starts with `selector`. */
function declared(selector: string, name: string): string | undefined {
  const opening = `${selector} {`;
  const start = styles.indexOf(opening);
  if (start < 0) return undefined;
  const body = styles
    .slice(start + opening.length, styles.indexOf("}", start))
    .replace(/\/\*[\s\S]*?\*\//g, "");
  const declaration = body.split(";").find((part) => part.trim().startsWith(`${name}:`));
  return declaration?.slice(declaration.indexOf(":") + 1).trim();
}

/** The light-mode colour of a badge class: its `--badge`, resolved through the `:root` token. */
function colourOf(className: string): string | undefined {
  const value = declared(`.${className}`, "--badge");
  const token = /^var\((--[\w-]+)\)$/.exec(value ?? "")?.[1];
  return token === undefined ? value : declared(":root", token);
}

function rendered(status: ElementStatus) {
  const { unmount } = render(<StatusBadge status={status} />);
  const badge = screen.getByTestId("status-badge");
  const seen = {
    className: [...badge.classList].find((c) => c.startsWith("status-")) ?? "",
    text: badge.textContent,
    icon: badge.querySelector("[aria-hidden='true']")?.textContent ?? "",
    name: badge.getAttribute("title"),
  };
  unmount();
  return seen;
}

describe("StatusBadge", () => {
  test("each_status_has_distinct_colour_class_and_label", () => {
    const seen = STATUSES.map(rendered);
    const distinct = (values: (string | null | undefined)[]) => new Set(values).size;
    expect(distinct(seen.map((s) => s.className))).toBe(STATUSES.length);
    expect(distinct(seen.map((s) => s.text))).toBe(STATUSES.length);
    expect(distinct(seen.map((s) => s.icon))).toBe(STATUSES.length);
    const colours = seen.map((s) => colourOf(s.className));
    expect(colours.every((c) => c?.startsWith("#") === true)).toBe(true);
    expect(distinct(colours)).toBe(STATUSES.length);
  });

  test("labels_name_the_review_state", () => {
    expect(STATUS_LOOK.proposed.label).toMatch(/proposed/i);
    expect(STATUS_LOOK.included.label).toMatch(/waiting for approval/i);
    expect(STATUS_LOOK.approved.label).toMatch(/approved/i);
    expect(STATUS_LOOK.excluded.label).toMatch(/excluded/i);
    expect(STATUS_LOOK.rejected.label).toMatch(/rejected/i);
    expect(STATUS_LOOK.deprecated.label).toMatch(/deprecated/i);
  });

  test("icon_is_decorative_and_label_is_text", () => {
    render(<StatusBadge status="included" />);
    const badge = screen.getByTestId("status-badge");
    expect(badge).toHaveTextContent("Waiting for approval");
    expect(badge.querySelector("[aria-hidden='true']")).not.toBeNull();
  });
});
