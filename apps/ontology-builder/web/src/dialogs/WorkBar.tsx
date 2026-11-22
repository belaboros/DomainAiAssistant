// The work bar above the review panes (T26): user statements, authoring, ingestion, marking
// passages not ignorable, Save and, for a domain admin, Publish. A read-only session can open
// none of them; a user sees Publish disabled with the reason (FR-3).
import { useState } from "react";
import type { IndexEntry, Role } from "../api";
import { AuthorDialog } from "./AuthorDialog";
import { IngestDialog } from "./IngestDialog";
import { NotIgnorableDialog } from "./NotIgnorableDialog";
import { PublishDialog } from "./PublishDialog";
import { SaveDialog, type Saving } from "./SaveDialog";
import { EditStatementDialog, NewStatementDialog } from "./StatementDialog";
import { type DialogProps, messageOf, type WorkApi } from "./workApi";

export interface WorkBarProps {
  ontology: string;
  role: Role;
  writer: boolean;
  elements: readonly IndexEntry[];
  api: WorkApi;
  onChanged: () => Promise<void>;
}

type Open = "new" | "edit" | "author" | "ingest" | "ignorable" | "publish" | null;

function Dialog({
  open,
  props,
  elements,
}: {
  open: Open;
  props: DialogProps;
  elements: readonly IndexEntry[];
}) {
  switch (open) {
    case "new":
      return <NewStatementDialog {...props} />;
    case "edit":
      return <EditStatementDialog {...props} />;
    case "author":
      return <AuthorDialog {...props} elements={elements} />;
    case "ingest":
      return <IngestDialog {...props} />;
    case "ignorable":
      return <NotIgnorableDialog {...props} />;
    case "publish":
      return <PublishDialog {...props} />;
    case null:
      return null;
  }
}

function useSave(api: WorkApi, ontology: string, onChanged: () => Promise<void>) {
  const [saving, setSaving] = useState<Saving | null>(null);
  const save = async () => {
    setSaving({ state: "saving" });
    try {
      const commit = await api.save(ontology);
      setSaving({ state: "saved", commit });
      if (commit.ok) await onChanged();
    } catch (error) {
      setSaving({ state: "failed", message: messageOf(error) });
    }
  };
  return {
    saving,
    save,
    close: () => {
      setSaving(null);
    },
  };
}

export function WorkBar({ ontology, role, writer, elements, api, onChanged }: WorkBarProps) {
  const [open, setOpen] = useState<Open>(null);
  const [status, setStatus] = useState<string | null>(null);
  const { saving, save, close } = useSave(api, ontology, onChanged);
  const admin = role === "domain_admin";
  const props: DialogProps = {
    ontology,
    api,
    onChanged,
    onClose: (message) => {
      setOpen(null);
      setStatus(message ?? null);
    },
  };
  const button = (label: string, which: Exclude<Open, null>) => (
    <button
      type="button"
      disabled={!writer}
      onClick={() => {
        setStatus(null);
        setOpen(which);
      }}
    >
      {label}
    </button>
  );
  return (
    <section className="work-bar" aria-label="Work">
      {button("New statement…", "new")}
      {button("Edit statement…", "edit")}
      {button("Author element…", "author")}
      {button("Ingest folder…", "ingest")}
      {button("Mark not ignorable…", "ignorable")}
      <button type="button" disabled={!writer} onClick={() => void save()}>
        Save
      </button>
      <button
        type="button"
        disabled={!writer || !admin}
        aria-describedby={admin ? undefined : "publish-admin-only"}
        onClick={() => {
          setOpen("publish");
        }}
      >
        Publish…
      </button>
      {!admin && (
        <span className="hint" id="publish-admin-only">
          Only a domain admin can publish.
        </span>
      )}
      {status !== null && <p role="status">{status}</p>}
      <Dialog open={open} props={props} elements={elements} />
      {saving !== null && <SaveDialog saving={saving} onClose={close} />}
    </section>
  );
}
