from __future__ import annotations
from datetime import datetime

import os
from typing import Callable, Generator
from functional.etl_workflows.streamed.etl_stream_core import (
    EtlSourceDataRecord,
    RunEnvironment,
    get_source_data,
    process_record,
    write_csv_data,
)
from functional.functional_tools.composing_common import Issue, IssueType
from functional.functional_tools.composing_stream import ItemProcessingContext


PipelineItem = ItemProcessingContext[RunEnvironment, EtlSourceDataRecord]
PipelineStream = Generator[ItemProcessingContext, None, None]


class DataPipeline:
    def __init__(self, data_generator: PipelineStream):
        self.data_generator = data_generator

    def apply(
        self, item_func: Callable[[ItemProcessingContext], ItemProcessingContext]
    ) -> DataPipeline:
        return DataPipeline(
            (
                processed
                for processed in (item_func(item) for item in self.data_generator)
                if processed.success
            )
        )

    def bind(
        self, stream_func: Callable[[PipelineStream], PipelineStream]
    ) -> DataPipeline:
        return DataPipeline(data_generator=stream_func(self.data_generator))


def read_csv_file(environment: RunEnvironment) -> PipelineStream:
    for item in get_source_data(file_fqn=environment.input_file):
        yield ItemProcessingContext(environment=environment, item=item, issues=[])


def clean_data(item: ItemProcessingContext) -> ItemProcessingContext:
    try:
        result = process_record(item.item)
        if result.sepal_length is not None and result.sepal_length > 80:
            raise ValueError(f"Sepal length {result.petal_length} too big")
        return ItemProcessingContext(
            environment=item.environment, item=result, issues=item.issues
        )
    except Exception as error:  # pylint: disable=broad-exception-caught
        return ItemProcessingContext(
            environment=item.environment,
            item=item.item,
            issues=(
                item.issues + [Issue(issue_type=IssueType.ERROR, message=str(error))]
            ),
        )


# def aggregate_data(data_list):
#     # Simula operazioni di aggregazione
#     result_dict = {}
#     for data in data_list:
#         group_key = data["ColonnaGruppo"]
#         if group_key not in result_dict:
#             result_dict[group_key] = {
#                 "ColonnaGruppo": group_key,
#                 "SommaColonnaNumerica": 0,
#             }
#         result_dict[group_key]["SommaColonnaNumerica"] += data["ColonnaNumerica"]
#     return result_dict.values()


def log_errors(environment: RunEnvironment, stream: PipelineStream) -> PipelineStream:
    with open(environment.log_file, "a", encoding="utf-8") as logfile:
        for element in stream:
            for issue in element.issues:
                msg = f"{datetime.now()}: {issue.message}\n"
                logfile.write(msg)
            yield element


def export_data(environment: RunEnvironment, stream: PipelineStream):
    write_csv_data(
        out_file=environment.out_file, data=(element.item for element in stream)
    )


# pylint: disable=duplicate-code
def example_workflow_main():
    input_file = os.path.join(os.path.dirname(__file__), "data", "input", "iris.data")
    out_file = os.path.join(os.path.dirname(__file__), "data", "output", "out.txt")
    log_file = os.path.join(os.path.dirname(__file__), "data", "log", "log.txt")

    run_environment: RunEnvironment = RunEnvironment(
        input_file=input_file, log_file=log_file, out_file=out_file
    )

    (
        DataPipeline(data_generator=read_csv_file(environment=run_environment))
        .apply(clean_data)
        .bind(lambda stm: log_errors(environment=run_environment, stream=stm))
        .bind(lambda stm: export_data(environment=run_environment, stream=stm))
    )


if __name__ == "__main__":
    example_workflow_main()
