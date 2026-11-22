// The element list: one row per shown element, with its status and level badges and a check
// box for multi-select (FR-18 to FR-20). The label opens the element in the detail pane.
import type { IndexEntry } from "../api";
import { LevelBadge } from "./LevelBadge";
import { StatusBadge } from "./StatusBadge";

export interface ElementListProps {
  entries: readonly IndexEntry[];
  selected: ReadonlySet<string>;
  /** The element open in the detail pane, if any. */
  current: string | null;
  onOpen: (id: string) => void;
  onToggle: (id: string) => void;
  /** Select (true) or unselect (false) every shown element. */
  onToggleAll: (on: boolean) => void;
}

interface RowProps {
  entry: IndexEntry;
  checked: boolean;
  current: boolean;
  onOpen: (id: string) => void;
  onToggle: (id: string) => void;
}

function rowClass(checked: boolean, current: boolean): string | undefined {
  const names = [checked ? "selected" : "", current ? "current" : ""].filter((n) => n !== "");
  return names.length === 0 ? undefined : names.join(" ");
}

function Row({ entry, checked, current, onOpen, onToggle }: RowProps) {
  const name = entry.label === "" ? entry.id : entry.label;
  return (
    <tr className={rowClass(checked, current)} aria-current={current ? "true" : undefined}>
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
        <button
          type="button"
          className="link"
          onClick={() => {
            onOpen(entry.id);
          }}
        >
          {name}
        </button>
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

export function ElementList(props: ElementListProps) {
  const { entries, selected, current, onOpen, onToggle, onToggleAll } = props;
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
              current={entry.id === current}
              onOpen={onOpen}
              onToggle={onToggle}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
