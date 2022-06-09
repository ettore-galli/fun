from __future__ import annotations
from dataclasses import dataclass

import os
from typing import List, Optional, Any, Callable, Dict

from services.config import read_config
from services.order import get_order
from services.exchange import get_exchange
from services.price import get_price
from services.writer import write_output


class WorkflowPayload:

    def __init__(self, data: Optional[Any] = None, success: Optional[bool] = None):
        self.data: Optional[Any] = data
        self.success: bool = success if success is not None else True

    def clone(self, data: Optional[Any] = None, success: Optional[bool] = None):
        return WorkflowPayload(data=data if data is not None else self.data, success=success if success is not None else self.success)

    def __repr__(self):
        return str(self.config) + str(self.data)

    @classmethod
    def unit(cls, data: Optional[Any] = None, success: Optional[bool] = None):
        return WorkflowPayload(data, success)

    def bind(self, f: Callable[[WorkflowPayload], WorkflowPayload]):
        return f(self.clone())

    def __rshift__(self, other):
        return self.bind(other)


def read_console_input(payload: WorkflowPayload) -> WorkflowPayload:
    return WorkflowPayload(data=input())


def parse_input(payload: WorkflowPayload) -> WorkflowPayload:
    try:
        return WorkflowPayload(data=int(payload.data))
    except ValueError as e:
        return WorkflowPayload(success=False, data=str(e))


def produce_output(payload: WorkflowPayload) -> WorkflowPayload:
    print(f"* {payload.data} *")


if __name__ == "__main__":

    WorkflowPayload.unit() \
        .bind(read_console_input) \
        .bind(parse_input) \
        .bind(produce_output)
