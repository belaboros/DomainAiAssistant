// Entry point of the review GUI: mounts the app shell with the real API calls.
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  act,
  addStatement,
  author,
  currentSession,
  elementDetail,
  elementIndex,
  estimate,
  ingest,
  publish,
  reviseStatement,
  runRecord,
  save,
  signIn,
  signOut,
  units,
} from "./api";
import { App } from "./shell/App";
import "./styles.css";

const API = {
  currentSession,
  signIn,
  signOut,
  elementIndex,
  element: elementDetail,
  act,
  units,
  addStatement,
  reviseStatement,
  author,
  estimate,
  ingest,
  runRecord,
  save,
  publish,
};

const root = document.getElementById("root");
if (root === null) throw new Error("index.html has no #root element");
createRoot(root).render(
  <StrictMode>
    <App api={API} />
  </StrictMode>,
);
