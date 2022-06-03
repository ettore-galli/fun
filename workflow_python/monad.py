# https://www.csse.canterbury.ac.nz/greg.ewing/essays/monads/DemystifyingMonads.html
from __future__ import annotations
from typing import Callable, Any


class Monad:
    def __init__(self, value=None, success: bool = True):
        self.value = value
        self.success = success

    @classmethod
    def unit(cls, value: Any = None):
        return Monad(value)

    @staticmethod
    def _merge_data(current: Monad, new: Monad):
        return Monad(new.value or current.value, success=current.success and new.success)

    def bind(self, f: Callable[[Any], Monad]):
        return Monad._merge_data(self, f(self.value))

    def __or__(self, f):
        return self.bind(f)


def pure_input(_):
    return Monad(f"-- {input()} --")


def pure_print(text: str):
    print(text)
    return Monad.unit()


if __name__ == '__main__':
    print("1 ---")
    Monad().bind(pure_input).bind(pure_print)
    print("2 ---")
    Monad() | pure_input | pure_print
