"""The tests never see the git variables of a hook that runs them (T29).

``git commit -- <path>`` runs the pre-commit hooks with ``GIT_INDEX_FILE`` pointing at a temporary
index of the real repository. Tests that run git in a temporary repository inherited it and wrote
their own blobs into that index, so the real commit failed with "invalid object".
"""

from __future__ import annotations

import os


def test_no_git_variables_reach_a_test() -> None:
    assert sorted(key for key in os.environ if key.startswith("GIT_")) == []
