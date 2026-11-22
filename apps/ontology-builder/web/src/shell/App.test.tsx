// The app shell: the sign-in window until someone signs in, then the header with who is
// signed in, a read-only notice for a second session, and sign-out.
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, test, vi } from "vitest";
import type { SessionOut } from "../api";
import { fakeWork } from "../dialogs/fixtures/units";
import { App, type AppApi } from "./App";

const ALICE: SessionOut = { user: "alice", role: "user", writer: true, ontology: "pets" };

function api(current: SessionOut | null, signedIn: SessionOut = ALICE): AppApi {
  return {
    ...fakeWork(),
    currentSession: vi.fn(() => Promise.resolve(current)),
    signIn: vi.fn(() => Promise.resolve(signedIn)),
    signOut: vi.fn(() => Promise.resolve()),
    elementIndex: vi.fn(() => Promise.resolve({ elements: [], corpora: [], pending: 0 })),
    element: vi.fn(() => Promise.reject(new Error("no elements"))),
    act: vi.fn(() => Promise.resolve({ results: [], pending: 0 })),
  };
}

describe("App", () => {
  test("shows_sign_in_when_nobody_is_signed_in", async () => {
    render(<App api={api(null)} />);
    expect(await screen.findByRole("heading", { name: /sign in/i })).toBeInTheDocument();
  });

  test("shows_who_is_signed_in_after_sign_in", async () => {
    const user = userEvent.setup();
    render(<App api={api(null)} />);
    await user.type(await screen.findByLabelText(/user name/i), "alice");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(await screen.findByText("alice")).toBeInTheDocument();
    expect(screen.getByText("User")).toBeInTheDocument();
  });

  test("keeps_an_existing_session", async () => {
    render(<App api={api({ ...ALICE, user: "bob", role: "domain_admin" })} />);
    expect(await screen.findByText("bob")).toBeInTheDocument();
    expect(screen.getByText("Domain admin")).toBeInTheDocument();
    expect(screen.queryByText(/read-only/i)).not.toBeInTheDocument();
  });

  test("shows_the_review_screen_of_the_open_ontology", async () => {
    const calls = api(ALICE);
    render(<App api={calls} />);
    expect(await screen.findByRole("region", { name: "Filters" })).toBeInTheDocument();
    expect(calls.elementIndex).toHaveBeenCalledWith("pets");
    expect(screen.getByText(/pets/)).toBeInTheDocument();
  });

  test("second_session_is_marked_read_only", async () => {
    render(<App api={api({ ...ALICE, writer: false })} />);
    expect(await screen.findByText(/read-only/i)).toBeInTheDocument();
  });

  test("shows_the_server_email_warning_after_sign_in", async () => {
    const user = userEvent.setup();
    const warned = { ...ALICE, user: "a@b", warning: "This looks like an email address." };
    render(<App api={api(null, warned)} />);
    await user.type(await screen.findByLabelText(/user name/i), "a@b");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(await screen.findByRole("status")).toHaveTextContent(/looks like an email address/i);
  });

  test("sign_out_returns_to_sign_in", async () => {
    const user = userEvent.setup();
    const calls = api(ALICE);
    render(<App api={calls} />);
    await user.click(await screen.findByRole("button", { name: "Sign out" }));
    expect(calls.signOut).toHaveBeenCalledOnce();
    expect(await screen.findByRole("heading", { name: /sign in/i })).toBeInTheDocument();
  });

  test("shows_when_the_server_cannot_be_reached", async () => {
    const calls = api(null);
    calls.currentSession = () => Promise.reject(new Error("the server is not reachable"));
    render(<App api={calls} />);
    expect(await screen.findByRole("alert")).toHaveTextContent("the server is not reachable");
  });
});
