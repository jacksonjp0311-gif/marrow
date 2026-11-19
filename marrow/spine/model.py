from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Example:
    inputs: Mapping[str, int]
    expected: int


@dataclass(frozen=True)
class CodeTask:
    task_id: str
    source: str
    examples: Sequence[Example]
    family: str = "unknown"
