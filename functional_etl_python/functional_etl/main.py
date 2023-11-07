import sys

from functional_etl.common.environment import RunEnvironment
from functional_etl.sources.csv_source import get_source_data


def main():
    run_environment: RunEnvironment = retrieve_run_environment()
    for data in get_source_data(run_environment.data_source_file):
        print(data)


def retrieve_run_environment() -> RunEnvironment:
    return RunEnvironment(data_source_file=sys.argv[1])


if __name__ == "__main__:":
    main()
