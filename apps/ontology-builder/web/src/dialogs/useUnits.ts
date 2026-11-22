// The source units of the open ontology, loaded when a dialog that picks from them opens.
import { useEffect, useState } from "react";
import type { Unit } from "../api";
import { messageOf, type WorkApi } from "./workApi";

export type Units =
  | { state: "loading" }
  | { state: "failed"; message: string }
  | { state: "ready"; units: readonly Unit[] };

export function useUnits(api: WorkApi, ontology: string): Units {
  const [units, setUnits] = useState<Units>({ state: "loading" });
  useEffect(() => {
    let live = true;
    api.units(ontology).then(
      (found) => {
        if (live) setUnits({ state: "ready", units: found });
      },
      (error: unknown) => {
        if (live) setUnits({ state: "failed", message: messageOf(error) });
      },
    );
    return () => {
      live = false;
    };
  }, [api, ontology]);
  return units;
}
