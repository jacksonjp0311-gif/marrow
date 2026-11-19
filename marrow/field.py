"""Sparse binary field. Append-only. Fixed readout."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
FIELD = ROOT / "data" / "field.jsonl"

def append(event: dict[str, Any]) -> None:
    FIELD.parent.mkdir(parents=True, exist_ok=True)
    with FIELD.open("a") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")

def readout(query: str, k: int = 16) -> dict[str, Any]:
    # Placeholder: fixed-size integer geometry readout.
    # Returns k activations + overlap receipts.
    return {
        "query": query,
        "slots": k,
        "activations": [0] * k,
        "overlaps": [],
        "receipt": "exact",
    }
