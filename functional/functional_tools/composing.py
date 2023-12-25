from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import functools
from typing import Generic, Iterable, List, Optional, Protocol, TypeVar

T = TypeVar("T")
U = TypeVar("U")
G = TypeVar("G")
S = TypeVar("S")


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
    new_issues: List[Issue] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return not any(issue.issue_type == IssueType.ERROR for issue in self.issues)

    def with_issues(self, new_issues: List[Issue]) -> ExecutionContext:
        return ExecutionContext(
            environment=self.environment,
            payload=self.payload,
            issues=self.issues + new_issues,
            new_issues=new_issues,
        )

    def with_payload(self, new_payload: T) -> ExecutionContext:
        return ExecutionContext(
            environment=self.environment,
            payload=new_payload,
            issues=self.issues,
        )


# pylint: disable=too-few-public-methods
class ComposableApplicationFunction(Protocol):
    def __call__(self, context: ExecutionContext) -> ExecutionContext:
        ...


@dataclass(frozen=True)
class ItemProcessingResult(Generic[T]):
    item: T
    issues: List[Issue]

    @property
    def success(self) -> bool:
        return not any(issue.issue_type == IssueType.ERROR for issue in self.issues)


@dataclass(frozen=True)
class StreamExecutionContext(Generic[U, S]):
    environment: U
    stream: Optional[Iterable[S]] = None
    # global_result: G


#     @property
#     def success(self) -> bool:
#         return not any(issue.issue_type == IssueType.ERROR for issue in self.issues)

#     def with_issues(self, new_issues: List[Issue]) -> ExecutionContext:
#         return ExecutionContext(
#             environment=self.environment,
#             payload=self.payload,
#             issues=self.issues + new_issues,
#             new_issues=new_issues,
#         )

#     def with_payload(self, new_payload: T) -> ExecutionContext:
#         return ExecutionContext(
#             environment=self.environment,
#             payload=new_payload,
#             issues=self.issues,
#         )


# pylint: disable=too-few-public-methods
class ComposableStreamApplicationFunction(Protocol):
    def __call__(self, context: StreamExecutionContext) -> StreamExecutionContext:
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


def composable_identity_stream(
    context: StreamExecutionContext,
) -> StreamExecutionContext:
    return context


def bind_stream(
    first: ComposableStreamApplicationFunction,
    second: ComposableStreamApplicationFunction,
) -> ComposableStreamApplicationFunction:
    def bound_function(context: StreamExecutionContext) -> StreamExecutionContext:
        result = first(context)
        return second(result)

    return bound_function


def bind_stream_all(
    composables: Iterable[ComposableStreamApplicationFunction],
) -> ComposableStreamApplicationFunction:
    return functools.reduce(bind_stream, composables, composable_identity_stream)
