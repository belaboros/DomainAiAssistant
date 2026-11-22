// Mark passages not ignorable (FR-14): the units the LLM proposed ignorable, with the category
// and reason; extraction on the chosen ones runs after the cost confirmation, like an ingestion.
import { useState } from "react";
import type { Unit } from "../api";
import { Modal, Problem } from "./Modal";
import { RunSteps } from "./RunSteps";
import { type RunFlow, useRun } from "./useRun";
import { useUnits } from "./useUnits";
import type { DialogProps } from "./workApi";

function ignorable(units: readonly Unit[]): Unit[] {
  return units.filter((u) => u.ignorable?.proposed === true && u.ignorable.status !== "rejected");
}

function category(unit: Unit): string {
  return unit.ignorable?.category.replaceAll("_", " ") ?? "";
}

function Chooser(props: { units: readonly Unit[]; flow: RunFlow; onClose: () => void }) {
  const { units, flow, onClose } = props;
  const [chosen, setChosen] = useState<readonly string[]>([]);
  const toggle = (id: string) => {
    setChosen(chosen.includes(id) ? chosen.filter((c) => c !== id) : [...chosen, id]);
  };
  if (units.length === 0) return <p>No passage is proposed ignorable.</p>;
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        void flow.estimate({ units: [...chosen] });
      }}
    >
      <div className="picker-list">
        {units.map((unit) => (
          <label key={unit.id} className="check">
            <input
              type="checkbox"
              checked={chosen.includes(unit.id)}
              onChange={() => {
                toggle(unit.id);
              }}
            />{" "}
            <span>{unit.text}</span>{" "}
            <span className="hint">
              ({category(unit)}: {unit.ignorable?.reason})
            </span>
          </label>
        ))}
      </div>
      <div className="dialog-buttons">
        <button type="submit" disabled={chosen.length === 0 || flow.state.step === "estimating"}>
          Estimate
        </button>
        <button type="button" className="secondary" onClick={onClose}>
          Cancel
        </button>
      </div>
    </form>
  );
}

export function NotIgnorableDialog({ ontology, api, onChanged, onClose }: DialogProps) {
  const units = useUnits(api, ontology);
  const flow = useRun(api, ontology, onChanged);
  const choosing = flow.state.step === "choose" || flow.state.step === "estimating";
  const close = () => {
    onClose();
  };
  return (
    <Modal title="Mark passages not ignorable" busy={flow.state.step === "running"} onClose={close}>
      {units.state === "loading" && <p className="loading">Loading the passages…</p>}
      {units.state === "ready" && choosing && (
        <Chooser units={ignorable(units.units)} flow={flow} onClose={close} />
      )}
      <RunSteps flow={flow} onClose={close} />
      <Problem message={units.state === "failed" ? units.message : flow.problem} />
    </Modal>
  );
}
