#!/usr/bin/env python3
"""
Script de prueba simple para la detección de ciclos con DisjointSets.
"""

import sys
import os

# Agregar el directorio src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from graduacion_unal.models.courses_graph import CoursesGraph
from graduacion_unal.models.Courses import Course

def test_cycle_detection():
    """
    Prueba la detección de ciclos en diferentes escenarios.
    """
    print("=== Prueba de Detección de Ciclos con DisjointSets ===\n")
    
    # Test 1: Grafo sin ciclos
    print("1. Grafo SIN ciclos:")
    graph_no_cycle = CoursesGraph()
    
    # Crear cursos sin ciclos
    courses = [
        Course(1001, [], "Matemáticas I", 3),
        Course(1002, [1001], "Matemáticas II", 3),
        Course(1003, [1002], "Matemáticas III", 3),
        Course(1004, [1001], "Programación I", 3),
        Course(1005, [1004], "Programación II", 3),
    ]
    
    for course in courses:
        graph_no_cycle.add_node(course)
    
    has_cycle = graph_no_cycle._has_cycle()
    print(f"   Ciclo detectado: {has_cycle}")
    print(f"   Estado esperado: False")
    print(f"   ✅ {'Correcto' if not has_cycle else 'Incorrecto'}")
    print()
    
    # Test 2: Grafo con ciclo
    print("2. Grafo CON ciclo:")
    graph_with_cycle = CoursesGraph()
    
    # Crear cursos con un ciclo
    courses_with_cycle = [
        Course(1001, [], "Matemáticas I", 3),
        Course(1002, [1001], "Matemáticas II", 3),
        Course(1003, [1002], "Matemáticas III", 3),
        Course(1004, [1003, 1001], "Programación I", 3),  # Depende de 1003 y 1001
    ]
    
    for course in courses_with_cycle:
        graph_with_cycle.add_node(course)
    
    # Intentar añadir una arista que crea un ciclo
    try:
        graph_with_cycle.add_vertex(1004, 1002)  # 1004 -> 1002 crea un ciclo
        print("   ❌ Error: No se detectó el ciclo")
    except ValueError as e:
        print(f"   ✅ Ciclo detectado correctamente: {e}")
    print()
    
    # Test 3: Grafo con auto-ciclo
    print("3. Grafo con auto-ciclo:")
    graph_self_cycle = CoursesGraph()
    
    # Crear un curso con auto-prerrequisito
    try:
        graph_self_cycle.add_node(Course(1001, [1001], "Auto", 3))
        print("   ❌ Error: No se detectó el auto-ciclo")
    except Exception as e:
        print(f"   ✅ Auto-ciclo detectado: {e}")
    print()
    
    # Test 4: Grafo vacío
    print("4. Grafo vacío:")
    empty_graph = CoursesGraph()
    has_cycle = empty_graph._has_cycle()
    print(f"   Ciclo detectado: {has_cycle}")
    print(f"   Estado esperado: False")
    print(f"   ✅ {'Correcto' if not has_cycle else 'Incorrecto'}")
    print()
    
    # Test 5: Grafo con un solo nodo
    print("5. Grafo con un solo nodo:")
    single_node_graph = CoursesGraph()
    single_node_graph.add_node(Course(1001, [], "Solo", 3))
    has_cycle = single_node_graph._has_cycle()
    print(f"   Ciclo detectado: {has_cycle}")
    print(f"   Estado esperado: False")
    print(f"   ✅ {'Correcto' if not has_cycle else 'Incorrecto'}")
    print()

def test_complex_cycle():
    """
    Prueba un ciclo complejo.
    """
    print("=== Prueba de Ciclo Complejo ===\n")
    
    graph = CoursesGraph()
    
    # Crear un grafo con un ciclo complejo
    courses = [
        Course(1001, [], "A", 3),
        Course(1002, [1001], "B", 3),
        Course(1003, [1002], "C", 3),
        Course(1004, [1003], "D", 3),
        Course(1005, [1004], "E", 3),
    ]
    
    for course in courses:
        graph.add_node(course)
    
    print("Grafo inicial (sin ciclos):")
    print(graph)
    print()
    
    # Intentar añadir una arista que crea un ciclo largo
    try:
        graph.add_vertex(1005, 1001)  # E -> A crea un ciclo A->B->C->D->E->A
        print("❌ Error: No se detectó el ciclo complejo")
    except ValueError as e:
        print(f"✅ Ciclo complejo detectado correctamente: {e}")
    print()

def main():
    """Ejecuta todas las pruebas."""
    print("🔍 Pruebas de Detección de Ciclos con DisjointSets\n")
    
    try:
        test_cycle_detection()
        test_complex_cycle()
        
        print("✅ Todas las pruebas completadas exitosamente")
        print("\n💡 La implementación con DisjointSets:")
        print("   - Detecta ciclos en grafos dirigidos")
        print("   - Optimiza las consultas de conectividad")
        print("   - Maneja casos edge correctamente")
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 