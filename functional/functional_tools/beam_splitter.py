import queue

from typing import Generator, Tuple, TypeVar

T = TypeVar("T")


def beam_splitter(
    source: Generator[T, None, None]
) -> Tuple[Generator[T, None, None], Generator[T, None, None]]:
    beam_a: queue.Queue = queue.Queue()
    beam_b: queue.Queue = queue.Queue()

    def gen(this_beam: queue.Queue):
        siter = iter(source)
        while True:
            if this_beam.empty():
                try:
                    item = next(siter)
                except StopIteration:
                    return
                beam_a.put(item)
                beam_b.put(item)
            yield this_beam.get(block=True)

    return gen(beam_a), gen(beam_b)
