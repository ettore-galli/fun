from itertools import tee
import os
from typing import Generator, Optional
from functional.etl_workflow.etl_core import (
    EtlSourceDataRecord,
    RunEnvironment,
    echo_data,
    get_source_data,
    write_csv_data,
)
from functional.functional_tools.composing import (
    ExecutionContext,
    Issue,
    IssueType,
    bind_all,
)

EtlContextPayload = Optional[Generator[EtlSourceDataRecord, None, None]]
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

    workflow = bind_all([read_data_step, echo_data_step, write_csv_data_step])

    workflow(context=context)


if __name__ == "__main__":
    etl_workflow_main()
