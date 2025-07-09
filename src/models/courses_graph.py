from structures.hash import HashMap
from structures.disjoint_sets import DisjointSets
from models.Courses import Course
from typing import List, Optional


class CoursesGraph:
    """
    Clase que representa un grafo dirigido de materias (Nodos), y prerrequisitos (Aristas)

    Atributos:
        adjacency_list: HashMap que almacena la lista de "dependencias" del grafo.
        number_nodes: Número de nodos(prerrequisitos) en el grafo.
        courses_map: HashMap que mapea ID de curso -> objeto Course.
    """

    def __init__(self):
        self.adjacency_list = HashMap()
        self.courses_map = HashMap()
        self.number_nodes: int = 0

    def build_from_courses(self, courses: List[Course]) -> None:
        """
        Construye el grafo a partir de una lista de cursos.
        
        Args:
            courses: Lista de objetos Course
        """
        # Limpiar el grafo actual
        self.adjacency_list = HashMap()
        self.courses_map = HashMap()
        self.number_nodes = 0
        
        # Añadir todos los cursos al mapa
        for course in courses:
            self.courses_map.put(course.id, course)
            self.adjacency_list.put(course.id, [])
            self.number_nodes += 1
        
        # Construir las relaciones de dependencia
        for course in courses:
            for prereq_id in course.prereqs:
                # Verificar que el prerrequisito existe
                if not self.courses_map.contains(prereq_id):
                    raise ValueError(f"Prerrequisito {prereq_id} no encontrado para el curso {course.id}")
                
                # Añadir la relación: prereq_id -> course.id
                prereq_course = self.courses_map.get(prereq_id)
                prereq_course.add_dependent_course(course.id)
                
                # Actualizar la lista de adyacencia
                current_adjacent = self.adjacency_list.get(prereq_id)
                if course.id not in current_adjacent:
                    current_adjacent.append(course.id)
                    self.adjacency_list.put(prereq_id, current_adjacent)
    
    def get_course(self, course_id: int) -> Optional[Course]:
        """
        Obtiene un curso por su ID.
        
        Args:
            course_id: ID del curso
            
        Returns:
            Objeto Course si existe, None en caso contrario
        """
        try:
            return self.courses_map.get(course_id)
        except KeyError:
            return None
    
    def get_all_courses(self) -> List[Course]:
        """
        Obtiene todos los cursos del grafo.
        
        Returns:
            Lista de todos los objetos Course
        """
        courses = []
        for course_id, course in self.courses_map.items():
            courses.append(course)
        return courses
    
    def get_courses_without_prerequisites(self) -> List[Course]:
        """
        Obtiene todos los cursos que no tienen prerrequisitos.
        
        Returns:
            Lista de cursos sin prerrequisitos
        """
        courses_without_prereqs = []
        for course_id, course in self.courses_map.items():
            if not course.has_prerequisites():
                courses_without_prereqs.append(course)
        return courses_without_prereqs
    
    def get_ready_courses(self, completed_courses: List[int]) -> List[Course]:
        """
        Obtiene todos los cursos que pueden ser tomados dado los cursos completados.
        
        Args:
            completed_courses: Lista de IDs de cursos completados
            
        Returns:
            Lista de cursos que pueden ser tomados
        """
        ready_courses = []
        for course_id, course in self.courses_map.items():
            if course_id not in completed_courses and course.is_ready_to_take(completed_courses):
                ready_courses.append(course)
        return ready_courses

    def add_node(self, course: Course) -> None:
        """
        Añade un nodo (curso) al grafo.
        
        Args:
            course: Objeto Course a añadir
        """
        if not self.courses_map.contains(course.id):
            self.courses_map.put(course.id, course)
            self.adjacency_list.put(course.id, [])
            self.number_nodes += 1
            
            # Actualizar las relaciones de dependencia
            for prereq_id in course.prereqs:
                if self.courses_map.contains(prereq_id):
                    prereq_course = self.courses_map.get(prereq_id)
                    prereq_course.add_dependent_course(course.id)
                    
                    current_adjacent = self.adjacency_list.get(prereq_id)
                    if course.id not in current_adjacent:
                        current_adjacent.append(course.id)
                        self.adjacency_list.put(prereq_id, current_adjacent)

    def remove_node(self, course_id: int) -> bool:
        """
        Elimina un nodo del grafo, y todas sus aristas adjacentes.
        
        Args:
            course_id: ID del curso a eliminar
            
        Returns:
            True si se eliminó exitosamente, False si no existía
        """
        if not self.courses_map.contains(course_id):
            return False
        
        course = self.courses_map.get(course_id)
        
        # Remover de la lista de adyacencia
        self.adjacency_list.remove(course_id)
        
        # Remover de los cursos dependientes
        for dependent_id in course.adjacent:
            if self.courses_map.contains(dependent_id):
                dependent_course = self.courses_map.get(dependent_id)
                dependent_course.prereqs.remove(course_id)
                dependent_course.in_degree = len(dependent_course.prereqs)
        
        # Remover del mapa de cursos
        self.courses_map.remove(course_id)
        self.number_nodes -= 1
        
        return True

    def add_vertex(self, prereq_id: int, course_id: int) -> bool:
        """
        Añade una arista al grafo (prerrequisito -> materia).
        Detecta si la arista añadida genera un ciclo en el grafo.
        
        Args:
            prereq_id: ID del curso prerrequisito
            course_id: ID del curso dependiente
            
        Returns:
            True si se añadió exitosamente, False si ya existía
            
        Raises:
            ValueError: Si se detecta un ciclo
        """
        # Verificar que ambos cursos existen
        if not self.courses_map.contains(prereq_id) or not self.courses_map.contains(course_id):
            return False
        
        course = self.courses_map.get(course_id)
        
        # Verificar si la relación ya existe
        if prereq_id in course.prereqs:
            return False
        
        # Añadir la relación
        course.prereqs.append(prereq_id)
        course.in_degree = len(course.prereqs)
        
        prereq_course = self.courses_map.get(prereq_id)
        prereq_course.add_dependent_course(course_id)
        
        # Actualizar lista de adyacencia
        current_adjacent = self.adjacency_list.get(prereq_id)
        if course_id not in current_adjacent:
            current_adjacent.append(course_id)
            self.adjacency_list.put(prereq_id, current_adjacent)
        
        # Verificar si se creó un ciclo
        if self._has_cycle():
            # Revertir el cambio
            course.prereqs.remove(prereq_id)
            course.in_degree = len(course.prereqs)
            prereq_course.remove_dependent_course(course_id)
            current_adjacent.remove(course_id)
            self.adjacency_list.put(prereq_id, current_adjacent)
            raise ValueError("No se puede añadir la relación: se detectó un ciclo")
        
        return True

    def remove_edge(self, prereq_id: int, course_id: int) -> bool:
        """
        Elimina una arista (Prerrequisito).
        
        Args:
            prereq_id: ID del curso prerrequisito
            course_id: ID del curso dependiente
            
        Returns:
            True si se eliminó exitosamente, False si no existía
        """
        if not self.courses_map.contains(course_id):
            return False
        
        course = self.courses_map.get(course_id)
        
        if prereq_id not in course.prereqs:
            return False
        
        # Remover la relación
        course.prereqs.remove(prereq_id)
        course.in_degree = len(course.prereqs)
        
        if self.courses_map.contains(prereq_id):
            prereq_course = self.courses_map.get(prereq_id)
            prereq_course.remove_dependent_course(course_id)
        
        # Actualizar lista de adyacencia
        current_adjacent = self.adjacency_list.get(prereq_id)
        if course_id in current_adjacent:
            current_adjacent.remove(course_id)
            self.adjacency_list.put(prereq_id, current_adjacent)
        
        return True

    def _has_cycle(self) -> bool:
        """
        Detecta si el grafo tiene ciclos usando DFS.
        
        Returns:
            True si hay un ciclo, False en caso contrario
        """
        if self.number_nodes == 0:
            return False
        
        # Obtener todos los IDs de cursos
        course_ids = list(self.courses_map.keys())
        if not course_ids:
            return False
        
        # Para grafos dirigidos, usamos DFS simple
        visited = set()
        rec_stack = set()
        
        def dfs(course_id: int) -> bool:
            visited.add(course_id)
            rec_stack.add(course_id)
            
            for neighbor_id in self.get_neighbors(course_id):
                if neighbor_id not in visited:
                    if dfs(neighbor_id):
                        return True
                elif neighbor_id in rec_stack:
                    # Ciclo detectado: encontramos un back edge
                    return True
            
            rec_stack.remove(course_id)
            return False
        
        for course_id in course_ids:
            if course_id not in visited:
                if dfs(course_id):
                    return True
        
        return False

    def get_neighbors(self, course_id: int) -> List[int]:
        """
        Retorna una lista de los sucesores de un nodo (Nodos que dependen de un curso).
        
        Args:
            course_id: ID del curso
            
        Returns:
            Lista de IDs de cursos dependientes
        """
        try:
            return list(self.adjacency_list.get(course_id) or [])
        except KeyError:
            return []
    
    def __str__(self) -> str:
        lines = []
        for course_id, course in self.courses_map.items():
            neighbors = self.get_neighbors(course_id)
            lines.append(f"{course_id} ({course.name}) -> {neighbors}")
        return "\n".join(lines)