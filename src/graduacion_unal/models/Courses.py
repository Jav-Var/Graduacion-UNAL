# planner.py

# Courses.py

import json
from typing import List
import argparse
from graduacion_unal.structures.hash import HashMap    # <- tu HashMap
from graduacion_unal.structures.queue_ds import Queue    # <- tu Queue con enqueue/is_empty

# ... resto de tu código ...
              # tu implementación renombrada en src/queue_ds.py

class Course:
    def __init__(self, id: int, prereqs: List[int]) -> None:
        self.id = id
        self.prereqs = prereqs
        self.in_degree = len(prereqs)
        self.adjacent: List[int] = []  # cursos dependientes

def load_courses(path: str) -> List[Course]:
    """
    Lee un JSON con:
    [
      { "id": 101, "prereqs": [] },
      { "id": 102, "prereqs": [101] },
      ...
    ]
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [Course(item['id'], item['prereqs']) for item in data]

def build_graph(courses: List[Course]) -> HashMap:
    """
    Construye un HashMap que mapea id → Course y llena 'adjacent'.
    """
    mapa = HashMap()
    for c in courses:
        mapa.put(c.id, c)
    for c in courses:
        for pre in c.prereqs:
            prereq_course: Course = mapa.get(pre)
            prereq_course.adjacent.append(c.id)
    return mapa

def plan_semesters(mapa: HashMap, max_per_sem: int) -> List[List[int]]:
    """
    Orden topológico con límite por semestre.
    Devuelve lista de semestres (listas de IDs).
    """
    q = Queue()
    # Encolar todos los de in_degree 0
    for course_id, course in mapa.items():
        if course.in_degree == 0:
            q.enqueue(course_id)

    result: List[List[int]] = []

    while not q.is_empty():
        semestre: List[int] = []
        for _ in range(max_per_sem):
            if q.is_empty():
                break
            cid = q.dequeue()
            semestre.append(cid)
            course = mapa.get(cid)
            for neigh_id in course.adjacent:
                neigh = mapa.get(neigh_id)
                neigh.in_degree -= 1
                if neigh.in_degree == 0:
                    q.enqueue(neigh_id)
        result.append(semestre)

    total = sum(len(s) for s in result)
    if total != mapa.size:
        raise ValueError("Ciclo detectado o cursos faltantes")
    return result

def main():
    parser = argparse.ArgumentParser(description="Planificador de semestres UNAL")
    parser.add_argument("-i", "--input",  required=True,
                        help="Ruta al JSON de cursos")
    parser.add_argument("-m", "--max-per-sem", type=int, default=6,
                        help="Máximo de cursos por semestre")
    parser.add_argument("-o", "--output",
                        help="Archivo JSON de salida")
    args = parser.parse_args()

    courses = load_courses(args.input)
    mapa = build_graph(courses)
    plan = plan_semesters(mapa, args.max_per_sem)

    for idx, sem in enumerate(plan, start=1):
        print(f"Semestre {idx}: {sem}")
    print(f"Semestres totales: {len(plan)}")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
