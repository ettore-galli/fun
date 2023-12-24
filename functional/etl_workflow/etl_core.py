import csv
from dataclasses import dataclass
from typing import Generator, Iterable, Optional


@dataclass(frozen=True, kw_only=True)
class EtlSourceDataRecord:
    """
    1. sepal length in cm
    2. sepal width in cm
    3. petal length in cm
    4. petal width in cm
    5. class:
        -- Iris Setosa
        -- Iris Versicolour
        -- Iris Virginica
    """

    sepal_length: Optional[float]
    sepal_width: Optional[float]
    petal_length: Optional[float]
    petal_width: Optional[float]
    iris_class: Optional[str]


IRIS_FIELDS = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "iris_class",
]


@dataclass(frozen=True)
class RunEnvironment:
    input_file: str
    log_file: str


def get_source_data(file_fqn: str) -> Generator[EtlSourceDataRecord, None, None]:
    with open(
        file_fqn,
        encoding="utf-8",
    ) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=IRIS_FIELDS)
        for row in reader:
            yield EtlSourceDataRecord(**dict(row))


def echo_data(data: Iterable[EtlSourceDataRecord]) -> None:
    for item in data:
        print(item)
