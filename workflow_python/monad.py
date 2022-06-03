# https://www.csse.canterbury.ac.nz/greg.ewing/essays/monads/DemystifyingMonads.html
from __future__ import annotations
from typing import Callable, Any


class Monad:
    def __init__(self, value):
        self.value = value

    @classmethod
    def unit(cls, value: Any = None):
        return Monad(value)

    def bind(self, f: Callable[[Any], Monad]):
        return f(self.value)


def pure_input(_):
    return Monad(f"-- {input()} --")


def pure_print(text: str):
    print(text)
    return Monad.unit()


if __name__ == '__main__':
    Monad.unit("start-value").bind(pure_input).bind(pure_print)
