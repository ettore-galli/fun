from dataclasses import dataclass
from typing import Any, Generator, Optional, Protocol


@dataclass(frozen=True)
class RunEnvironment:
    data_source_file: str
    output_file: str
