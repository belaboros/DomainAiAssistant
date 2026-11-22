// Level badges: each level has its own class and a short text.
import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";
import type { Level } from "../api";
import { LevelBadge } from "./LevelBadge";

const LEVELS: readonly Level[] = ["level-1", "level-2", "level-3", "ignorable"];

describe("LevelBadge", () => {
  test("each_level_has_its_own_class_and_text", () => {
    const seen = LEVELS.map((level) => {
      const { unmount } = render(<LevelBadge level={level} />);
      const badge = screen.getByTestId("level-badge");
      const found = { className: badge.className, text: badge.textContent };
      unmount();
      return found;
    });
    expect(new Set(seen.map((s) => s.className)).size).toBe(LEVELS.length);
    expect(seen.map((s) => s.text)).toEqual(["L1", "L2", "L3", "Ignorable"]);
  });
});
