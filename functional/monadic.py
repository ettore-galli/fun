from dataclasses import dataclass
from typing import Any, List, Protocol


Payload = Any


@dataclass(frozen=True)
class ExecutionContext:
    payload: Payload
    errors: List[Any]
    log: List[str]


# pylint: disable=too-few-public-methods
class ApplicationFunction(Protocol):
    def __call__(self, payload: Payload) -> Payload:
        ...


# pylint: disable=too-few-public-methods
class ComposableApplicationFunction(Protocol):
    def __call__(self, execution_context: ExecutionContext) -> ExecutionContext:
        ...


def elevate(
    application_function: ApplicationFunction, payload: Payload
) -> ComposableApplicationFunction:
    return lambda function: ExecutionContext(
        payload=application_function(payload), errors=[], log=[]
    )
