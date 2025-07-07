#!/usr/bin/env python3
"""
Script de prueba para verificar la API de servicios de cursos.
"""

import sys
import os

# Añadir el directorio src al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from graduacion_unal.api.courses_service import CoursesService

def test_api_service():
    """
    Prueba la API de servicios de cursos.
    """
    print("🧪 Probando API de servicios de cursos...")
    
    # Crear instancia del servicio
    service = CoursesService()
    
    try:
        # 1. Cargar el grafo desde JSON
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'courses.json'))
        print(f"📁 Cargando grafo desde: {json_path}")
        
        result = service.load_graph_from_json(json_path)
        print(f"✅ Resultado: {result['message']}")
        print(f"📊 Cursos cargados: {result['courses_count']}")
        
        # 2. Obtener información del grafo
        print(f"\n📊 Información del grafo:")
        info = service.get_graph_info()
        if info['success']:
            print(f"  - Total de cursos: {info['total_courses']}")
            print(f"  - Cursos sin prerrequisitos: {info['courses_without_prereqs']}")
            print(f"  - Cursos con prerrequisitos: {info['courses_with_prereqs']}")
            print(f"  - Total de créditos: {info['total_credits']}")
            print(f"  - Tiene ciclos: {info['has_cycle']}")
        
        # 3. Obtener todos los cursos
        print(f"\n📚 Todos los cursos:")
        courses_result = service.get_all_courses()
        if courses_result['success']:
            for course in courses_result['courses']:
                print(f"  - {course['id']}: {course['name']} ({course['credits']} créditos)")
                if course['prereqs']:
                    print(f"    Prerrequisitos: {course['prereqs']}")
        
        # 4. Obtener cursos sin prerrequisitos
        print(f"\n🎯 Cursos sin prerrequisitos:")
        no_prereqs_result = service.get_courses_without_prerequisites()
        if no_prereqs_result['success']:
            for course in no_prereqs_result['courses']:
                print(f"  - {course['id']}: {course['name']}")
        
        # 5. Obtener cursos listos para tomar (sin cursos completados)
        print(f"\n📋 Cursos listos para tomar (sin cursos completados):")
        ready_result = service.get_ready_courses([])
        if ready_result['success']:
            for course in ready_result['courses']:
                print(f"  - {course['id']}: {course['name']}")
        
        # 6. Obtener cursos listos para tomar (con algunos cursos completados)
        print(f"\n📋 Cursos listos para tomar (con cursos 1001 y 1004 completados):")
        ready_result = service.get_ready_courses([1001, 1004])
        if ready_result['success']:
            for course in ready_result['courses']:
                print(f"  - {course['id']}: {course['name']}")
        
        # 7. Obtener un curso específico
        print(f"\n🔍 Información del curso 1006:")
        course_result = service.get_course_by_id(1006)
        if course_result['success']:
            course = course_result['course']
            print(f"  - ID: {course['id']}")
            print(f"  - Nombre: {course['name']}")
            print(f"  - Créditos: {course['credits']}")
            print(f"  - Prerrequisitos: {course['prereqs']}")
            print(f"  - Cursos dependientes: {course['adjacent']}")
        
        # 8. Verificar ciclos
        print(f"\n🔍 Verificando ciclos:")
        cycle_result = service.check_for_cycles()
        if cycle_result['success']:
            print(f"  - {cycle_result['message']}")
        
        # 9. Probar añadir un nuevo curso
        print(f"\n➕ Probando añadir un nuevo curso:")
        new_course_data = {
            "id": 1016,
            "name": "Seminario de Grado",
            "credits": 2,
            "prereqs": [1015]  # Requiere Inteligencia Artificial
        }
        add_result = service.add_course(new_course_data)
        print(f"  - Resultado: {add_result['message']}")
        
        # 10. Verificar que el curso se añadió
        print(f"\n✅ Verificando que el curso se añadió:")
        course_result = service.get_course_by_id(1016)
        if course_result['success']:
            course = course_result['course']
            print(f"  - {course['id']}: {course['name']} ({course['credits']} créditos)")
            print(f"    Prerrequisitos: {course['prereqs']}")
        
        # 11. Probar añadir un prerrequisito
        print(f"\n🔗 Probando añadir prerrequisito:")
        prereq_result = service.add_prerequisite(1006, 1016)  # Estructuras de Datos como prerrequisito adicional
        print(f"  - Resultado: {prereq_result['message']}")
        
        # 12. Probar eliminar un prerrequisito
        print(f"\n🔗 Probando eliminar prerrequisito:")
        remove_prereq_result = service.remove_prerequisite(1006, 1016)
        print(f"  - Resultado: {remove_prereq_result['message']}")
        
        # 13. Probar eliminar el curso añadido
        print(f"\n🗑️  Probando eliminar curso:")
        remove_result = service.remove_course(1016)
        print(f"  - Resultado: {remove_result['message']}")
        
        print(f"\n🎉 ¡Todas las pruebas de la API pasaron exitosamente!")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_service() 