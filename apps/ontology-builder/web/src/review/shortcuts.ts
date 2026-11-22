// The review keyboard shortcuts (T25): j/k next and previous element, i include, x exclude,
// e correct, 1–3 set the level, a approve. Keys typed into a field, or with a modifier, are not
// shortcuts.
import { useEffect, useRef } from "react";
import type { Level } from "../api";

export type Shortcut =
  | { kind: "next" }
  | { kind: "previous" }
  | { kind: "include" }
  | { kind: "exclude" }
  | { kind: "edit" }
  | { kind: "level"; level: Level }
  | { kind: "approve" };

const KEYS: ReadonlyMap<string, Shortcut> = new Map<string, Shortcut>([
  ["j", { kind: "next" }],
  ["k", { kind: "previous" }],
  ["i", { kind: "include" }],
  ["x", { kind: "exclude" }],
  ["e", { kind: "edit" }],
  ["1", { kind: "level", level: "level-1" }],
  ["2", { kind: "level", level: "level-2" }],
  ["3", { kind: "level", level: "level-3" }],
  ["a", { kind: "approve" }],
]);

function typing(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  return target.isContentEditable || ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName);
}

export function shortcutOf(event: KeyboardEvent): Shortcut | undefined {
  if (event.ctrlKey || event.metaKey || event.altKey || typing(event.target)) return undefined;
  return KEYS.get(event.key);
}

/** Calls `handle` for each shortcut pressed while `enabled`. */
export function useShortcuts(handle: (shortcut: Shortcut) => void, enabled: boolean): void {
  const latest = useRef(handle);
  useEffect(() => {
    latest.current = handle;
  });
  useEffect(() => {
    if (!enabled) return undefined;
    const listener = (event: KeyboardEvent) => {
      const shortcut = shortcutOf(event);
      if (shortcut !== undefined) latest.current(shortcut);
    };
    window.addEventListener("keydown", listener);
    return () => {
      window.removeEventListener("keydown", listener);
    };
  }, [enabled]);
}
