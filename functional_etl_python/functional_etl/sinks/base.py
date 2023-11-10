from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generator, Optional, Protocol


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


class EtlDataSink(Protocol):
    def write(self, record: EtlOutputDataRecord) -> None:
        ...
