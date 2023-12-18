from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class IssueType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class Issue:
    type: IssueType
    message: str
    data: Dict


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
