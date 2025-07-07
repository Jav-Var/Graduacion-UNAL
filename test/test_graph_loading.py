#!/usr/bin/env python3
"""
Script de prueba para verificar la carga del grafo desde JSON.
"""

import sys
import os

# Añadir el directorio src al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from graduacion_unal.models.courses_graph import CoursesGraph

def test_graph_loading():
    """
    Prueba la carga del grafo desde el archivo JSON.
    """
    print("🧪 Probando carga del grafo desde JSON...")
    
    # Crear instancia del grafo
    graph = CoursesGraph()
    
    try:
        # Cargar el grafo desde el JSON
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'courses.json'))
        print(f"📁 Cargando datos desde: {json_path}")
        
        graph.initialize_graph(json_path)
        
        print("✅ Grafo cargado exitosamente!")
        print(f"📊 Número de cursos: {graph.number_nodes}")
        
        # Mostrar información de los cursos
        print("\n📚 Cursos cargados:")
        for course_id, course in graph.courses_map.items():
            print(f"  - {course.id}: {course.name} ({course.credits} créditos)")
            if course.prereqs:
                print(f"    Prerrequisitos: {course.prereqs}")
            else:
                print(f"    Sin prerrequisitos")
        
        # Mostrar cursos sin prerrequisitos
        courses_without_prereqs = graph.get_courses_without_prerequisites()
        print(f"\n🎯 Cursos sin prerrequisitos ({len(courses_without_prereqs)}):")
        for course in courses_without_prereqs:
            print(f"  - {course.id}: {course.name}")
        
        # Mostrar estructura del grafo
        print(f"\n🕸️  Estructura del grafo:")
        print(graph)
        
        # Probar detección de ciclos
        print(f"\n🔍 Verificando ciclos en el grafo...")
        has_cycle = graph._has_cycle()
        if has_cycle:
            print("⚠️  Se detectó un ciclo en el grafo!")
        else:
            print("✅ No se detectaron ciclos en el grafo")
        
        # Probar obtención de cursos listos para tomar
        print(f"\n📋 Cursos listos para tomar (sin cursos completados):")
        ready_courses = graph.get_ready_courses([])
        for course in ready_courses:
            print(f"  - {course.id}: {course.name}")
        
        print(f"\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de que el archivo data/courses.json existe")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_graph_loading() 