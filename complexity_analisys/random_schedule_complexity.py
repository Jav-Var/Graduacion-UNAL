import time
import json
import random
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
import os

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from graduacion_unal.api.courses_service import CoursesService
from graduacion_unal.api.schedule_service import ScheduleService

def generar_grafo_aleatorio(n_cursos: int, densidad: float = 0.3) -> list:
    """
    Genera un grafo aleatorio de cursos con n_cursos nodos y densidad de aristas dada.
    
    Args:
        n_cursos: Número de cursos a generar
        densidad: Probabilidad de que exista una arista entre dos nodos (0-1)
    
    Returns:
        Lista de diccionarios con la información de los cursos
    """
    cursos = []
    
    for i in range(1, n_cursos + 1):
        # Generar prerrequisitos aleatorios (solo de cursos con ID menor para evitar ciclos)
        posibles_prereqs = list(range(1, i))
        prereqs = []
        
        for prereq_id in posibles_prereqs:
            if random.random() < densidad:
                prereqs.append(prereq_id)
        
        curso = {
            "id": i,
            "name": f"Materia {i}",
            "credits": random.randint(1, 4),  # 1-4 créditos por materia
            "prereqs": prereqs
        }
        cursos.append(curso)
    
    return cursos

def medir_tiempo_random_schedule(n_cursos: int, densidad: float = 0.3, max_credits: int = 18, repeticiones: int = 5) -> float:
    """
    Mide el tiempo de ejecución del método random_schedule para un grafo de n_cursos.
    
    Args:
        n_cursos: Número de cursos en el grafo
        densidad: Densidad de aristas del grafo
        max_credits: Máximo de créditos por semestre
        repeticiones: Número de repeticiones para promediar
    
    Returns:
        Tiempo promedio de ejecución en segundos
    """
    tiempos = []
    
    for _ in range(repeticiones):
        # Generar grafo aleatorio
        cursos = generar_grafo_aleatorio(n_cursos, densidad)
        
        # Crear archivo temporal
        temp_file = f"temp_courses_{n_cursos}.json"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(cursos, f, ensure_ascii=False, indent=2)
        
        try:
            # Inicializar servicios
            courses_service = CoursesService()
            schedule_service = ScheduleService()
            
            # Cargar grafo
            resultado_carga = courses_service.load_graph_from_json(temp_file)
            if not resultado_carga.get('success'):
                print(f"Error cargando grafo de {n_cursos} cursos: {resultado_carga.get('message')}")
                continue
            
            # Sincronizar schedule service
            schedule_service.set_graph(courses_service.graph)
            
            # Medir tiempo de random_schedule
            start_time = time.time()
            resultado = schedule_service.generate_random_schedule(max_credits)
            end_time = time.time()
            
            if resultado.get('success'):
                tiempos.append(end_time - start_time)
            else:
                print(f"Error en random_schedule para {n_cursos} cursos: {resultado.get('message')}")
                
        except Exception as e:
            print(f"Excepción para {n_cursos} cursos: {e}")
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    return np.mean(tiempos) if tiempos else 0.0

def analizar_complejidad_random_schedule():
    """
    Realiza el análisis de complejidad empírico del método random_schedule.
    """
    print("=== Análisis de Complejidad Empírico: random_schedule ===")
    
    # Configuración del análisis
    tamanos = [100, 500, 1000, 2000, 3000, 4000, 5000]  # Número de cursos
    densidades = [0.1, 0.3, 0.5]  # Diferentes densidades de grafo
    max_credits = 18
    repeticiones = 3
    
    resultados = {}
    
    for densidad in densidades:
        print(f"\n--- Analizando con densidad {densidad} ---")
        tiempos_densidad = []
        
        for n_cursos in tamanos:
            print(f"  Probando con {n_cursos} cursos...")
            tiempo_promedio = medir_tiempo_random_schedule(n_cursos, densidad, max_credits, repeticiones)
            tiempos_densidad.append(tiempo_promedio)
            print(f"    Tiempo promedio: {tiempo_promedio:.6f} segundos")
        
        resultados[f"densidad_{densidad}"] = {
            "tamanos": tamanos,
            "tiempos": tiempos_densidad
        }
    
    # Generar gráficas
    generar_graficas_complejidad(resultados, tamanos)
    
    # Análisis teórico
    analizar_complejidad_teorica(tamanos, resultados)
    
    return resultados

def generar_graficas_complejidad(resultados: dict, tamanos: list):
    """
    Genera gráficas de complejidad para diferentes densidades.
    """
    plt.figure(figsize=(15, 10))
    
    # Gráfica 1: Tiempo vs Tamaño para diferentes densidades
    plt.subplot(2, 2, 1)
    for densidad_key, data in resultados.items():
        densidad = densidad_key.split('_')[1]
        plt.plot(data['tamanos'], data['tiempos'], marker='o', label=f'Densidad {densidad}')
    
    plt.xlabel('Número de Cursos (n)')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Tiempo de Ejecución vs Tamaño del Grafo')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    
    # Gráfica 2: Comparación con complejidades teóricas
    plt.subplot(2, 2, 2)
    for densidad_key, data in resultados.items():
        densidad = densidad_key.split('_')[1]
        plt.plot(data['tamanos'], data['tiempos'], marker='o', label=f'Densidad {densidad}')
    
    # Líneas de referencia para complejidades teóricas
    n_array = np.array(tamanos)
    plt.plot(n_array, n_array * np.log(n_array) * 1e-6, '--', label='O(n log n)', alpha=0.7)
    plt.plot(n_array, n_array**2 * 1e-7, '--', label='O(n²)', alpha=0.7)
    
    plt.xlabel('Número de Cursos (n)')
    plt.ylabel('Tiempo (segundos)')
    plt.title('Comparación con Complejidades Teóricas')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
    
    # Gráfica 3: Tiempo por densidad
    plt.subplot(2, 2, 3)
    densidades = []
    tiempos_promedio = []
    
    for densidad_key, data in resultados.items():
        densidad = float(densidad_key.split('_')[1])
        tiempo_promedio = np.mean(data['tiempos'])
        densidades.append(densidad)
        tiempos_promedio.append(tiempo_promedio)
    
    plt.bar(densidades, tiempos_promedio)
    plt.xlabel('Densidad del Grafo')
    plt.ylabel('Tiempo Promedio (segundos)')
    plt.title('Impacto de la Densidad en el Tiempo de Ejecución')
    plt.grid(True, alpha=0.3)
    
    # Gráfica 4: Análisis de escalabilidad
    plt.subplot(2, 2, 4)
    for densidad_key, data in resultados.items():
        densidad = densidad_key.split('_')[1]
        # Calcular factor de crecimiento
        factores = []
        for i in range(1, len(data['tiempos'])):
            if data['tiempos'][i-1] > 0:
                factor = data['tiempos'][i] / data['tiempos'][i-1]
                factores.append(factor)
        
        if factores:
            plt.plot(data['tamanos'][1:], factores, marker='s', label=f'Densidad {densidad}')
    
    plt.xlabel('Número de Cursos (n)')
    plt.ylabel('Factor de Crecimiento')
    plt.title('Factor de Crecimiento del Tiempo')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('random_schedule_complexity_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def analizar_complejidad_teorica(tamanos: list, resultados: dict):
    """
    Realiza análisis teórico de la complejidad observada.
    """
    print("\n=== Análisis Teórico de Complejidad ===")
    
    # Analizar cada densidad
    for densidad_key, data in resultados.items():
        densidad = densidad_key.split('_')[1]
        print(f"\n--- Densidad {densidad} ---")
        
        tiempos = data['tiempos']
        n_values = data['tamanos']
        
        # Calcular complejidad empírica
        if len(tiempos) >= 2:
            # Usar los últimos puntos para calcular la complejidad
            n1, n2 = n_values[-2], n_values[-1]
            t1, t2 = tiempos[-2], tiempos[-1]
            
            if t1 > 0:
                ratio_n = n2 / n1
                ratio_t = t2 / t1
                
                # Estimar exponente de complejidad
                if ratio_t > 0:
                    exponente = np.log(ratio_t) / np.log(ratio_n)
                    print(f"  Ratio n: {ratio_n:.2f}")
                    print(f"  Ratio tiempo: {ratio_t:.2f}")
                    print(f"  Exponente estimado: {exponente:.2f}")
                    
                    if exponente < 1.5:
                        complejidad = "O(n log n) o mejor"
                    elif exponente < 2.5:
                        complejidad = "O(n²)"
                    else:
                        complejidad = f"O(n^{exponente:.1f})"
                    
                    print(f"  Complejidad estimada: {complejidad}")
        
        # Análisis de tendencia
        if len(tiempos) >= 3:
            # Calcular factor de crecimiento promedio
            factores = []
            for i in range(1, len(tiempos)):
                if tiempos[i-1] > 0:
                    factor = tiempos[i] / tiempos[i-1]
                    factores.append(factor)
            
            if factores:
                factor_promedio = np.mean(factores)
                print(f"  Factor de crecimiento promedio: {factor_promedio:.2f}")

def main():
    """
    Función principal para ejecutar el análisis de complejidad.
    """
    print("Iniciando análisis de complejidad del método random_schedule...")
    
    try:
        resultados = analizar_complejidad_random_schedule()
        
        # Guardar resultados en JSON
        with open('random_schedule_complexity_results.json', 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        
        print("\n=== Análisis Completado ===")
        print("Resultados guardados en 'random_schedule_complexity_results.json'")
        print("Gráficas guardadas en 'random_schedule_complexity_analysis.png'")
        
    except Exception as e:
        print(f"Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 