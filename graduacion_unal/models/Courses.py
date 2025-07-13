import json
from typing import List
import argparse
from graduacion_unal.structures.hash import HashMap  
from graduacion_unal.structures.queue import Queue   


### PARA LA PROXIMA ENTREGA
## PARA MANEJAR CURSOS Y GRAFOS DE CURSOS
## NO SE UTILIZA EN LA ACTUAL VERSION


class Course:
    """
    Modelo que representa una asignatura/curso en el plan de estudios.
    
    Atributos:
        id: Identificador único del curso
        name: Nombre del curso (opcional)
        credits: Número de créditos del curso (opcional)
        prereqs: Lista de IDs de cursos que son prerrequisitos
        in_degree: Número de prerrequisitos (calculado automáticamente)
        adjacent: Lista de IDs de cursos que dependen de este curso
    """
    
    def __init__(self, id: int, prereqs: List[int], name: str = "", credits: int = 0) -> None:
        self.id = id
        self.name = name
        self.credits = credits
        self.prereqs = prereqs
        self.in_degree = len(prereqs)
        self.adjacent: List[int] = []  # cursos dependientes
    
    def add_dependent_course(self, course_id: int) -> None:
        """
        Añade un curso que depende de este curso.
        
        Args:
            course_id: ID del curso dependiente
        """
        if course_id not in self.adjacent:
            self.adjacent.append(course_id)
    
    def remove_dependent_course(self, course_id: int) -> bool:
        """
        Remueve un curso dependiente.
        
        Args:
            course_id: ID del curso dependiente a remover
            
        Returns:
            True si se removió, False si no existía
        """
        if course_id in self.adjacent:
            self.adjacent.remove(course_id)
            return True
        return False
    
    def has_prerequisites(self) -> bool:
        """
        Verifica si el curso tiene prerrequisitos.
        
        Returns:
            True si tiene prerrequisitos, False en caso contrario
        """
        return len(self.prereqs) > 0
    
    def is_ready_to_take(self, completed_courses: List[int]) -> bool:
        """
        Verifica si el curso puede ser tomado dado los cursos completados.
        
        Args:
            completed_courses: Lista de IDs de cursos completados
            
        Returns:
            True si se pueden tomar todos los prerrequisitos, False en caso contrario
        """
        return all(prereq in completed_courses for prereq in self.prereqs)
    
    def __str__(self) -> str:
        return f"Course(id={self.id}, name='{self.name}', credits={self.credits}, prereqs={self.prereqs})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Course):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)

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
