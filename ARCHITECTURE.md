# Arquitectura del Proyecto Graduación-UNAL

### Estructura de Carpetas

```
src/
├── models/          # Entidades y modelos de datos
├── structures/      # Estructuras de datos personalizadas
├── adapters/        # Adaptadores para conversión de datos
├── api/            # Servicios de API (lógica de negocio)
├── gui/
```


### 1. **Models** (Entidades)
- **`Courses.py`**: Modelo de datos para cursos
- **`courses_graph.py`**: Modelo del grafo de dependencias
- **`courses_schedule.py`**: Modelo de planificación semestral

**Responsabilidad**: Solo contienen la estructura de datos y métodos básicos de validación.

### 2. **Structures** (Estructuras de Datos)
- **`hash.py`**: Implementación personalizada de HashMap
- **`queue.py`**: Implementación personalizada de Queue
- **`disjoint_sets.py`**: Implementación clasica de disjoint sets


### 3. **Adapters** (Adaptadores)
- **`courses_adapter.py`**: Convierte datos JSON a objetos Course

**Responsabilidad**: Traducir datos entre diferentes formatos (JSON ↔ Objetos).

### 4. **API** (Servicios de Negocio)
- **`courses_service.py`**: Servicio principal para operaciones de cursos

**Responsabilidad**: Manejar la lógica de negocio y proporcionar una interfaz limpia para las operaciones.

## Flujo de Datos

```
JSON → Adapter → Model → API → Interfaz GUI
```
