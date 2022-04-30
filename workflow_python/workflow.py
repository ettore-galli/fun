from __future__ import annotations
from dataclasses import dataclass

import os
from typing import List, Optional, Any, Callable, Dict

from services.config import read_config
from services.order import get_order
from services.exchange import get_exchange
from services.price import get_price
from services.writer import write_output


class WorkflowPayload:

    def __init__(self, config: Optional[Any] = None, data: Optional[Any] = None):
        self.data: Optional[Any] = data
        self.config: Optional[Any] = config

    def __repr__(self):
        return str(self.config) + str(self.data)

    @classmethod
    def unit(cls, config: Any, data: Any):
        return WorkflowPayload(config, data)

    def bind(self, f: Callable[[WorkflowPayload], WorkflowPayload]):
        return f(self)

    def __rshift__(self, other):
        return self.bind(other)


def read_config_action(payload: WorkflowPayload) -> WorkflowPayload:
    return WorkflowPayload(config=read_config("./cfg/config.ini"))


def read_order_action(payload: WorkflowPayload) -> WorkflowPayload:
    return WorkflowPayload(data=get_order(service_url=payload.config["orders_url"], order_number=1))


# def print_config_action(config: Dict) -> WorkflowPayload:
#     print(config)
#     return WorkflowPayload()


# def print_input_action(input: List) -> WorkflowPayload:
#     for item in input:
#         print(item)
#     return WorkflowPayload()


# def compose_output_file_name(entry: str, config: Dict):
#     return os.path.join(
#         config["output_directory"],
#         f'{config["output_file_prefix"]}_{entry[:10].strip()}.txt',
#     )


# def write_output_action(cfg: Dict, input: List) -> WorkflowPayload:
#     for entry_data in input:
#         output_file_name = compose_output_file_name(entry_data, cfg)
#         print(f"Writing {output_file_name}")
#         write_output(entry_data, output_file_name)

#     return WorkflowPayload()


# def workflow() -> WorkflowPayload:
#     read_config_action().bind(


# def workflow() -> WorkflowPayload:
#     read_config_action().bind(
#         lambda c: read_input_action(c["input_file"]).bind(
#             lambda input: print_config_action(c).bind(
#                 lambda _: print_input_action(input).bind(
#                     lambda _: write_output_action(c, input)
#                 )
#             )
#         )
#     )
if __name__ == "__main__":
    print(os.path.abspath("."))
    print(
        WorkflowPayload.unit({}, {}).bind(
            read_config_action).bind(read_order_action)
    )
