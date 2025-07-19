import pandas as pd
import matplotlib.pyplot as plt

# Gráfico de comparación de velocidad de distintos metodos
# cual es la eficiencia de:
'''

   has_cycle(): detecta ciclos en el grafo de cursos, asegurando que la planificación sea válida.
   generate_greedy_schedule()
Genera una sugerencia de materias por semestre tratando de optimizar el avance (más materias posibles por semestre).
'''

# Tamaños de listas (puedes modificar hasta 100000 si hiciste pruebas más grandes)
sizes = [100, 1000, 10000, 100000]#, 1000000, 10000000]

# Tiempos promedio de cada estructura por tamaño (en milisegundos)
# Reemplaza estos valores con los datos reales que mediste
times_simple = [0, 3, 397, 44373]       # SimpleLinkedList
times_tail = [0, 3, 455, 50528]         # LinkedListWithTail
times_double = [0, 0, 0, 2]       # DoublyLinkedList

# Crear DataFrame para visualizar los datos
df = pd.DataFrame({
    'Tamaño': sizes,
    'SimpleLinkedList': times_simple,
    'LinkedListWithTail': times_tail,
    'DoublyLinkedList': times_double
})

print(df)  # Mostrar tabla en consola

# Graficar los tiempos
plt.figure(figsize=(10, 7))
plt.plot(df['Tamaño'], df['SimpleLinkedList'], marker='o', label='SimpleLinkedList')
plt.plot(df['Tamaño'], df['LinkedListWithTail'], marker='s', label='LinkedListWithTail')
plt.plot(df['Tamaño'], df['DoublyLinkedList'], marker='^', label='DoublyLinkedList')

plt.xscale('log')
plt.xlabel('Tamaño de la lista (log scale)')
plt.ylabel('Tiempo promedio (ms)')
plt.title('Comparación de velocidad - Método addAfter')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
