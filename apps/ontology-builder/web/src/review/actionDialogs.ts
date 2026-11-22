// What each dialog of an element action asks for (FR-17, FR-23 to FR-25), as plain data that
// ActionDialog renders, and the payload it sends: the keys the server's handlers read.
import type { ElementDetail, IndexEntry } from "../api";
import { LEVEL_NAME } from "./LevelBadge";

export type DialogAction =
  "exclude" | "reject" | "correct" | "level" | "merge" | "split" | "reassign" | "deprecate";

export interface Choice {
  value: string;
  label: string;
}

interface Common {
  name: string;
  label: string;
  required?: boolean;
}

export type Field =
  | (Common & { kind: "text"; initial?: string })
  | (Common & {
      kind: "select";
      choices: readonly Choice[];
      initial?: string;
      /** Choosing a value here sets the named text field to the matching text. */
      fills?: { name: string; values: ReadonlyMap<string, string> };
    })
  | (Common & { kind: "checks"; choices: readonly Choice[] });

export interface DialogSpec {
  action: DialogAction;
  title: string;
  submit: string;
  fields: readonly Field[];
}

export type Values = ReadonlyMap<string, string | readonly string[]>;

const LEVELS: readonly Choice[] = [
  { value: "level-1", label: LEVEL_NAME["level-1"] },
  { value: "level-2", label: LEVEL_NAME["level-2"] },
  { value: "level-3", label: LEVEL_NAME["level-3"] },
  { value: "ignorable", label: LEVEL_NAME.ignorable },
];

/** The text fields a user can correct, per element type (lists and IDs have their own actions). */
function correctable(type: ElementDetail["type"]): readonly string[] {
  switch (type) {
    case "statement":
      return ["label", "definition", "text"];
    case "concept":
      return ["label", "definition", "scope_note"];
    case "relation":
      return ["label", "definition", "predicate_label"];
    case "rule":
      return ["label", "definition", "actor", "action", "condition"];
    case "property":
      return ["label", "definition", "name", "value", "unit"];
    case "term":
      return ["label", "definition"];
  }
}

export function fieldName(field: string): string {
  const words = field.replaceAll("_", " ");
  return words.charAt(0).toUpperCase() + words.slice(1);
}

function textOf(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "number") return String(value);
  return "";
}

function choiceOf(entry: IndexEntry): Choice {
  const name = entry.label === "" ? entry.id : entry.label;
  return { value: entry.id, label: `${name} (${entry.type})` };
}

function reason(required = false): Field {
  return { kind: "text", name: "reason", label: "Reason", required };
}

function correctSpec(detail: ElementDetail): Field[] {
  const fields = correctable(detail.type);
  const current = new Map(Object.entries(detail.record));
  const values = new Map(fields.map((f) => [f, textOf(current.get(f))]));
  const first = fields[0] ?? "label";
  return [
    {
      kind: "select",
      name: "field",
      label: "Field",
      choices: fields.map((f) => ({ value: f, label: fieldName(f) })),
      initial: first,
      fills: { name: "value", values },
    },
    { kind: "text", name: "value", label: "New value", initial: values.get(first) ?? "" },
    reason(),
  ];
}

/** Each mention of a term, named by the text of its passage. */
function mentionChoices(detail: ElementDetail): Choice[] {
  const texts = new Map(detail.evidence.map((e) => [e.unit, e.text ?? e.unit]));
  return (detail.record.mentions ?? []).map((m) => ({
    value: m.unit,
    label: texts.get(m.unit) ?? m.unit,
  }));
}

function splitSpec(detail: ElementDetail): Field[] {
  return [
    {
      kind: "checks",
      name: "units",
      label: "Mentions of the new sense",
      choices: mentionChoices(detail),
      required: true,
    },
    { kind: "text", name: "label", label: "Label of the new sense", required: true },
    { kind: "text", name: "scope_note", label: "Scope note of the new sense" },
    { kind: "text", name: "definition", label: "Definition of the new sense" },
    { kind: "text", name: "original_scope_note", label: "Scope note of the original" },
    reason(),
  ];
}

interface Others {
  concepts: Choice[];
  sameType: Choice[];
}

function others(detail: ElementDetail, elements: readonly IndexEntry[]): Others {
  const rest = elements.filter((e) => e.id !== detail.id);
  return {
    concepts: rest.filter((e) => e.type === "concept").map(choiceOf),
    sameType: rest.filter((e) => e.type === detail.type).map(choiceOf),
  };
}

function allConcepts(elements: readonly IndexEntry[]): Choice[] {
  return elements.filter((e) => e.type === "concept").map(choiceOf);
}

function fieldsOf(
  action: DialogAction,
  detail: ElementDetail,
  elements: readonly IndexEntry[],
): Field[] {
  switch (action) {
    case "exclude":
    case "reject":
      return [reason(true)];
    case "correct":
      return correctSpec(detail);
    case "level":
      return [
        {
          kind: "select",
          name: "level",
          label: "Level",
          choices: LEVELS,
          initial: detail.record.level,
        },
        reason(),
      ];
    case "merge":
      return [
        {
          kind: "select",
          name: "into",
          label: "Keep concept",
          choices: others(detail, elements).concepts,
          required: true,
        },
        reason(),
      ];
    case "split":
      return splitSpec(detail);
    case "reassign":
      return [
        {
          kind: "select",
          name: "unit",
          label: "Mention",
          choices: mentionChoices(detail),
          required: true,
        },
        {
          kind: "select",
          name: "concept",
          label: "Move to concept",
          choices: allConcepts(elements),
          required: true,
        },
        reason(),
      ];
    case "deprecate":
      return [
        {
          kind: "select",
          name: "replacement",
          label: "Replaced by",
          choices: others(detail, elements).sameType,
        },
        reason(),
      ];
  }
}

const WORDS: ReadonlyMap<DialogAction, { verb: string; submit: string }> = new Map([
  ["exclude", { verb: "Exclude", submit: "Exclude" }],
  ["reject", { verb: "Reject", submit: "Reject" }],
  ["correct", { verb: "Correct", submit: "Correct" }],
  ["level", { verb: "Set the level of", submit: "Set level" }],
  ["merge", { verb: "Merge", submit: "Merge" }],
  ["split", { verb: "Split the senses of", submit: "Split" }],
  ["reassign", { verb: "Reassign a mention of", submit: "Reassign" }],
  ["deprecate", { verb: "Deprecate", submit: "Deprecate" }],
]);

export function dialogFor(
  action: DialogAction,
  detail: ElementDetail,
  elements: readonly IndexEntry[],
): DialogSpec {
  const words = WORDS.get(action) ?? { verb: action, submit: action };
  const label = detail.record.label === "" ? detail.id : detail.record.label;
  return {
    action,
    title: `${words.verb} ${label}`,
    submit: words.submit,
    fields: fieldsOf(action, detail, elements),
  };
}

/** The first value of every field: its initial value, the first choice, or nothing. */
export function initialValues(spec: DialogSpec): Values {
  return new Map(
    spec.fields.map((field): [string, string | readonly string[]] => {
      if (field.kind === "checks") return [field.name, []];
      if (field.kind === "text") return [field.name, field.initial ?? ""];
      return [field.name, field.initial ?? (field.required ? (field.choices[0]?.value ?? "") : "")];
    }),
  );
}

function filled(value: string | readonly string[] | undefined): boolean {
  if (value === undefined) return false;
  return typeof value === "string" ? value.trim() !== "" : value.length > 0;
}

/** True when every required field has a value. */
export function complete(spec: DialogSpec, values: Values): boolean {
  return spec.fields.every((field) => !field.required || filled(values.get(field.name)));
}

/** The action's payload: every field with a value (text trimmed); empty ones are left out. */
export function payloadOf(spec: DialogSpec, values: Values): Record<string, unknown> {
  const entries: [string, unknown][] = [];
  for (const field of spec.fields) {
    const value = values.get(field.name);
    if (!filled(value)) continue;
    entries.push([field.name, typeof value === "string" ? value.trim() : value]);
  }
  return Object.fromEntries(entries);
}
