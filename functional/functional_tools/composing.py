from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import functools
import queue
import threading
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


# pylint: disable=too-few-public-methods
class ComposableStreamApplicationFunction(Protocol):
    def __call__(self, context: StreamExecutionContext) -> StreamExecutionContext:
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


@dataclass(frozen=True)
class QueueExecutionContext(Generic[U, S]):
    environment: U
    input_stream: queue.Queue[S]
    output_stream: queue.Queue[S]


@dataclass(frozen=True)
class ItemProcessingContext(Generic[U, T]):
    environment: U
    item: T
    issues: List[Issue]

    @property
    def success(self) -> bool:
        return not any(issue.issue_type == IssueType.ERROR for issue in self.issues)


# pylint: disable=too-few-public-methods
class QueueItemProcessor(Protocol):
    def __call__(
        self, item_processing_context: ItemProcessingContext
    ) -> ItemProcessingContext:
        ...


class QueueItemPredicate(Protocol):
    def __call__(self, item_processing_context: ItemProcessingContext) -> bool:
        ...


# pylint: disable=too-few-public-methods
class QueueApplicationFunction(Protocol):
    def __call__(self, context: QueueExecutionContext) -> QueueExecutionContext:
        ...


def stream_processing_map(
    context: QueueExecutionContext,
    source: Optional[Iterable[ItemProcessingContext]],
    item_processor: QueueItemProcessor,
) -> QueueExecutionContext:
    def process_elements():
        while True:
            item = context.input_stream.get()
            processed_item = item_processor(item)
            context.output_stream.put(processed_item)
            context.input_stream.task_done()

    threading.Thread(target=process_elements, daemon=True).start()

    if source:
        for element in source:
            context.input_stream.put(element)

    context.input_stream.join()

    return context


def stream_processing_filter(
    context: QueueExecutionContext,
    source: Optional[Iterable[ItemProcessingContext]],
    item_predicate: QueueItemPredicate,
) -> QueueExecutionContext:
    def process_elements():
        while True:
            item = context.input_stream.get()
            if item_predicate(item):
                context.output_stream.put(item)
            context.input_stream.task_done()

    threading.Thread(target=process_elements, daemon=True).start()

    if source:
        for element in source:
            context.input_stream.put(element)

    context.input_stream.join()

    return context


def identity_processor(
    item_processing_context: ItemProcessingContext,
) -> ItemProcessingContext:
    return item_processing_context


def stream_lift(
    context: QueueExecutionContext,
    source: Iterable[ItemProcessingContext],
) -> QueueExecutionContext:
    context = stream_processing_map(
        context=context, source=source, item_processor=identity_processor
    )
    return QueueExecutionContext(
        environment=context.environment,
        input_stream=context.output_stream,
        output_stream=queue.Queue(),
    )


def bind_stream_processing(
    first: QueueApplicationFunction, second: Optional[QueueApplicationFunction] = None
) -> QueueApplicationFunction:
    def bound_function(context: QueueExecutionContext) -> QueueExecutionContext:
        result = first(
            QueueExecutionContext(
                environment=context.environment,
                input_stream=context.input_stream,
                output_stream=queue.Queue(),
            )
        )
        return (
            second(
                QueueExecutionContext(
                    environment=result.environment,
                    input_stream=result.output_stream,
                    output_stream=queue.Queue(),
                )
            )
            if second is not None
            else result
        )

    return bound_function


def bind_queue_stream_identity(
    context: QueueExecutionContext,
) -> QueueExecutionContext:
    return context


def bind_queue_stream_all(
    composables: Iterable[QueueApplicationFunction],
) -> QueueApplicationFunction:
    return functools.reduce(
        bind_stream_processing, composables, bind_queue_stream_identity
    )
