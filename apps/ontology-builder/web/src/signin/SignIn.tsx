// The sign-in window (FR-2): a user name and a role, no password. Anyone can take any role;
// the hint asks for a handle, because every decision is recorded in a public dataset.
import { type SyntheticEvent, useState } from "react";
import type { Role, SessionOut, SignIn as SignInBody } from "../api";
import { EMAIL_WARNING, looksLikeEmail } from "./email";

export interface SignInProps {
  signIn: (body: SignInBody) => Promise<SessionOut>;
  onSignedIn: (session: SessionOut) => void;
}

const ROLES: readonly { value: Role; label: string }[] = [
  { value: "user", label: "User" },
  { value: "domain_admin", label: "Domain admin" },
];

function messageOf(error: unknown): string {
  return error instanceof Error ? error.message : "signing in failed";
}

export function SignIn({ signIn, onSignedIn }: SignInProps) {
  const [user, setUser] = useState("");
  const [role, setRole] = useState<Role>("user");
  const [warned, setWarned] = useState(false);
  const [problem, setProblem] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const changeUser = (value: string) => {
    setUser(value);
    setWarned(false);
    setProblem(null);
  };

  const submit = async (event: SyntheticEvent) => {
    event.preventDefault();
    const name = user.trim();
    if (name === "") {
      setProblem("Type a user name first.");
      return;
    }
    if (looksLikeEmail(name) && !warned) {
      setWarned(true);
      setProblem(EMAIL_WARNING);
      return;
    }
    setBusy(true);
    try {
      onSignedIn(await signIn({ user: name, role }));
    } catch (error) {
      setProblem(messageOf(error));
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="sign-in">
      <form onSubmit={(event) => void submit(event)} noValidate>
        <h1>Sign in to OntologyBuilder</h1>
        <p className="hint" id="handle-hint">
          Use a handle, not a real name or email address: the dataset is public, and every decision
          you make is recorded with this name.
        </p>
        <label>
          User name
          <input
            name="user"
            value={user}
            maxLength={64}
            autoComplete="off"
            autoFocus
            aria-describedby="handle-hint"
            onChange={(event) => {
              changeUser(event.target.value);
            }}
          />
        </label>
        <fieldset>
          <legend>Role</legend>
          {ROLES.map((option) => (
            <label key={option.value}>
              <input
                type="radio"
                name="role"
                value={option.value}
                checked={role === option.value}
                onChange={() => {
                  setRole(option.value);
                }}
              />
              {option.label}
            </label>
          ))}
        </fieldset>
        {problem !== null && (
          <p className="problem" role="alert">
            {problem}
          </p>
        )}
        <button type="submit" disabled={busy}>
          {warned ? "Sign in anyway" : "Sign in"}
        </button>
      </form>
    </main>
  );
}
