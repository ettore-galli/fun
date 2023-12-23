from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Protocol, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class IssueType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True)
class Issue:
    issue_type: IssueType
    message: str


@dataclass(frozen=True)
class ExecutionContext(Generic[T, U]):
    environment: U
    payload: T
    errors: List[Issue]
    log: List[str]

    @property
    def success(self) -> bool:
        return len(self.errors) == 0


# pylint: disable=too-few-public-methods
class ApplicationFunction(Protocol):
    def __call__(self, payload: T) -> T:
        ...


# pylint: disable=too-few-public-methods
class ComposableApplicationFunction(Protocol):
    def __call__(self, execution_context: ExecutionContext) -> ExecutionContext:
        ...


def elevate(
    application_function: ApplicationFunction, payload: T
) -> ComposableApplicationFunction:
    return lambda function: ExecutionContext(
        environment=None, payload=application_function(payload), errors=[], log=[]
    )
