import random
import time
import matplotlib.pyplot as plt

from graduacion_unal.models.courses_graph import CoursesGraph
from graduacion_unal.models.Courses import Course

def make_random_courses(n, max_prereqs=3):
    courses = []
    for i in range(n):
        k = random.randint(0, min(max_prereqs, i))
        prereqs = random.sample(range(i), k) if i > 0 else []
        course = Course(i, prereqs)
        try:
            course.name = f"Course{i}"
        except AttributeError:
            pass
        courses.append(course)
    return courses

def benchmark_courses_graph(sizes, trials=5):
    ops = [
        'init','build','get_course','all_courses','no_prereq','ready',
        'add_node','remove_node','add_edge','remove_edge','neighbors','str'
    ]
    times = {op: [] for op in ops}

    for n in sizes:
        accum = {op: 0.0 for op in ops}
        for _ in range(trials):
            courses    = make_random_courses(n)
            sample_ids = random.choices(range(n), k=n)
            half_ids   = random.sample(range(n), k=n//2)
            new_courses= make_random_courses(n//2, max_prereqs=0)
            rem_ids    = random.sample(range(n), k=n//2)

            # init
            start = time.perf_counter()
            graph = CoursesGraph()
            accum['init'] += time.perf_counter() - start

            # build_from_courses
            start = time.perf_counter()
            graph.build_from_courses(courses)
            accum['build'] += time.perf_counter() - start

            # get_course
            start = time.perf_counter()
            for cid in sample_ids:
                _ = graph.get_course(cid)
            accum['get_course'] += time.perf_counter() - start

            # get_all_courses
            start = time.perf_counter()
            _ = graph.get_all_courses()
            accum['all_courses'] += time.perf_counter() - start

            # get_courses_without_prerequisites
            start = time.perf_counter()
            _ = graph.get_courses_without_prerequisites()
            accum['no_prereq'] += time.perf_counter() - start

            # get_ready_courses
            start = time.perf_counter()
            _ = graph.get_ready_courses(half_ids)
            accum['ready'] += time.perf_counter() - start

            # add_node
            start = time.perf_counter()
            for c in new_courses:
                graph.add_node(c)
            accum['add_node'] += time.perf_counter() - start

            # remove_node
            start = time.perf_counter()
            for cid in rem_ids:
                graph.remove_node(cid)
            accum['remove_node'] += time.perf_counter() - start

            # add_edge (skip ciclos)
            start = time.perf_counter()
            for i in range(len(half_ids) - 1):
                try:
                    graph.add_vertex(half_ids[i], half_ids[i + 1])
                except ValueError:
                    # Ya existía o creaba ciclo: lo ignoramos
                    pass
            accum['add_edge'] += time.perf_counter() - start

            # remove_edge (ignoramos si no existe)
            start = time.perf_counter()
            for i in range(len(half_ids) - 1):
                graph.remove_edge(half_ids[i], half_ids[i + 1])
            accum['remove_edge'] += time.perf_counter() - start

            # get_neighbors
            start = time.perf_counter()
            for cid in sample_ids:
                _ = graph.get_neighbors(cid)
            accum['neighbors'] += time.perf_counter() - start

            # __str__
            start = time.perf_counter()
            _ = str(graph)
            accum['str'] += time.perf_counter() - start

        # Promediar
        for op in ops:
            times[op].append(accum[op] / trials)

        print(
            f"n={n:5d} | build={times['build'][-1]:.4f}s | get={times['get_course'][-1]:.4f}s"
            f" | all={times['all_courses'][-1]:.4f}s | no_pr={times['no_prereq'][-1]:.4f}s"
            f" | ready={times['ready'][-1]:.4f}s"
        )

    return times

def plot_courses_graph_results(sizes, times):
    plt.figure(figsize=(12, 8))
    for op, vals in times.items():
        plt.plot(sizes, vals, marker='o', label=op)
    plt.xlabel("Número de cursos iniciales (n)")
    plt.ylabel("Tiempo medio (s)")
    plt.title("Benchmark de operaciones de CoursesGraph")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sizes = [500, 1000, 2000, 4000]
    times = benchmark_courses_graph(sizes, trials=3)
    plot_courses_graph_results(sizes, times)

