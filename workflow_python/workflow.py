# https://www.csse.canterbury.ac.nz/greg.ewing/essays/monads/DemystifyingMonads.html
from __future__ import annotations
from typing import Callable, Any, Optional


class Workflow:
    def __init__(self, value=lambda: Workflow("start"), success: bool = True, message: Optional[str] = None):
        self.value = value
        self.success = success
        self.message = message

    @staticmethod
    def start():
        return Workflow()

    @classmethod
    def unit(cls, value: Any = None):
        return Workflow(lambda _: value)

    def run(self):
        return self.value()

    def bind(self, f: Callable[[Any], Workflow]):
        if not self.success:
            return Workflow(value=self.value or self.message, success=self.success, message=self.message)
        return f(self.value())

    def then(self, f: Callable[[], Workflow]):
        if not self.success:
            return Workflow(value=self.value or self.message, success=self.success, message=self.message)
        return f()

    def __or__(self, f):
        return self.bind(f)

    def __rshift__(self, f):
        return self.bind(f)

    def __pow__(self, f):
        return self.then(f)


def pure_input(_):
    value = input()
    if value == "xxx":
        return Workflow(lambda: None, success=False, message=f"error: {value}")
    return Workflow(lambda: value)


def pure_input_action():
    value = input()
    if value == "xxx":
        return Workflow(lambda: None, success=False, message=f"error: {value}")
    return Workflow(lambda: value)


def pure_print(text): return Workflow(lambda: print(f"* {text} *"))


if __name__ == '__main__':
    print("1 --- raw")
    # workflow_raw = Monad(lambda: "init") >> \
    #     (lambda _: Monad(lambda: input())) >> \
    #     (lambda text: Monad(lambda: print(f"* {text} *")))

    # workflow_raw.run()

    print("2 --- better (actual complex functions")
    workflow_better = Workflow(lambda: "init") ** pure_input_action >> pure_print
    workflow_better.run()

    print("3 --- mocked")
    workflow_mock = Workflow(lambda: "example value") >> pure_print
    workflow_mock.run()
