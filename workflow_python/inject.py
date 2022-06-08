
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Result:
    success: Optional[bool] = True
    message: Optional[str] = None
    data: Optional[float] = None

    def __repr__(self) -> str:
        return self.data if self.success else self.message


def ask_for_input():
    return input()


def process(input_value: Optional[Any]) -> Result:
    try:
        return Result(data=f"*** {float(input_value) * 5} ***")
    except Exception as error:
        return Result(success=False, message=str(error))


def output_result(result):
    print("-" * 50)
    print(result)
    print("-" * 50)


def workflow(get_input, process, put_output):
    input_value = get_input()
    result = process(input_value)
    put_output(result)


if __name__ == '__main__':
    workflow(ask_for_input, process, output_result)
