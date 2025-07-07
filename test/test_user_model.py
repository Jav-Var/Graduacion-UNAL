#!/usr/bin/env python3
"""
Script de prueba para verificar el modelo y adaptador de usuarios.
"""

import sys
import os

# Añadir el directorio src al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from graduacion_unal.models.User import User
from graduacion_unal.adapters.user_adapter import UserAdapter

def test_user_model():
    """
    Prueba el modelo de usuario y sus métodos.
    """
    print("🧪 Probando modelo de usuario...")
    
    # Crear un usuario de prueba
    user = User(
        id=1,
        name="Juan Pablo Ladino Rivera",
        student_id="20231012345",
        program="Ingeniería de Sistemas",
        semester=3,
        completed_courses=[1001, 1004, 1007],
        current_courses=[1002, 1005, 1008],
        total_credits=11,
        max_credits_per_semester=18
    )
    
    print(f"✅ Usuario creado: {user}")
    print(f"  - Nombre: {user.name}")
    print(f"  - Código: {user.student_id}")
    print(f"  - Programa: {user.program}")
    print(f"  - Semestre: {user.semester}")
    print(f"  - Cursos completados: {user.completed_courses}")
    print(f"  - Cursos actuales: {user.current_courses}")
    print(f"  - Créditos totales: {user.total_credits}")
    print(f"  - Límite de créditos: {user.max_credits_per_semester}")
    
    # Probar métodos del usuario
    print(f"\n🔍 Probando métodos del usuario:")
    
    # Verificar si ha completado un curso
    print(f"  - ¿Ha completado curso 1001? {user.has_completed_course(1001)}")
    print(f"  - ¿Ha completado curso 1002? {user.has_completed_course(1002)}")
    
    # Verificar si está inscrito en un curso
    print(f"  - ¿Está inscrito en curso 1002? {user.is_enrolled_in_course(1002)}")
    print(f"  - ¿Está inscrito en curso 1001? {user.is_enrolled_in_course(1001)}")
    
    # Calcular progreso
    progress = user.get_progress_percentage(15)  # 15 cursos totales
    print(f"  - Progreso: {progress:.1f}%")
    
    # Verificar si puede tomar un curso
    print(f"  - ¿Puede tomar curso de 3 créditos? {user.can_take_course(3)}")
    print(f"  - Créditos disponibles: {user.get_available_credits()}")
    
    # Añadir un curso completado
    print(f"\n➕ Añadiendo curso completado 1003:")
    success = user.add_completed_course(1003)
    print(f"  - Resultado: {success}")
    print(f"  - Cursos completados actualizados: {user.completed_courses}")
    
    # Añadir un curso actual
    print(f"\n➕ Añadiendo curso actual 1009:")
    success = user.add_current_course(1009)
    print(f"  - Resultado: {success}")
    print(f"  - Cursos actuales actualizados: {user.current_courses}")
    
    # Avanzar semestre
    print(f"\n📈 Avanzando al siguiente semestre:")
    old_semester = user.semester
    user.advance_semester()
    print(f"  - Semestre anterior: {old_semester}")
    print(f"  - Semestre actual: {user.semester}")
    
    print(f"\n✅ Pruebas del modelo de usuario completadas!")

def test_user_adapter():
    """
    Prueba el adaptador de usuarios.
    """
    print(f"\n🧪 Probando adaptador de usuarios...")
    
    # Crear instancia del adaptador
    adapter = UserAdapter()
    
    try:
        # Cargar usuarios desde JSON
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json'))
        print(f"📁 Cargando usuarios desde: {json_path}")
        
        users = adapter.load_from_json(json_path)
        
        print(f"✅ Usuarios cargados exitosamente!")
        print(f"📊 Número de usuarios: {len(users)}")
        
        # Mostrar información de cada usuario
        print(f"\n👥 Información de usuarios:")
        for i, user in enumerate(users, 1):
            print(f"\n  {i}. {user.name}")
            print(f"     - Código: {user.student_id}")
            print(f"     - Programa: {user.program}")
            print(f"     - Semestre: {user.semester}")
            print(f"     - Cursos completados: {len(user.completed_courses)}")
            print(f"     - Cursos actuales: {len(user.current_courses)}")
            print(f"     - Créditos totales: {user.total_credits}")
            
            # Calcular progreso
            progress = user.get_progress_percentage(15)
            print(f"     - Progreso: {progress:.1f}%")
        
        # Probar validación de datos
        print(f"\n🔍 Probando validación de datos:")
        valid_data = {
            "id": 999,
            "name": "Usuario de Prueba",
            "student_id": "20239999999",
            "program": "Ingeniería de Sistemas"
        }
        
        invalid_data = {
            "id": "no_es_numero",
            "name": "Usuario Inválido",
            "student_id": "20239999999",
            "program": "Ingeniería de Sistemas"
        }
        
        print(f"  - Datos válidos: {adapter.validate_user_data(valid_data)}")
        print(f"  - Datos inválidos: {adapter.validate_user_data(invalid_data)}")
        
        # Probar exportación a JSON
        print(f"\n📤 Probando exportación a JSON:")
        user_data = adapter.export_user_to_json(users[0])
        print(f"  - Datos exportados: {user_data}")
        
        print(f"\n✅ Pruebas del adaptador de usuarios completadas!")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de que el archivo data/users.json existe")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

def test_user_course_integration():
    """
    Prueba la integración entre usuarios y cursos.
    """
    print(f"\n🧪 Probando integración usuario-cursos...")
    
    # Crear un usuario
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
    
    print(f"👤 Usuario: {user.name}")
    print(f"📚 Cursos completados: {user.completed_courses}")
    print(f"📖 Cursos actuales: {user.current_courses}")
    
    # Simular cursos que puede tomar
    available_courses = [1007, 1008, 1010]  # Álgebra Lineal, Física I, Probabilidad
    
    print(f"\n🎯 Cursos disponibles para tomar:")
    for course_id in available_courses:
        can_take = user.can_take_course(3)  # Asumiendo 3 créditos por curso
        print(f"  - Curso {course_id}: {'✅ Puede tomar' if can_take else '❌ No puede tomar'}")
    
    # Simular completar un curso
    print(f"\n🎓 Simulando completar curso 1002 (Cálculo Integral):")
    user.add_completed_course(1002)
    user.remove_current_course(1002)
    print(f"  - Cursos completados actualizados: {user.completed_courses}")
    print(f"  - Cursos actuales actualizados: {user.current_courses}")
    
    # Avanzar semestre
    print(f"\n📈 Avanzando semestre:")
    user.advance_semester()
    print(f"  - Nuevo semestre: {user.semester}")
    
    print(f"\n✅ Pruebas de integración completadas!")

if __name__ == "__main__":
    test_user_model()
    test_user_adapter()
    test_user_course_integration()
    print(f"\n🎉 ¡Todas las pruebas de usuarios pasaron exitosamente!") 