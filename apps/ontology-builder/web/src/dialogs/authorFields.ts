// What the author dialog asks for, per element type (FR-22): the fields each type needs, as plain
// data that FieldInput renders; the server checks the record again.
import type { ElementType, IndexEntry } from "../api";
import { type Choice, choiceOf, type Field, LEVELS } from "../review/actionDialogs";

export const TYPES: readonly Choice[] = [
  { value: "concept", label: "Concept" },
  { value: "relation", label: "Relation" },
  { value: "rule", label: "Rule" },
  { value: "term", label: "Term" },
  { value: "property", label: "Property" },
  { value: "statement", label: "Statement" },
];

const MODALITIES: readonly Choice[] = [
  { value: "must", label: "must" },
  { value: "must_not", label: "must not" },
  { value: "may", label: "may" },
];

function text(name: string, label: string, required = false): Field {
  return { kind: "text", name, label, required };
}

function select(name: string, label: string, choices: readonly Choice[]): Field {
  return { kind: "select", name, label, choices, required: true };
}

function concepts(elements: readonly IndexEntry[]): Choice[] {
  return elements.filter((e) => e.type === "concept").map(choiceOf);
}

function specific(type: ElementType, elements: readonly IndexEntry[]): Field[] {
  switch (type) {
    case "statement":
      return [text("text", "Text", true)];
    case "term":
      return [text("definition", "Definition")];
    case "concept":
      return [text("definition", "Definition"), text("scope_note", "Scope note")];
    case "relation":
      return [
        select("subject", "Subject", concepts(elements)),
        text("predicate_label", "Predicate label", true),
        select("object", "Object", concepts(elements)),
        text("definition", "Definition"),
      ];
    case "rule":
      return [
        select("modality", "Modality", MODALITIES),
        text("actor", "Actor", true),
        text("action", "Action", true),
        text("condition", "Condition"),
      ];
    case "property":
      return [
        select("of", "Of element", elements.map(choiceOf)),
        text("name", "Name", true),
        text("value", "Value", true),
        text("unit", "Unit"),
      ];
  }
}

/** The fields of an authored element of ``type``: label and level first, then its own. */
export function authorFields(type: ElementType, elements: readonly IndexEntry[]): Field[] {
  return [
    text("label", "Label", true),
    { kind: "select", name: "level", label: "Level", choices: LEVELS, required: true },
    ...specific(type, elements),
  ];
}
