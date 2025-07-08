import json
from typing import List, Dict, Any
from graduacion_unal.models.User import User

class UserAdapter:
    """
    Adaptador para cargar y traducir datos de usuarios desde JSON a objetos User.
    """
    
    def __init__(self):
        self.users_data: List[Dict[str, Any]] = []
    
    def load_from_json(self, file_path: str) -> List[User]:
        """
        Carga los datos de usuarios desde un archivo JSON y los convierte a objetos User.
        
        Args:
            file_path: Ruta al archivo JSON con los datos de usuarios
            
        Returns:
            Lista de objetos User
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            json.JSONDecodeError: Si el JSON está mal formateado
            KeyError: Si falta algún campo requerido en el JSON
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.users_data = json.load(f)
            
            users = []
            for user_data in self.users_data:
                user = self._create_user_from_data(user_data)
                users.append(user)
            
            return users
            
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error al parsear JSON: {e}")
    
    def _create_user_from_data(self, user_data: Dict[str, Any]) -> User:
        """
        Crea un objeto User a partir de un diccionario de datos.
        
        Args:
            user_data: Diccionario con los datos del usuario
            
        Returns:
            Objeto User creado
            
        Raises:
            KeyError: Si falta algún campo requerido
        """
        required_fields = ['id', 'name', 'student_id', 'program']
        
        # Verificar campos requeridos
        for field in required_fields:
            if field not in user_data:
                raise KeyError(f"Campo requerido '{field}' no encontrado en: {user_data}")
        
        user_id = user_data['id']
        name = user_data['name']
        student_id = user_data['student_id']
        program = user_data['program']
        
        # Campos opcionales con valores por defecto
        semester = user_data.get('semester', 1)
        completed_courses = user_data.get('completed_courses', [])
        current_courses = user_data.get('current_courses', [])
        total_credits = user_data.get('total_credits', 0)
        max_credits_per_semester = user_data.get('max_credits_per_semester', 18)
        
        # Validar tipos de datos
        if not isinstance(user_id, int):
            raise ValueError(f"El ID del usuario debe ser un entero, se recibió: {type(user_id)}")
        
        if not isinstance(name, str):
            raise ValueError(f"El nombre debe ser una cadena, se recibió: {type(name)}")
        
        if not isinstance(student_id, str):
            raise ValueError(f"El código estudiantil debe ser una cadena, se recibió: {type(student_id)}")
        
        if not isinstance(program, str):
            raise ValueError(f"El programa debe ser una cadena, se recibió: {type(program)}")
        
        if not isinstance(semester, int):
            raise ValueError(f"El semestre debe ser un entero, se recibió: {type(semester)}")
        
        if not isinstance(completed_courses, list):
            raise ValueError(f"Los cursos completados deben ser una lista, se recibió: {type(completed_courses)}")
        
        if not isinstance(current_courses, list):
            raise ValueError(f"Los cursos actuales deben ser una lista, se recibió: {type(current_courses)}")
        
        # Validar que todos los IDs de cursos sean enteros
        for course_id in completed_courses + current_courses:
            if not isinstance(course_id, int):
                raise ValueError(f"Los IDs de cursos deben ser enteros, se recibió: {type(course_id)}")
        
        return User(
            id=user_id,
            name=name,
            student_id=student_id,
            program=program,
            semester=semester,
            completed_courses=completed_courses,
            current_courses=current_courses,
            total_credits=total_credits,
            max_credits_per_semester=max_credits_per_semester
        )
    
    def get_users_data(self) -> List[Dict[str, Any]]:
        """
        Retorna los datos originales de los usuarios.
        
        Returns:
            Lista de diccionarios con los datos de los usuarios
        """
        return self.users_data.copy()
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> bool:
        """
        Valida que los datos de un usuario sean correctos.
        
        Args:
            user_data: Diccionario con los datos del usuario
            
        Returns:
            True si los datos son válidos, False en caso contrario
        """
        try:
            self._create_user_from_data(user_data)
            return True
        except (KeyError, ValueError):
            return False
    
    def export_user_to_json(self, user: User) -> Dict[str, Any]:
        """
        Convierte un objeto User a un diccionario para exportar a JSON.
        
        Args:
            user: Objeto User a convertir
            
        Returns:
            Diccionario con los datos del usuario
        """
        return {
            "id": user.id,
            "name": user.name,
            "student_id": user.student_id,
            "program": user.program,
            "semester": user.semester,
            "completed_courses": user.completed_courses,
            "current_courses": user.current_courses,
            "total_credits": user.total_credits,
            "max_credits_per_semester": user.max_credits_per_semester
        }
    
    def save_users_to_json(self, users: List[User], file_path: str) -> None:
        """
        Guarda una lista de usuarios en un archivo JSON.
        
        Args:
            users: Lista de objetos User
            file_path: Ruta del archivo donde guardar
            
        Raises:
            IOError: Si hay error al escribir el archivo
        """
        try:
            users_data = []
            for user in users:
                users_data.append(self.export_user_to_json(user))
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            raise IOError(f"Error al guardar usuarios en JSON: {str(e)}") 