from typing import Any, Optional, Iterator

class Node:
    
    """Clase que representa un nodo en una singly linked list.
    Cada nodo contiene un valor y una referencia al siguiente nodo."""

    __slots__ = ('value', 'next')

    def __init__(self, value: Any) -> None:
        self.value: Any = value
        self.next: Optional[Node] = None

class Queue:
    """
    Queue implementada utilizando una singly linked list para complejidad O(1)
    en las operaciones enqueue and dequeue.
    """
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size: int = 0

    def enqueue(self, item: Any) -> None:
        """
        Agrega un elemento al final de la queue.

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
        Elimina y retorna el elemento del frente de la queue.
        Time complexity: O(1)

        Raises:
            IndexError: si la queue esta vacia.
        """
        if self.is_empty():
            raise IndexError("dequeue de queue vacia")

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
        Retorna el elemento de enfrente sin eliminarlo.

        Raises:
            IndexError: Si la queue esta vacia.
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")
        assert self.head is not None
        return self.head.value

    def is_empty(self) -> bool:
        """
        Metodo que retorna True si la queue no tiene elementos, de lo contrario False.

        Returns:
            bool: True si la queue esta vacia, False en caso contrario.

        """
        return self.size == 0

    def __len__(self) -> int:
        """
        Returns:
            el numero de elementos de la queue.
        """
        return self.size

    def __iter__(self) -> Iterator[Any]:
        """
        Itera sobre los elementos de la queue desde el frente hasta la parte trasera.
        """
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __repr__(self) -> str:
        """
        Representacion de tipo String de la queue para debugging.
        """
        items = ", ".join(repr(item) for item in self)
        return f"Queue([{items}])"
