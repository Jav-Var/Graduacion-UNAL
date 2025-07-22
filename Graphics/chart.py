import pandas as pd
import matplotlib.pyplot as plt

# Gráfico de comparación de velocidad de distintos metodos
# cual es la eficiencia de:
'''
   has_cycle(): detecta ciclos en el grafo de cursos, asegurando que la planificación sea válida.
   generate_greedy_schedule()
Genera una sugerencia de materias por semestre tratando de optimizar el avance (más materias posibles por semestre).
'''

cycle5 = (0.108196 + 0.116130 + 0.110240 + 0.104920 + 0.121999)/5
cycle4 = (0.011042 + 0.014326 + 0.007716 + 0.015919 + 0.014844)/5
cycle3 = (0.002012 + 0.002009 + 0.002010 + 0.002013 + 0.002010)/5

random3 = (0.108614 + 0.130669 + 0.124312 + 0.116591 + 0.106091)/5
random4 = (11.770519 + 12.651165 + 12.751587 + 11.813576 + 12.074679)/5
random5 = None
# Tamaños de listas (puedes modificar hasta 100000 si hiciste pruebas más grandes)

load_graph5 = (1.689442 + 1.929522 + 1.805621 + 1.702393 + 1.757078)/5
load_graph4 = (0.155727 + 0.103114 + 0.093217 + 0.093273 + 0.097903)/5
load_graph3 = (0.012715 + 0.012832 + 0.016856 + 0.012615 + 0.011561)/5
sizes = [ 1000, 10000, 100000]#, 1000000, 10000000]

# Tiempos promedio de cada estructura por tamaño (en milisegundos)
# Reemplaza estos valores con los datos reales que mediste

_has_cycle = [ cycle3, cycle4, cycle5]       
generate_random_schedule = [ random3, random4, random5]         
load_graph_from_json = [load_graph3, load_graph4, load_graph5]  # Tiempos de load_graph_from_json por tamaño

# Crear DataFrame para visualizar los datos
df = pd.DataFrame({
    'Tamaño': sizes,
    '_has_cycle': _has_cycle,
    'generate_random_schedule': generate_random_schedule,
    'load_graph_from_json': load_graph_from_json
})

print(df)  # Mostrar tabla en consola

# Graficar los tiempos
plt.figure(figsize=(10, 7))
plt.plot(df['Tamaño'], df['_has_cycle'], marker='o', label='has_cycle')
plt.plot(df['Tamaño'], df['generate_random_schedule'], marker='s', label='generate_random_schedule')
plt.plot(df['Tamaño'], df['load_graph_from_json'], marker='^', label='load_graph_from_json')

plt.xscale('log')
plt.xlabel('Cantidad de materias (log scale)')
plt.ylabel('Tiempo promedio (ms)')
plt.title('Comparación de velocidad')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
