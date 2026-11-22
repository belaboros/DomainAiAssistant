// The element list: one row per shown element, with its status and level badges and a check
// box for multi-select (FR-18 to FR-20).
import type { IndexEntry } from "../api";
import { LevelBadge } from "./LevelBadge";
import { StatusBadge } from "./StatusBadge";

export interface ElementListProps {
  entries: readonly IndexEntry[];
  selected: ReadonlySet<string>;
  onToggle: (id: string) => void;
  /** Select (true) or unselect (false) every shown element. */
  onToggleAll: (on: boolean) => void;
}

function Row(props: { entry: IndexEntry; checked: boolean; onToggle: (id: string) => void }) {
  const { entry, checked, onToggle } = props;
  const name = entry.label === "" ? entry.id : entry.label;
  return (
    <tr className={checked ? "selected" : undefined}>
      <td>
        <input
          type="checkbox"
          aria-label={`Select ${name}`}
          checked={checked}
          onChange={() => {
            onToggle(entry.id);
          }}
        />
      </td>
      <td>
        <div>{name}</div>
        {entry.definition !== "" && <div className="definition">{entry.definition}</div>}
      </td>
      <td>{entry.type}</td>
      <td>
        <StatusBadge status={entry.status} />
      </td>
      <td>
        <LevelBadge level={entry.level} />
      </td>
    </tr>
  );
}

export function ElementList({ entries, selected, onToggle, onToggleAll }: ElementListProps) {
  const all = entries.length > 0 && entries.every((e) => selected.has(e.id));
  return (
    <div className="element-list-wrap">
      <table className="element-list">
        <thead>
          <tr>
            <th>
              <input
                type="checkbox"
                aria-label="Select every element shown"
                checked={all}
                disabled={entries.length === 0}
                onChange={() => {
                  onToggleAll(!all);
                }}
              />
            </th>
            <th>Label</th>
            <th>Type</th>
            <th>Status</th>
            <th>Level</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry) => (
            <Row
              key={entry.id}
              entry={entry}
              checked={selected.has(entry.id)}
              onToggle={onToggle}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
