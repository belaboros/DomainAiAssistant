// The app shell: asks the server who is signed in, shows the sign-in window until someone is,
// then the header (ontology, user, role, read-only notice, sign-out) around the review screen.
import { useEffect, useState } from "react";
import type { Role, SessionOut, SignIn as SignInBody } from "../api";
import { type ReviewApi, ReviewScreen } from "../review/ReviewScreen";
import { SignIn } from "../signin/SignIn";

/** The session calls of the API; injected so the shell can be tested without a server. */
export interface SessionApi {
  currentSession: () => Promise<SessionOut | null>;
  signIn: (body: SignInBody) => Promise<SessionOut>;
  signOut: () => Promise<void>;
}

/** Every API call the shell and its screens use. */
export type AppApi = SessionApi & ReviewApi;

const ROLE_LABEL: Record<Role, string> = { user: "User", domain_admin: "Domain admin" };

type Loaded = { state: "loading" } | { state: "failed"; message: string } | { state: "ready" };

function messageOf(error: unknown): string {
  return error instanceof Error ? error.message : "the server is not reachable";
}

function Header({ session, onSignOut }: { session: SessionOut; onSignOut: () => void }) {
  return (
    <header className="shell-header">
      <span className="app-name">OntologyBuilder</span>
      <span className="ontology">{session.ontology}</span>
      <span className="who">
        Signed in as <strong>{session.user}</strong> · <span>{ROLE_LABEL[session.role]}</span>
      </span>
      {!session.writer && (
        <span className="read-only">
          Read-only: another session of this server is signed in, so this one cannot change
          anything.
        </span>
      )}
      <button type="button" onClick={onSignOut}>
        Sign out
      </button>
    </header>
  );
}

export function App({ api }: { api: AppApi }) {
  const [session, setSession] = useState<SessionOut | null>(null);
  const [loaded, setLoaded] = useState<Loaded>({ state: "loading" });

  useEffect(() => {
    api.currentSession().then(
      (current) => {
        setSession(current);
        setLoaded({ state: "ready" });
      },
      (error: unknown) => {
        setLoaded({ state: "failed", message: messageOf(error) });
      },
    );
  }, [api]);

  const signOut = () => {
    api.signOut().then(
      () => {
        setSession(null);
      },
      (error: unknown) => {
        setLoaded({ state: "failed", message: messageOf(error) });
      },
    );
  };

  if (loaded.state === "loading") return <p className="loading">Loading…</p>;
  if (loaded.state === "failed") {
    return (
      <p className="problem" role="alert">
        {loaded.message}
      </p>
    );
  }
  if (session === null) return <SignIn signIn={api.signIn} onSignedIn={setSession} />;
  return (
    <>
      <Header session={session} onSignOut={signOut} />
      {session.warning != null && (
        <p className="warning" role="status">
          {session.warning}
        </p>
      )}
      <main className="review">
        <ReviewScreen session={session} api={api} />
      </main>
    </>
  );
}
