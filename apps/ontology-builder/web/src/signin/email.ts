// The same test as the server's name_warning (api/state.py), so the GUI can warn before it
// signs in (spec 0002, edge case "the user types an email address as user name").
const EMAIL = /[^@\s]+@[^@\s]+\.[^@\s]+/;

export const EMAIL_WARNING =
  "This looks like an email address. The dataset is public: use a handle, not a real name " +
  "or email address.";

export function looksLikeEmail(name: string): boolean {
  return EMAIL.test(name);
}
