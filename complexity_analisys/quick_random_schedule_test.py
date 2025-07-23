import time
import json
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from graduacion_unal.api.courses_service import CoursesService
from graduacion_unal.api.schedule_service import ScheduleService

def generar_grafo_simple(n_cursos: int, densidad: float = 0.2) -> list:
    """
    Genera un grafo simple para pruebas rápidas.
    """
    cursos = []
    
    for i in range(1, n_cursos + 1):
        # Solo algunos prerrequisitos para mantener el grafo simple
        posibles_prereqs = list(range(1, i))
        prereqs = []
        
        for prereq_id in posibles_prereqs:
            if random.random() < densidad:
                prereqs.append(prereq_id)
        
        curso = {
            "id": i,
            "name": f"Materia {i}",
            "credits": random.randint(1, 4),
            "prereqs": prereqs
        }
        cursos.append(curso)
    
    return cursos

def prueba_rapida_random_schedule():
    """
    Prueba rápida del método random_schedule con tamaños pequeños.
    """
    print("=== Prueba Rápida: random_schedule ===")
    
    # Configuración para prueba rápida
    tamanos = [50, 100, 200, 300, 400, 500]  # Tamaños más pequeños
    densidad = 0.2  # Densidad baja para grafos simples
    max_credits = 18
    repeticiones = 2  # Menos repeticiones para velocidad
    
    resultados = {
        "tamanos": tamanos,
        "tiempos": [],
        "semestres_generados": [],
        "cursos_por_semestre": []
    }
    
    for n_cursos in tamanos:
        print(f"\nProbando con {n_cursos} cursos...")
        
        # Generar grafo
        cursos = generar_grafo_simple(n_cursos, densidad)
        
        # Crear archivo temporal
        temp_file = f"temp_test_{n_cursos}.json"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(cursos, f, ensure_ascii=False, indent=2)
        
        try:
            # Inicializar servicios
            courses_service = CoursesService()
            schedule_service = ScheduleService()
            
            # Cargar grafo
            resultado_carga = courses_service.load_graph_from_json(temp_file)
            if not resultado_carga.get('success'):
                print(f"  Error cargando grafo: {resultado_carga.get('message')}")
                continue
            
            # Sincronizar schedule service
            schedule_service.set_graph(courses_service.graph)
            
            # Medir tiempo
            tiempos_ejecucion = []
            semestres_totales = []
            cursos_promedio = []
            
            for _ in range(repeticiones):
                start_time = time.time()
                resultado = schedule_service.generate_random_schedule(max_credits)
                end_time = time.time()
                
                if resultado.get('success'):
                    tiempos_ejecucion.append(end_time - start_time)
                    semestres_totales.append(resultado.get('total_semesters', 0))
                    
                    # Calcular promedio de cursos por semestre
                    schedule = resultado.get('schedule', {})
                    if schedule:
                        cursos_por_sem = [len(sem['courses']) for sem in schedule.values()]
                        cursos_promedio.append(np.mean(cursos_por_sem))
                    else:
                        cursos_promedio.append(0)
                else:
                    print(f"  Error en ejecución: {resultado.get('message')}")
            
            # Guardar resultados
            if tiempos_ejecucion:
                resultados["tiempos"].append(np.mean(tiempos_ejecucion))
                resultados["semestres_generados"].append(np.mean(semestres_totales))
                resultados["cursos_por_semestre"].append(np.mean(cursos_promedio))
                
                print(f"  Tiempo promedio: {np.mean(tiempos_ejecucion):.6f} segundos")
                print(f"  Semestres generados: {np.mean(semestres_totales):.1f}")
                print(f"  Cursos por semestre: {np.mean(cursos_promedio):.1f}")
            else:
                resultados["tiempos"].append(0)
                resultados["semestres_generados"].append(0)
                resultados["cursos_por_semestre"].append(0)
                
        except Exception as e:
            print(f"  Excepción: {e}")
            resultados["tiempos"].append(0)
            resultados["semestres_generados"].append(0)
            resultados["cursos_por_semestre"].append(0)
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    return resultados

def generar_grafica_rapida(resultados: dict):
    """
    Genera gráficas para la prueba rápida.
    """
    plt.figure(figsize=(15, 5))
    
    # Gráfica 1: Tiempo de ejecución
    plt.subplot(1, 3, 1)
    plt.plot(resultados["tamanos"], resultados["tiempos"], marker='o', linewidth=2, markersize=8)
    plt.xlabel('Número de Cursos')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de Ejecución vs Tamaño')
    plt.grid(True, alpha=0.3)
    
    # Gráfica 2: Semestres generados
    plt.subplot(1, 3, 2)
    plt.plot(resultados["tamanos"], resultados["semestres_generados"], marker='s', linewidth=2, markersize=8, color='orange')
    plt.xlabel('Número de Cursos')
    plt.ylabel('Número de Semestres')
    plt.title('Semestres Generados vs Tamaño')
    plt.grid(True, alpha=0.3)
    
    # Gráfica 3: Cursos por semestre
    plt.subplot(1, 3, 3)
    plt.plot(resultados["tamanos"], resultados["cursos_por_semestre"], marker='^', linewidth=2, markersize=8, color='green')
    plt.xlabel('Número de Cursos')
    plt.ylabel('Cursos por Semestre')
    plt.title('Cursos por Semestre vs Tamaño')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('quick_random_schedule_test.png', dpi=300, bbox_inches='tight')
    plt.show()

def analizar_tendencia_rapida(resultados: dict):
    """
    Análisis rápido de la tendencia observada.
    """
    print("\n=== Análisis de Tendencia ===")
    
    tiempos = resultados["tiempos"]
    tamanos = resultados["tamanos"]
    
    # Calcular factor de crecimiento
    if len(tiempos) >= 2:
        print("Factores de crecimiento del tiempo:")
        for i in range(1, len(tiempos)):
            if tiempos[i-1] > 0:
                factor = tiempos[i] / tiempos[i-1]
                ratio_n = tamanos[i] / tamanos[i-1]
                print(f"  {tamanos[i-1]} → {tamanos[i]} cursos: factor tiempo = {factor:.2f}, ratio n = {ratio_n:.2f}")
        
        # Estimar complejidad
        if len(tiempos) >= 3:
            # Usar los últimos puntos
            n1, n2 = tamanos[-2], tamanos[-1]
            t1, t2 = tiempos[-2], tiempos[-1]
            
            if t1 > 0:
                ratio_n = n2 / n1
                ratio_t = t2 / t1
                exponente = np.log(ratio_t) / np.log(ratio_n)
                
                print(f"\nEstimación de complejidad:")
                print(f"  Exponente estimado: {exponente:.2f}")
                
                if exponente < 1.5:
                    print(f"  Complejidad estimada: O(n log n) o mejor")
                elif exponente < 2.5:
                    print(f"  Complejidad estimada: O(n²)")
                else:
                    print(f"  Complejidad estimada: O(n^{exponente:.1f})")

def main():
    """
    Función principal para la prueba rápida.
    """
    print("Iniciando prueba rápida del método random_schedule...")
    
    try:
        resultados = prueba_rapida_random_schedule()
        
        # Generar gráficas
        generar_grafica_rapida(resultados)
        
        # Análisis de tendencia
        analizar_tendencia_rapida(resultados)
        
        # Guardar resultados
        with open('quick_random_schedule_results.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        
        print("\n=== Prueba Rápida Completada ===")
        print("Resultados guardados en 'quick_random_schedule_results.json'")
        print("Gráficas guardadas en 'quick_random_schedule_test.png'")
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 