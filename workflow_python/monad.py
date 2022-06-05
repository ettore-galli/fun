# https://www.csse.canterbury.ac.nz/greg.ewing/essays/monads/DemystifyingMonads.html
from __future__ import annotations
from typing import Callable, Any, Optional


class Monad:
    def __init__(self, value=lambda: Monad(None), success: bool = True, message: Optional[str] = None):
        self.value = value
        self.success = success
        self.message = message

    @staticmethod
    def start():
        return Monad()

    @classmethod
    def unit(cls, value: Any = None):
        return Monad(lambda _: value)

    def run(self):
        return self.value()

    # @staticmethod
    # def _merge_data(current: Monad, new: Monad):
    #     def strmsg(message: Optional[str] = None):
    #         return message if message is not None else ""
    #     return Monad(new.value or current.value, success=current.success and new.success, message=strmsg(current.message) + strmsg(new.message))

    def bind(self, f: Callable[[Any], Monad]):
        if not self.success:
            return Monad(value=self.value or self.message, success=self.success, message=self.message)
        return f(self.value())

    def __or__(self, f):
        return self.bind(f)

    def __rshift__(self, f):
        return self.bind(f)


def pure_input(_): return Monad(lambda: input())
def pure_print(text): return Monad(lambda: print(f"* {text} *"))


if __name__ == '__main__':
    print("1 ---")
    workflow_raw = Monad.start() >> \
        (lambda _: Monad(lambda: input())) >> \
        (lambda text: Monad(lambda: print(f"* {text} *")))

    workflow_raw.run()
