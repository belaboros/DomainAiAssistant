// Entry point of the review GUI: mounts the app shell with the real API calls.
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { act, currentSession, elementDetail, elementIndex, signIn, signOut } from "./api";
import { App } from "./shell/App";
import "./styles.css";

const API = { currentSession, signIn, signOut, elementIndex, element: elementDetail, act };

const root = document.getElementById("root");
if (root === null) throw new Error("index.html has no #root element");
createRoot(root).render(
  <StrictMode>
    <App api={API} />
  </StrictMode>,
);
