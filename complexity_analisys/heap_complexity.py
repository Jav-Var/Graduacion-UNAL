import random
import time
import matplotlib.pyplot as plt

from graduacion_unal.structures.heap import MaxHeap

def random_numbers(n):
    """Genera una lista de n números aleatorios."""
    return [random.random() for _ in range(n)]

def benchmark_maxheap(sizes, trials=5):
    """
    Para cada n en sizes, mide el tiempo medio de:
      - push: insertar n elementos de golpe
      - pop: extraer todos los elementos de un heap de tamaño n
      - __len__: consultar len() n veces tras llenar el heap
      - is_empty: consultar is_empty() n veces tras vaciar el heap
    Devuelve un dict con listas de tiempos medios.
    """
    times = {
        'push': [],
        'pop': [],
        'len': [],
        'is_empty': []
    }

    for n in sizes:
        t_push = t_pop = t_len = t_empty = 0.0

        for _ in range(trials):
            data = random_numbers(n)

            # Medir push
            heap = MaxHeap()
            start = time.perf_counter()
            for x in data:
                heap.push(x)
            t_push += time.perf_counter() - start

            # Medir __len__
            start = time.perf_counter()
            for _ in range(n):
                _ = len(heap)
            t_len += time.perf_counter() - start

            # Medir pop
            start = time.perf_counter()
            while not heap.is_empty():
                heap.pop()
            t_pop += time.perf_counter() - start

            # Medir is_empty
            start = time.perf_counter()
            for _ in range(n):
                _ = heap.is_empty()
            t_empty += time.perf_counter() - start

        # Promediar
        times['push'].append(t_push / trials)
        times['pop'].append(t_pop / trials)
        times['len'].append(t_len / trials)
        times['is_empty'].append(t_empty / trials)

        print(f"n={n:6d} | push={times['push'][-1]:.4f}s | pop={times['pop'][-1]:.4f}s "
              f"| len={times['len'][-1]:.4f}s | is_empty={times['is_empty'][-1]:.4f}s")

    return times

def plot_heap_results(sizes, times):
    """
    Grafica tiempo medio vs. tamaño para cada operación del MaxHeap.
    """
    plt.figure(figsize=(8, 6))
    for op, vals in times.items():
        plt.plot(sizes, vals, marker='o', label=op)
    plt.xlabel("Número de elementos (n)")
    plt.ylabel("Tiempo medio (s)")
    plt.title("Benchmark de operaciones de MaxHeap")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sizes = [1000, 2000, 4000, 6000, 8000, 10000]
    times = benchmark_maxheap(sizes, trials=5)
    plot_heap_results(sizes, times)
