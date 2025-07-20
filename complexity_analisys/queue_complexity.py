import random
import time
import matplotlib.pyplot as plt

from graduacion_unal.structures.queue import Queue

def random_items(n):
    """Genera una lista de n valores aleatorios."""
    return [random.random() for _ in range(n)]

def benchmark_queue(sizes, trials=5):
    """
    Para cada n en sizes, mide el tiempo medio de cada operación de Queue:
      - enqueue: insertar n elementos
      - dequeue: extraer n elementos
      - peek: mirar el frente n veces (tras llenar)
      - is_empty: comprobar n veces (tras vaciar)
      - __len__: consultar len() n veces (tras llenar)
      - iterar: recorrer toda la queue con __iter__
    Devuelve un dict con listas de tiempos medios.
    """
    times = {
        'enqueue': [],
        'dequeue': [],
        'peek': [],
        'is_empty': [],
        'len': [],
        'iterate': []
    }

    for n in sizes:
        t_enq = t_deq = t_peek = t_empty = t_len = t_iter = 0.0

        for _ in range(trials):
            data = random_items(n)

            # Medir enqueue
            q = Queue()
            start = time.perf_counter()
            for x in data:
                q.enqueue(x)
            t_enq += time.perf_counter() - start

            # Medir __len__
            start = time.perf_counter()
            for _ in range(n):
                _ = len(q)
            t_len += time.perf_counter() - start

            # Medir peek
            start = time.perf_counter()
            for _ in range(n):
                try:
                    _ = q.peek()
                except IndexError:
                    pass
            t_peek += time.perf_counter() - start

            # Medir iteración completa
            start = time.perf_counter()
            for _ in q:
                pass
            t_iter += time.perf_counter() - start

            # Medir dequeue
            start = time.perf_counter()
            while not q.is_empty():
                try:
                    q.dequeue()
                except IndexError:
                    break
            t_deq += time.perf_counter() - start

            # Medir is_empty
            start = time.perf_counter()
            for _ in range(n):
                _ = q.is_empty()
            t_empty += time.perf_counter() - start

        # Promediar sobre trials
        times['enqueue'].append(t_enq / trials)
        times['dequeue'].append(t_deq / trials)
        times['peek'].append(t_peek / trials)
        times['is_empty'].append(t_empty / trials)
        times['len'].append(t_len / trials)
        times['iterate'].append(t_iter / trials)

        print(
            f"n={n:6d} | enqueue={times['enqueue'][-1]:.4f}s | dequeue={times['dequeue'][-1]:.4f}s "
            f"| peek={times['peek'][-1]:.4f}s | is_empty={times['is_empty'][-1]:.4f}s "
            f"| len={times['len'][-1]:.4f}s | iterate={times['iterate'][-1]:.4f}s"
        )

    return times

def plot_queue_results(sizes, times):
    """
    Grafica tiempo medio vs. tamaño para cada operación de la Queue.
    """
    plt.figure(figsize=(8, 6))
    for op, vals in times.items():
        plt.plot(sizes, vals, marker='o', label=op)
    plt.xlabel("Número de elementos (n)")
    plt.ylabel("Tiempo medio (s)")
    plt.title("Benchmark de operaciones de Queue")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sizes = [1000, 2000, 4000, 6000, 8000, 10000]
    times = benchmark_queue(sizes, trials=5)
    plot_queue_results(sizes, times)
