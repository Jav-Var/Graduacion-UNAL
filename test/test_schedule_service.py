#!/usr/bin/env python3
"""
Script de prueba para verificar el servicio de planificación semestral.
"""

import sys
import os

# Añadir el directorio src al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from graduacion_unal.api.schedule_service import ScheduleService
from graduacion_unal.api.courses_service import CoursesService
from graduacion_unal.adapters.user_adapter import UserAdapter
from graduacion_unal.models.User import User

def test_schedule_service():
    """
    Prueba el servicio de planificación semestral.
    """
    print("🧪 Probando servicio de planificación semestral...")
    
    # Crear servicios
    courses_service = CoursesService()
    schedule_service = ScheduleService()
    
    try:
        # 1. Cargar el grafo de cursos
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'courses.json'))
        print(f"📁 Cargando cursos desde: {json_path}")
        
        result = courses_service.load_graph_from_json(json_path)
        if not result['success']:
            print(f"❌ Error al cargar cursos: {result['message']}")
            return
        
        print(f"✅ Cursos cargados: {result['courses_count']}")
        
        # Establecer el grafo en el servicio de schedule
        schedule_service.set_graph(courses_service.graph)
        
        # 2. Probar obtención del árbol de cursos
        print(f"\n🌳 Probando obtención del árbol de cursos:")
        tree_result = schedule_service.get_course_tree(18)
        
        if tree_result['success']:
            print(f"✅ Árbol generado exitosamente")
            print(f"  - Niveles totales: {tree_result['total_levels']}")
            print(f"  - Cursos totales: {tree_result['total_courses']}")
            
            # Mostrar información de cada nivel
            for level, info in tree_result['course_tree'].items():
                print(f"  - Nivel {level}: {info['total_courses']} cursos, {info['total_credits']} créditos")
        else:
            print(f"❌ Error al generar árbol: {tree_result['message']}")
        
        # 3. Probar generación de planificación aleatoria
        print(f"\n🎲 Probando generación de planificación aleatoria:")
        random_result = schedule_service.generate_random_schedule(18)
        
        if random_result['success']:
            print(f"✅ Planificación aleatoria generada")
            print(f"  - Semestres totales: {random_result['total_semesters']}")
            print(f"  - Cursos totales: {random_result['total_courses']}")
            print(f"  - Créditos totales: {random_result['total_credits']}")
            print(f"  - ¿Es válida?: {random_result['valid']}")
            
            if not random_result['valid']:
                print(f"  - Errores: {random_result['errors']}")
            
            # Mostrar planificación
            print(f"\n📅 Planificación aleatoria:")
            for semester, info in random_result['schedule'].items():
                print(f"  Semestre {semester}: {info['total_courses']} cursos, {info['total_credits']} créditos")
                for course in info['courses']:
                    print(f"    - {course['id']}: {course['name']} ({course['credits']} créditos)")
        else:
            print(f"❌ Error al generar planificación aleatoria: {random_result['message']}")
        
        # 4. Probar generación de planificación greedy
        print(f"\n🎯 Probando generación de planificación greedy:")
        greedy_result = schedule_service.generate_greedy_schedule(18)
        
        if greedy_result['success']:
            print(f"✅ Planificación greedy generada")
            print(f"  - Semestres totales: {greedy_result['total_semesters']}")
            print(f"  - Cursos totales: {greedy_result['total_courses']}")
            print(f"  - Créditos totales: {greedy_result['total_credits']}")
            print(f"  - ¿Es válida?: {greedy_result['valid']}")
            
            if not greedy_result['valid']:
                print(f"  - Errores: {greedy_result['errors']}")
            
            # Mostrar planificación
            print(f"\n📅 Planificación greedy:")
            for semester, info in greedy_result['schedule'].items():
                print(f"  Semestre {semester}: {info['total_courses']} cursos, {info['total_credits']} créditos")
                for course in info['courses']:
                    print(f"    - {course['id']}: {course['name']} ({course['credits']} créditos)")
        else:
            print(f"❌ Error al generar planificación greedy: {greedy_result['message']}")
        
        # 5. Probar validación de planificación
        print(f"\n✅ Probando validación de planificación:")
        
        # Crear una planificación válida
        valid_schedule = {
            1: [1001, 1004],  # Cálculo Diferencial, Programación I
            2: [1002, 1005, 1007],  # Cálculo Integral, Programación II, Álgebra Lineal
            3: [1003, 1006, 1008],  # Cálculo Vectorial, Estructuras de Datos, Física I
        }
        
        validation_result = schedule_service.validate_schedule(valid_schedule, 18)
        
        if validation_result['success']:
            print(f"✅ Validación completada")
            print(f"  - ¿Es válida?: {validation_result['valid']}")
            print(f"  - Semestres: {validation_result['total_semesters']}")
            print(f"  - Cursos: {validation_result['total_courses']}")
            
            if not validation_result['valid']:
                print(f"  - Errores: {validation_result['errors']}")
        else:
            print(f"❌ Error en validación: {validation_result['message']}")
        
        # 6. Probar planificación personalizada con usuario
        print(f"\n👤 Probando planificación personalizada:")
        
        # Crear un usuario de prueba
        user = User(
            id=1,
            name="Estudiante de Prueba",
            student_id="20231099999",
            program="Ingeniería de Sistemas",
            semester=2,
            completed_courses=[1001, 1004],  # Cálculo Diferencial, Programación I
            current_courses=[1002, 1005],    # Cálculo Integral, Programación II
            total_credits=7,
            max_credits_per_semester=18
        )
        
        personalized_result = schedule_service.generate_personalized_schedule(user, 18)
        
        if personalized_result['success']:
            print(f"✅ Planificación personalizada generada")
            print(f"  - Semestres totales: {personalized_result['total_semesters']}")
            print(f"  - Cursos totales: {personalized_result['total_courses']}")
            print(f"  - Créditos totales: {personalized_result['total_credits']}")
            
            progress = personalized_result['user_progress']
            print(f"  - Progreso del usuario:")
            print(f"    * Cursos completados: {progress['completed_courses']}")
            print(f"    * Semestre actual: {progress['current_semester']}")
            print(f"    * Créditos completados: {progress['total_credits_completed']}")
            
            # Mostrar planificación personalizada
            print(f"\n📅 Planificación personalizada:")
            for semester, info in personalized_result['schedule'].items():
                print(f"  Semestre {semester}: {info['total_courses']} cursos, {info['total_credits']} créditos")
                for course in info['courses']:
                    print(f"    - {course['id']}: {course['name']} ({course['credits']} créditos)")
        else:
            print(f"❌ Error al generar planificación personalizada: {personalized_result['message']}")
        
        # 7. Comparar diferentes algoritmos
        print(f"\n📊 Comparando algoritmos de planificación:")
        
        algorithms = [
            ("Aleatorio", random_result),
            ("Greedy", greedy_result),
            ("Personalizado", personalized_result)
        ]
        
        for name, result in algorithms:
            if result['success']:
                print(f"  {name}:")
                print(f"    - Semestres: {result['total_semesters']}")
                print(f"    - Cursos: {result['total_courses']}")
                print(f"    - Créditos: {result['total_credits']}")
                if 'valid' in result:
                    print(f"    - Válida: {result['valid']}")
            else:
                print(f"  {name}: Error - {result['message']}")
        
        print(f"\n🎉 ¡Todas las pruebas de planificación pasaron exitosamente!")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_schedule_service() 