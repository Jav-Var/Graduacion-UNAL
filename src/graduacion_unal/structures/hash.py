from typing import Any, Optional, Iterator

class Entry:
    """
    Helper class representing a key-value pair node for a singly linked list in each bucket.
    """

    __slots__ = ('key', 'value', 'next')

    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.value: Any = value
        self.next: Optional[Entry] = None


class HashMap:
    """
    A hash map  implementation using separate chaining.

    Attributes:
        capacity: Number of buckets.
        size: Total number of key-value pairs.
        buckets: Array of bucket heads (each a linked list of Entry nodes).
    """

    __slots__ = ('buckets', 'size', 'capacity', 'load_factor')
    LOAD_FACTOR = 0.75
    INITIAL_CAPACITY = 8


    def __init__(self) -> None:
        """
        Initialize the hash map.

        Args:
            initialcapacity: Number of buckets to start with (must be > 0).
            load_factor: Threshold ratio of size/capacity to trigger resizing.
        """
        self.capacity: int = self.INITIAL_CAPACITY
        self.load_factor: float = self.LOAD_FACTOR
        self.buckets: list[Optional[Entry]] = [None] * self.capacity
        self.size: int = 0


    def bucket_index(self, key: Any) -> int:
        return hash(key) % self.capacity


    def resize(self) -> None:
        """
        Double the capacity and rehash all existing entries.
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        oldsize = self.size
        self.size = 0

        for head in old_buckets:
            current = head
            while current:
                self.set(current.key, current.value)
                current = current.next
        assert self.size == oldsize


    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update the given key with its value.

        Time complexity: O(1) on average, amortized.
        """
        if (self.size + 1) / self.capacity > self.load_factor:
            self.resize()

        idx = self.bucket_index(key)
        head = self.buckets[idx]
        current = head
        # update existing
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        # insert new
        new_entry = Entry(key, value)
        new_entry.next = head
        self.buckets[idx] = new_entry
        self.size += 1
    

    def get(self, key: Any) -> Any:
        """
        Return the value associated with key.

        Raises:
            KeyError: If key is not present.
        """
        idx = self.bucket_index(key)
        current = self.buckets[idx]
        while current != None:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"{key!r} not found")


    def remove(self, key: Any) -> Any:
        """
        Remove the entry for key and return its value.

        Raises:
            KeyError: If key is not present.
        """
        idx = self.bucket_index(key)
        current = self.buckets[idx]
        prev: Optional[Entry] = None

        while current:
            if current.key == key:
                if prev is None:
                    self.buckets[idx] = current.next
                else:
                    prev.next = current.next
                self.size -= 1
                return current.value
            prev, current = current, current.next

        raise KeyError(f"{key!r} not found")


    def contains(self, key: Any) -> bool:
        try:
            self.get(key)
            return True
        except KeyError:
            return False


    def items(self) -> Iterator[tuple[Any, Any]]:
        # walk each bucket
        for head in self.buckets:
            current = head
            while current:
                yield current.key, current.value
                current = current.next