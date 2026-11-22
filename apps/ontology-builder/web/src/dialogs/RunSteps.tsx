// What an ingestion dialog shows after the choice: the estimate and the confirm button, the
// running state, then the run record and its commit (FR-6, FR-27).
import type { Estimate, IngestOut, RunRecord } from "../api";
import { CommitLine } from "./CommitLine";
import type { RunFlow } from "./useRun";
import { count } from "./workApi";

function cost(estimate: Estimate): string {
  if (estimate.cost_usd === null) {
    return `Estimated cost: no price is known for ${estimate.model}, so only the tokens are shown.`;
  }
  return `Estimated cost: about $${estimate.cost_usd.toFixed(2)}.`;
}

export function EstimateLines({ estimate }: { estimate: Estimate }) {
  return (
    <div className="estimate">
      <p>
        {count(estimate.documents)} documents · {count(estimate.units)} source units
      </p>
      <p>
        {count(estimate.input_tokens)} input tokens and up to {count(estimate.output_tokens)} output
        tokens with {estimate.model}
      </p>
      <p>{cost(estimate)}</p>
    </div>
  );
}

function confirmLabel(estimate: Estimate): string {
  return estimate.cost_usd === null ? "Run" : `Run for about $${estimate.cost_usd.toFixed(2)}`;
}

function Record({ record }: { record: RunRecord }) {
  return (
    <>
      <p>
        {record.model}: {count(record.input_tokens)} input tokens, {count(record.output_tokens)}{" "}
        output tokens
      </p>
      <p>
        Started {record.started_at}, ended {record.ended_at ?? "not yet"}
      </p>
      {record.skipped && record.skipped.length > 0 && (
        <>
          <h3>Skipped items</h3>
          <ul>
            {record.skipped.map((item, at) => (
              <li key={at}>
                {item.where}: {item.item} ({item.reason})
              </li>
            ))}
          </ul>
        </>
      )}
    </>
  );
}

function Finished({ out, record }: { out: IngestOut; record: RunRecord | null }) {
  return (
    <div className="run-record">
      <p>
        Run <code>{out.run_id}</code>: <strong>{out.status}</strong>
      </p>
      {record !== null && <Record record={record} />}
      <CommitLine commit={out.commit} done="Committed" />
    </div>
  );
}

export function RunSteps({ flow, onClose }: { flow: RunFlow; onClose: () => void }) {
  const { state } = flow;
  if (state.step === "estimated") {
    return (
      <>
        <EstimateLines estimate={state.estimate} />
        <div className="dialog-buttons">
          <button type="button" onClick={() => void flow.run()}>
            {confirmLabel(state.estimate)}
          </button>
          <button type="button" className="secondary" onClick={onClose}>
            Cancel
          </button>
        </div>
      </>
    );
  }
  if (state.step === "running") {
    return (
      <p className="loading">
        Running on {count(state.estimate.documents)} documents and {count(state.estimate.units)}{" "}
        source units. This can take a few minutes; the result is committed when it ends.
      </p>
    );
  }
  if (state.step === "done") {
    return (
      <>
        <Finished out={state.out} record={state.record} />
        <div className="dialog-buttons">
          <button type="button" onClick={onClose}>
            Close
          </button>
        </div>
      </>
    );
  }
  return null;
}
