from typing import List, Optional

class User:
    """
    Modelo que representa un estudiante/usuario del sistema.
    
    Attributes:
        id: Identificador único del usuario
        name: Nombre completo del estudiante
        student_id: Código estudiantil
        program: Programa académico (ej: "Ingeniería de Sistemas")
        semester: Semestre actual del estudiante
        completed_courses: Lista de IDs de cursos completados
        current_courses: Lista de IDs de cursos en los que está inscrito actualmente
        total_credits: Total de créditos aprobados
        max_credits_per_semester: Límite de créditos por semestre
    """
    
    def __init__(self, 
                 id: int, 
                 name: str, 
                 student_id: str, 
                 program: str,
                 semester: int = 1,
                 completed_courses: List[int] = None,
                 current_courses: List[int] = None,
                 total_credits: int = 0,
                 max_credits_per_semester: int = 18):
        self.id = id
        self.name = name
        self.student_id = student_id
        self.program = program
        self.semester = semester
        self.completed_courses = completed_courses or []
        self.current_courses = current_courses or []
        self.total_credits = total_credits
        self.max_credits_per_semester = max_credits_per_semester
    
    def add_completed_course(self, course_id: int) -> bool:
        """
        Añade un curso a la lista de cursos completados.
        
        Args:
            course_id: ID del curso completado
            
        Returns:
            True si se añadió exitosamente, False si ya existía
        """
        if course_id not in self.completed_courses:
            self.completed_courses.append(course_id)
            return True
        return False
    
    def remove_completed_course(self, course_id: int) -> bool:
        """
        Remueve un curso de la lista de cursos completados.
        
        Args:
            course_id: ID del curso a remover
            
        Returns:
            True si se removió exitosamente, False si no existía
        """
        if course_id in self.completed_courses:
            self.completed_courses.remove(course_id)
            return True
        return False
    
    def add_current_course(self, course_id: int) -> bool:
        """
        Añade un curso a la lista de cursos actuales.
        
        Args:
            course_id: ID del curso actual
            
        Returns:
            True si se añadió exitosamente, False si ya existía
        """
        if course_id not in self.current_courses:
            self.current_courses.append(course_id)
            return True
        return False
    
    def remove_current_course(self, course_id: int) -> bool:
        """
        Remueve un curso de la lista de cursos actuales.
        
        Args:
            course_id: ID del curso a remover
            
        Returns:
            True si se removió exitosamente, False si no existía
        """
        if course_id in self.current_courses:
            self.current_courses.remove(course_id)
            return True
        return False
    
    def has_completed_course(self, course_id: int) -> bool:
        """
        Verifica si el usuario ha completado un curso específico.
        
        Args:
            course_id: ID del curso a verificar
            
        Returns:
            True si el curso está completado, False en caso contrario
        """
        return course_id in self.completed_courses
    
    def is_enrolled_in_course(self, course_id: int) -> bool:
        """
        Verifica si el usuario está inscrito en un curso específico.
        
        Args:
            course_id: ID del curso a verificar
            
        Returns:
            True si está inscrito, False en caso contrario
        """
        return course_id in self.current_courses
    
    def get_progress_percentage(self, total_courses: int) -> float:
        """
        Calcula el porcentaje de progreso basado en cursos completados.
        
        Args:
            total_courses: Número total de cursos en el programa
            
        Returns:
            Porcentaje de progreso (0.0 a 100.0)
        """
        if total_courses == 0:
            return 0.0
        return (len(self.completed_courses) / total_courses) * 100.0
    
    def can_take_course(self, course_credits: int) -> bool:
        """
        Verifica si el usuario puede tomar un curso basado en su límite de créditos.
        
        Args:
            course_credits: Créditos del curso a verificar
            
        Returns:
            True si puede tomar el curso, False en caso contrario
        """
        current_credits = sum(self.current_courses)  # Simplificado, debería obtener créditos reales
        return (current_credits + course_credits) <= self.max_credits_per_semester
    
    def advance_semester(self) -> None:
        """
        Avanza al siguiente semestre.
        """
        self.semester += 1
    
    def get_available_credits(self) -> int:
        """
        Calcula los créditos disponibles para el semestre actual.
        
        Returns:
            Número de créditos disponibles
        """
        current_credits = sum(self.current_courses)  # Simplificado
        return max(0, self.max_credits_per_semester - current_credits)
    
    def __str__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', student_id='{self.student_id}', program='{self.program}', semester={self.semester})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
