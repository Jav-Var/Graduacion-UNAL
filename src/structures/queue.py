from typing import Any, Optional, Iterator

class Node:
    """
    Helper class representing a node for a singly linked list.
    """
    
    __slots__ = ('value', 'next')

    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.next: Optional[Node] = None

class Queue:
    """
    Queue implementation using a singly linked list for O(1) enqueue and dequeue operations.
    """
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size: int = 0

    def enqueue(self, item: Any) -> None:
        """
        Add an item to the end of the queue.

        Time complexity: O(1)
        """
        new_node = Node(item)

        if self.is_empty():
            self.head = new_node
        else:
            assert self.tail is not None  # for type checking
            self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def dequeue(self) -> Any:
        """
        Remove and return the item from the front of the queue.

        Time complexity: O(1)

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")

        assert self.head is not None  # for type checking
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        # If the queue is now empty, reset tail as well
        if self.is_empty():
            self.tail = None
        return value

    def peek(self) -> Any:
        """
        Return the front item without removing it.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")
        assert self.head is not None
        return self.head.value

    def is_empty(self) -> bool:
        """
        Check whether the queue is empty.

        Returns:
            True if the queue has no items, False otherwise.
        """
        return self.size == 0

    def __len__(self) -> int:
        """
        Return the number of items in the queue.
        """
        return self.size

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over the queue's items from front to back.
        """
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        """
        String representation of the queue for debugging.
        """
        items = ", ".join(repr(item) for item in self)
        return f"Queue([{items}])"
