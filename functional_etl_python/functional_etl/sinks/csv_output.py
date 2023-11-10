import csv
from dataclasses import asdict
from typing import List
from functional_etl.sinks.base import EtlDataSink, EtlOutputDataRecord


class CsvEtlDataSink(EtlDataSink):
    def __init__(
        self,
        out_file: str,
        fieldnames: List[str] = EtlOutputDataRecord.__dataclass_fields__,
    ) -> None:
        super().__init__()
        self.out_file = out_file
        self.fieldnames: List[str] = fieldnames or []
        self.writer = csv.DictWriter(
            f=open(self.out_file, mode="w", encoding="utf-8"), fieldnames=fieldnames
        )
        self.writer.writeheader()

    def write(self, record: EtlOutputDataRecord) -> None:
        self.writer.writerow(asdict(record))
