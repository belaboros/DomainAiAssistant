// Author an element (FR-22): its type, the fields of that type, a level, and evidence picked
// from the source units. Without evidence it cannot be sent; the server checks again.
import { useMemo, useState } from "react";
import type { ElementType, IndexEntry, Unit } from "../api";
import { type Change, FieldInput } from "../review/ActionDialog";
import { complete, initialValues, payloadOf, type Values } from "../review/actionDialogs";
import { authorFields, TYPES } from "./authorFields";
import { EvidencePicker } from "./EvidencePicker";
import { Modal, Problem } from "./Modal";
import { useUnits } from "./useUnits";
import { type DialogProps, messageOf } from "./workApi";

type AuthorProps = DialogProps & { elements: readonly IndexEntry[] };

function useSend(props: AuthorProps) {
  const { ontology, api, onChanged, onClose } = props;
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState<string | null>(null);
  const send = async (type: ElementType, fields: Record<string, unknown>) => {
    setBusy(true);
    setProblem(null);
    try {
      const id = await api.author(ontology, { type, fields });
      await onChanged();
      onClose(`Element ${id} authored (included, unsaved).`);
    } catch (error) {
      setProblem(messageOf(error));
      setBusy(false);
    }
  };
  return { busy, problem, send };
}

function TypeSelect({ type, onChange }: { type: ElementType; onChange: (t: ElementType) => void }) {
  return (
    <label>
      Type
      <select
        value={type}
        onChange={(event) => {
          onChange(event.target.value as ElementType);
        }}
      >
        {TYPES.map((choice) => (
          <option key={choice.value} value={choice.value}>
            {choice.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function AuthorForm(props: AuthorProps & { units: readonly Unit[] }) {
  const { elements, units, onClose } = props;
  const [type, setType] = useState<ElementType>("concept");
  const [values, setValues] = useState<Values>(new Map());
  const [evidence, setEvidence] = useState<readonly string[]>([]);
  const { busy, problem, send } = useSend(props);
  const form = useMemo(() => ({ fields: authorFields(type, elements) }), [type, elements]);
  const shown = useMemo(() => new Map([...initialValues(form), ...values]), [form, values]);
  const change: Change = (name, value) => {
    setValues((current) => new Map(current).set(name, value));
  };
  const ready = complete(form, shown) && evidence.length > 0;
  return (
    <Modal title="Author an element" busy={busy} onClose={onClose}>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          const fields = {
            ...payloadOf(form, shown),
            evidence: evidence.map((unit) => ({ unit })),
          };
          if (ready) void send(type, fields);
        }}
      >
        <TypeSelect type={type} onChange={setType} />
        {form.fields.map((field, at) => (
          <FieldInput
            key={field.name}
            field={field}
            values={shown}
            onChange={change}
            first={at === 0}
          />
        ))}
        <EvidencePicker units={units} chosen={evidence} onChange={setEvidence} />
        <Problem message={problem} />
        <div className="dialog-buttons">
          <button type="submit" disabled={busy || !ready}>
            Author
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

export function AuthorDialog(props: AuthorProps) {
  const units = useUnits(props.api, props.ontology);
  if (units.state === "ready") return <AuthorForm {...props} units={units.units} />;
  return (
    <Modal title="Author an element" onClose={props.onClose}>
      {units.state === "loading" ? <p className="loading">Loading the passages…</p> : null}
      <Problem message={units.state === "failed" ? units.message : null} />
    </Modal>
  );
}
