// Publish (FR-29, FR-35; AC-27 and AC-31 in the GUI; AC-3 in the GUI): admin only; the version
// defaults to the next minor; the result is the version and change log, or the offenders.
import { screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";
import { dialog, renderBar } from "./setup";

describe("publish_dialog", () => {
  test("user_cannot_publish", () => {
    const { api } = renderBar({ role: "user" });
    const button = screen.getByRole("button", { name: "Publish…" });
    expect(button).toBeDisabled();
    expect(button).toHaveAccessibleDescription(/only a domain admin can publish/i);
    expect(api.publish).not.toHaveBeenCalled();
  });

  test("default_version_is_the_next_minor", async () => {
    const { api, onChanged, user } = renderBar({ role: "domain_admin" });
    await user.click(screen.getByRole("button", { name: "Publish…" }));
    expect(dialog().getByLabelText(/version/i)).toHaveValue("");
    await user.click(dialog().getByRole("button", { name: "Publish" }));
    expect(api.publish).toHaveBeenCalledWith("pets", null);
    expect(await dialog().findByText(/published version 1\.1\.0/i)).toBeInTheDocument();
    expect(dialog().getByText(/## Added/)).toBeInTheDocument();
    expect(screen.getByRole("dialog")).toHaveTextContent("fedcba9");
    expect(onChanged).toHaveBeenCalled();
  });

  test("chosen_version_is_sent", async () => {
    const { api, user } = renderBar({ role: "domain_admin" });
    await user.click(screen.getByRole("button", { name: "Publish…" }));
    await user.type(dialog().getByLabelText(/version/i), "2.0.0");
    await user.click(dialog().getByRole("button", { name: "Publish" }));
    expect(api.publish).toHaveBeenCalledWith("pets", "2.0.0");
  });

  test("offenders_are_listed", async () => {
    const blocked = () =>
      Promise.resolve({
        version: null,
        changelog: null,
        offenders: [
          {
            element_id: "ru_lead",
            element_label: "lead in the stairwell",
            target_id: "cn_leash",
            target_label: "leash",
            target_status: "proposed",
          },
        ],
        warnings: [],
        commit: { ok: true, sha: "1111111222222", output: "" },
      });
    const { user } = renderBar({ role: "domain_admin", api: { publish: blocked } });
    await user.click(screen.getByRole("button", { name: "Publish…" }));
    await user.click(dialog().getByRole("button", { name: "Publish" }));
    const alert = await dialog().findByRole("alert");
    expect(alert).toHaveTextContent(/not published/i);
    const offenders = screen.getByRole("dialog");
    expect(offenders).toHaveTextContent("lead in the stairwell");
    expect(offenders).toHaveTextContent("leash");
    expect(offenders).toHaveTextContent("proposed");
  });

  test("warnings_on_deprecated_references_are_shown", async () => {
    const warned = () =>
      Promise.resolve({
        version: "1.1.0",
        changelog: "# 1.1.0",
        offenders: [],
        warnings: [
          {
            element_id: "ru_lead",
            element_label: "lead in the stairwell",
            target_id: "cn_old",
            target_label: "old leash",
            target_status: "deprecated",
          },
        ],
        commit: { ok: true, sha: "1111111222222", output: "" },
      });
    const { user } = renderBar({ role: "domain_admin", api: { publish: warned } });
    await user.click(screen.getByRole("button", { name: "Publish…" }));
    await user.click(dialog().getByRole("button", { name: "Publish" }));
    expect(await dialog().findByText(/old leash/)).toBeInTheDocument();
  });
});
