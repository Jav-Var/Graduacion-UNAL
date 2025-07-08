import json
from typing import List, Dict, Any
from graduacion_unal.models.Courses import Course

class CoursesAdapter:
    """
    Adaptador para cargar y traducir datos de cursos desde JSON a objetos Course.
    """
    
    def __init__(self):
        self.courses_data: List[Dict[str, Any]] = []
    
    def load_from_json(self, file_path: str) -> List[Course]:
        """
        Carga los datos de cursos desde un archivo JSON y los convierte a objetos Course.
        
        Args:
            file_path: Ruta al archivo JSON con los datos de cursos
            
        Returns:
            Lista de objetos Course
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            json.JSONDecodeError: Si el JSON está mal formateado
            KeyError: Si falta algún campo requerido en el JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.courses_data = json.load(f)
            
            courses = []
            for course_data in self.courses_data:
                course = self._create_course_from_data(course_data)
                courses.append(course)
            
            return courses
            
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error al parsear JSON: {e}")
    
    def _create_course_from_data(self, course_data: Dict[str, Any]) -> Course:
        """
        Crea un objeto Course a partir de un diccionario de datos.
        
        Args:
            course_data: Diccionario con los datos del curso
            
        Returns:
            Objeto Course creado
            
        Raises:
            KeyError: Si falta algún campo requerido
        """
        required_fields = ['id', 'prereqs']
        
        # Verificar campos requeridos
        for field in required_fields:
            if field not in course_data:
                raise KeyError(f"Campo requerido '{field}' no encontrado en: {course_data}")
        
        course_id = course_data['id']
        prereqs = course_data['prereqs']
        name = course_data.get('name', '')
        credits = course_data.get('credits', 0)
        
        # Validar tipos de datos
        if not isinstance(course_id, int):
            raise ValueError(f"El ID del curso debe ser un entero, se recibió: {type(course_id)}")
        
        if not isinstance(prereqs, list):
            raise ValueError(f"Los prerrequisitos deben ser una lista, se recibió: {type(prereqs)}")
        
        # Validar que todos los prerrequisitos sean enteros
        for prereq in prereqs:
            if not isinstance(prereq, int):
                raise ValueError(f"Los IDs de prerrequisitos deben ser enteros, se recibió: {type(prereq)}")
        
        return Course(course_id, prereqs, name, credits)
    
    def get_courses_data(self) -> List[Dict[str, Any]]:
        """
        Retorna los datos originales de los cursos.
        
        Returns:
            Lista de diccionarios con los datos de los cursos
        """
        return self.courses_data.copy()
    
    def validate_course_data(self, course_data: Dict[str, Any]) -> bool:
        """
        Valida que los datos de un curso sean correctos.
        
        Args:
            course_data: Diccionario con los datos del curso
            
        Returns:
            True si los datos son válidos, False en caso contrario
        """
        try:
            self._create_course_from_data(course_data)
            return True
        except (KeyError, ValueError):
            return False
        
    def get_course_by_id(self, course_id: int) -> Course:
        """
        Obtiene un curso por su ID.
        
        Args:
            course_id: ID del curso a buscar
            
        Returns:
            Objeto Course encontrado o None si no existe
        """
        for course in self.courses_data:
            if course['id'] == course_id:
                return self._create_course_from_data(course)
        return None

