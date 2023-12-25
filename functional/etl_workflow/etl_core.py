import csv
from dataclasses import dataclass, asdict, fields
from typing import Any, Generator, Iterable, List, Optional


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


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class EtlOutputDataRecord:
    sepal_length: Optional[float] = None
    sepal_width: Optional[float] = None
    petal_length: Optional[float] = None
    petal_width: Optional[float] = None
    avg_sepal_length: Optional[float] = None
    avg_sepal_width: Optional[float] = None
    avg_petal_length: Optional[float] = None
    avg_petal_width: Optional[float] = None
    is_probably_outlier: Optional[bool] = False
    iris_class: Optional[str] = None


@dataclass(frozen=True)
class RunEnvironment:
    input_file: str
    out_file: str
    log_file: str


def get_source_data(file_fqn: str) -> Generator[EtlSourceDataRecord, None, None]:
    with open(
        file_fqn,
        encoding="utf-8",
    ) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=IRIS_FIELDS)
        for row in reader:
            yield EtlSourceDataRecord(**dict(row))


def float_or_zero(candidate: Any):
    try:
        return float(candidate)
    except (TypeError, ValueError):
        return 0.0


def process_record(record: EtlSourceDataRecord) -> EtlSourceDataRecord:
    return EtlSourceDataRecord(
        **{
            **asdict(record),
            **{
                "sepal_length": 10 * float_or_zero(record.sepal_length),
                "sepal_width": 10 * float_or_zero(record.sepal_width),
                "petal_length": 10 * float_or_zero(record.petal_length),
                "petal_width": 10 * float_or_zero(record.petal_width),
                "iris_class": str(record.iris_class).upper(),
            },
        }
    )


def preprocess_data(
    data: Iterable[EtlSourceDataRecord],
) -> Generator[EtlSourceDataRecord, None, None]:
    for item in data:
        yield process_record(item)


def echo_data(data: Iterable[EtlSourceDataRecord]) -> None:
    for item in data:
        print(item)


def write_csv_data(out_file: str, data: Iterable[EtlSourceDataRecord]) -> None:
    fieldnames: List[str] = [field.name for field in fields(EtlOutputDataRecord)]

    with open(out_file, mode="w", encoding="utf-8") as out_csv_file:
        writer = csv.DictWriter(f=out_csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for record in data:
            writer.writerow(asdict(record))
