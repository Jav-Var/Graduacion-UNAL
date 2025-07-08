import random
from typing import List, Dict, Any, Set
from graduacion_unal.models.courses_graph import CoursesGraph
from graduacion_unal.models.Courses import Course

class Schedule:
    """
    Metodo para una planificacion de semestres valida.

    Esta clase se encarga de las utilidades para la generacion de una planificacion de semestres valida.
    """

    def __init__(self):
        pass

    def tree_of_availible_courses(self, max_credits_per_semester: int, courses_graph: CoursesGraph) -> Dict[int, List[int]]:
        """
        Metodo para calcular el numero minimo de semestres necesarios para completar el plan de estudios.
        
        Implementa un "arbol" basado en los prerequisitos de los cursos. 
        
        Definimos la "altura" de la asignatura como la profundidad máxima de los prerequisitos.

        Nivel 1: Cursos sin prerequisitos.
        Nivel 2: Cursos con a lo sumo un prerequisito sin prerequisito. 
        Nivel 3: Cursos con a lo sumo un prerequisitos con un prerequisito sin prerequisito.
        
        El arbol generado debe representar las asignaturas que se pueden tomar en un semestre, por ejemplo:

        En el semestre 1 se puede tomar todas las de nivel 1.
        En el semestre 2 se puede tomar todas las de nivel 2.
        En el semestre 3 se puede tomar todas las de nivel 3.

        NOTA: Pueden excederse de los creditos permitidos por semestre, el arbol solo
        representa las asignaturas que se pueden tomar en un semestre.    
        """
        if not courses_graph:
            return {}
        
        # Obtener todos los cursos
        all_courses = courses_graph.get_all_courses()
        
        # Calcular niveles de cada curso
        course_levels = {}
        visited = set()
        
        def calculate_level(course_id: int) -> int:
            """Calcula el nivel de un curso basado en sus prerrequisitos."""
            if course_id in course_levels:
                return course_levels[course_id]
            
            if course_id in visited:
                return 0  # Evitar ciclos
            
            visited.add(course_id)
            course = courses_graph.get_course(course_id)
            
            if not course or not course.prereqs:
                course_levels[course_id] = 1
                return 1
            
            # El nivel es el máximo nivel de los prerrequisitos + 1
            max_prereq_level = 0
            for prereq_id in course.prereqs:
                prereq_level = calculate_level(prereq_id)
                max_prereq_level = max(max_prereq_level, prereq_level)
            
            course_levels[course_id] = max_prereq_level + 1
            return course_levels[course_id]
        
        # Calcular niveles para todos los cursos
        for course in all_courses:
            if course.id not in course_levels:
                calculate_level(course.id)
        
        # Organizar cursos por nivel
        tree = {}
        for course_id, level in course_levels.items():
            if level not in tree:
                tree[level] = []
            tree[level].append(course_id)
        
        return tree

    def is_valid_schedule(self, schedule: Dict[int, List[int]], courses_graph: CoursesGraph, max_credits_per_semester: int) -> Dict[str, Any]:
        """
        Metodo para verificar si una planificacion de semestres es valida. Con base a los prerequisitos y un tope de creditos por semestre.
        
        Recibe un diccionario de semestres, donde cada semestre es una lista de asignaturas.

        Ejemplo:
        {
            1: [1, 2, 3],
            2: [4, 5, 6],
        }

        Revisar que las asignaturas de cada semestre sean validas, es decir, que se cumplan los prerequisitos y que el numero de creditos no exceda el maximo permitido por semestre.
        """
        if not courses_graph:
            return {
                "valid": False,
                "errors": ["Grafo de cursos no cargado"]
            }
        
        errors = []
        completed_courses = set()
        
        # Verificar cada semestre en orden
        for semester in sorted(schedule.keys()):
            semester_courses = schedule[semester]
            
            # Verificar créditos del semestre
            semester_credits = 0
            for course_id in semester_courses:
                course = courses_graph.get_course(course_id)
                if course:
                    semester_credits += course.credits
                else:
                    errors.append(f"Curso {course_id} no encontrado en el semestre {semester}")
            
            if semester_credits > max_credits_per_semester:
                errors.append(f"Semestre {semester} excede el límite de créditos: {semester_credits} > {max_credits_per_semester}")
            
            # Verificar prerrequisitos
            for course_id in semester_courses:
                course = courses_graph.get_course(course_id)
                if course:
                    for prereq_id in course.prereqs:
                        if prereq_id not in completed_courses:
                            errors.append(f"Curso {course_id} en semestre {semester} requiere prerrequisito {prereq_id} que no ha sido completado")
            
            # Agregar cursos del semestre a completados
            completed_courses.update(semester_courses)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "total_semesters": len(schedule),
            "total_courses": sum(len(courses) for courses in schedule.values())
        }

    def random_schedule(self, max_credits_per_semester: int, courses_graph: CoursesGraph) -> Dict[int, List[int]]:
        """
        Metodo para generar una planificacion de semestres aleatoria con un maximo de creditos por semestre.
        
        Generar el grafo de cursos y seleccionar aleatoriamente entre las asignaturas que se pueden tomar en un semestre, que a lo mas sumen el maximo de creditos por semestre.
        
        Retorna una programacion de semestres en el siguiente formato:
        {
            1: [1, 2, 3], ## materias seleccionadas para tomar en el semestre 1
            2: [4, 5, 6], ## materias seleccionadas para tomar en el semestre 2
            ...
            n: [i, j, k] ## materias seleccionadas para tomar en el semestre n
        }
        """
        if not courses_graph:
            return {}
        
        # Obtener el árbol de cursos disponibles
        course_tree = self.tree_of_availible_courses(max_credits_per_semester, courses_graph)
        
        schedule = {}
        completed_courses = set()
        current_semester = 1
        
        # Procesar cada nivel del árbol
        for level in sorted(course_tree.keys()):
            available_courses = course_tree[level]
            
            # Filtrar cursos que ya están completados
            available_courses = [course_id for course_id in available_courses if course_id not in completed_courses]
            
            if not available_courses:
                continue
            
            # Seleccionar cursos aleatoriamente respetando el límite de créditos
            selected_courses = []
            current_credits = 0
            
            # Mezclar cursos disponibles
            random.shuffle(available_courses)
            
            for course_id in available_courses:
                course = courses_graph.get_course(course_id)
                if course and (current_credits + course.credits) <= max_credits_per_semester:
                    selected_courses.append(course_id)
                    current_credits += course.credits
            
            if selected_courses:
                schedule[current_semester] = selected_courses
                completed_courses.update(selected_courses)
                current_semester += 1
        
        return schedule

    def max_greedy_schedule(self, max_credits_per_semester: int, courses_graph: CoursesGraph) -> Dict[int, List[int]]:
        """
        Genera una planificación de semestres usando un algoritmo greedy que maximiza los créditos por semestre.
        
        Args:
            max_credits_per_semester: Límite de créditos por semestre
            courses_graph: Grafo de cursos
            
        Returns:
            Diccionario con la planificación de semestres
        """
        if not courses_graph:
            return {}
        
        # Obtener el árbol de cursos disponibles
        course_tree = self.tree_of_availible_courses(max_credits_per_semester, courses_graph)
        
        schedule = {}
        completed_courses = set()
        current_semester = 1
        
        # Procesar cada nivel del árbol
        for level in sorted(course_tree.keys()):
            available_courses = course_tree[level]
            
            # Filtrar cursos que ya están completados
            available_courses = [course_id for course_id in available_courses if course_id not in completed_courses]
            
            if not available_courses:
                continue
            
            # Ordenar cursos por créditos (mayor a menor) para maximizar créditos por semestre
            course_credits = []
            for course_id in available_courses:
                course = courses_graph.get_course(course_id)
                if course:
                    course_credits.append((course_id, course.credits))
            
            # Ordenar por créditos descendente
            course_credits.sort(key=lambda x: x[1], reverse=True)
            
            # Seleccionar cursos greedy
            selected_courses = []
            current_credits = 0
            
            for course_id, credits in course_credits:
                if (current_credits + credits) <= max_credits_per_semester:
                    selected_courses.append(course_id)
                    current_credits += credits
            
            if selected_courses:
                schedule[current_semester] = selected_courses
                completed_courses.update(selected_courses)
                current_semester += 1
        
        return schedule