from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import functools
from typing import Generic, Iterable, List, Protocol, TypeVar

T = TypeVar("T")
U = TypeVar("U")
C = TypeVar("C")


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
class ComposableApplicationFunction(Protocol):
    def __call__(self, context: ExecutionContext) -> ExecutionContext:
        ...


def bind(
    first: ComposableApplicationFunction, second: ComposableApplicationFunction
) -> ComposableApplicationFunction:
    def bound_function(context: ExecutionContext) -> ExecutionContext:
        result = first(context)
        if result.success:
            return second(result)
        return result

    return bound_function


def composable_identity(context: ExecutionContext) -> ExecutionContext:
    return context


def bind_all(
    composables: Iterable[ComposableApplicationFunction],
) -> ComposableApplicationFunction:
    return functools.reduce(bind, composables, composable_identity)
