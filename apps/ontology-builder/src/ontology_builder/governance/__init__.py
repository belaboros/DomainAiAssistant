"""governance component.

Applies review, authoring and governance actions under the role and status rules,
recording each decision.
"""

from __future__ import annotations

from ontology_builder.governance.actions import ACTIONS, apply_action
from ontology_builder.governance.actors import (
    Actor,
    GovernanceRefusedError,
    actor_of,
    new_decision,
    publish_decision,
    require_admin,
)
from ontology_builder.governance.authoring import author_element
from ontology_builder.governance.bulk import ActionResult, apply_bulk
from ontology_builder.governance.changes import ChangeSet
from ontology_builder.governance.ontology import (
    create_ontology,
    default_base_iri,
    edit_scope,
    require_scope,
)
from ontology_builder.governance.statements import add_user_statement, revise_user_statement
from ontology_builder.governance.status import (
    ADMIN_ACTIONS,
    TRANSITIONS,
    snapshot_of,
    state_of,
    target_status,
)

__all__ = [
    "ACTIONS",
    "ADMIN_ACTIONS",
    "TRANSITIONS",
    "ActionResult",
    "Actor",
    "ChangeSet",
    "GovernanceRefusedError",
    "actor_of",
    "add_user_statement",
    "apply_action",
    "apply_bulk",
    "author_element",
    "create_ontology",
    "default_base_iri",
    "edit_scope",
    "new_decision",
    "publish_decision",
    "require_admin",
    "require_scope",
    "revise_user_statement",
    "snapshot_of",
    "state_of",
    "target_status",
]
