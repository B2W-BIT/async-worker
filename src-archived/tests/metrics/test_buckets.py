import unittest

from asyncworker.conf import INFINITY
from asyncworker.metrics import exponential_buckets
from asyncworker.metrics.buckets import linear_buckets


class ExponentialBucketsTests(unittest.TestCase):
    def test_it_raises_an_error_when_count_isnt_a_positive_integer(self):
        with self.assertRaises(ValueError):
            exponential_buckets(start=100, factor=2, count=0)

        with self.assertRaises(ValueError):
            exponential_buckets(start=100, factor=2, count=-1)

    def test_it_raises_an_error_when_start_is_negative(self):
        with self.assertRaises(ValueError):
            exponential_buckets(start=-10, factor=2, count=100)

    def test_it_raises_an_error_when_factor_le_1(self):
        for factor in [1, 0, -1]:
            with self.assertRaises(ValueError):
                exponential_buckets(start=100, factor=factor, count=10)

    def test_generated_buckets_length(self):
        count = 5
        buckets = exponential_buckets(start=100.0, factor=2, count=count)
        self.assertEqual(len(buckets), count + 1)

    def test_it_generates_an_exponential_series(self):
        buckets = exponential_buckets(start=100.0, factor=2, count=5)
        self.assertEqual(
            buckets, [100.0, 200.0, 400.0, 800.0, 1600.0, INFINITY]
        )


class LinearBucketsTests(unittest.TestCase):
    def test_it_raises_an_error_when_count_isnt_a_positive_integer(self):
        with self.assertRaises(ValueError):
            linear_buckets(start=100.0, width=100, count=0)

        with self.assertRaises(ValueError):
            linear_buckets(start=100.0, width=100, count=-1)

    def test_generated_bucket_length(self):
        count = 5
        buckets = linear_buckets(start=100.0, width=100, count=count)
        self.assertEqual(count + 1, len(buckets))

    def test_it_generates_a_linear_series(self):
        buckets = linear_buckets(start=100.0, width=100, count=5)
        self.assertEqual(buckets, [100.0, 200.0, 300.0, 400.0, 500.0, INFINITY])

        buckets = linear_buckets(start=100.0, width=1000, count=5)
        self.assertEqual(
            buckets, [100.0, 1100.0, 2100.0, 3100.0, 4100.0, INFINITY]
        )
