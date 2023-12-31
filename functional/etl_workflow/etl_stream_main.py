import functools
import os
import queue
from typing import Generator
from functional.etl_workflow.etl_core import (
    EtlSourceDataRecord,
    RunEnvironment,
    process_record,
)
from functional.etl_workflow.etl_stream_core import get_source_data, is_record_valid
from functional.functional_tools.composing import (
    ExecutionContext,
    ItemProcessingContext,
    QueueExecutionContext,
    bind_queue_stream_all,
    stream_processing_filter,
    stream_processing_map,
)

StreamItem = ItemProcessingContext[RunEnvironment, EtlSourceDataRecord]
EtlContext = ExecutionContext[StreamItem, RunEnvironment]


def get_source_data_stream(
    environment: RunEnvironment, file_fqn: str
) -> Generator[ItemProcessingContext, None, None]:
    for element in get_source_data(file_fqn=file_fqn):
        yield ItemProcessingContext(environment=environment, item=element, issues=[])


def acquire_record_data_processor(
    item_processing_context: ItemProcessingContext,
) -> ItemProcessingContext:
    acquired_record_data = process_record(item_processing_context.item)
    result_context = ItemProcessingContext(
        environment=item_processing_context.environment,
        item=acquired_record_data,
        issues=item_processing_context.issues,
    )
    return result_context


def print_data_processor(
    item_processing_context: ItemProcessingContext,
) -> ItemProcessingContext:
    print(
        f"{item_processing_context.item.sepal_length}"
        f"\t{item_processing_context.item.sepal_width}"
        f"\t{item_processing_context.item.petal_length}"
        f"\t{item_processing_context.item.petal_width}"
        f"\t{item_processing_context.item.iris_class}"
    )

    return item_processing_context


def filter_record_data_processor(
    item_processing_context: ItemProcessingContext,
) -> bool:
    return is_record_valid(item_processing_context.item)


def read_data_step(context: EtlContext) -> EtlContext:
    return context


def echo_data_step(context: EtlContext) -> EtlContext:
    return context


def preprocess_data_step(context: EtlContext) -> EtlContext:
    return context


def select_records_step(context: EtlContext) -> EtlContext:
    return context


def log_issues_step(context: EtlContext) -> EtlContext:
    return context


def write_csv_data_step(context: EtlContext) -> EtlContext:
    return context


def etl_workflow_main():
    input_file = os.path.join(os.path.dirname(__file__), "data", "input", "iris.data")
    out_file = os.path.join(os.path.dirname(__file__), "data", "output", "out.txt")
    log_file = os.path.join(os.path.dirname(__file__), "data", "log", "log.txt")

    run_environment: RunEnvironment = RunEnvironment(
        input_file=input_file, log_file=log_file, out_file=out_file
    )

    start_context = QueueExecutionContext[RunEnvironment, ItemProcessingContext](
        environment=run_environment,
        input_stream=queue.Queue(),
        output_stream=queue.Queue(),
    )

    workflow = bind_queue_stream_all(
        [
            functools.partial(
                stream_processing_map,
                item_processor=acquire_record_data_processor,
                source=get_source_data_stream(
                    environment=run_environment, file_fqn=run_environment.input_file
                ),
            ),
            functools.partial(
                stream_processing_map,
                item_processor=print_data_processor,
                source=None,
            ),
            functools.partial(
                stream_processing_filter,
                item_predicate=filter_record_data_processor,
                source=None,
            ),
            functools.partial(
                stream_processing_map,
                item_processor=print_data_processor,
                source=None,
            ),
        ]
    )

    result = workflow(start_context).output_stream
    print(result)


if __name__ == "__main__":
    etl_workflow_main()
