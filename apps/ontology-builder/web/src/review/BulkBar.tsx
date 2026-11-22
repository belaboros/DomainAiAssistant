// The bulk bar (FR-18): one action on every selected element in one step. Anyone can include,
// exclude (with a reason) and set the level; a domain admin can also approve and reject (with a
// reason). The server checks role and status again for every ID and answers per ID.
import { useState } from "react";
import type { ActionResult, Level, Role } from "../api";

export type BulkAction = "include" | "exclude" | "level" | "approve" | "reject";
export type BulkAct = (
  action: BulkAction,
  ids: readonly string[],
  payload: Record<string, unknown>,
) => Promise<ActionResult[]>;

export interface BulkBarProps {
  selected: readonly string[];
  role: Role;
  /** False for a read-only second session. */
  writer: boolean;
  act: BulkAct;
  onClear: () => void;
}

type ReasonAction = "exclude" | "reject";

const REASON_WORDS: Readonly<Record<ReasonAction, { verb: string; doing: string }>> = {
  exclude: { verb: "Exclude", doing: "excluding" },
  reject: { verb: "Reject", doing: "rejecting" },
};

const LEVELS: readonly { value: Level; label: string }[] = [
  { value: "level-1", label: "Level 1" },
  { value: "level-2", label: "Level 2" },
  { value: "level-3", label: "Level 3" },
  { value: "ignorable", label: "Ignorable" },
];

type Outcome =
  | { kind: "none" }
  | { kind: "done"; results: ActionResult[] }
  | { kind: "failed"; message: string };

function ResultLine({ outcome }: { outcome: Outcome }) {
  if (outcome.kind === "none") return null;
  if (outcome.kind === "failed") {
    return (
      <p className="problem bulk-result" role="alert">
        {outcome.message}
      </p>
    );
  }
  const refused = outcome.results.filter((r) => !r.ok);
  const changed = outcome.results.length - refused.length;
  return (
    <div className="bulk-result" role="status">
      {refused.length === 0
        ? `${String(changed)} changed.`
        : `${String(changed)} changed, ${String(refused.length)} refused:`}
      {refused.length > 0 && (
        <ul>
          {refused.map((r) => (
            <li key={r.element_id}>{r.message}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

interface ReasonFormProps {
  action: ReasonAction;
  count: number;
  busy: boolean;
  onConfirm: (reason: string) => void;
  onCancel: () => void;
}

function ReasonForm({ action, count, busy, onConfirm, onCancel }: ReasonFormProps) {
  const [reason, setReason] = useState("");
  const words = action === "exclude" ? REASON_WORDS.exclude : REASON_WORDS.reject;
  const trimmed = reason.trim();
  return (
    <form
      className="reason"
      onSubmit={(event) => {
        event.preventDefault();
        if (trimmed !== "") onConfirm(trimmed);
      }}
    >
      <label>
        Reason for {words.doing}{" "}
        <input
          value={reason}
          autoFocus
          onChange={(event) => {
            setReason(event.target.value);
          }}
        />
      </label>
      <button type="submit" disabled={busy || trimmed === ""}>
        {words.verb} {count}
      </button>
      <button type="button" className="secondary" onClick={onCancel}>
        Cancel
      </button>
    </form>
  );
}

function messageOf(error: unknown): string {
  return error instanceof Error ? error.message : "the action failed";
}

export function BulkBar({ selected, role, writer, act, onClear }: BulkBarProps) {
  const [level, setLevel] = useState<Level>("level-1");
  const [asking, setAsking] = useState<ReasonAction | null>(null);
  const [busy, setBusy] = useState(false);
  const [outcome, setOutcome] = useState<Outcome>({ kind: "none" });
  const blocked = busy || !writer || selected.length === 0;
  const admin = role === "domain_admin";

  const run = async (action: BulkAction, payload: Record<string, unknown> = {}) => {
    setBusy(true);
    setAsking(null);
    try {
      setOutcome({ kind: "done", results: await act(action, selected, payload) });
    } catch (error) {
      setOutcome({ kind: "failed", message: messageOf(error) });
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="bulk-bar" aria-label="Bulk actions">
      <span>{selected.length} selected</span>
      <button type="button" disabled={blocked} onClick={() => void run("include")}>
        Include
      </button>
      <button
        type="button"
        disabled={blocked}
        onClick={() => {
          setAsking("exclude");
        }}
      >
        Exclude…
      </button>
      <label>
        Set level to{" "}
        <select
          value={level}
          disabled={!writer}
          onChange={(event) => {
            setLevel(event.target.value as Level);
          }}
        >
          {LEVELS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
      <button type="button" disabled={blocked} onClick={() => void run("level", { level })}>
        Set level
      </button>
      {admin && (
        <>
          <button type="button" disabled={blocked} onClick={() => void run("approve")}>
            Approve
          </button>
          <button
            type="button"
            disabled={blocked}
            onClick={() => {
              setAsking("reject");
            }}
          >
            Reject…
          </button>
        </>
      )}
      <button
        type="button"
        className="secondary"
        disabled={selected.length === 0}
        onClick={onClear}
      >
        Clear selection
      </button>
      {asking !== null && (
        <ReasonForm
          action={asking}
          count={selected.length}
          busy={busy}
          onConfirm={(reason) => void run(asking, { reason })}
          onCancel={() => {
            setAsking(null);
          }}
        />
      )}
      <ResultLine outcome={outcome} />
    </section>
  );
}
