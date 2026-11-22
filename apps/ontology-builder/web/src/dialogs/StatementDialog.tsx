// New and edited user statements (FR-21): a new statement becomes a source unit under
// 90_user_statements; editing one adds a revision and keeps its ID.
import { useState } from "react";
import type { Unit } from "../api";
import { Modal, Problem } from "./Modal";
import { useUnits } from "./useUnits";
import { type DialogProps, messageOf } from "./workApi";

interface FormProps {
  title: string;
  submit: string;
  initial: string;
  onClose: () => void;
  send: (text: string) => Promise<void>;
  children?: React.ReactNode;
}

function StatementForm({ title, submit, initial, onClose, send, children }: FormProps) {
  const [text, setText] = useState(initial);
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState<string | null>(null);
  const submitText = async () => {
    setBusy(true);
    setProblem(null);
    try {
      await send(text.trim());
    } catch (error) {
      setProblem(messageOf(error));
      setBusy(false);
    }
  };
  return (
    <Modal title={title} busy={busy} onClose={onClose}>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void submitText();
        }}
      >
        {children}
        <label>
          Statement
          <textarea
            rows={4}
            value={text}
            autoFocus
            onChange={(event) => {
              setText(event.target.value);
            }}
          />
        </label>
        <Problem message={problem} />
        <div className="dialog-buttons">
          <button type="submit" disabled={busy || text.trim() === ""}>
            {submit}
          </button>
          <button
            type="button"
            className="secondary"
            disabled={busy}
            onClick={() => {
              onClose();
            }}
          >
            Cancel
          </button>
        </div>
      </form>
    </Modal>
  );
}

export function NewStatementDialog({ ontology, api, onChanged, onClose }: DialogProps) {
  const send = async (text: string) => {
    const id = await api.addStatement(ontology, text);
    await onChanged();
    onClose(`Statement ${id} added (unsaved).`);
  };
  return (
    <StatementForm
      title="New user statement"
      submit="Add statement"
      initial=""
      onClose={onClose}
      send={send}
    />
  );
}

function shortText(text: string): string {
  return text.length > 80 ? `${text.slice(0, 79)}…` : text;
}

function EditForm(props: DialogProps & { statements: readonly Unit[] }) {
  const { ontology, api, onChanged, onClose, statements } = props;
  const [chosen, setChosen] = useState(statements[0]);
  if (chosen === undefined) return null;
  const send = async (text: string) => {
    const id = await api.reviseStatement(ontology, chosen.id, text);
    await onChanged();
    onClose(`Statement ${id} revised (unsaved).`);
  };
  return (
    <StatementForm
      key={chosen.id}
      title="Edit a user statement"
      submit="Save revision"
      initial={chosen.text}
      onClose={onClose}
      send={send}
    >
      <label>
        User statement
        <select
          value={chosen.id}
          onChange={(event) => {
            setChosen(statements.find((s) => s.id === event.target.value) ?? chosen);
          }}
        >
          {statements.map((s) => (
            <option key={s.id} value={s.id}>
              {shortText(s.text)}
            </option>
          ))}
        </select>
      </label>
      <p className="hint">
        Revision {chosen.revisions} by {chosen.author ?? "unknown"}; the ID {chosen.id} stays.
      </p>
    </StatementForm>
  );
}

export function EditStatementDialog(props: DialogProps) {
  const units = useUnits(props.api, props.ontology);
  if (units.state !== "ready") {
    return (
      <Modal title="Edit a user statement" onClose={props.onClose}>
        {units.state === "loading" ? <p className="loading">Loading…</p> : null}
        <Problem message={units.state === "failed" ? units.message : null} />
      </Modal>
    );
  }
  const statements = units.units.filter((u) => u.kind === "user_statement");
  if (statements.length === 0) {
    return (
      <Modal title="Edit a user statement" onClose={props.onClose}>
        <p>There are no user statements yet. Add one with New statement.</p>
        <div className="dialog-buttons">
          <button
            type="button"
            onClick={() => {
              props.onClose();
            }}
          >
            Close
          </button>
        </div>
      </Modal>
    );
  }
  return <EditForm {...props} statements={statements} />;
}
