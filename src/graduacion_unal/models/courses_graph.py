from graduacion_unal.structures.hash import HashMap

class CoursesGraph:
    """
    Clase que representa un grafo dirigido de materias (Nodos), y prerrequisitos (Aristas)
    
    """

    def __init__(self):
        self.adjacency_list = HashMap()
        self.number_nodes: int = 0

    def add_node(self, value):
        """
        Añade un nodo al grafo.
        """
        pass

    def remove_node(self, value):
        """
        Elimina un nodo del grafo, y todas sus aristas adjacentes
        """
        pass

    def add_vertex(self):
        """
        Añade una arista al grafo (prerrequisito -> materia).
        Detecta si la arista añadida genera un ciclo en el grafo,
        En caso de detectar un ciclo debe lanzar un error.
        """
        pass 

    def remove_edge(self, prereq_id, course_id):
        """
        Elimina una arista (Prerrequisito).
        """


    def get_neighbors(self, course_id):
        """
        Retorna una lista de los sucesores de un nodo (Nodos que dependen de un curso).
        """
        return list(self.adjacency_list.get(course_id) or [])
    
    def __str__(self):
        lines = []
        for cid, neighbors in self.adjacency_list.items():
            lines.append(f"{cid} -> {neighbors}")
        return "\n".join(lines)