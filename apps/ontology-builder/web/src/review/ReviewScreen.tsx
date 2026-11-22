// The review screen: loads the compact index of the open ontology, filters it in the browser
// (FR-19), and runs bulk actions (FR-18) on the selected elements that are shown. After an
// action the index is loaded again, since the server decides what changed.
import { useCallback, useEffect, useMemo, useState } from "react";
import type { ActionIn, ActionsOut, ElementsOut, SessionOut } from "../api";
import { BulkBar, type BulkAct } from "./BulkBar";
import { ElementList } from "./ElementList";
import { filterIndex, type IndexFilters } from "./filter";
import { FilterBar } from "./FilterBar";

/** The review calls of the API; injected so the screen can be tested without a server. */
export interface ReviewApi {
  elementIndex: (ontology: string) => Promise<ElementsOut>;
  act: (ontology: string, body: ActionIn) => Promise<ActionsOut>;
}

type Loaded =
  | { state: "loading" }
  | { state: "failed"; message: string }
  | { state: "ready"; index: ElementsOut };

function messageOf(error: unknown): string {
  return error instanceof Error ? error.message : "the element index could not be loaded";
}

function toggled(selected: ReadonlySet<string>, id: string): Set<string> {
  const next = new Set(selected);
  if (next.has(id)) next.delete(id);
  else next.add(id);
  return next;
}

function useIndex(api: ReviewApi, ontology: string) {
  const [loaded, setLoaded] = useState<Loaded>({ state: "loading" });
  const reload = useCallback(
    () =>
      api.elementIndex(ontology).then(
        (index) => {
          setLoaded({ state: "ready", index });
        },
        (error: unknown) => {
          setLoaded({ state: "failed", message: messageOf(error) });
        },
      ),
    [api, ontology],
  );
  useEffect(() => {
    void reload();
  }, [reload]);
  return { loaded, reload };
}

function PendingLine({ pending }: { pending: number }) {
  if (pending === 0) return null;
  return <span>{pending === 1 ? "1 unsaved change" : `${String(pending)} unsaved changes`}</span>;
}

interface ReadyProps {
  session: SessionOut;
  index: ElementsOut;
  act: BulkAct;
}

function Ready({ session, index, act }: ReadyProps) {
  const [filters, setFilters] = useState<IndexFilters>({});
  const [selected, setSelected] = useState<ReadonlySet<string>>(new Set());
  const shown = useMemo(() => filterIndex(index.elements, filters), [index, filters]);
  const chosen = useMemo(
    () => shown.filter((e) => selected.has(e.id)).map((e) => e.id),
    [shown, selected],
  );
  const toggleAll = (on: boolean) => {
    const next = new Set(selected);
    for (const entry of shown) {
      if (on) next.add(entry.id);
      else next.delete(entry.id);
    }
    setSelected(next);
  };
  return (
    <>
      <FilterBar filters={filters} corpora={index.corpora} onChange={setFilters} />
      <BulkBar
        selected={chosen}
        role={session.role}
        writer={session.writer}
        act={act}
        onClear={() => {
          setSelected(new Set());
        }}
      />
      <p className="counts">
        {shown.length} of {index.elements.length} elements <PendingLine pending={index.pending} />
      </p>
      <ElementList
        entries={shown}
        selected={selected}
        onToggle={(id) => {
          setSelected(toggled(selected, id));
        }}
        onToggleAll={toggleAll}
      />
    </>
  );
}

export function ReviewScreen({ session, api }: { session: SessionOut; api: ReviewApi }) {
  const { ontology } = session;
  const { loaded, reload } = useIndex(api, ontology);
  const act: BulkAct = async (action, ids, payload) => {
    const out = await api.act(ontology, { action, ids: [...ids], payload });
    await reload();
    return out.results;
  };
  if (loaded.state === "loading") return <p className="loading">Loading the elements…</p>;
  if (loaded.state === "failed") {
    return (
      <p className="problem" role="alert">
        {loaded.message}
      </p>
    );
  }
  return <Ready session={session} index={loaded.index} act={act} />;
}
