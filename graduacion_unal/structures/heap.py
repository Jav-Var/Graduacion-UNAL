from typing import Dict, List, Tuple
from graduacion_unal.structures.queue import Queue

class MaxHeap:
    """
    Implementación de un Max-Heap genérico.
    Almacena elementos comparables directamente (por ejemplo, tuplas donde el primer elemento define la prioridad).
    """
    def __init__(self) -> None:
        self._data: List = []

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self._data[idx] > self._data[parent]:
            self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            left = 2 * idx + 1
            right = left + 1
            largest = idx
            if left < n and self._data[left] > self._data[largest]:
                largest = left
            if right < n and self._data[right] > self._data[largest]:
                largest = right
            if largest == idx:
                break
            self._data[idx], self._data[largest] = self._data[largest], self._data[idx]
            idx = largest

    def push(self, item) -> None:
        """Inserta un elemento en el heap."""
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self):
        """Elimina y retorna el elemento de máxima prioridad."""
        if not self._data:
            raise IndexError("pop from empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data