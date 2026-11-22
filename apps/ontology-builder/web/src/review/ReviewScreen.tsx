// The review screen: loads the compact index of the open ontology, filters it in the browser
// (FR-19), runs bulk actions (FR-18) on the selected elements that are shown, and shows the open
// element in the detail pane (FR-16, FR-17; j/k move through the shown elements). After an
// action the index and the open element are loaded again, since the server decides what changed.
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type {
  ActionIn,
  ActionsOut,
  ElementDetail as Detail,
  ElementsOut,
  IndexEntry,
  SessionOut,
} from "../api";
import type { DetailAct } from "./Actions";
import { BulkBar, type BulkAct } from "./BulkBar";
import { ElementDetail } from "./ElementDetail";
import { ElementList } from "./ElementList";
import { filterIndex, type IndexFilters } from "./filter";
import { FilterBar } from "./FilterBar";
import { useShortcuts } from "./shortcuts";

/** The review calls of the API; injected so the screen can be tested without a server. */
export interface ReviewApi {
  elementIndex: (ontology: string) => Promise<ElementsOut>;
  element: (ontology: string, id: string) => Promise<Detail>;
  act: (ontology: string, body: ActionIn) => Promise<ActionsOut>;
}

type Opened =
  | { state: "none" }
  | { state: "loading" }
  | { state: "failed"; message: string }
  | { state: "ready"; detail: Detail };

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

/** The open element; a late answer for an element that is no longer open is dropped. */
function useOpened(api: ReviewApi, ontology: string) {
  const [current, setCurrent] = useState<string | null>(null);
  const [opened, setOpened] = useState<Opened>({ state: "none" });
  const latest = useRef<string | null>(null);
  const load = useCallback(
    async (id: string) => {
      try {
        const detail = await api.element(ontology, id);
        if (latest.current === id) setOpened({ state: "ready", detail });
      } catch (error) {
        if (latest.current === id) setOpened({ state: "failed", message: messageOf(error) });
      }
    },
    [api, ontology],
  );
  const open = (id: string) => {
    if (id === latest.current) return;
    latest.current = id;
    setCurrent(id);
    setOpened({ state: "loading" });
    void load(id);
  };
  return { current, opened, open, load };
}

/** The element after (or before) the current one among those shown; the first if none is. */
function stepped(shown: readonly IndexEntry[], current: string | null, by: 1 | -1): string | null {
  if (shown.length === 0) return null;
  const at = shown.findIndex((e) => e.id === current);
  if (at < 0) return shown[0]?.id ?? null;
  const next = Math.min(Math.max(at + by, 0), shown.length - 1);
  return shown.at(next)?.id ?? null;
}

interface DetailPaneProps {
  opened: Opened;
  session: SessionOut;
  index: ElementsOut;
  act: DetailAct;
}

function DetailPane({ opened, session, index, act }: DetailPaneProps) {
  if (opened.state === "none") {
    return <p className="hint">Open an element to review it, or press j.</p>;
  }
  if (opened.state === "loading") return <p className="loading">Loading the element…</p>;
  if (opened.state === "failed") {
    return (
      <p className="problem" role="alert">
        {opened.message}
      </p>
    );
  }
  return (
    <ElementDetail
      detail={opened.detail}
      corpora={index.corpora}
      elements={index.elements}
      role={session.role}
      writer={session.writer}
      act={act}
    />
  );
}

function PendingLine({ pending }: { pending: number }) {
  if (pending === 0) return null;
  return <span>{pending === 1 ? "1 unsaved change" : `${String(pending)} unsaved changes`}</span>;
}

interface ReadyProps {
  session: SessionOut;
  index: ElementsOut;
  act: BulkAct;
  opened: Opened;
  current: string | null;
  open: (id: string) => void;
  actOnOpen: DetailAct;
}

function Ready({ session, index, act, opened, current, open, actOnOpen }: ReadyProps) {
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
  useShortcuts((shortcut) => {
    if (shortcut.kind !== "next" && shortcut.kind !== "previous") return;
    const id = stepped(shown, current, shortcut.kind === "next" ? 1 : -1);
    if (id !== null) open(id);
  }, true);
  return (
    <div className="review-panes">
      <div className="list-pane">
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
          current={current}
          onOpen={open}
          onToggle={(id) => {
            setSelected(toggled(selected, id));
          }}
          onToggleAll={toggleAll}
        />
      </div>
      <div className="detail-pane">
        <DetailPane opened={opened} session={session} index={index} act={actOnOpen} />
      </div>
    </div>
  );
}

export function ReviewScreen({ session, api }: { session: SessionOut; api: ReviewApi }) {
  const { ontology } = session;
  const { loaded, reload } = useIndex(api, ontology);
  const { current, opened, open, load } = useOpened(api, ontology);
  const act: BulkAct = async (action, ids, payload) => {
    const out = await api.act(ontology, { action, ids: [...ids], payload });
    await reload();
    if (current !== null) await load(current);
    return out.results;
  };
  const actOnOpen: DetailAct = async (action, payload) => {
    if (current === null) return [];
    const out = await api.act(ontology, { action, ids: [current], payload });
    await Promise.all([reload(), load(current)]);
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
  return (
    <Ready
      session={session}
      index={loaded.index}
      act={act}
      opened={opened}
      current={current}
      open={open}
      actOnOpen={actOnOpen}
    />
  );
}
