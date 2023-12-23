from __future__ import annotations
from dataclasses import dataclass, field
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
    issues: List[Issue] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return not any(issue.issue_type == IssueType.ERROR for issue in self.issues)

    def with_issues(self, new_issues: List[Issue]) -> ExecutionContext:
        return ExecutionContext(
            environment=self.environment,
            payload=self.payload,
            issues=self.issues + new_issues,
        )


# pylint: disable=too-few-public-methods
class ApplicationFunction(Protocol, Generic[T]):
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
        environment=None, payload=application_function(payload)
    )
