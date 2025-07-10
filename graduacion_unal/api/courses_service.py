from typing import List, Dict, Any, Optional
from graduacion_unal.models.Courses import Course
from graduacion_unal.models.courses_graph import CoursesGraph
from graduacion_unal.adapters.courses_adapter import CoursesAdapter
from graduacion_unal.api.schedule_service import ScheduleService


class CoursesService:
    """
    Servicio de API para manejar la lógica de negocio de cursos.
    Mantiene una única instancia del grafo y maneja la persistencia.
    Es la única interfaz que debe usar la GUI.
    """
    
    def __init__(self):
        self.graph = CoursesGraph()
        self.adapter = CoursesAdapter()
        self.current_file_path: Optional[str] = None
        self._is_modified = False
    
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
            # Cargar cursos usando el adaptador
            courses = self.adapter.load_from_json(json_path)
            
            # Construir el grafo
            self.graph.build_from_courses(courses)
            
            # Actualizar estado
            self.current_file_path = json_path
            self._is_modified = False
            
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
        except ValueError as e:
            return {
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": f"Error de validación en los datos: {str(e)}",
                "details": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": "LOAD_ERROR",
                "message": f"Error al cargar el grafo: {str(e)}",
                "details": str(e)
            }
    
    def save_graph_to_json(self, json_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Guarda el grafo actual en un archivo JSON.
        
        Args:
            json_path: Ruta del archivo JSON (opcional, usa el actual si no se especifica)
            
        Returns:
            Diccionario con el resultado de la operación
        """
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado para guardar"
            }
        
        try:
            # Usar la ruta actual si no se especifica una nueva
            save_path = json_path or self.current_file_path
            if not save_path:
                return {
                    "success": False,
                    "error": "NO_FILE_PATH",
                    "message": "No se especificó una ruta de archivo"
                }
            
            # Obtener todos los cursos del grafo
            courses = self.graph.get_all_courses()
            
            # Guardar usando el adaptador
            self.adapter.save_to_json(courses, save_path)
            
            # Actualizar estado
            self.current_file_path = save_path
            self._is_modified = False
            
            return {
                "success": True,
                "message": f"Grafo guardado exitosamente en: {save_path}",
                "file_path": save_path,
                "courses_count": len(courses)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "SAVE_ERROR",
                "message": f"Error al guardar el grafo: {str(e)}",
                "details": str(e)
            }
    
    def get_all_courses(self) -> Dict[str, Any]:
        """
        Obtiene todos los cursos del grafo.
        
        Returns:
            Diccionario con la lista de cursos
        """
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
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
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
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
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
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
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
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
                "error": "NO_GRAPH",
                "message": "No hay grafo inicializado"
            }
        
        try:
            # Validar datos del curso usando el adaptador
            if not self.adapter.validate_course_data(course_data):
                return {
                    "success": False,
                    "error": "INVALID_DATA",
                    "message": "Los datos del curso no son válidos. Verifique que el ID sea único y todos los campos sean del tipo correcto."
                }
            
            # Crear el curso
            course = self.adapter._create_course_from_data(course_data)
            
            # Añadir al grafo
            self.graph.add_node(course)
            
            # Añadir ID al adaptador para mantener coherencia
            self.adapter.add_course_id(course.id)
            
            self._is_modified = True
            
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
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
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
                # Remover ID del adaptador para mantener coherencia
                self.adapter.remove_course_id(course_id)
                self._is_modified = True
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
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
            }
        
        try:
            # Validar datos del prerrequisito usando el adaptador
            if not self.adapter.validate_prerequisite_data(course_id, prereq_id):
                return {
                    "success": False,
                    "error": "INVALID_PREREQ_DATA",
                    "message": "Los datos del prerrequisito no son válidos. Verifique que ambos IDs existan y sean diferentes."
                }
            
            success = self.graph.add_vertex(prereq_id, course_id)
            
            if success:
                self._is_modified = True
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
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
            }
        
        try:
            success = self.graph.remove_edge(prereq_id, course_id)
            
            if success:
                self._is_modified = True
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
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
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
        if not self.graph or self.graph.number_nodes == 0:
            return {
                "success": False,
                "error": "NO_GRAPH",
                "message": "No hay grafo cargado"
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
                "has_cycle": self.graph._has_cycle(),
                "current_file": self.current_file_path,
                "is_modified": self._is_modified
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "INFO_ERROR",
                "message": f"Error al obtener información del grafo: {str(e)}",
                "details": str(e)
            }
    
    def is_modified(self) -> bool:
        """
        Verifica si el grafo ha sido modificado desde la última carga/guardado.
        
        Returns:
            True si ha sido modificado, False en caso contrario
        """
        return self._is_modified
    
    def get_current_file_path(self) -> Optional[str]:
        """
        Obtiene la ruta del archivo actual.
        
        Returns:
            Ruta del archivo actual o None si no hay archivo cargado
        """
        return self.current_file_path 

    def get_course_tree(self, max_credits_per_semester: int = 18) -> dict:
        """
        Devuelve la malla curricular organizada por niveles usando ScheduleService.
        """
        schedule_service = ScheduleService()
        schedule_service.set_graph(self.graph)
        return schedule_service.get_course_tree(max_credits_per_semester) 

    def generate_random_schedule(self, max_credits_per_semester: int = 18) -> dict:
        """
        Devuelve una malla generada aleatoriamente por semestres usando ScheduleService.
        """
        schedule_service = ScheduleService()
        schedule_service.set_graph(self.graph)
        return schedule_service.generate_random_schedule(max_credits_per_semester) 