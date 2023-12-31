import functools
import queue

from typing import Dict, Generator, List


from functional.functional_tools.composing_stream import (
    ItemProcessingContext,
    ItemProcessingResult,
    QueueExecutionContext,
    bind_stream_processing,
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
