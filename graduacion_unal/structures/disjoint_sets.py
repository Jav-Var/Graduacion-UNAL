class DisjointSets:
    """
    Implementación de Conjuntos Disjuntos (Disjoint Sets) con optimizaciones.
    
    Esta estructura de datos mantiene una colección de conjuntos disjuntos,
    donde cada conjunto tiene un representante único. Las operaciones principales
    son find (encontrar el representante) y union (unir dos conjuntos).
    
    Optimizaciones implementadas:
    - Path compression en find()
    - Union by rank en union()
    """
    
    def __init__(self, size: int):
        """
        Inicializa los conjuntos disjuntos.
        
        Args:
            size: Numero total de elementos (0 a size-1)
        """
        self.parent = list(range(size))  # Cada elemento es su propio padre inicialmente
        self.rank = [0] * size          # Altura del árbol para optimización
        self.size = size
        self.num_sets = size            # Número de conjuntos disjuntos
    
    def find(self, x: int) -> int:
        """
        Encuentra el representante (raíz) del conjunto que contiene x.
        Implementa path compression para optimización.
        
        Args:
            x: Elemento cuyo representante queremos encontrar
            
        Returns:
            El representante del conjunto que contiene x
            
        Raises:
            IndexError: Si x está fuera del rango válido
        """
        if x < 0 or x >= self.size:
            raise IndexError(f"Índice {x} fuera del rango [0, {self.size-1}]")
        
        # Path compression: hacer que todos los nodos en el camino apunten directamente a la raíz
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        Une los conjuntos que contienen x e y.
        Implementa union by rank para optimización.
        
        Args:
            x: Primer elemento
            y: Segundo elemento
            
        Returns:
            True si los conjuntos se unieron, False si ya estaban en el mismo conjunto
            
        Raises:
            IndexError: Si x o y están fuera del rango válido
        """
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            raise IndexError(f"Índices fuera del rango [0, {self.size-1}]")
        
        root_x = self.find(x)
        root_y = self.find(y)
        
        # Si ya están en el mismo conjunto, no hacer nada
        if root_x == root_y:
            return False
        
        # Union by rank: conectar el árbol más pequeño al más grande
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            # Si tienen el mismo rank, conectar uno al otro y aumentar el rank
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.num_sets -= 1
        return True
    
    def connected(self, x: int, y: int) -> bool:
        """
        Verifica si dos elementos están en el mismo conjunto.
        
        Args:
            x: Primer elemento
            y: Segundo elemento
            
        Returns:
            True si x e y están en el mismo conjunto, False en caso contrario
        """
        return self.find(x) == self.find(y)
    
    def get_set_size(self, x: int) -> int:
        """
        Obtiene el tamaño del conjunto que contiene x.
        
        Args:
            x: Elemento del conjunto
            
        Returns:
            Número de elementos en el conjunto que contiene x
        """
        root = self.find(x)
        count = 0
        for i in range(self.size):
            if self.find(i) == root:
                count += 1
        return count
    
    def get_all_sets(self) -> dict:
        """
        Obtiene todos los conjuntos disjuntos.
        
        Returns:
            Diccionario donde las claves son los representantes y los valores
            son listas de elementos en cada conjunto
        """
        sets = {}
        for i in range(self.size):
            root = self.find(i)
            if root not in sets:
                sets[root] = []
            sets[root].append(i)
        return sets
    
    def get_num_sets(self) -> int:
        """
        Obtiene el número actual de conjuntos disjuntos.
        
        Returns:
            Número de conjuntos disjuntos
        """
        return self.num_sets
    
    def reset(self):
        """
        Reinicia la estructura a su estado inicial.
        """
        self.parent = list(range(self.size))
        self.rank = [0] * self.size
        self.num_sets = self.size
    
    def __str__(self) -> str:
        """
        Representación en string de la estructura.
        """
        sets = self.get_all_sets()
        result = f"DisjointSets(size={self.size}, sets={self.num_sets}):\n"
        for root, elements in sets.items():
            result += f"  Set {root}: {elements}\n"
        return result.rstrip()
    
    def __repr__(self) -> str:
        return f"DisjointSets(size={self.size}, sets={self.num_sets})"

        