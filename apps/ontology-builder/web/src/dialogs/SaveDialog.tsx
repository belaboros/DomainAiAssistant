// Save (FR-27): the pending changes, the decisions and the rebuilt raw release as one commit,
// with the hooks running; the dialog shows the commit, or the hook output when a hook refused.
import type { CommitOut } from "../api";
import { CommitLine } from "./CommitLine";
import { Modal, Problem } from "./Modal";

export type Saving =
  | { state: "saving" }
  | { state: "saved"; commit: CommitOut }
  | { state: "failed"; message: string };

export function SaveDialog({ saving, onClose }: { saving: Saving; onClose: () => void }) {
  const busy = saving.state === "saving";
  return (
    <Modal title="Save" busy={busy} onClose={onClose}>
      {busy && <p className="loading">Saving… the git hooks are running.</p>}
      {saving.state === "saved" && <CommitLine commit={saving.commit} done="Saved" />}
      <Problem message={saving.state === "failed" ? saving.message : null} />
      <div className="dialog-buttons">
        <button type="button" disabled={busy} onClick={onClose}>
          Close
        </button>
      </div>
    </Modal>
  );
}
