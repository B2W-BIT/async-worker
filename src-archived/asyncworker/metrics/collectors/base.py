import abc
from typing import Iterable

from prometheus_client import Metric


class BaseCollector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def collect(self) -> Iterable[Metric]:
        """A method that returns a list of Metric objects"""
