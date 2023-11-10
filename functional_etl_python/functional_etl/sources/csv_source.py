import csv
from typing import Generator

from functional_etl.sources.base import EtlSourceDataRecord


IRIS_FIELDS = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "iris_class",
]


def get_source_data(file_fqn: str) -> Generator[EtlSourceDataRecord, None, None]:
    with open(
        file_fqn,
        encoding="utf-8",
    ) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=IRIS_FIELDS)
        for row in reader:
            yield EtlSourceDataRecord(**row)
