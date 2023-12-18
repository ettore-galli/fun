from typing import Any, Generator, Protocol

from functional_etl.data.base import EtlSourceDataRecord


class EtlDataSource(Protocol):
    def __call__(self, *args: Any, **kwds: Any) -> Generator[EtlSourceDataRecord, None, None]:
        return super().__call__(*args, **kwds)
