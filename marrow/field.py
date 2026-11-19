"""Sparse binary field. Append-only. Fixed readout.

Geometry: 4096-bit codes. Overlap is integer intersection size.
Receipts are exact.
"""
from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
FIELD = ROOT / "data" / "field.jsonl"
BITS = 4096

def _hash_to_bits(text: str, density: int = 64) -> set[int]:
    """Deterministic sparse projection. Density is number of set bits."""
    h = hashlib.sha256(text.encode()).digest()
    bits = set()
    for i in range(density):
        # Walk the hash to pick bit positions
        idx = int.from_bytes(h[i % 32: (i % 32) + 4], "big") % BITS
        bits.add(idx)
    return bits

def append(event: dict[str, Any]) -> None:
    """Append an event with its sparse signature."""
    FIELD.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(event, sort_keys=True, separators=(",", ":"))
    event = dict(event)  # copy
    event["_bits"] = sorted(_hash_to_bits(text))
    with FIELD.open("a") as f:
        f.write(json.dumps(event, separators=(",", ":")) + "\n")

def _load() -> list[dict[str, Any]]:
    if not FIELD.exists():
        return []
    rows = []
    with FIELD.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def readout(query: str, k: int = 16) -> dict[str, Any]:
    """Fixed-size readout. Returns top-k by integer overlap + exact receipts."""
    qbits = _hash_to_bits(query)
    rows = _load()
    scored = []
    for row in rows:
        rbits = set(row.get("_bits", []))
        overlap = len(qbits & rbits)
        scored.append((overlap, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:k]
    return {
        "query": query,
        "slots": k,
        "activations": [ov for ov, _ in top],
        "overlaps": [
            {
                "overlap": ov,
                "bits": len(row.get("_bits", [])),
                "mode": row.get("mode"),
                "task": row.get("task"),
            }
            for ov, row in top
        ],
        "receipt": "exact",
        "field_size": len(rows),
    }
