from __future__ import annotations
from dataclasses import dataclass

import os
from typing import List, Optional, Any, Callable, Dict

from config import read_config
from logger import log
from reader import read_input
from writer import write_output


class IO:
    def __init__(self, data: Optional[Any] = None):
        self.__data: Optional[Any] = data

    @classmethod
    def unit(cls, data: Any):
        return IO(data)

    def bind(self, f: Callable[[Any], IO]):
        return f(self.__data)

    def __rshift__(self, other):
        return self.bind(other)


def read_config_action() -> IO:
    return IO(data=read_config("./cfg/config.ini"))


def read_input_action(input_file_name: str) -> IO:
    return IO(data=list(read_input(input_file_name)))


def print_config_action(config: Dict) -> IO:
    print(config)
    return IO()


def print_input_action(input: List) -> IO:
    for item in input:
        print(item)
    return IO()


def compose_output_file_name(entry: str, config: Dict):
    return os.path.join(
        config["output_directory"],
        f'{config["output_file_prefix"]}_{entry[:10].strip()}.txt',
    )


def write_output_action(cfg: Dict, input: List) -> IO:
    for entry_data in input:
        output_file_name = compose_output_file_name(entry_data, cfg)
        print(f"Writing {output_file_name}")
        write_output(entry_data, output_file_name)

    return IO()


def workflow() -> IO:
    read_config_action().bind(
        lambda c: read_input_action(c["input_file"]).bind(
            lambda input: print_config_action(c).bind(
                lambda _: print_input_action(input).bind(
                    lambda _: write_output_action(c, input)
                )
            )
        )
    )


if __name__ == "__main__":
    print(os.path.abspath("."))
    workflow()
