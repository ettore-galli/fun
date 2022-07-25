from dataclasses import dataclass
from typing import Any, Callable, List

from yaml import compose


@dataclass
class WriterResult:
    value: Any
    log: List[str]


def square(input: float) -> float:
    return input**2


def format(input: float) -> str:
    return f"*{input}*"


def square_step(input: float) -> WriterResult:
    squared = square(input)
    return WriterResult(value=squared, log=[f"{input} ** 2 --> {squared} "])


def format_step(input: float) -> WriterResult:
    formatted = format(input)
    return WriterResult(value=formatted, log=[f"{input} --> {formatted}  "])


WriterKleisliArrow = Callable[[Any], WriterResult]


def compose_writers(a: WriterKleisliArrow, b: WriterKleisliArrow) -> WriterKleisliArrow:
    def _composed(value: Any) -> WriterResult:
        middle_step = a(value)
        final_step = b(middle_step.value)
        return WriterResult(
            value=final_step.value, log=middle_step.log + final_step.log
        )

    return _composed


if __name__ == "__main__":
    composed = compose_writers(square_step, format_step)

    print(composed(7))