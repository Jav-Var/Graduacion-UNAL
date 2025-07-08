from typing import Any, Optional, Iterator

class Entry:
    """
    
    Clase auxiliar que representa un nodo de par clave-valor en una lista simplemente enlazada
    dentro de cada cubeta (bucket) del hash map.
    """

    __slots__ = ('key', 'value', 'next')

    def __init__(self, key: Any, value: Any) -> None:
        self.key: Any = key
        self.value: Any = value
        self.next: Optional[Entry] = None


class HashMap:
    """
    Una implementacion de hash map utilizando encadenamiento separado.

    Attributes:
        capacity: Numero de buckets.
        size: Numero total de parejas key-value.
        buckets: Array de las head de los buckets (cada lista enlazada de nodos de entrada).
    """

    __slots__ = ('buckets', 'size', 'capacity', 'load_factor')
    LOAD_FACTOR = 0.75
    INITIAL_CAPACITY = 8


    def __init__(self) -> None:
        """
        Inicializar el hash map.

        Args:
            initialcapacity: Numero de buckets con los que empezar (debe ser > 0).
            load_factor: Relacion de umbral de tamaño/capacidad para activar el cambio de tamaño.
        """
        self.capacity: int = self.INITIAL_CAPACITY
        self.load_factor: float = self.LOAD_FACTOR
        self.buckets: list[Optional[Entry]] = [None] * self.capacity
        self.size: int = 0


    def bucket_index(self, key: Any) -> int:
        return hash(key) % self.capacity


    def resize(self) -> None:
        """
        Duplica la capacidad y rehashea todas las entradas existentes.
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        oldsize = self.size
        self.size = 0

        for head in old_buckets:
            current = head
            while current:
                self.put(current.key, current.value)
                current = current.next
        assert self.size == oldsize


    def put(self, key: Any, value: Any) -> None:
        """
        Inserta o actualiza la clave con su valor.
        Time complexity: O(1) en promedio, amortized.
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
        Return:
            El valor asociado a la key.

        Raises:
            KeyError: Si la key no se encuentra.
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
        Elimina el elemento asociado a la key y retorna su valor.
        Raises:
            KeyError: Si la key no se encuentra.
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
        """        
        Verifica si la key existe en el hash map.
        Args:
            key: La clave a verificar.
        Returns:
            True si la clave existe, False en caso contrario.
        """
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
    
    def keys(self) -> Iterator[Any]:
        """
        Returns:
        Un iterador sobre las claves en el hash map.
        """
        for key, _ in self.items():
            yield key
    
    def values(self) -> Iterator[Any]:
        """
        Returns:
        Un iterador sobre los valores en el hash map.
        """
        for _, value in self.items():
            yield value
    
    def __len__(self) -> int:
        """
        Returns:
        El número de parejas key-value que hay en el hash map.
        """
        return self.size
    
    def __iter__(self) -> Iterator[tuple[Any, Any]]:
        """
        Returns:
        Un iterador sobre las parejas key-value en el hash map.
        """
        return self.items()