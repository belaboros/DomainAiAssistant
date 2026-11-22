// Every decision on the open element (FR-26): when, who in which role, the action, the field,
// the old and the new value, and the reason. Saved decisions come first, then unsaved ones.
import type { Decision, Role } from "../api";

function roleName(role: Role): string {
  return role === "domain_admin" ? "Domain admin" : "User";
}

function shown(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "string") return value;
  return JSON.stringify(value);
}

/** An ISO time as "YYYY-MM-DD HH:MM" (UTC, as recorded). */
function when(at: string): string {
  return at.replace("T", " ").slice(0, 16);
}

function Row({ decision }: { decision: Decision }) {
  const changed = decision.old !== undefined || decision.new !== undefined;
  return (
    <tr>
      <td>{when(decision.at)}</td>
      <td>
        {decision.user} · {roleName(decision.role)}
      </td>
      <td>{decision.action}</td>
      <td>{decision.field ?? "—"}</td>
      <td>{changed ? `${shown(decision.old)} → ${shown(decision.new)}` : "—"}</td>
      <td>{decision.reason ?? "—"}</td>
    </tr>
  );
}

export function DecisionHistory({ decisions }: { decisions: readonly Decision[] }) {
  return (
    <section className="decision-history" aria-label="Decision history">
      <h3>Decision history</h3>
      {decisions.length === 0 ? (
        <p className="hint">No decisions yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>When</th>
              <th>Who</th>
              <th>Action</th>
              <th>Field</th>
              <th>Change</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>
            {decisions.map((decision) => (
              <Row key={decision.id} decision={decision} />
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
