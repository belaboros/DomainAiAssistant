// The level of an element (FR-13): level-1 to level-3, or ignorable.
import type { Level } from "../api";

export const LEVEL_LABEL: Readonly<Record<Level, string>> = {
  "level-1": "L1",
  "level-2": "L2",
  "level-3": "L3",
  ignorable: "Ignorable",
};

export const LEVEL_NAME: Readonly<Record<Level, string>> = {
  "level-1": "Level 1",
  "level-2": "Level 2",
  "level-3": "Level 3",
  ignorable: "Ignorable",
};

export function LevelBadge(props: { level: Level }) {
  return (
    <span
      className={`badge level-${props.level}`}
      data-testid="level-badge"
      title={LEVEL_NAME[props.level]}
    >
      {LEVEL_LABEL[props.level]}
    </span>
  );
}
