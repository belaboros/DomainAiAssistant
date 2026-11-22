// End to end (T27; AC-25, AC-15, AC-19): the review GUI against `ontology-builder serve` on the
// fixture dataset of tools/e2e_server.py, in a temporary git repository with a bare remote.
// sign in → filter → bulk level → save (one commit, nothing pushed) → failing hook shown →
// admin publish blocked by FR-35 → fix → publish 1.0.0.
import { expect, type Page, test } from "@playwright/test";
import {
  DATASET,
  commitCount,
  headFiles,
  headSha,
  headSubject,
  hookFails,
  remoteMain,
  workingChanges,
} from "./repo";

const GOVERNED = `${DATASET}03_release/01_governed/`;
const UNRELATED = [" M notes.md"];

async function signIn(page: Page, user: string, role: "User" | "Domain admin") {
  await page.getByLabel("User name").fill(user);
  await page.getByRole("radio", { name: role }).check();
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByText(`Signed in as ${user}`)).toBeVisible();
}

async function signOut(page: Page) {
  await page.getByRole("button", { name: "Sign out" }).click();
  await expect(page.getByLabel("User name")).toBeVisible();
}

function bulk(page: Page) {
  return page.getByRole("region", { name: "Bulk actions" });
}

async function filterType(page: Page, type: string) {
  await page.getByRole("region", { name: "Filters" }).getByLabel("Type").selectOption(type);
}

async function setLevel(page: Page, level: string) {
  await bulk(page).getByLabel("Set level to").selectOption(level);
  await bulk(page).getByRole("button", { name: "Set level", exact: true }).click();
}

async function clearSelection(page: Page) {
  const clear = bulk(page).getByRole("button", { name: "Clear selection" });
  if (await clear.isEnabled()) await clear.click();
}

/** Click Save and return the Save dialog once the save has finished. */
async function save(page: Page) {
  await page.getByRole("region", { name: "Work" }).getByRole("button", { name: "Save" }).click();
  const dialog = page.getByRole("dialog", { name: "Save" });
  await expect(dialog.getByText("Saving…")).toBeHidden();
  return dialog;
}

async function closeDialog(page: Page, name: string) {
  await page.getByRole("dialog", { name }).getByRole("button", { name: "Close" }).click();
  await expect(page.getByRole("dialog", { name })).toBeHidden();
}

/** Publish with a version and return the Publish dialog once the build has finished. */
async function publish(page: Page, version: string) {
  await page.getByRole("button", { name: "Publish…" }).click();
  const dialog = page.getByRole("dialog", { name: "Publish a governed release" });
  await dialog.getByLabel("Version").fill(version);
  await dialog.getByRole("button", { name: "Publish", exact: true }).click();
  await expect(dialog.getByRole("button", { name: "Close" })).toBeVisible();
  return dialog;
}

/** Nothing was pushed, and the unrelated change is still uncommitted. */
function expectRepoUntouchedOutsideDataset(pushed: string) {
  expect(remoteMain()).toBe(pushed);
  expect(workingChanges()).toEqual(UNRELATED);
}

test("review, save with hooks, and publish through the GUI", async ({ page }) => {
  const pushed = remoteMain();
  expect(headSha()).toBe(pushed);
  expect(workingChanges()).toEqual(UNRELATED);
  await page.goto("/");

  await test.step("sign in as a user", async () => {
    await signIn(page, "e2e-reviewer", "User");
  });

  await test.step("each status has its own colour and label (AC-19)", async () => {
    const proposed = page
      .getByRole("row", { name: /\bdog\b.*concept/ })
      .getByTestId("status-badge");
    const approved = page
      .getByRole("row", { name: /keep the dog on a lead.*\brule\b/ })
      .getByTestId("status-badge");
    await expect(proposed).toHaveText(/Proposed/);
    await expect(approved).toHaveText(/Approved/);
    const colour = (badge: typeof proposed) =>
      badge.evaluate((node) => getComputedStyle(node).color);
    expect(await colour(proposed)).not.toBe(await colour(approved));
  });

  await test.step("the evidence is shown above the proposal (AC-15)", async () => {
    await page.getByRole("button", { name: "stairwell", exact: true }).click();
    const detail = page.getByRole("article", { name: "Element detail" });
    const evidence = detail.getByRole("region", { name: "Evidence" });
    await expect(evidence).toContainText("The stairwell connects the floors");
    const evidenceFirst = await detail.evaluate((node) => {
      const shown = node.querySelector(".evidence");
      const proposal = node.querySelector(".proposal");
      if (shown === null || proposal === null) return false;
      return (shown.compareDocumentPosition(proposal) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
    });
    expect(evidenceFirst).toBe(true);
  });

  await test.step("filter the concepts and set their level in bulk", async () => {
    await filterType(page, "concept");
    await expect(page.getByRole("row")).toHaveCount(4); // the header and three concepts
    await page.getByLabel("Select every element shown").check();
    await setLevel(page, "level-3");
    await expect(bulk(page).getByRole("status")).toHaveText("3 changed.");
  });

  await test.step("save makes one commit of the dataset only, and pushes nothing (AC-25)", async () => {
    const before = commitCount();
    const dialog = await save(page);
    await expect(dialog).toContainText("Nothing was pushed.");
    const sha = headSha();
    await expect(dialog.getByRole("code")).toHaveText(sha.slice(0, 7));
    expect(commitCount()).toBe(before + 1);
    expect(headFiles().length).toBeGreaterThan(0);
    expect(headFiles().every((path) => path.startsWith(DATASET))).toBe(true);
    expectRepoUntouchedOutsideDataset(pushed);
    await closeDialog(page, "Save");
  });

  await test.step("a failing hook commits nothing and its output is shown (AC-25)", async () => {
    const before = commitCount();
    await clearSelection(page);
    await page.getByLabel("Select dog").check();
    await setLevel(page, "level-1");
    await expect(bulk(page).getByRole("status")).toHaveText("1 changed.");
    hookFails(true);
    const dialog = await save(page);
    await expect(dialog.getByRole("alert")).toContainText("A git hook failed");
    await expect(dialog.locator(".hook-output")).toContainText(
      "detect-secrets: a secret was found",
    );
    expect(commitCount()).toBe(before);
    expectRepoUntouchedOutsideDataset(pushed);
    await closeDialog(page, "Save");
    hookFails(false);
    await expect(await save(page)).toContainText("Nothing was pushed.");
    expect(commitCount()).toBe(before + 1);
    await closeDialog(page, "Save");
  });

  await test.step("an admin's publish is blocked by the proposed concept (FR-35)", async () => {
    await signOut(page);
    await signIn(page, "e2e-admin", "Domain admin");
    const dialog = await publish(page, "1.0.0");
    await expect(dialog.getByRole("alert")).toContainText("Not published");
    await expect(dialog.getByRole("listitem")).toHaveText(
      "keep the dog on a lead → lead (proposed)",
    );
    expect(headFiles().some((path) => path.startsWith(GOVERNED))).toBe(false);
    expectRepoUntouchedOutsideDataset(pushed);
    await closeDialog(page, "Publish a governed release");
  });

  await test.step("approve the concept, save, and publish 1.0.0", async () => {
    await clearSelection(page);
    await page.getByLabel("Select lead").check();
    await bulk(page).getByRole("button", { name: "Approve" }).click();
    await expect(bulk(page).getByRole("status")).toHaveText("1 changed.");
    await expect(await save(page)).toContainText("Nothing was pushed.");
    await closeDialog(page, "Save");
    const dialog = await publish(page, "1.0.0");
    await expect(dialog).toContainText("Published version 1.0.0.");
    expect(headSubject()).toBe("Publish ontology e2e-house-rules 1.0.0");
    expect(headFiles()).toContain(`${GOVERNED}manifest.json`);
    expect(headFiles().every((path) => path.startsWith(DATASET))).toBe(true);
    expectRepoUntouchedOutsideDataset(pushed);
  });
});
