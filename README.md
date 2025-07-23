## Graduación-UNAL:
### Descripción del Proyecto
Graduación-UNAL es una herramienta para estudiantes de la Universidad Nacional de Colombia que calcula el número mínimo de semestres necesarios para completar un programa académico, respetando relaciones de prerrequisito y el límite de creditos por semestre.

**Problema que resuelve:**  
Los estudiantes necesitan planificar su carrera considerando complejas relaciones de prerrequisitos y límites de carga académica, lo que requiere cálculos manuales propensos a errores.

**Integrantes**
- Javier Miguel Vargas Mendez 
- Samuel Jose Moreno Penaranda
- Samuel Felipe Palacios Olaya
- Juan Pablo Ladino Rivera


### Características Principales
🎓 Cálculo del plan de estudios óptimo

📊 Visualización de cronograma semestral

⚠️ Detección de ciclos en prerrequisitos

📥 Importación/exportación de datos en JSON

🧮 Organización y entorno de pruebas 

### 📦 Requisitos

- Python 3.11
- Instala PyQt5 con el siguiente comando:

```bash
pip install PyQt5
```

### Punto de entrada (PyQt)

Ejecutar: 
- Opcion 1:  
python graduacion_unal/gui/app.py
- Opcion 2(windows):  
python -m graduacion_unal.gui.app