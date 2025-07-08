# Documentación de la API de Planificación de Cursos

Este módulo contiene los servicios principales para la gestión de cursos, usuarios y planificación semestral en la carrera universitaria. Aquí se documentan los métodos implementados en los servicios de API:

- `courses_service.py`: Servicio para gestión de cursos y grafo de prerrequisitos.
- `schedule_service.py`: Servicio para generación y validación de planificaciones semestrales.
- `user_adapter.py`: Adaptador para cargar y exportar usuarios desde/hacia JSON.

---

## 1. Servicio de Cursos (`courses_service.py`)

### Métodos principales

#### `load_graph_from_json(json_path: str) -> dict`
Carga el grafo de cursos desde un archivo JSON.

**Ejemplo:**
```python
from graduacion_unal.api.courses_service import CoursesService

service = CoursesService()
result = service.load_graph_from_json('data/courses.json')
if result['success']:
    print('Cursos cargados:', result['courses_count'])
```

#### `get_course(course_id: int) -> Course | None`
Obtiene un curso por su ID.

**Ejemplo:**
```python
course = service.get_course(1001)
if course:
    print(course.name, course.credits)
```

#### `get_all_courses() -> list[Course]`
Obtiene la lista de todos los cursos cargados.

---

## 2. Servicio de Planificación (`schedule_service.py`)

### Métodos principales

#### `set_graph(graph: CoursesGraph) -> None`
Establece el grafo de cursos para el servicio de planificación.

#### `get_course_tree(max_credits_per_semester: int = 18) -> dict`
Obtiene el árbol de cursos organizados por niveles (semestres posibles).

**Ejemplo:**
```python
from graduacion_unal.api.schedule_service import ScheduleService
schedule_service = ScheduleService()
schedule_service.set_graph(service.graph)
tree = schedule_service.get_course_tree(18)
print(tree['course_tree'])
```

#### `generate_random_schedule(max_credits_per_semester: int = 18) -> dict`
Genera una planificación aleatoria válida.

**Ejemplo:**
```python
random_plan = schedule_service.generate_random_schedule(18)
print(random_plan['schedule'])
```

#### `generate_greedy_schedule(max_credits_per_semester: int = 18) -> dict`
Genera una planificación usando un algoritmo greedy (maximiza créditos por semestre).

**Ejemplo:**
```python
greedy_plan = schedule_service.generate_greedy_schedule(18)
print(greedy_plan['schedule'])
```

#### `validate_schedule(schedule: dict, max_credits_per_semester: int = 18) -> dict`
Valida una planificación personalizada.

**Ejemplo:**
```python
plan = {1: [1001, 1004], 2: [1002, 1005, 1007]}
validation = schedule_service.validate_schedule(plan, 18)
print(validation['valid'], validation['errors'])
```

#### `generate_personalized_schedule(user: User, max_credits_per_semester: int = 18) -> dict`
Genera una planificación personalizada para un usuario según su avance.

**Ejemplo:**
```python
from graduacion_unal.models.User import User
user = User(id=1, name='Estudiante', student_id='202312345', program='Ingeniería', completed_courses=[1001], current_courses=[1002])
personal_plan = schedule_service.generate_personalized_schedule(user, 18)
print(personal_plan['schedule'])
```

---

## 3. Adaptador de Usuarios (`user_adapter.py`)

### Métodos principales

#### `load_from_json(file_path: str) -> list[User]`
Carga usuarios desde un archivo JSON.

**Ejemplo:**
```python
from graduacion_unal.adapters.user_adapter import UserAdapter
adapter = UserAdapter()
users = adapter.load_from_json('data/users.json')
for user in users:
    print(user.name, user.completed_courses)
```

#### `export_user_to_json(user: User) -> dict`
Convierte un objeto User a un diccionario exportable a JSON.

**Ejemplo:**
```python
user_dict = adapter.export_user_to_json(users[0])
print(user_dict)
```

#### `save_users_to_json(users: list[User], file_path: str) -> None`
Guarda una lista de usuarios en un archivo JSON.

**Ejemplo:**
```python
adapter.save_users_to_json(users, 'data/usuarios_exportados.json')
```

#### `validate_user_data(user_data: dict) -> bool`
Valida la estructura de un diccionario de usuario.

**Ejemplo:**
```python
is_valid = adapter.validate_user_data({'id': 1, 'name': 'Test', 'student_id': '2023', 'program': 'Ingeniería'})
print(is_valid)
```

---

## Notas
- Todos los métodos devuelven diccionarios con claves como `success`, `errors`, `schedule`, etc., para fácil integración.
- Puedes combinar los servicios para flujos completos: cargar cursos, cargar usuarios, generar y validar planificaciones.

---

