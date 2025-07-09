import json
from typing import List, Dict, Any
from models.Courses import Course


class CoursesAdapter:
    """
    Adaptador para cargar y traducir datos de cursos desde JSON a objetos Course.
    Solo se encarga de la conversión de datos, sin lógica de negocio.
    """
    
    def __init__(self):
        self._existing_ids = set()  # Para validar IDs únicos
    
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
            ValueError: Si hay IDs duplicados o datos inválidos
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                courses_data = json.load(f)
            
            # Limpiar IDs existentes al cargar nuevo archivo
            self._existing_ids.clear()
            
            courses = []
            for course_data in courses_data:
                course = self._create_course_from_data(course_data)
                courses.append(course)
                # Añadir ID a la lista de existentes
                self._existing_ids.add(course.id)
            
            return courses
            
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error al parsear JSON: {e}")
    
    def save_to_json(self, courses: List[Course], file_path: str) -> None:
        """
        Guarda una lista de cursos en un archivo JSON.
        
        Args:
            courses: Lista de objetos Course
            file_path: Ruta del archivo JSON donde guardar
            
        Raises:
            IOError: Si hay error al escribir el archivo
        """
        try:
            courses_data = []
            for course in courses:
                course_data = {
                    "id": course.id,
                    "name": course.name,
                    "credits": course.credits,
                    "prereqs": course.prereqs
                }
                courses_data.append(course_data)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(courses_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            raise IOError(f"Error al guardar el archivo: {str(e)}")
    
    def _create_course_from_data(self, course_data: Dict[str, Any]) -> Course:
        """
        Crea un objeto Course a partir de un diccionario de datos.
        
        Args:
            course_data: Diccionario con los datos del curso
            
        Returns:
            Objeto Course creado
            
        Raises:
            KeyError: Si falta algún campo requerido
            ValueError: Si los tipos de datos no son correctos o hay IDs duplicados
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
        
        # Validar que el ID sea único (solo si ya tenemos IDs cargados)
        if course_id in self._existing_ids:
            raise ValueError(f"El ID {course_id} ya existe. Los IDs deben ser únicos.")
        
        return Course(course_id, prereqs, name, credits)
    
    def validate_course_data(self, course_data: Dict[str, Any]) -> bool:
        """
        Valida que los datos de un curso sean correctos.
        
        Args:
            course_data: Diccionario con los datos del curso
            
        Returns:
            True si los datos son válidos, False en caso contrario
        """
        try:
            # Verificar campos requeridos
            required_fields = ['id', 'prereqs']
            for field in required_fields:
                if field not in course_data:
                    return False
            
            # Validar tipos
            if not isinstance(course_data['id'], int):
                return False
            
            if not isinstance(course_data['prereqs'], list):
                return False
            
            # Validar prerrequisitos
            for prereq in course_data['prereqs']:
                if not isinstance(prereq, int):
                    return False
            
            # Validar que el ID sea único
            if course_data['id'] in self._existing_ids:
                return False
            
            return True
            
        except (KeyError, ValueError):
            return False
    
    def validate_prerequisite_data(self, course_id: int, prereq_id: int) -> bool:
        """
        Valida que los datos para añadir un prerrequisito sean correctos.
        
        Args:
            course_id: ID del curso al que se añade el prerrequisito
            prereq_id: ID del curso prerrequisito
            
        Returns:
            True si los datos son válidos, False en caso contrario
        """
        try:
            # Validar tipos
            if not isinstance(course_id, int) or not isinstance(prereq_id, int):
                return False
            
            # Validar que ambos IDs existan en el sistema
            if course_id not in self._existing_ids or prereq_id not in self._existing_ids:
                return False
            
            # Validar que no sea el mismo curso
            if course_id == prereq_id:
                return False
            
            return True
            
        except (TypeError, ValueError):
            return False
    
    def add_course_id(self, course_id: int) -> None:
        """
        Añade un ID de curso al conjunto de IDs existentes.
        Útil para mantener la coherencia cuando se añaden cursos desde la GUI.
        
        Args:
            course_id: ID del curso a añadir
        """
        self._existing_ids.add(course_id)
    
    def remove_course_id(self, course_id: int) -> None:
        """
        Remueve un ID de curso del conjunto de IDs existentes.
        Útil para mantener la coherencia cuando se eliminan cursos.
        
        Args:
            course_id: ID del curso a remover
        """
        self._existing_ids.discard(course_id)
    
    def get_existing_ids(self) -> set:
        """
        Obtiene el conjunto de IDs existentes.
        
        Returns:
            Conjunto de IDs de cursos existentes
        """
        return self._existing_ids.copy()
    
    def clear_existing_ids(self) -> None:
        """
        Limpia el conjunto de IDs existentes.
        Útil cuando se carga un nuevo archivo.
        """
        self._existing_ids.clear()

