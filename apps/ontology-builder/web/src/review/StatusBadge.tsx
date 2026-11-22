// The status of an element (FR-20): a colour, an icon and a text label, so status never depends
// on colour alone. The colours are the --badge values of the .status-* classes in styles.css;
// the icons follow the raw release's badges (● proposed, ◐ waiting for approval).
import type { ElementStatus } from "../api";

export const STATUS_LOOK: Readonly<Record<ElementStatus, { icon: string; label: string }>> = {
  proposed: { icon: "●", label: "Proposed" },
  included: { icon: "◐", label: "Waiting for approval" },
  approved: { icon: "✔", label: "Approved" },
  excluded: { icon: "⊘", label: "Excluded" },
  rejected: { icon: "✖", label: "Rejected" },
  deprecated: { icon: "⌛", label: "Deprecated" },
};

export function StatusBadge(props: { status: ElementStatus }) {
  const look = STATUS_LOOK[props.status];
  return (
    <span className={`badge status-${props.status}`} data-testid="status-badge" title={look.label}>
      <span aria-hidden="true">{look.icon}</span> {look.label}
    </span>
  );
}
