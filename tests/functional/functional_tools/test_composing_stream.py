import functools
import queue

from typing import Dict, Generator, Iterable, List


from functional.functional_tools.composing_stream import (
    ItemProcessingContext,
    ItemProcessingResult,
    QueueExecutionContext,
    bind_stream_processing,
    stream_processing_reduce_adapter,
    stream_processing_map,
)


def test_stream_processing_various():
    def data_source() -> Generator[ItemProcessingContext, None, None]:
        return (
            ItemProcessingContext[Dict, str](
                item=str(100 + item), issues=[], environment={}
            )
            for item in range(10)
        )

    def item_processor_1(
        item_processing_context: ItemProcessingContext,
    ) -> ItemProcessingContext:
        result_context = ItemProcessingContext(
            environment=item_processing_context.environment,
            item=f"=1={item_processing_context.item}=1=",
            issues=item_processing_context.issues,
        )
        return result_context

    def item_processor_2(
        item_processing_context: ItemProcessingContext,
    ) -> ItemProcessingContext:
        result_context = ItemProcessingContext(
            environment=item_processing_context.environment,
            item=f"=2={item_processing_context.item}=2=",
            issues=item_processing_context.issues,
        )
        return result_context

    bound_stream_processes = bind_stream_processing(
        functools.partial(
            stream_processing_map, item_processor=item_processor_1, source=data_source()
        ),
        functools.partial(
            stream_processing_map, item_processor=item_processor_2, source=None
        ),
    )

    start_context = QueueExecutionContext[Dict, ItemProcessingContext](
        environment={}, input_stream=queue.Queue(), output_stream=queue.Queue()
    )

    result_context = bound_stream_processes(start_context)

    items: List[str] = []

    while True:
        try:
            element: ItemProcessingResult = result_context.output_stream.get_nowait()
            items.append(element.item)
            result_context.output_stream.task_done()
        except queue.Empty:
            break

    assert items == [
        "=2==1=100=1==2=",
        "=2==1=101=1==2=",
        "=2==1=102=1==2=",
        "=2==1=103=1==2=",
        "=2==1=104=1==2=",
        "=2==1=105=1==2=",
        "=2==1=106=1==2=",
        "=2==1=107=1==2=",
        "=2==1=108=1==2=",
        "=2==1=109=1==2=",
    ]


def test_stream_processing_base():
    def data_source() -> Generator[ItemProcessingContext, None, None]:
        return (
            ItemProcessingContext(environment={}, item=record, issues=[])
            for record in [
                {"id": 1, "categoria": "A", "peso": 32},
                {"id": 2, "categoria": "A", "peso": 31},
                {"id": 3, "categoria": "B", "peso": 21},
                {"id": 4, "categoria": "B", "peso": 23},
                {"id": 5, "categoria": "B", "peso": 22},
                {"id": 6, "categoria": "C", "peso": 52},
                {"id": 7, "categoria": "C", "peso": 53},
                {"id": 8, "categoria": "C", "peso": 50},
            ]
        )

    sums: Dict = {}

    def all_items_processor_consumer(
        all_items: Iterable[ItemProcessingContext],
    ) -> None:
        for item in all_items:
            sums[item.item["categoria"]] = item.item.get("peso", 0) + item.item["peso"]

    bound_stream_processes = bind_stream_processing(
        functools.partial(
            stream_processing_reduce_adapter,
            all_items_processor_consumer=all_items_processor_consumer,
            source=data_source(),
        ),
    )

    start_context = QueueExecutionContext[Dict, ItemProcessingContext](
        environment={}, input_stream=queue.Queue(), output_stream=queue.Queue()
    )

    result_context = bound_stream_processes(start_context)

    assert result_context.output_stream.empty() is False
    assert sums == {"A": 62, "B": 44, "C": 100}
