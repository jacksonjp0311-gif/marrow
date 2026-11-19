"""Bounded arithmetic expression synthesis.

Adapted from NOMAD GENESIS. Single-return integer functions of (x, y).
Search sees public examples only. No unrestricted code generation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .learner import ContextualOperatorLearner
from .safe_eval import evaluate


@dataclass(frozen=True)
class IOExample:
    x: int
    y: int
    expected: int


@dataclass
class GrammarPrior:
    operator: ContextualOperatorLearner

    def __init__(self) -> None:
        self.operator = ContextualOperatorLearner()

    def order(self, context: int) -> tuple[str, ...]:
        return tuple(self.operator.rank(context))

    def update(self, context: int, op: str, success: bool) -> None:
        self.operator.update(context, op, success)


def synthesize(examples: Iterable[IOExample], *, prior: GrammarPrior | None = None, max_nodes: int = 5) -> str | None:
    """Minimal bottom-up search for a matching expression."""
    rows = list(examples)
    if not rows:
        return None
    goal = tuple(e.expected for e in rows)
    atoms = [("x", tuple(e.x for e in rows)), ("y", tuple(e.y for e in rows))]
    atoms += [(str(k), tuple(k for _ in rows)) for k in (0, 1, 2)]
    # Simple expansion: only binary ops on atoms for the first version
    ops = ("+", "-", "*")
    if prior:
        # Map learned order if available
        pass
    for left_text, left_vals in atoms:
        for right_text, right_vals in atoms:
            for op in ops:
                try:
                    expr = f"({left_text}{op}{right_text})"
                    vals = tuple(evaluate(expr, {"x": e.x, "y": e.y}) for e in rows)
                    if vals == goal:
                        return expr
                except Exception:
                    continue
    return None
