// The filters of the element list (FR-19): type, status, level, corpus and document, and a
// full-text search over labels, definitions and evidence text.
import type { Corpus } from "../api";
import { documentsOf, type IndexFilters } from "./filter";
import { LEVEL_NAME } from "./LevelBadge";
import { STATUS_LOOK } from "./StatusBadge";

interface Option {
  value: string;
  label: string;
}

const TYPES: readonly Option[] = [
  { value: "statement", label: "Statement" },
  { value: "term", label: "Term" },
  { value: "concept", label: "Concept" },
  { value: "relation", label: "Relation" },
  { value: "rule", label: "Rule" },
  { value: "property", label: "Property" },
];

const STATUSES: readonly Option[] = Object.entries(STATUS_LOOK).map(([value, look]) => ({
  value,
  label: look.label,
}));

const LEVELS: readonly Option[] = Object.entries(LEVEL_NAME).map(([value, label]) => ({
  value,
  label,
}));

interface ChoiceProps {
  label: string;
  all: string;
  value: string;
  options: readonly Option[];
  onChange: (value: string) => void;
}

function Choice({ label, all, value, options, onChange }: ChoiceProps) {
  return (
    <label>
      {label}
      <select
        value={value}
        onChange={(event) => {
          onChange(event.target.value);
        }}
      >
        <option value="">{all}</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

export interface FilterBarProps {
  filters: IndexFilters;
  corpora: readonly Corpus[];
  onChange: (filters: IndexFilters) => void;
}

export function FilterBar({ filters, corpora, onChange }: FilterBarProps) {
  const corpus = filters.corpus ?? "";
  const set = (change: IndexFilters) => {
    onChange({ ...filters, ...change });
  };
  const corpusOptions = corpora.map((c) => ({ value: c.folder, label: c.folder }));
  const documentOptions = documentsOf(corpora, corpus).map((d) => ({
    value: d.id,
    label: d.label,
  }));
  return (
    <section className="filters" aria-label="Filters">
      <label className="search">
        Search
        <input
          type="search"
          value={filters.q ?? ""}
          placeholder="Labels, definitions, evidence"
          onChange={(event) => {
            set({ q: event.target.value });
          }}
        />
      </label>
      <Choice
        label="Type"
        all="All types"
        value={filters.type ?? ""}
        options={TYPES}
        onChange={(type) => {
          set({ type });
        }}
      />
      <Choice
        label="Status"
        all="All statuses"
        value={filters.status ?? ""}
        options={STATUSES}
        onChange={(status) => {
          set({ status });
        }}
      />
      <Choice
        label="Level"
        all="All levels"
        value={filters.level ?? ""}
        options={LEVELS}
        onChange={(level) => {
          set({ level });
        }}
      />
      <Choice
        label="Corpus"
        all="All corpora"
        value={corpus}
        options={corpusOptions}
        onChange={(chosen) => {
          set({ corpus: chosen, document: "" });
        }}
      />
      <Choice
        label="Document"
        all="All documents"
        value={filters.document ?? ""}
        options={documentOptions}
        onChange={(document) => {
          set({ document });
        }}
      />
    </section>
  );
}
