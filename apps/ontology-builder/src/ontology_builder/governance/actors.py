"""Who acts, and the refusal every governance rule raises (FR-2, FR-3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ontology_builder.model import Decision, DecisionAction, Role, validate_record
from ontology_builder.store import DatasetStore


class GovernanceRefusedError(PermissionError):
    """An action is refused by a role, name, scope or status rule; the message says why."""


@dataclass(frozen=True)
class Actor:
    """The signed-in person: a handle, never a real name or email address, and a role."""

    user: str
    role: Role


def actor_of(user: str, role: str) -> Actor:
    """The actor of a handle and a role name (``user`` or ``domain_admin``)."""
    try:
        return Actor(user, Role(role))
    except ValueError:
        raise GovernanceRefusedError(f"unknown role {role!r}: use user or domain_admin") from None


def require_admin(actor: Actor, what: str) -> None:
    if actor.role != Role.domain_admin:
        raise GovernanceRefusedError(f"only a domain admin can {what}")


def new_decision(
    store: DatasetStore, actor: Actor, action: DecisionAction, **fields: Any
) -> Decision:
    """A decision record with a minted ID and the store's clock."""
    data = {
        "id": store.minter.new("decision"),
        "at": store.clock.now(),
        "user": actor.user,
        "role": actor.role,
        "action": action,
        **fields,
    }
    return validate_record(Decision, data)


def publish_decision(store: DatasetStore, actor: Actor, version: str) -> Decision:
    """The ``publish`` decision of a governed release (FR-26); only a domain admin publishes."""
    require_admin(actor, "publish a governed release")
    return new_decision(store, actor, DecisionAction.publish, new=version)
