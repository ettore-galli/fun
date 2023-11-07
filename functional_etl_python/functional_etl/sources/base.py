from dataclasses import dataclass
from typing import Any, Generator, Optional, Protocol


@dataclass(frozen=True)
class EtlDataRecord:
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

 
class EtlDataSource(Protocol):
    def __call__(self, *args: Any, **kwds: Any) -> Generator[EtlDataRecord, None, None]:
        return super().__call__(*args, **kwds)
