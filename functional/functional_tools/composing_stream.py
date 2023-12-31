from __future__ import annotations
from dataclasses import dataclass

import functools
import queue
import threading

from typing import Generic, Iterable, List, Optional, Protocol

from functional.functional_tools.composing_common import Issue, IssueType, T, U, S


@dataclass(frozen=True)
class ItemProcessingResult(Generic[T]):
    item: T
    issues: List[Issue]

    @property
    def success(self) -> bool:
        return not any(issue.issue_type == IssueType.ERROR for issue in self.issues)


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
