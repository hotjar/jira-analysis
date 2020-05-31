from typing import Iterator


def integers(start=1, end=3, num_values=10) -> Iterator[int]:
    integer_range = list(range(start, end + 1))
    i = 0
    for _ in range(num_values):
        if i >= len(integer_range):
            i = 0
        yield integer_range[i]
        i += 1
