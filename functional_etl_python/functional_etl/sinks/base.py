from __future__ import annotations

from typing import Any, Protocol

from functional_etl.data.base import EtlOutputDataRecord


class EtlDataSink(Protocol):
    def write(self, record: EtlOutputDataRecord) -> None:
        ...
