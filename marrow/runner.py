"""Awake and sleep cycles."""
from __future__ import annotations

from datetime import datetime, timezone
from marrow.field import append, readout

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def awake(task: str) -> dict:
    context = readout(task)
    result = {
        "task": task,
        "context": context,
        "status": "done",
        "ts": _now(),
    }
    append({"mode": "awake", "task": task, "result": result, "ts": _now()})
    return result

def sleep() -> dict:
    # Consolidation: currently just records the sleep event.
    # Drift measurement and pruning come later.
    append({"mode": "sleep", "action": "consolidate", "ts": _now()})
    return {"status": "consolidated", "ts": _now()}
