from typing import Any, Generator

from functional.functional_tools.beam_splitter import beam_splitter


def test_generators_behaviour():
    source: Generator[Any, None, None] = (f"-- {index} --" for index in range(10))

    split_a, split_b = beam_splitter(source=source)

    expected = [
        "-- 0 --",
        "-- 1 --",
        "-- 2 --",
        "-- 3 --",
        "-- 4 --",
        "-- 5 --",
        "-- 6 --",
        "-- 7 --",
        "-- 8 --",
        "-- 9 --",
    ]
    assert list(split_a) == expected
    assert list(split_b) == expected
