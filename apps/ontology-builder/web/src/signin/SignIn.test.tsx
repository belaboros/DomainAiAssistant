// The sign-in window (FR-2, AC-2): a handle and a role, no password, with the handle hint and
// a warning before signing in with something that looks like an email address.
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, test, vi } from "vitest";
import type { SessionOut, SignIn as SignInBody } from "../api";
import { SignIn } from "./SignIn";

function setup(reply: Partial<SessionOut> | Error = {}) {
  const signIn = vi.fn((body: SignInBody): Promise<SessionOut> => {
    if (reply instanceof Error) return Promise.reject(reply);
    return Promise.resolve({
      user: body.user,
      role: body.role,
      writer: true,
      ontology: "pets",
      ...reply,
    });
  });
  const onSignedIn = vi.fn();
  render(<SignIn signIn={signIn} onSignedIn={onSignedIn} />);
  return { signIn, onSignedIn, user: userEvent.setup() };
}

describe("SignIn", () => {
  test("shows_handle_hint", () => {
    setup();
    expect(screen.getByRole("heading", { name: /sign in/i })).toBeInTheDocument();
    expect(screen.getByText(/use a handle, not a real name or email address/i)).toBeVisible();
    expect(screen.getByText(/the dataset is public/i)).toBeVisible();
    expect(screen.queryByLabelText(/password/i)).not.toBeInTheDocument();
  });

  test("offers_both_roles_with_user_as_default", () => {
    setup();
    expect(screen.getByRole("radio", { name: "User" })).toBeChecked();
    expect(screen.getByRole("radio", { name: "Domain admin" })).not.toBeChecked();
  });

  test("signs_in_with_user_name_and_role", async () => {
    const { signIn, onSignedIn, user } = setup();
    await user.type(screen.getByLabelText(/user name/i), "alice");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(signIn).toHaveBeenCalledExactlyOnceWith({ user: "alice", role: "user" });
    expect(onSignedIn).toHaveBeenCalledExactlyOnceWith({
      user: "alice",
      role: "user",
      writer: true,
      ontology: "pets",
    });
  });

  test("signs_in_as_domain_admin", async () => {
    const { signIn, user } = setup();
    await user.type(screen.getByLabelText(/user name/i), "bob");
    await user.click(screen.getByRole("radio", { name: "Domain admin" }));
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(signIn).toHaveBeenCalledExactlyOnceWith({ user: "bob", role: "domain_admin" });
  });

  test("blank_user_name_is_refused_without_a_request", async () => {
    const { signIn, user } = setup();
    await user.type(screen.getByLabelText(/user name/i), "   ");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(signIn).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toHaveTextContent(/type a user name/i);
  });

  test("email_like_name_warns_before_signing_in", async () => {
    const { signIn, onSignedIn, user } = setup({ warning: "looks like an email address" });
    await user.type(screen.getByLabelText(/user name/i), "alice@example.org");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(signIn).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toHaveTextContent(/looks like an email address/i);

    await user.click(screen.getByRole("button", { name: "Sign in anyway" }));
    expect(signIn).toHaveBeenCalledExactlyOnceWith({ user: "alice@example.org", role: "user" });
    expect(onSignedIn).toHaveBeenCalledOnce();
  });

  test("editing_the_name_clears_the_email_warning", async () => {
    const { user } = setup();
    const name = screen.getByLabelText(/user name/i);
    await user.type(name, "alice@example.org");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    await user.clear(name);
    await user.type(name, "alice");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Sign in" })).toBeEnabled();
  });

  test("shows_the_server_refusal", async () => {
    const { onSignedIn, user } = setup(new Error("the server is not reachable"));
    await user.type(screen.getByLabelText(/user name/i), "alice");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("the server is not reachable");
    expect(onSignedIn).not.toHaveBeenCalled();
  });
});
