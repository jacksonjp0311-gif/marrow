"""Awake and sleep cycles."""
from __future__ import annotations

from datetime import datetime, timezone
from marrow.field import append, readout
from marrow.spine.genesis import IOExample, synthesize

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def awake(task: str) -> dict:
    context = readout(task)
    # Toy synthesis: try to find an expression for a fixed public example set
    examples = (
        IOExample(1, 2, 3),
        IOExample(2, 3, 5),
        IOExample(4, 5, 9),
    )
    candidate = synthesize(examples)
    result = {
        "task": task,
        "context": context,
        "candidate": candidate,
        "status": "synthesized" if candidate else "abstained",
        "ts": _now(),
    }
    append({"mode": "awake", "task": task, "result": result, "ts": _now()})
    return result

def sleep() -> dict:
    append({"mode": "sleep", "action": "consolidate", "ts": _now()})
    return {"status": "consolidated", "ts": _now()}
