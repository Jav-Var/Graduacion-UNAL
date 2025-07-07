
from src.graduacion_unal.models.courses_graph import CoursesGraph

class Schedule:
    """
    Metodo para una planificacion de semestres valida.

    """

    def __init__(self):
        pass

    def min_semesters_to_complete(self, max_credits_per_semester: int, courses_graph: CoursesGraph):
        """
        Metodo para calcular el numero minimo de semestres necesarios para completar el plan de estudios.
        """
        pass

    def is_valid_schedule(self, schedule: list[list[int]], courses_graph: CoursesGraph):
        """
        Metodo para verificar si una planificacion de semestres es valida. Con base a los prerequisitos y un tope de creditos por semestre.
        """
        pass


    def random_schedule(self, max_credits_per_semester: int, courses_graph: CoursesGraph):
        """
        Metodo para generar una planificacion de semestres aleatoria.
        """
        pass