import random
import time
import matplotlib.pyplot as plt

from graduacion_unal.structures.disjoint_sets import DisjointSets

def benchmark_disjoint_sets(sizes, trials=5):
    """
    Para cada n en sizes (tamaño inicial de DisjointSets), mide el tiempo medio de:
      - __init__: inicializar la estructura
      - union: hacer n uniones sobre pares aleatorios
      - find: hacer n búsquedas de representante sobre elementos aleatorios
      - connected: hacer n comprobaciones de conexión entre pares aleatorios
      - get_set_size: hacer n consultas de tamaño de conjunto sobre elementos aleatorios
      - get_all_sets: obtener todos los conjuntos
      - get_num_sets: obtener el número de conjuntos
      - reset: reiniciar la estructura
    Devuelve un dict con listas de tiempos medios por operación.
    """
    times = {
        'init': [],
        'union': [],
        'find': [],
        'connected': [],
        'get_set_size': [],
        'get_all_sets': [],
        'get_num_sets': [],
        'reset': []
    }

    for n in sizes:
        t_init = t_union = t_find = t_conn = t_size = t_all = t_num = t_reset = 0.0

        for _ in range(trials):
            # __init__
            start = time.perf_counter()
            ds = DisjointSets(n)
            t_init += time.perf_counter() - start

            # Preparar pares y elems aleatorios
            pairs = [(random.randrange(n), random.randrange(n)) for _ in range(n)]
            elems = [random.randrange(n) for _ in range(n)]

            # union
            start = time.perf_counter()
            for x, y in pairs:
                ds.union(x, y)
            t_union += time.perf_counter() - start

            # find
            start = time.perf_counter()
            for x in elems:
                ds.find(x)
            t_find += time.perf_counter() - start

            # connected
            start = time.perf_counter()
            for x, y in pairs:
                ds.connected(x, y)
            t_conn += time.perf_counter() - start

            # get_set_size
            start = time.perf_counter()
            for x in elems:
                ds.get_set_size(x)
            t_size += time.perf_counter() - start

            # get_all_sets
            start = time.perf_counter()
            ds.get_all_sets()
            t_all += time.perf_counter() - start

            # get_num_sets
            start = time.perf_counter()
            ds.get_num_sets()
            t_num += time.perf_counter() - start

            # reset
            start = time.perf_counter()
            ds.reset()
            t_reset += time.perf_counter() - start

        # Promediar
        times['init'].append(t_init / trials)
        times['union'].append(t_union / trials)
        times['find'].append(t_find / trials)
        times['connected'].append(t_conn / trials)
        times['get_set_size'].append(t_size / trials)
        times['get_all_sets'].append(t_all / trials)
        times['get_num_sets'].append(t_num / trials)
        times['reset'].append(t_reset / trials)

        print(
            f"n={n:6d} | init={times['init'][-1]:.4f}s | union={times['union'][-1]:.4f}s "
            f"| find={times['find'][-1]:.4f}s | connected={times['connected'][-1]:.4f}s\n"
            f"          get_set_size={times['get_set_size'][-1]:.4f}s | get_all_sets={times['get_all_sets'][-1]:.4f}s "
            f"| get_num_sets={times['get_num_sets'][-1]:.4f}s | reset={times['reset'][-1]:.4f}s"
        )

    return times

def plot_disjoint_sets_results(sizes, times):
    """
    Grafica tiempo medio vs. tamaño para cada operación de DisjointSets.
    """
    plt.figure(figsize=(10, 6))
    for op, vals in times.items():
        plt.plot(sizes, vals, marker='o', label=op)
    plt.xlabel("Número de elementos iniciales (n)")
    plt.ylabel("Tiempo medio (s)")
    plt.title("Benchmark de operaciones de DisjointSets")
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sizes = [1000, 2000, 4000, 8000, 16000]
    times = benchmark_disjoint_sets(sizes, trials=5)
    plot_disjoint_sets_results(sizes, times)
