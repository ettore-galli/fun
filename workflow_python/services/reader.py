from typing import Generator


def read_input(input_file_name: str) -> Generator[str, None, None]:
    for row in open(input_file_name, "r"):
        yield row

