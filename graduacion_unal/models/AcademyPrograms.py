#### PARA LA SIGUIENTE VERSION DE LA ENTREGA
## PARA MANEJAR TIPOS DE MATERIAS Y VARIOS USUARIOS

class AcademyProgram:
    def __init__(self, name: str, credits: int, courses: List[Course]):
        self.name = name
        self.credits = credits
        self.obligatory_courses = []
        self.credits_of_elective_courses= 0 
        self.optative_courses_blocks = {}
        

    def build_graph(self):
        self.graph = Graph()
        for course in self.courses:
            self.graph.add_course(course)



    def _set_blocks(self):
        """
        Ejemplo de bloqe 
        {
            "bloque_de_optativas1": {
                "materias_disponibles": [1,2,3,4]
                "creditos_exigidos": 10 
            },
            "bloque_de_optativas2": {
                "materias_disponibles": [5,6,7,8]
                "creditos_exigidos": 10 
            },
        
        }
        """

    def _set_obligatory_courses(self):
        """
        Ejemplo de obligatorias (por id de la materia):
        [1,2,3,4]
        """

    def _set_credits_of_elective_courses(self, credits: int = 0):
        """
        Ejemplo de creditos de optativas:
        10
        """
        if type(credits) != int:
            raise ValueError("Los creditos deben ser un numero entero") 
        self.credits_of_elective_courses = credits



