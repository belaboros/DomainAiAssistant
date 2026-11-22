// The API calls of the work bar's dialogs (T26); injected so they can be tested without a server.
import type {
  AuthorIn,
  CommitOut,
  Estimate,
  RunBody,
  IngestOut,
  PublishOut,
  RunRecord,
  Unit,
} from "../api";

export interface WorkApi {
  units: (ontology: string) => Promise<Unit[]>;
  addStatement: (ontology: string, text: string) => Promise<string>;
  reviseStatement: (ontology: string, id: string, text: string) => Promise<string>;
  author: (ontology: string, body: AuthorIn) => Promise<string>;
  estimate: (ontology: string, body: RunBody) => Promise<Estimate>;
  ingest: (ontology: string, body: RunBody) => Promise<IngestOut>;
  runRecord: (ontology: string, id: string) => Promise<RunRecord>;
  save: (ontology: string) => Promise<CommitOut>;
  publish: (ontology: string, version: string | null) => Promise<PublishOut>;
}

/** What every dialog of the work bar gets. */
export interface DialogProps {
  ontology: string;
  api: WorkApi;
  /** Reload what the server changed (the element index, the open element). */
  onChanged: () => Promise<void>;
  /** Close the dialog, with a message for the work bar's status line when there is one. */
  onClose: (message?: string) => void;
}

export function messageOf(error: unknown): string {
  return error instanceof Error ? error.message : "the request failed";
}

/** A number as people read it: 198,000. */
export function count(value: number): string {
  return value.toLocaleString("en-US");
}
