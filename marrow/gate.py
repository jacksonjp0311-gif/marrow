"""Gate. Rejects what fails the check.

Currently a placeholder that always passes. The structure is here so
later checks (held-out, twin control lead, etc.) can reject candidates.
"""
from __future__ import annotations

from typing import Any

def check(candidate: dict[str, Any]) -> dict[str, Any]:
    """Return pass/fail with reason."""
    return {
        "pass": True,
        "reason": "placeholder",
        "candidate": candidate,
    }
