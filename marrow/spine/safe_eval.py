from __future__ import annotations

import ast
import operator
from typing import Mapping


_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.FloorDiv: operator.floordiv,
}
_UNARYOPS = {ast.USub: operator.neg, ast.UAdd: operator.pos}


class UnsafeExpression(ValueError):
    pass


def parse_expr(source: str) -> ast.Expression:
    tree = ast.parse(source, mode="eval")
    validate(tree)
    return tree


def validate(tree: ast.AST) -> None:
    allowed = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Name,
        ast.Constant,
        ast.Load,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.FloorDiv,
        ast.USub,
        ast.UAdd,
    )
    for node in ast.walk(tree):
        if not isinstance(node, allowed):
            raise UnsafeExpression(f"unsupported syntax: {type(node).__name__}")
        if isinstance(node, ast.Constant) and not isinstance(node.value, int):
            raise UnsafeExpression("only integer constants are allowed")
        if isinstance(node, ast.Name) and node.id not in {"x", "y"}:
            raise UnsafeExpression(f"unsupported variable: {node.id}")


def evaluate(source: str, inputs: Mapping[str, int]) -> int:
    tree = parse_expr(source)
    return _eval(tree.body, inputs)


def _eval(node: ast.AST, inputs: Mapping[str, int]) -> int:
    if isinstance(node, ast.Constant):
        return int(node.value)
    if isinstance(node, ast.Name):
        if node.id not in inputs:
            raise KeyError(node.id)
        return int(inputs[node.id])
    if isinstance(node, ast.UnaryOp):
        return _UNARYOPS[type(node.op)](_eval(node.operand, inputs))
    if isinstance(node, ast.BinOp):
        left = _eval(node.left, inputs)
        right = _eval(node.right, inputs)
        if isinstance(node.op, ast.FloorDiv) and right == 0:
            raise ZeroDivisionError
        return _BINOPS[type(node.op)](left, right)
    raise UnsafeExpression(f"unsupported node: {type(node).__name__}")
