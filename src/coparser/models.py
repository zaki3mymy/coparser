from collections import namedtuple, deque
from typing import Generic, TypeVar


Line = namedtuple("Line", ["content"])

Docstring = namedtuple("Docstring", ["content"])
Function = namedtuple("Function", ["name", "children"])
Class = namedtuple("Class", ["name", "children"])
Module = namedtuple("Module", ["name", "children"])
Package = namedtuple("Package", ["name", "children"])
Summary = namedtuple("Summary", ["children"])

Node = namedtuple("Node", ["kind", "value", "children"])

T = TypeVar("T")


class MyStack(Generic[T]):
    def __init__(self):
        self._stack = deque()

    def push(self, item: T):
        self._stack.append(item)

    def pop(self) -> T:
        return self._stack.pop()

    def peek(self) -> T:
        return self._stack[-1]

    def is_empty(self) -> bool:
        return len(self._stack) == 0
