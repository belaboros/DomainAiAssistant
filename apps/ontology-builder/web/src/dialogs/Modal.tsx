// The frame of a work-bar dialog: a modal with a title; Escape closes it unless it is busy.
import type { ReactNode } from "react";

export interface ModalProps {
  title: string;
  busy?: boolean;
  onClose: () => void;
  children: ReactNode;
}

export function Modal({ title, busy = false, onClose, children }: ModalProps) {
  return (
    <div className="dialog-backdrop">
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        className="dialog"
        onKeyDown={(event) => {
          if (event.key === "Escape" && !busy) onClose();
        }}
      >
        <h2>{title}</h2>
        {children}
      </div>
    </div>
  );
}

export function Problem({ message }: { message: string | null }) {
  if (message === null) return null;
  return (
    <p className="problem" role="alert">
      {message}
    </p>
  );
}
