# Arquitectura del Proyecto Graduación-UNAL

## 🏗️ Arquitectura Limpia

El proyecto sigue los principios de **Clean Architecture** para separar las responsabilidades y facilitar el mantenimiento y las pruebas.

### 📁 Estructura de Carpetas

```
src/graduacion_unal/
├── models/          # Entidades y modelos de datos
├── structures/      # Estructuras de datos personalizadas
├── adapters/        # Adaptadores para conversión de datos
├── api/            # Servicios de API (lógica de negocio)
└── database/       # Capa de persistencia (futuro)
```

## 🎯 Separación de Responsabilidades

### 1. **Models** (Entidades)
- **`Courses.py`**: Modelo de datos para cursos
- **`courses_graph.py`**: Modelo del grafo de dependencias
- **`courses_schedule.py`**: Modelo de planificación semestral

**Responsabilidad**: Solo contienen la estructura de datos y métodos básicos de validación.

### 2. **Structures** (Estructuras de Datos)
- **`hash.py`**: Implementación personalizada de HashMap
- **`queue.py`**: Implementación personalizada de Queue

**Responsabilidad**: Proporcionar estructuras de datos eficientes para el proyecto.

### 3. **Adapters** (Adaptadores)
- **`courses_adapter.py`**: Convierte datos JSON a objetos Course

**Responsabilidad**: Traducir datos entre diferentes formatos (JSON ↔ Objetos).

### 4. **API** (Servicios de Negocio)
- **`courses_service.py`**: Servicio principal para operaciones de cursos

**Responsabilidad**: Manejar la lógica de negocio y proporcionar una interfaz limpia para las operaciones.

## 🔄 Flujo de Datos

```
JSON → Adapter → Model → API → Interfaz (futuro)
```

### Ejemplo de Flujo:

1. **Carga de Datos**:
   ```
   data/courses.json → CoursesAdapter → List[Course] → CoursesGraph
   ```

2. **Operación de Negocio**:
   ```
   API Request → CoursesService → CoursesGraph → Response
   ```

## 🚀 Uso de la API

### Inicialización
```python
from graduacion_unal.api.courses_service import CoursesService

service = CoursesService()
result = service.load_graph_from_json("data/courses.json")
```

### Operaciones Principales

#### 1. Cargar Grafo
```python
result = service.load_graph_from_json("path/to/courses.json")
if result['success']:
    print(f"Cargados {result['courses_count']} cursos")
```

#### 2. Obtener Información
```python
# Todos los cursos
courses = service.get_all_courses()

# Cursos sin prerrequisitos
no_prereqs = service.get_courses_without_prerequisites()

# Cursos listos para tomar
ready_courses = service.get_ready_courses([1001, 1004])

# Información del grafo
info = service.get_graph_info()
```

#### 3. Modificar Grafo
```python
# Añadir curso
new_course = {
    "id": 1016,
    "name": "Nuevo Curso",
    "credits": 3,
    "prereqs": [1001]
}
result = service.add_course(new_course)

# Añadir prerrequisito
service.add_prerequisite(1001, 1016)

# Eliminar curso
service.remove_course(1016)
```

#### 4. Validaciones
```python
# Verificar ciclos
cycle_check = service.check_for_cycles()

# Obtener curso específico
course = service.get_course_by_id(1001)
```

## 📊 Respuestas de la API

Todas las operaciones retornan diccionarios con la siguiente estructura:

### Éxito
```python
{
    "success": True,
    "message": "Operación exitosa",
    "data": {...}  # Datos específicos de la operación
}
```

### Error
```python
{
    "success": False,
    "error": "ERROR_TYPE",
    "message": "Descripción del error",
    "details": "Información adicional"
}
```

## 🧪 Pruebas

### Ejecutar Pruebas
```bash
# Prueba de carga del grafo
python3 test/test_graph_loading.py

# Prueba de la API
python3 test/test_api_service.py
```

## 🔮 Futuras Extensiones

### 1. Interfaz Gráfica
- **Web UI**: Flask/FastAPI + React/Vue
- **Desktop UI**: Tkinter/PyQt
- **Mobile**: React Native/Flutter

### 2. Persistencia
- **SQLite**: Para desarrollo
- **PostgreSQL**: Para producción
- **Redis**: Para caché

### 3. Servicios Adicionales
- **ScheduleService**: Planificación semestral
- **UserService**: Gestión de usuarios
- **ProgressService**: Seguimiento de progreso

## 🎯 Beneficios de la Arquitectura

1. **Separación de Responsabilidades**: Cada capa tiene una función específica
2. **Testabilidad**: Fácil de probar cada componente por separado
3. **Mantenibilidad**: Cambios en una capa no afectan otras
4. **Escalabilidad**: Fácil agregar nuevas funcionalidades
5. **Independencia**: Los modelos no dependen de la interfaz

## 📝 Convenciones

- **Models**: Solo estructura de datos y validaciones básicas
- **API**: Manejo de errores y respuestas estandarizadas
- **Adapters**: Conversión de datos sin lógica de negocio
- **Tests**: Un test por funcionalidad principal 