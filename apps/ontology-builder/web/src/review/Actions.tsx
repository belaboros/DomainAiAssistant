// The actions on the open element (FR-17, FR-23 to FR-25): include, exclude, correct, set the
// level, merge (concepts), split and reassign (terms), and for a domain admin approve, reject
// and deprecate. For a user the admin actions are shown disabled, with the reason (FR-3). The
// server checks role and status again and answers per ID; its message is shown.
import { useState } from "react";
import type { ActionName, ActionResult, ElementDetail, IndexEntry, Role } from "../api";
import { ActionDialog } from "./ActionDialog";
import { type DialogAction, dialogFor } from "./actionDialogs";
import { type Shortcut, useShortcuts } from "./shortcuts";

export type DetailAct = (
  action: ActionName,
  payload: Record<string, unknown>,
) => Promise<ActionResult[]>;

export interface ActionsProps {
  detail: ElementDetail;
  /** Every element of the index, for the merge, reassign and deprecate pickers. */
  elements: readonly IndexEntry[];
  role: Role;
  /** False for a read-only second session. */
  writer: boolean;
  act: DetailAct;
}

type Outcome =
  { kind: "none" } | { kind: "done"; message: string } | { kind: "refused"; message: string };

const ADMIN_ONLY = "Only a domain admin can approve, reject or deprecate.";

function messageOf(error: unknown): string {
  return error instanceof Error ? error.message : "the action failed";
}

function outcomeOf(results: readonly ActionResult[], id: string): Outcome {
  const mine = results.find((r) => r.element_id === id) ?? results[0];
  if (mine === undefined) return { kind: "done", message: "Done." };
  return mine.ok
    ? { kind: "done", message: `Done: ${mine.message}` }
    : { kind: "refused", message: mine.message };
}

function OutcomeLine({ outcome }: { outcome: Outcome }) {
  if (outcome.kind === "none") return null;
  if (outcome.kind === "refused") {
    return (
      <p className="problem" role="alert">
        {outcome.message}
      </p>
    );
  }
  return <p role="status">{outcome.message}</p>;
}

function useRunner(detail: ElementDetail, act: DetailAct) {
  const [busy, setBusy] = useState(false);
  const [outcome, setOutcome] = useState<Outcome>({ kind: "none" });
  const run = async (action: ActionName, payload: Record<string, unknown> = {}) => {
    setBusy(true);
    try {
      setOutcome(outcomeOf(await act(action, payload), detail.id));
    } catch (error) {
      setOutcome({ kind: "refused", message: messageOf(error) });
    } finally {
      setBusy(false);
    }
  };
  return { busy, outcome, setOutcome, run };
}

interface ButtonsProps {
  type: ElementDetail["type"];
  blocked: boolean;
  run: (action: ActionName) => void;
  ask: (action: DialogAction) => void;
}

function ReviewButtons({ type, blocked, run, ask }: ButtonsProps) {
  const button = (label: string, onClick: () => void) => (
    <button type="button" disabled={blocked} onClick={onClick}>
      {label}
    </button>
  );
  return (
    <div className="action-row">
      {button("Include", () => {
        run("include");
      })}
      {button("Exclude…", () => {
        ask("exclude");
      })}
      {button("Correct…", () => {
        ask("correct");
      })}
      {button("Set level…", () => {
        ask("level");
      })}
      {type === "concept" &&
        button("Merge into…", () => {
          ask("merge");
        })}
      {type === "term" &&
        button("Split senses…", () => {
          ask("split");
        })}
      {type === "term" &&
        button("Reassign mention…", () => {
          ask("reassign");
        })}
    </div>
  );
}

function AdminButtons(props: ButtonsProps & { admin: boolean }) {
  const { admin, blocked, run, ask } = props;
  const off = blocked || !admin;
  return (
    <div className="action-row">
      <button
        type="button"
        disabled={off}
        aria-describedby={admin ? undefined : "admin-only"}
        onClick={() => {
          run("approve");
        }}
      >
        Approve
      </button>
      <button
        type="button"
        disabled={off}
        aria-describedby={admin ? undefined : "admin-only"}
        onClick={() => {
          ask("reject");
        }}
      >
        Reject…
      </button>
      <button
        type="button"
        disabled={off}
        aria-describedby={admin ? undefined : "admin-only"}
        onClick={() => {
          ask("deprecate");
        }}
      >
        Deprecate…
      </button>
      {!admin && (
        <span className="hint" id="admin-only">
          {ADMIN_ONLY}
        </span>
      )}
    </div>
  );
}

export function Actions({ detail, elements, role, writer, act }: ActionsProps) {
  const [asking, setAsking] = useState<DialogAction | null>(null);
  const { busy, outcome, setOutcome, run } = useRunner(detail, act);
  const admin = role === "domain_admin";
  const blocked = busy || !writer;
  const start = (action: ActionName, payload: Record<string, unknown> = {}) => {
    setAsking(null);
    void run(action, payload);
  };

  const onShortcut = (shortcut: Shortcut) => {
    if (busy) return;
    if (shortcut.kind === "include") start("include");
    else if (shortcut.kind === "level") start("level", { level: shortcut.level });
    else if (shortcut.kind === "exclude") setAsking("exclude");
    else if (shortcut.kind === "edit") setAsking("correct");
    else if (shortcut.kind === "approve" && admin) start("approve");
    else if (shortcut.kind === "approve")
      setOutcome({ kind: "refused", message: "Only a domain admin can approve." });
  };
  useShortcuts(onShortcut, writer && asking === null);

  return (
    <section className="actions" aria-label="Actions">
      <ReviewButtons type={detail.type} blocked={blocked} run={start} ask={setAsking} />
      <AdminButtons
        type={detail.type}
        admin={admin}
        blocked={blocked}
        run={start}
        ask={setAsking}
      />
      <p className="hint">
        Keys: j/k next/previous · i include · x exclude · e correct · 1–3 level · a approve
      </p>
      {asking !== null && (
        <ActionDialog
          spec={dialogFor(asking, detail, elements)}
          busy={busy}
          onSubmit={(payload) => {
            start(asking, payload);
          }}
          onCancel={() => {
            setAsking(null);
          }}
        />
      )}
      <OutcomeLine outcome={outcome} />
    </section>
  );
}
