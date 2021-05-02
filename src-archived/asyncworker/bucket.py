from typing import List, TypeVar, Generic

T = TypeVar("T")


class Bucket(Generic[T]):
    def __init__(self, size: int) -> None:
        self.size = size
        # fixme: Criar uma interface comum para as *Message
        # para substituir esse Any
        self._items: List[T] = []

    def is_full(self) -> bool:
        return len(self._items) == self.size

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def put(self, item: T):
        if self.is_full():
            error_msg = f"Bucket is at full capacity: {self.size}"
            raise BucketFullException(error_msg)
        self._items.append(item)

    def pop_all(self) -> List[T]:
        _r = self._items
        self._items = []
        return _r

    @property
    def used(self) -> int:
        return len(self._items)


class BucketFullException(Exception):
    pass
