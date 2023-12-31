from dataclasses import dataclass
from enum import Enum
from typing import TypeVar


T = TypeVar("T")
U = TypeVar("U")
G = TypeVar("G")
S = TypeVar("S")


class IssueType(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True)
class Issue:
    issue_type: IssueType
    message: str
