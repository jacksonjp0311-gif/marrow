"""Awake and sleep cycles."""
from marrow.field import append, readout

def awake(task: str) -> dict:
    context = readout(task)
    # Work happens here.
    result = {"task": task, "context": context, "status": "done"}
    append({"mode": "awake", "task": task, "result": result})
    return result

def sleep() -> dict:
    # Consolidate recent events into the field.
    append({"mode": "sleep", "action": "consolidate"})
    return {"status": "consolidated"}
