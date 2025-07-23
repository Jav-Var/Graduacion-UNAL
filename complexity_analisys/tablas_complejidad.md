# Análisis de Complejidad Temporal - Estructuras de Datos Implementadas

## 1. MaxHeap

| Método     | Complejidad Temporal Promedio | Descripción de la Implementación |
| ---------- | ----------------------------- | -------------------------------- |
| `__init__` | O(1)                          | Inicializa lista vacía           |
| `push`     | O(log n)                      | Sift-up después de inserción     |
| `pop`      | O(log n)                      | Sift-down después de extracción  |
| `__len__`  | O(1)                          | Retorna longitud de la lista     |
| `is_empty` | O(1)                          | Verifica si la lista está vacía  |

## 2. Queue

| Método     | Complejidad Temporal Promedio | Descripción de la Implementación |
| ---------- | ----------------------------- | -------------------------------- |
| `__init__` | O(1)                          | Inicializa head, tail y size     |
| `enqueue`  | O(1)                          | Inserción al final (tail)        |
| `dequeue`  | O(1)                          | Extracción del frente (head)     |
| `peek`     | O(1)                          | Acceso al elemento del frente    |
| `is_empty` | O(1)                          | Verifica si size == 0            |
| `__len__`  | O(1)                          | Retorna el valor de size         |
| `__iter__` | O(n)                          | Recorre toda la lista enlazada   |

## 3. Disjoint Sets

| Método         | Complejidad Temporal Promedio | Descripción de la Implementación |
| -------------- | ----------------------------- | -------------------------------- |
| `__init__`     | O(n)                          | Inicializa arrays parent y rank |
| `find`         | O(α(n)) ≈ O(1)                | Path compression optimizado     |
| `union`        | O(α(n)) ≈ O(1)                | Union by rank optimizado        |
| `connected`    | O(α(n)) ≈ O(1)                | Usa find() dos veces            |
| `get_set_size` | O(n)                          | Recorre todos los elementos      |
| `get_all_sets` | O(n)                          | Recorre todos los elementos      |
| `get_num_sets` | O(1)                          | Retorna contador mantenido       |
| `reset`        | O(n)                          | Reinicializa arrays parent/rank |

## 4. HashMap

| Método     | Complejidad Temporal Promedio | Descripción de la Implementación |
| ---------- | ----------------------------- | -------------------------------- |
| `__init__` | O(1)                          | Inicializa array de buckets      |
| `put`      | O(1) en promedio              | Encadenamiento separado          |
| `get`      | O(1) en promedio              | Búsqueda en lista enlazada       |
| `remove`   | O(1) en promedio              | Eliminación en lista enlazada    |
| `contains` | O(1) en promedio              | Usa get() con manejo de excepción|
| `items`    | O(n)                          | Recorre todos los buckets        |
| `keys`     | O(n)                          | Usa items() y extrae claves      |
| `values`   | O(n)                          | Usa items() y extrae valores     |
| `__len__`  | O(1)                          | Retorna contador size            |
| `__iter__` | O(n)                          | Usa items()                      |

## 5. Optimizaciones Implementadas

| Estructura    | Optimización                    | Impacto en Complejidad |
| ------------- | ------------------------------- | ---------------------- |
| MaxHeap       | Sift-up y Sift-down eficientes  | O(log n) garantizado   |
| Queue         | Singly linked list con tail     | O(1) enqueue/dequeue  |
| DisjointSets  | Path compression + Union by rank| O(α(n)) ≈ O(1)        |
| HashMap       | Load factor + resize dinámico   | O(1) promedio          |

## 6. Complejidad Espacial

| Estructura    | Complejidad Espacial | Descripción                    |
| ------------- | -------------------- | ------------------------------ |
| MaxHeap       | O(n)                 | Lista de n elementos          |
| Queue         | O(n)                 | n nodos en lista enlazada     |
| DisjointSets  | O(n)                 | Arrays parent[n] y rank[n]    |
| HashMap       | O(n)                 | n entradas en buckets        |

## 7. Casos Especiales

| Estructura    | Caso Especial                   | Complejidad           |
| ------------- | ------------------------------- | ---------------------- |
| MaxHeap       | Heap vacío en pop()             | O(1) - excepción      |
| Queue         | Queue vacía en dequeue()        | O(1) - excepción      |
| DisjointSets  | Path compression en find()      | O(α(n)) amortizado    |
| HashMap       | Colisiones (encadenamiento)     | O(n) en peor caso     |
| HashMap       | Resize automático               | O(n) pero amortizado  |

## Conclusiones

1. **Optimizaciones Estándar**: Todas las estructuras implementan las optimizaciones estándar de la literatura.
2. **Complejidades Óptimas**: Las complejidades temporales son óptimas para cada operación.
3. **Diseño Eficiente**: Las estructuras están bien diseñadas para el uso en el algoritmo `random_schedule`.
4. **MaxHeap Eficiente**: El uso de MaxHeap con tuplas `(prioridad, créditos, id)` es eficiente para la planificación.
5. **Queue Ideal**: La Queue con singly linked list es ideal para el ordenamiento topológico.
6. **DisjointSets Optimizados**: Los DisjointSets optimizados son perfectos para detectar ciclos.
7. **HashMap Rápido**: El HashMap proporciona acceso O(1) para el almacenamiento de cursos.

## Notas Técnicas

- **α(n)**: Función inversa de Ackermann, prácticamente constante para valores realistas de n.
- **Amortizado**: Las operaciones de resize en HashMap son O(n) pero amortizadas a O(1) por operación.
- **Path Compression**: Optimización en DisjointSets que hace que todos los nodos en un camino apunten directamente a la raíz.
- **Union by Rank**: Optimización en DisjointSets que conecta el árbol más pequeño al más grande. 