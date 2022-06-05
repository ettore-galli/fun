# https://www.csse.canterbury.ac.nz/greg.ewing/essays/monads/DemystifyingMonads.html
from __future__ import annotations
from typing import Callable, Any, Optional


class Monad:
    def __init__(self, value=lambda: Monad("start"), success: bool = True, message: Optional[str] = None):
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

    def then(self, f: Callable[[], Monad]):
        if not self.success:
            return Monad(value=self.value or self.message, success=self.success, message=self.message)
        return f()

    def __or__(self, f):
        return self.bind(f)

    def __rshift__(self, f):
        return self.bind(f)

    def __add__(self, f):
        return self.then(f)


def pure_input(_):
    value = input()
    if value == "xxx":
        return Monad(lambda: None, success=False, message=f"error: {value}")
    return Monad(lambda: value)

def pure_input_action():
    value = input()
    if value == "xxx":
        return Monad(lambda: None, success=False, message=f"error: {value}")
    return Monad(lambda: value)

def pure_print(text): return Monad(lambda: print(f"* {text} *"))


if __name__ == '__main__':
    print("1 --- raw")
    # workflow_raw = Monad(lambda: "init") >> \
    #     (lambda _: Monad(lambda: input())) >> \
    #     (lambda text: Monad(lambda: print(f"* {text} *")))

    # workflow_raw.run()

    print("2 --- better (actual complex functions")
    workflow_better = Monad(lambda: "init") + pure_input_action >> pure_print
    workflow_better.run()

    print("3 --- mocked")
    workflow_mock = Monad(lambda: "example value") >> pure_print
    workflow_mock.run()
