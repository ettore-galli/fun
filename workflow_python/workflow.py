from __future__ import annotations
from dataclasses import dataclass

import os
from typing import Optional, Any, Callable,   Union

from copy import deepcopy


@dataclass(init=True, frozen=True)
class WorkflowPayload:
    user_input: Optional[str] = None
    number: Optional[Union[float, int]] = None


class WorkflowContext:

    def __init__(self, data: Optional[Any] = None, success: Optional[bool] = None):
        self.data: Optional[Any] = data
        self.success: bool = success if success is not None else True

    def __repr__(self):
        return str(self.config) + str(self.data)

    @classmethod
    def unit(cls, data: Optional[Any] = None, success: Optional[bool] = None):
        return WorkflowContext(data, success)

    def bind(self, f: Callable[[WorkflowContext], WorkflowContext]):
        return f(deepcopy(self.data))

    def __rshift__(self, other):
        return self.bind(other)


def read_console_input(_: WorkflowPayload) -> WorkflowContext:
    return WorkflowContext(data=WorkflowPayload(user_input=input()))


def parse_input(payload: WorkflowPayload) -> WorkflowContext:
    try:
        return WorkflowContext(data=WorkflowPayload(number=float(payload.user_input)))
    except ValueError:
        return WorkflowContext(success=False, data=payload)


def produce_output(payload: WorkflowPayload) -> WorkflowContext:
    print(f"* {payload.number} *")


if __name__ == "__main__":

    WorkflowContext.unit() \
        .bind(read_console_input) \
        .bind(parse_input) \
        .bind(produce_output)
