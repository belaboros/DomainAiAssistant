"""The refusal every use case raises before it changes anything."""

from __future__ import annotations


class WorkflowRefusedError(RuntimeError):
    """A use case cannot run in the current state (lock, git, unsaved changes); nothing changed."""


class NotFoundError(LookupError):
    """An element or run the caller asked for does not exist."""
