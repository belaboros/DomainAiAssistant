// The open element (FR-16): its evidence passages first, then the proposal (type, label, level,
// reason; for an authored element, who wrote it), the actions, and the decision history.
import type { Corpus, ElementDetail as Detail, Evidence, IndexEntry, Role } from "../api";
import { Actions, type DetailAct } from "./Actions";
import { fieldName } from "./actionDialogs";
import { DecisionHistory } from "./DecisionHistory";
import { LEVEL_NAME, LevelBadge } from "./LevelBadge";
import { StatusBadge } from "./StatusBadge";

export interface ElementDetailProps {
  detail: Detail;
  corpora: readonly Corpus[];
  elements: readonly IndexEntry[];
  role: Role;
  writer: boolean;
  act: DetailAct;
}

/** Record fields shown on their own, or not at all; the others are listed by name. */
const SHOWN_APART = new Set([
  "id",
  "label",
  "definition",
  "level",
  "level_reason",
  "status",
  "status_reason",
  "origin",
  "replaced_by",
  "evidence",
  "mentions",
  "approved_snapshot",
]);

function documentNames(corpora: readonly Corpus[]): Map<string, string> {
  return new Map(
    corpora.flatMap((c) => c.documents.map((d): [string, string] => [d.id, d.title ?? d.path])),
  );
}

function Passage({ evidence, names }: { evidence: Evidence; names: Map<string, string> }) {
  if (evidence.text == null) {
    return <li className="passage missing">The passage {evidence.unit} was not found.</li>;
  }
  const document = evidence.document == null ? undefined : names.get(evidence.document);
  const quoted = evidence.quote != null && !evidence.text.includes(evidence.quote);
  return (
    <li className="passage" id={evidence.unit}>
      <blockquote>{evidence.text}</blockquote>
      {quoted && <p className="quote">Quoted: {evidence.quote}</p>}
      <p className="where">
        {[evidence.corpus, document ?? evidence.document, evidence.unit]
          .filter((part) => part != null)
          .join(" · ")}
      </p>
    </li>
  );
}

function EvidenceSection({ detail, corpora }: { detail: Detail; corpora: readonly Corpus[] }) {
  const names = documentNames(corpora);
  return (
    <section className="evidence" aria-label="Evidence">
      <h3>Evidence</h3>
      <ol>
        {detail.evidence.map((evidence) => (
          <Passage key={evidence.unit} evidence={evidence} names={names} />
        ))}
      </ol>
    </section>
  );
}

function shown(value: unknown): string {
  if (typeof value === "string") return value;
  if (Array.isArray(value) && value.every((v) => typeof v === "string")) return value.join(", ");
  return JSON.stringify(value);
}

function Extras({ detail }: { detail: Detail }) {
  const extras = Object.entries(detail.record).filter(
    ([key, value]) => !SHOWN_APART.has(key) && value != null,
  );
  return extras.map(([key, value]) => (
    <div key={key}>
      <dt>{fieldName(key)}</dt>
      <dd>{shown(value)}</dd>
    </div>
  ));
}

function ProposalSection({ detail }: { detail: Detail }) {
  const { record } = detail;
  const name =
    record.origin.kind === "llm"
      ? "LLM proposal"
      : `Authored by ${record.origin.author ?? "a user"}`;
  return (
    <section className="proposal" aria-label={name}>
      <h3>{name}</h3>
      <p className="kind">{detail.type}</p>
      <h2>{record.label === "" ? detail.id : record.label}</h2>
      {record.definition != null && <p className="definition">{record.definition}</p>}
      <dl>
        <div>
          <dt>Level</dt>
          <dd>
            <LevelBadge level={record.level} /> <span>{LEVEL_NAME[record.level]}</span>
            <p className="reason">{record.level_reason}</p>
          </dd>
        </div>
        <div>
          <dt>Status</dt>
          <dd>
            <StatusBadge status={record.status} />
            {record.status_reason != null && <p className="reason">{record.status_reason}</p>}
          </dd>
        </div>
        {record.replaced_by != null && (
          <div>
            <dt>Replaced by</dt>
            <dd>{record.replaced_by}</dd>
          </div>
        )}
        <Extras detail={detail} />
      </dl>
      {detail.pending && <p className="hint">This element has unsaved changes.</p>}
    </section>
  );
}

export function ElementDetail(props: ElementDetailProps) {
  const { detail, corpora, elements, role, writer, act } = props;
  return (
    <article className="element-detail" aria-label="Element detail">
      <EvidenceSection detail={detail} corpora={corpora} />
      <ProposalSection detail={detail} />
      <Actions
        key={detail.id}
        detail={detail}
        elements={elements}
        role={role}
        writer={writer}
        act={act}
      />
      <DecisionHistory decisions={detail.decisions} />
    </article>
  );
}
