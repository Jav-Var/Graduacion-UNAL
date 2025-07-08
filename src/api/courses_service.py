from typing import List, Dict, Any, Optional
from models.Courses import Course
from adapters.courses_adapter import CoursesAdapter

class CoursesService:
    """
    Servicio de API para manejar la lógica de negocio de cursos.
    Implementa la separación entre el modelo y la interfaz.
    """
    
    def __init__(self):
        self.graph: Optional[CoursesGraph] = None
        self.adapter = CoursesAdapter()
    
    def load_graph_from_json(self, json_path: str) -> Dict[str, Any]:
        """
        Carga el grafo desde un archivo JSON.
        
        Args:
            json_path: Ruta al archivo JSON
            
        Returns:
            Diccionario con información del resultado de la carga
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            json.JSONDecodeError: Si el JSON está mal formateado
            ValueError: Si hay errores en los datos
        """
        try:
            self.graph = CoursesGraph()
            self.graph.initialize_graph(json_path)
            
            return {
                "success": True,
                "message": "Grafo cargado exitosamente",
                "courses_count": self.graph.number_nodes,
                "file_path": json_path
            }
            
        except FileNotFoundError as e:
            return {
                "success": False,
                "error": "FILE_NOT_FOUND",
                "message": f"No se encontró el archivo: {json_path}",
                "details": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": "LOAD_ERROR",
                "message": f"Error al cargar el grafo: {str(e)}",
                "details": str(e)
            }
    
    def get_all_courses(self) -> Dict[str, Any]:
        """
        Obtiene todos los cursos del grafo.
        
        Returns:
            Diccionario con la lista de cursos
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            courses = self.graph.get_all_courses()
            courses_data = []
            
            for course in courses:
                courses_data.append({
                    "id": course.id,
                    "name": course.name,
                    "credits": course.credits,
                    "prereqs": course.prereqs,
                    "in_degree": course.in_degree,
                    "adjacent": course.adjacent
                })
            
            return {
                "success": True,
                "courses": courses_data,
                "total_count": len(courses_data)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "RETRIEVAL_ERROR",
                "message": f"Error al obtener los cursos: {str(e)}",
                "details": str(e)
            }
    
    def get_course_by_id(self, course_id: int) -> Dict[str, Any]:
        """
        Obtiene un curso específico por su ID.
        
        Args:
            course_id: ID del curso
            
        Returns:
            Diccionario con la información del curso
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            course = self.graph.get_course(course_id)
            
            if not course:
                return {
                    "success": False,
                    "error": "COURSE_NOT_FOUND",
                    "message": f"No se encontró el curso con ID: {course_id}"
                }
            
            return {
                "success": True,
                "course": {
                    "id": course.id,
                    "name": course.name,
                    "credits": course.credits,
                    "prereqs": course.prereqs,
                    "in_degree": course.in_degree,
                    "adjacent": course.adjacent
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "RETRIEVAL_ERROR",
                "message": f"Error al obtener el curso: {str(e)}",
                "details": str(e)
            }
    
    def get_courses_without_prerequisites(self) -> Dict[str, Any]:
        """
        Obtiene todos los cursos que no tienen prerrequisitos.
        
        Returns:
            Diccionario con la lista de cursos sin prerrequisitos
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            courses = self.graph.get_courses_without_prerequisites()
            courses_data = []
            
            for course in courses:
                courses_data.append({
                    "id": course.id,
                    "name": course.name,
                    "credits": course.credits
                })
            
            return {
                "success": True,
                "courses": courses_data,
                "total_count": len(courses_data)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "RETRIEVAL_ERROR",
                "message": f"Error al obtener los cursos sin prerrequisitos: {str(e)}",
                "details": str(e)
            }
    
    def get_ready_courses(self, completed_courses: List[int]) -> Dict[str, Any]:
        """
        Obtiene los cursos que pueden ser tomados dado los cursos completados.
        
        Args:
            completed_courses: Lista de IDs de cursos completados
            
        Returns:
            Diccionario con la lista de cursos listos para tomar
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            courses = self.graph.get_ready_courses(completed_courses)
            courses_data = []
            
            for course in courses:
                courses_data.append({
                    "id": course.id,
                    "name": course.name,
                    "credits": course.credits,
                    "prereqs": course.prereqs
                })
            
            return {
                "success": True,
                "courses": courses_data,
                "total_count": len(courses_data),
                "completed_courses": completed_courses
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "RETRIEVAL_ERROR",
                "message": f"Error al obtener los cursos listos: {str(e)}",
                "details": str(e)
            }
    
    def add_course(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Añade un nuevo curso al grafo.
        
        Args:
            course_data: Diccionario con los datos del curso
            
        Returns:
            Diccionario con el resultado de la operación
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            # Validar datos del curso
            if not self.adapter.validate_course_data(course_data):
                return {
                    "success": False,
                    "error": "INVALID_DATA",
                    "message": "Los datos del curso no son válidos"
                }
            
            # Crear el curso
            course = self.adapter._create_course_from_data(course_data)
            
            # Añadir al grafo
            self.graph.add_node(course)
            
            return {
                "success": True,
                "message": f"Curso '{course.name}' añadido exitosamente",
                "course_id": course.id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "ADD_ERROR",
                "message": f"Error al añadir el curso: {str(e)}",
                "details": str(e)
            }
    
    def remove_course(self, course_id: int) -> Dict[str, Any]:
        """
        Elimina un curso del grafo.
        
        Args:
            course_id: ID del curso a eliminar
            
        Returns:
            Diccionario con el resultado de la operación
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            # Obtener información del curso antes de eliminarlo
            course = self.graph.get_course(course_id)
            if not course:
                return {
                    "success": False,
                    "error": "COURSE_NOT_FOUND",
                    "message": f"No se encontró el curso con ID: {course_id}"
                }
            
            course_name = course.name
            
            # Eliminar el curso
            success = self.graph.remove_node(course_id)
            
            if success:
                return {
                    "success": True,
                    "message": f"Curso '{course_name}' eliminado exitosamente",
                    "course_id": course_id
                }
            else:
                return {
                    "success": False,
                    "error": "REMOVE_ERROR",
                    "message": f"No se pudo eliminar el curso con ID: {course_id}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": "REMOVE_ERROR",
                "message": f"Error al eliminar el curso: {str(e)}",
                "details": str(e)
            }
    
    def add_prerequisite(self, prereq_id: int, course_id: int) -> Dict[str, Any]:
        """
        Añade un prerrequisito a un curso.
        
        Args:
            prereq_id: ID del curso prerrequisito
            course_id: ID del curso dependiente
            
        Returns:
            Diccionario con el resultado de la operación
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            success = self.graph.add_vertex(prereq_id, course_id)
            
            if success:
                return {
                    "success": True,
                    "message": f"Prerrequisito {prereq_id} añadido al curso {course_id}",
                    "prereq_id": prereq_id,
                    "course_id": course_id
                }
            else:
                return {
                    "success": False,
                    "error": "ADD_PREREQ_ERROR",
                    "message": f"No se pudo añadir el prerrequisito {prereq_id} al curso {course_id}"
                }
                
        except ValueError as e:
            return {
                "success": False,
                "error": "CYCLE_DETECTED",
                "message": f"No se puede añadir el prerrequisito: {str(e)}",
                "details": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": "ADD_PREREQ_ERROR",
                "message": f"Error al añadir el prerrequisito: {str(e)}",
                "details": str(e)
            }
    
    def remove_prerequisite(self, prereq_id: int, course_id: int) -> Dict[str, Any]:
        """
        Elimina un prerrequisito de un curso.
        
        Args:
            prereq_id: ID del curso prerrequisito
            course_id: ID del curso dependiente
            
        Returns:
            Diccionario con el resultado de la operación
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            success = self.graph.remove_edge(prereq_id, course_id)
            
            if success:
                return {
                    "success": True,
                    "message": f"Prerrequisito {prereq_id} eliminado del curso {course_id}",
                    "prereq_id": prereq_id,
                    "course_id": course_id
                }
            else:
                return {
                    "success": False,
                    "error": "REMOVE_PREREQ_ERROR",
                    "message": f"No se pudo eliminar el prerrequisito {prereq_id} del curso {course_id}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": "REMOVE_PREREQ_ERROR",
                "message": f"Error al eliminar el prerrequisito: {str(e)}",
                "details": str(e)
            }
    
    def check_for_cycles(self) -> Dict[str, Any]:
        """
        Verifica si el grafo tiene ciclos.
        
        Returns:
            Diccionario con el resultado de la verificación
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            has_cycle = self.graph._has_cycle()
            
            return {
                "success": True,
                "has_cycle": has_cycle,
                "message": "Se detectó un ciclo en el grafo" if has_cycle else "No se detectaron ciclos en el grafo"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "CYCLE_CHECK_ERROR",
                "message": f"Error al verificar ciclos: {str(e)}",
                "details": str(e)
            }
    
    def get_graph_info(self) -> Dict[str, Any]:
        """
        Obtiene información general del grafo.
        
        Returns:
            Diccionario con información del grafo
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            courses = self.graph.get_all_courses()
            courses_without_prereqs = self.graph.get_courses_without_prerequisites()
            
            total_credits = sum(course.credits for course in courses)
            courses_with_prereqs = len(courses) - len(courses_without_prereqs)
            
            return {
                "success": True,
                "total_courses": len(courses),
                "courses_without_prereqs": len(courses_without_prereqs),
                "courses_with_prereqs": courses_with_prereqs,
                "total_credits": total_credits,
                "has_cycle": self.graph._has_cycle()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "INFO_ERROR",
                "message": f"Error al obtener información del grafo: {str(e)}",
                "details": str(e)
            } 