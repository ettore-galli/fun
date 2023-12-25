from dataclasses import asdict
from itertools import tee
import os
from typing import Iterator, List, Optional
from functional.etl_workflow.etl_core import (
    EtlSourceDataRecord,
    RunEnvironment,
    echo_data,
    get_source_data,
    preprocess_data,
    select_valid_records,
    write_csv_data,
)
from functional.functional_tools.composing import (
    ExecutionContext,
    Issue,
    IssueType,
    bind_all,
)

EtlContextPayload = Optional[Iterator[EtlSourceDataRecord]]
EtlContext = ExecutionContext[EtlContextPayload, RunEnvironment]


def read_data_step(context: EtlContext) -> EtlContext:
    try:
        data = get_source_data(context.environment.input_file)
        return context.with_payload(data)
    except Exception as error:  # pylint: disable=broad-exception-caught
        return context.with_issues(
            new_issues=[Issue(issue_type=IssueType.ERROR, message=str(error))]
        )


def echo_data_step(context: EtlContext) -> EtlContext:
    to_return, to_consume = tee(context.payload or [], 2)
    echo_data(to_consume)
    return context.with_payload(new_payload=to_return)


def preprocess_data_step(context: EtlContext) -> EtlContext:
    return context.with_payload(new_payload=preprocess_data(context.payload or []))


def select_records_step(context: EtlContext) -> EtlContext:
    issues: List[Issue] = []

    def discarded_record_hook(record):
        issues.append(
            Issue(issue_type=IssueType.WARNING, message=f"Discarded {asdict(record)}")
        )

    return context.with_payload(
        new_payload=select_valid_records(
            data=context.payload or [], discarded_record_hook=discarded_record_hook
        )
    )


def write_csv_data_step(context: EtlContext) -> EtlContext:
    to_return, to_consume = tee(context.payload or [], 2)
    write_csv_data(context.environment.out_file, to_consume)
    return context.with_payload(new_payload=to_return)


def etl_workflow_main():
    input_file = os.path.join(os.path.dirname(__file__), "data", "input", "iris.data")
    out_file = os.path.join(os.path.dirname(__file__), "data", "output", "out.txt")
    log_file = os.path.join(os.path.dirname(__file__), "data", "log", "log.txt")
    context = EtlContext(
        environment=RunEnvironment(
            input_file=input_file, log_file=log_file, out_file=out_file
        ),
        payload=None,
    )

    workflow = bind_all(
        [
            read_data_step,
            echo_data_step,
            preprocess_data_step,
            select_records_step,
            write_csv_data_step,
        ]
    )

    workflow(context=context)


if __name__ == "__main__":
    etl_workflow_main()
