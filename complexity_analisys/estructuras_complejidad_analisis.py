"""
Análisis de Complejidad Temporal de las Estructuras de Datos Implementadas

Este archivo contiene el análisis detallado de las complejidades temporales
de todas las estructuras de datos implementadas en el proyecto.
"""

def generar_tablas_complejidad():
    """
    Genera las tablas de complejidad temporal para todas las estructuras implementadas.
    """
    
    print("=" * 80)
    print("ANÁLISIS DE COMPLEJIDAD TEMPORAL - ESTRUCTURAS DE DATOS")
    print("=" * 80)
    
    # Tabla 1: MaxHeap
    print("\n" + "=" * 50)
    print("1. MAX HEAP (MaxHeap)")
    print("=" * 50)
    print("| Método     | Complejidad Temporal | Descripción de la Implementación |")
    print("| ---------- | -------------------- | -------------------------------- |")
    print("| `__init__` | O(1)                 | Inicializa lista vacía           |")
    print("| `push`     | O(log n)             | Sift-up después de inserción     |")
    print("| `pop`      | O(log n)             | Sift-down después de extracción  |")
    print("| `__len__`  | O(1)                 | Retorna longitud de la lista     |")
    print("| `is_empty` | O(1)                 | Verifica si la lista está vacía  |")
    
    # Tabla 2: Queue
    print("\n" + "=" * 50)
    print("2. QUEUE (Queue)")
    print("=" * 50)
    print("| Método     | Complejidad Temporal | Descripción de la Implementación |")
    print("| ---------- | -------------------- | -------------------------------- |")
    print("| `__init__` | O(1)                 | Inicializa head, tail y size     |")
    print("| `enqueue`  | O(1)                 | Inserción al final (tail)        |")
    print("| `dequeue`  | O(1)                 | Extracción del frente (head)     |")
    print("| `peek`     | O(1)                 | Acceso al elemento del frente    |")
    print("| `is_empty` | O(1)                 | Verifica si size == 0            |")
    print("| `__len__`  | O(1)                 | Retorna el valor de size         |")
    print("| `__iter__` | O(n)                 | Recorre toda la lista enlazada   |")
    
    # Tabla 3: Disjoint Sets
    print("\n" + "=" * 50)
    print("3. DISJOINT SETS (DisjointSets)")
    print("=" * 50)
    print("| Método         | Complejidad Temporal | Descripción de la Implementación |")
    print("| -------------- | -------------------- | -------------------------------- |")
    print("| `__init__`     | O(n)                 | Inicializa arrays parent y rank |")
    print("| `find`         | O(α(n)) ≈ O(1)       | Path compression optimizado     |")
    print("| `union`        | O(α(n)) ≈ O(1)       | Union by rank optimizado        |")
    print("| `connected`    | O(α(n)) ≈ O(1)       | Usa find() dos veces            |")
    print("| `get_set_size` | O(n)                 | Recorre todos los elementos      |")
    print("| `get_all_sets` | O(n)                 | Recorre todos los elementos      |")
    print("| `get_num_sets` | O(1)                 | Retorna contador mantenido       |")
    print("| `reset`        | O(n)                 | Reinicializa arrays parent/rank |")
    
    # Tabla 4: HashMap
    print("\n" + "=" * 50)
    print("4. HASH MAP (HashMap)")
    print("=" * 50)
    print("| Método     | Complejidad Temporal | Descripción de la Implementación |")
    print("| ---------- | -------------------- | -------------------------------- |")
    print("| `__init__` | O(1)                 | Inicializa array de buckets      |")
    print("| `put`      | O(1) promedio        | Encadenamiento separado          |")
    print("| `get`      | O(1) promedio        | Búsqueda en lista enlazada       |")
    print("| `remove`   | O(1) promedio        | Eliminación en lista enlazada    |")
    print("| `contains` | O(1) promedio        | Usa get() con manejo de excepción|")
    print("| `items`    | O(n)                 | Recorre todos los buckets        |")
    print("| `keys`     | O(n)                 | Usa items() y extrae claves      |")
    print("| `values`   | O(n)                 | Usa items() y extrae valores     |")
    print("| `__len__`  | O(1)                 | Retorna contador size            |")
    print("| `__iter__` | O(n)                 | Usa items()                      |")
    
    # Tabla 5: Resumen de Optimizaciones
    print("\n" + "=" * 50)
    print("5. OPTIMIZACIONES IMPLEMENTADAS")
    print("=" * 50)
    print("| Estructura    | Optimización                    | Impacto en Complejidad |")
    print("| ------------- | ------------------------------- | ---------------------- |")
    print("| MaxHeap       | Sift-up y Sift-down eficientes  | O(log n) garantizado   |")
    print("| Queue         | Singly linked list con tail     | O(1) enqueue/dequeue  |")
    print("| DisjointSets  | Path compression + Union by rank| O(α(n)) ≈ O(1)        |")
    print("| HashMap       | Load factor + resize dinámico   | O(1) promedio          |")
    
    # Tabla 6: Casos Especiales
    print("\n" + "=" * 50)
    print("6. CASOS ESPECIALES Y CONSIDERACIONES")
    print("=" * 50)
    print("| Estructura    | Caso Especial                   | Complejidad           |")
    print("| ------------- | ------------------------------- | ---------------------- |")
    print("| MaxHeap       | Heap vacío en pop()             | O(1) - excepción      |")
    print("| Queue         | Queue vacía en dequeue()        | O(1) - excepción      |")
    print("| DisjointSets  | Path compression en find()      | O(α(n)) amortizado    |")
    print("| HashMap       | Colisiones (encadenamiento)     | O(n) en peor caso     |")
    print("| HashMap       | Resize automático               | O(n) pero amortizado  |")

def analizar_complejidad_espacial():
    """
    Análisis de complejidad espacial de las estructuras.
    """
    print("\n" + "=" * 50)
    print("7. COMPLEJIDAD ESPACIAL")
    print("=" * 50)
    print("| Estructura    | Complejidad Espacial | Descripción                    |")
    print("| ------------- | -------------------- | ------------------------------ |")
    print("| MaxHeap       | O(n)                 | Lista de n elementos          |")
    print("| Queue         | O(n)                 | n nodos en lista enlazada     |")
    print("| DisjointSets  | O(n)                 | Arrays parent[n] y rank[n]    |")
    print("| HashMap       | O(n)                 | n entradas en buckets        |")

def generar_reporte_completo():
    """
    Genera un reporte completo de análisis de complejidad.
    """
    print("REPORTE DE ANÁLISIS DE COMPLEJIDAD TEMPORAL")
    print("Estructuras de Datos Implementadas")
    print("=" * 80)
    
    generar_tablas_complejidad()
    analizar_complejidad_espacial()
    
    print("\n" + "=" * 80)
    print("CONCLUSIONES DEL ANÁLISIS")
    print("=" * 80)
    print("1. Todas las estructuras implementan las optimizaciones estándar de la literatura.")
    print("2. Las complejidades temporales son óptimas para cada operación.")
    print("3. Las estructuras están bien diseñadas para el uso en el algoritmo random_schedule.")
    print("4. El uso de MaxHeap con tuplas (prioridad, créditos, id) es eficiente para la planificación.")
    print("5. La Queue con singly linked list es ideal para el ordenamiento topológico.")
    print("6. Los DisjointSets optimizados son perfectos para detectar ciclos.")
    print("7. El HashMap proporciona acceso O(1) para el almacenamiento de cursos.")

def main():
    """
    Función principal para generar el reporte de complejidad.
    """
    generar_reporte_completo()

if __name__ == "__main__":
    main() 