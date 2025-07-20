import random
import string
import time
import matplotlib.pyplot as plt

from graduacion_unal.structures.hash import HashMap

def random_strings(n, k=8):
    """Genera n strings aleatorios de longitud k."""
    letters = string.ascii_letters
    return [''.join(random.choices(letters, k=k)) for _ in range(n)]

def benchmark_hashmap(sizes, trials=5):
    """
    Para cada n en sizes, mide el tiempo medio de cada método de HashMap.
    Devuelve dicts de listas de tiempos: put, get, remove, contains, items.
    """
    times = {
        'put': [],
        'get': [],
        'remove': [],
        'contains': [],
        'items': []
    }

    for n in sizes:
        t_put = t_get = t_remove = t_contains = t_items = 0.0

        for _ in range(trials):
            keys = random_strings(n)
            values = list(range(n))

            hm = HashMap()

            # Medir put
            start = time.perf_counter()
            for k, v in zip(keys, values):
                hm.put(k, v)
            t_put += (time.perf_counter() - start)

            # Mezclar claves para get/contains/remove
            sample_keys = random.sample(keys, k=n//2)

            # Medir get
            start = time.perf_counter()
            for k in sample_keys:
                _ = hm.get(k)
            t_get += (time.perf_counter() - start)

            # Medir contains
            start = time.perf_counter()
            for k in sample_keys:
                _ = hm.contains(k)
            t_contains += (time.perf_counter() - start)

            # Medir items (iteración completa)
            start = time.perf_counter()
            for _ in hm.items():
                pass
            t_items += (time.perf_counter() - start)

            # Medir remove
            start = time.perf_counter()
            for k in sample_keys:
                _ = hm.remove(k)
            t_remove += (time.perf_counter() - start)

        # Promediar sobre trials
        times['put'].append(t_put / trials)
        times['get'].append(t_get / trials)
        times['remove'].append(t_remove / trials)
        times['contains'].append(t_contains / trials)
        times['items'].append(t_items / trials)

        print(f"n={n:6d} | put={times['put'][-1]:.4f}s | get={times['get'][-1]:.4f}s "
              f"| remove={times['remove'][-1]:.4f}s | contains={times['contains'][-1]:.4f}s "
              f"| items={times['items'][-1]:.4f}s")

    return times

def plot_results(sizes, times):
    """
    Genera un gráfico con el tiempo (eje Y) vs n (eje X) para cada método.
    """
    plt.figure(figsize=(8, 6))
    for method, t_vals in times.items():
        plt.plot(sizes, t_vals, label=method)
    plt.xlabel("Número de elementos (n)")
    plt.ylabel("Tiempo medio (s)")
    plt.title("Benchmark de métodos de HashMap")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Definir tamaños de prueba
    sizes = [1000, 2000, 4000, 6000, 8000, 10000]
    # Ejecutar benchmark
    times = benchmark_hashmap(sizes, trials=5)
    # Mostrar gráfico
    plot_results(sizes, times)
