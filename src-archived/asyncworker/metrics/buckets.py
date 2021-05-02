from typing import List

from asyncworker.conf import INFINITY


def exponential_buckets(start: float, factor: float, count: int) -> List[float]:
    """
    Creates 'count' buckets, where the lowest bucket has an upper bound of
    'start' and each following bucket's upper bound is 'factor' times the
    previous bucket's upper bound. The final +Inf bucket is not counted
    and is included in the returned slice. The returned list is meant to be
    used for the buckets field of Histogram.

    >>> exponential_buckets(start=100.0, factor=2, count=5)
    [100.0, 200.0, 400.0, 800.0, 1600.0, inf]

    >>> exponential_buckets(start=100.0, factor=2.5, count=5)
    [100.0, 250.0, 625.0, 1562.5, 3906.25, inf]
    """
    if count < 1:
        raise ValueError(f"Expected a positive `count` value. Got '{count}'")
    start = float(start)
    if start <= 0:
        raise ValueError(f"Expected a positive `start` value. Got '{start}'")
    if factor <= 1:
        raise ValueError(
            f"Exponential buckets need a `factor` greater than 1. Got '{factor}'"
        )

    def gen_steps():
        nonlocal start
        yield start
        for _ in range(count - 1):
            start = start * factor
            yield start

    return [*gen_steps(), INFINITY]


def linear_buckets(start: float, width: float, count: int) -> List[float]:
    """
    Creates 'count' buckets, each 'width' wide, where the lowest bucket has an
    upper bound of 'start'. The final +Inf bucket is not counted and is
    included in the returned slice. The returned list is meant to be used for
    the buckets field of Histograms.

    >>> linear_buckets(start=100.0, width=100, count=5)
    [100.0, 200.0, 300.0, 400.0, 500.0, inf]

    >>> linear_buckets(start=100.0, width=1000, count=5)
    [100.0, 1100.0, 2100.0, 3100.0, 4100.0, inf]

    """
    if count < 1:
        raise ValueError(f"Expected a positive `count` value. Got '{count}'")
    return [*(start + (width * n) for n in range(count)), INFINITY]
