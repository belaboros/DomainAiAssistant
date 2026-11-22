// Ingest a folder of Markdown files as a new corpus (FR-4, FR-6): the folder (under the sources
// root), the estimate, the confirmation, the running state and the run record.
import { useState } from "react";
import { Modal, Problem } from "./Modal";
import { RunSteps } from "./RunSteps";
import { useRun } from "./useRun";
import type { DialogProps } from "./workApi";

export function IngestDialog({ ontology, api, onChanged, onClose }: DialogProps) {
  const [folder, setFolder] = useState("");
  const flow = useRun(api, ontology, onChanged);
  const choosing = flow.state.step === "choose" || flow.state.step === "estimating";
  const close = () => {
    onClose();
  };
  return (
    <Modal title="Ingest a folder" busy={flow.state.step === "running"} onClose={close}>
      {choosing && (
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void flow.estimate({ folder: folder.trim() });
          }}
        >
          <label>
            Folder
            <input
              value={folder}
              autoFocus
              placeholder="user-manuals-pets-and-house-rules/dog-owners-manual"
              onChange={(event) => {
                setFolder(event.target.value);
              }}
            />
          </label>
          <p className="hint">
            A folder under the shared data folder; its Markdown files, sub-folders included, become
            a new corpus. Nothing is sent to the LLM before you confirm the estimate.
          </p>
          <div className="dialog-buttons">
            <button
              type="submit"
              disabled={folder.trim() === "" || flow.state.step === "estimating"}
            >
              Estimate
            </button>
            <button type="button" className="secondary" onClick={close}>
              Cancel
            </button>
          </div>
        </form>
      )}
      <RunSteps flow={flow} onClose={close} />
      <Problem message={flow.problem} />
    </Modal>
  );
}
