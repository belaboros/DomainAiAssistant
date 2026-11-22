// Publish a governed release (FR-29, FR-35; domain admin only): a version, empty for the next
// minor one; then the version and its change log, or the offenders that blocked it.
import { useState } from "react";
import type { PublishOut, Reference } from "../api";
import { CommitLine } from "./CommitLine";
import { Modal, Problem } from "./Modal";
import { type DialogProps, messageOf } from "./workApi";

function References({ found }: { found: readonly Reference[] }) {
  return (
    <ul>
      {found.map((r) => (
        <li key={`${r.element_id}-${r.target_id}`}>
          {r.element_label} → {r.target_label} ({r.target_status})
        </li>
      ))}
    </ul>
  );
}

function Published({ out }: { out: PublishOut }) {
  return (
    <div className="publish-result">
      {out.version === null ? (
        <>
          <p className="problem" role="alert">
            Not published: these approved elements refer to elements that are not approved. Approve
            or fix them, then publish again. The raw release was rebuilt.
          </p>
          <References found={out.offenders} />
        </>
      ) : (
        <>
          <p>Published version {out.version}.</p>
          {out.changelog !== null && <pre className="changelog">{out.changelog}</pre>}
        </>
      )}
      {out.warnings.length > 0 && (
        <>
          <p>These elements still refer to deprecated elements:</p>
          <References found={out.warnings} />
        </>
      )}
      <CommitLine commit={out.commit} done="Committed" />
    </div>
  );
}

function VersionForm(props: {
  busy: boolean;
  onPublish: (v: string | null) => void;
  onClose: () => void;
}) {
  const [version, setVersion] = useState("");
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        props.onPublish(version.trim() === "" ? null : version.trim());
      }}
    >
      <label>
        Version (empty: the next minor version)
        <input
          value={version}
          autoFocus
          placeholder="1.1.0"
          onChange={(event) => {
            setVersion(event.target.value);
          }}
        />
      </label>
      <div className="dialog-buttons">
        <button type="submit" disabled={props.busy}>
          Publish
        </button>
        <button type="button" className="secondary" disabled={props.busy} onClick={props.onClose}>
          Cancel
        </button>
      </div>
    </form>
  );
}

export function PublishDialog({ ontology, api, onChanged, onClose }: DialogProps) {
  const [busy, setBusy] = useState(false);
  const [out, setOut] = useState<PublishOut | null>(null);
  const [problem, setProblem] = useState<string | null>(null);
  const close = () => {
    onClose();
  };
  const publish = async (version: string | null) => {
    setBusy(true);
    setProblem(null);
    try {
      setOut(await api.publish(ontology, version));
      await onChanged();
    } catch (error) {
      setProblem(messageOf(error));
    } finally {
      setBusy(false);
    }
  };
  return (
    <Modal title="Publish a governed release" busy={busy} onClose={close}>
      {out === null ? (
        <VersionForm busy={busy} onPublish={(v) => void publish(v)} onClose={close} />
      ) : (
        <>
          <Published out={out} />
          <div className="dialog-buttons">
            <button type="button" onClick={close}>
              Close
            </button>
          </div>
        </>
      )}
      {busy && <p className="loading">Building the releases… the git hooks run after.</p>}
      <Problem message={problem} />
    </Modal>
  );
}
