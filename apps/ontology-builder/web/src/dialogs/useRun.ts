// The steps of an LLM run (FR-6): estimate (no LLM call), confirm, run, then the run record.
// The run is one synchronous request (Q50): the dialog shows a running state until it returns.
import { useState } from "react";
import type { Estimate, RunBody, IngestOut, RunRecord } from "../api";
import { messageOf, type WorkApi } from "./workApi";

export type RunStep =
  | { step: "choose" }
  | { step: "estimating" }
  | { step: "estimated"; body: RunBody; estimate: Estimate }
  | { step: "running"; body: RunBody; estimate: Estimate }
  | { step: "done"; out: IngestOut; record: RunRecord | null };

export interface RunFlow {
  state: RunStep;
  problem: string | null;
  estimate: (body: RunBody) => Promise<void>;
  run: () => Promise<void>;
}

async function recordOf(api: WorkApi, ontology: string, id: string): Promise<RunRecord | null> {
  try {
    return await api.runRecord(ontology, id);
  } catch {
    return null;
  }
}

export function useRun(api: WorkApi, ontology: string, onChanged: () => Promise<void>): RunFlow {
  const [state, setState] = useState<RunStep>({ step: "choose" });
  const [problem, setProblem] = useState<string | null>(null);
  const estimate = async (body: RunBody) => {
    setState({ step: "estimating" });
    setProblem(null);
    try {
      setState({ step: "estimated", body, estimate: await api.estimate(ontology, body) });
    } catch (error) {
      setState({ step: "choose" });
      setProblem(messageOf(error));
    }
  };
  const run = async () => {
    if (state.step !== "estimated") return;
    setState({ ...state, step: "running" });
    setProblem(null);
    try {
      const out = await api.ingest(ontology, state.body);
      const record = await recordOf(api, ontology, out.run_id);
      setState({ step: "done", out, record });
      await onChanged();
    } catch (error) {
      setState(state);
      setProblem(messageOf(error));
    }
  };
  return { state, problem, estimate, run };
}
