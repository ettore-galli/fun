from dataclasses import asdict
import sys

from functional_etl.common.environment import RunEnvironment
from functional_etl.sources.csv_source import get_source_data
from functional_etl.data.base import EtlOutputDataRecord
from functional_etl.sinks.csv_output import CsvEtlDataSink


def main():
    run_environment: RunEnvironment = retrieve_run_environment()
    writer = CsvEtlDataSink(run_environment.output_file)
    for data in get_source_data(run_environment.data_source_file):
        writer.write(EtlOutputDataRecord(**asdict(data)))


def retrieve_run_environment() -> RunEnvironment:
    return RunEnvironment(data_source_file=sys.argv[1], output_file=sys.argv[2])


if __name__ == "__main__:":
    main()
