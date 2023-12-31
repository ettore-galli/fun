from __future__ import annotations
from dataclasses import dataclass, field

import functools

from typing import Generic, Iterable, List, Protocol

from functional.functional_tools.composing_common import Issue, IssueType, T, U


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
