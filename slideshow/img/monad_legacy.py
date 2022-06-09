# https://www.csse.canterbury.ac.nz/greg.ewing/essays/monads/DemystifyingMonads.html
from __future__ import annotations
from typing import Callable, Any, Optional


class Monad:
    def __init__(self, value=None, success: bool = True, message: Optional[str] = None):
        self.value = value
        self.success = success
        self.message = message

    @classmethod
    def unit(cls, value: Any = None):
        return Monad(value)

    @staticmethod
    def _merge_data(current: Monad, new: Monad):
        def strmsg(message: Optional[str] = None):
            return message if message is not None else ""
        return Monad(new.value or current.value, success=current.success and new.success, message=strmsg(current.message) + strmsg(new.message))

    def bind(self, f: Callable[[Any], Monad]):
        if not self.success:
            return Monad(value=self.value or self.message, success=self.success, message=self.message)
        return Monad._merge_data(self, f(self.value))

    def __or__(self, f):
        return self.bind(f)


def pure_input(_):
    data = input()
    if data == "xxx":
        return Monad(success=False, value=None, message=f"{data} non ammesso come valore")
    return Monad(f"-- {data} --")


def pure_print(text: str):
    print("pure print called")
    print(text)
    return Monad.unit()

def pure_logger(text: str):
    print("pure logger called")
    print(f"log: {text}")
    return Monad.unit()

if __name__ == '__main__':
    print("1 ---")
    Monad().bind(pure_input).bind(pure_print)
    print("2 ---")
    Monad() | pure_input | pure_logger | pure_print
