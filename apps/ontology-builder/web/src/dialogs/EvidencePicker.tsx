// Pick the evidence of an authored element (FR-22): search the source units (corpus passages
// and user statements) by text and tick one or more. Chosen units stay listed while searching.
import { useMemo, useState } from "react";
import type { Unit } from "../api";

const SHOWN = 30;

export interface EvidencePickerProps {
  units: readonly Unit[];
  chosen: readonly string[];
  onChange: (chosen: readonly string[]) => void;
}

function matching(units: readonly Unit[], query: string, chosen: readonly string[]): Unit[] {
  const wanted = query.trim().toLocaleLowerCase();
  if (wanted === "") return [...units];
  return units.filter((u) => chosen.includes(u.id) || u.text.toLocaleLowerCase().includes(wanted));
}

function where(unit: Unit): string {
  return unit.kind === "user_statement"
    ? `user statement by ${unit.author ?? "unknown"}`
    : unit.corpus;
}

export function EvidencePicker({ units, chosen, onChange }: EvidencePickerProps) {
  const [query, setQuery] = useState("");
  const found = useMemo(() => matching(units, query, chosen), [units, query, chosen]);
  const toggle = (id: string) => {
    onChange(chosen.includes(id) ? chosen.filter((c) => c !== id) : [...chosen, id]);
  };
  return (
    <fieldset className="evidence-picker">
      <legend>Evidence</legend>
      <label>
        Find a passage
        <input
          type="search"
          value={query}
          onChange={(event) => {
            setQuery(event.target.value);
          }}
        />
      </label>
      <div className="picker-list">
        {found.slice(0, SHOWN).map((unit) => (
          <label key={unit.id} className="check">
            <input
              type="checkbox"
              checked={chosen.includes(unit.id)}
              onChange={() => {
                toggle(unit.id);
              }}
            />{" "}
            <span>{unit.text}</span> <span className="hint">({where(unit)})</span>
          </label>
        ))}
      </div>
      {found.length > SHOWN && (
        <p className="hint">
          {found.length - SHOWN} more passages match; refine the search to see them.
        </p>
      )}
      <p className="hint">
        {chosen.length === 0
          ? "Pick at least one passage as evidence."
          : `${String(chosen.length)} chosen.`}
      </p>
    </fieldset>
  );
}
