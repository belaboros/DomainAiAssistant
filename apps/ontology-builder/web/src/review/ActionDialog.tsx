// The dialog of one element action: the fields its spec asks for, a submit button that stays
// disabled until every required field has a value, and Cancel (or Escape).
import { useState } from "react";
import {
  complete,
  type DialogSpec,
  type Field,
  initialValues,
  payloadOf,
  type Values,
} from "./actionDialogs";

export interface ActionDialogProps {
  spec: DialogSpec;
  busy: boolean;
  onSubmit: (payload: Record<string, unknown>) => void;
  onCancel: () => void;
}

export type Change = (name: string, value: string | readonly string[]) => void;

function textValue(values: Values, name: string): string {
  const value = values.get(name);
  return typeof value === "string" ? value : "";
}

function listValue(values: Values, name: string): readonly string[] {
  const value = values.get(name);
  return Array.isArray(value) ? (value as readonly string[]) : [];
}

function Checks(props: { field: Field & { kind: "checks" }; values: Values; onChange: Change }) {
  const { field, values, onChange } = props;
  const chosen = listValue(values, field.name);
  const toggle = (value: string) => {
    onChange(
      field.name,
      chosen.includes(value) ? chosen.filter((v) => v !== value) : [...chosen, value],
    );
  };
  return (
    <fieldset>
      <legend>{field.label}</legend>
      {field.choices.map((choice) => (
        <label key={choice.value} className="check">
          <input
            type="checkbox"
            checked={chosen.includes(choice.value)}
            onChange={() => {
              toggle(choice.value);
            }}
          />{" "}
          {choice.label}
        </label>
      ))}
    </fieldset>
  );
}

function Select(props: { field: Field & { kind: "select" }; values: Values; onChange: Change }) {
  const { field, values, onChange } = props;
  return (
    <label>
      {field.label}
      <select
        value={textValue(values, field.name)}
        onChange={(event) => {
          const chosen = event.target.value;
          onChange(field.name, chosen);
          if (field.fills) onChange(field.fills.name, field.fills.values.get(chosen) ?? "");
        }}
      >
        {!field.required && <option value="">None</option>}
        {field.choices.map((choice) => (
          <option key={choice.value} value={choice.value}>
            {choice.label}
          </option>
        ))}
      </select>
    </label>
  );
}

/** One field of a form, by its kind: a text input, a select or a group of checkboxes. */
export function FieldInput(props: {
  field: Field;
  values: Values;
  onChange: Change;
  first: boolean;
}) {
  const { field, values, onChange, first } = props;
  if (field.kind === "checks") return <Checks field={field} values={values} onChange={onChange} />;
  if (field.kind === "select") return <Select field={field} values={values} onChange={onChange} />;
  return (
    <label>
      {field.label}
      <input
        value={textValue(values, field.name)}
        autoFocus={first}
        onChange={(event) => {
          onChange(field.name, event.target.value);
        }}
      />
    </label>
  );
}

export function ActionDialog({ spec, busy, onSubmit, onCancel }: ActionDialogProps) {
  const [values, setValues] = useState<Values>(() => initialValues(spec));
  const change: Change = (name, value) => {
    setValues((current) => new Map(current).set(name, value));
  };
  const firstText = spec.fields.find((f) => f.kind === "text")?.name;
  return (
    <div className="dialog-backdrop">
      <div role="dialog" aria-modal="true" aria-label={spec.title} className="dialog">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            if (complete(spec, values)) onSubmit(payloadOf(spec, values));
          }}
          onKeyDown={(event) => {
            if (event.key === "Escape") onCancel();
          }}
        >
          <h2>{spec.title}</h2>
          {spec.fields.map((field) => (
            <FieldInput
              key={field.name}
              field={field}
              values={values}
              onChange={change}
              first={field.name === firstText}
            />
          ))}
          <div className="dialog-buttons">
            <button type="submit" disabled={busy || !complete(spec, values)}>
              {spec.submit}
            </button>
            <button type="button" className="secondary" onClick={onCancel}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
