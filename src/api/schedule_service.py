from typing import List, Dict, Any, Optional
from graduacion_unal.models.courses_schedule import Schedule
from graduacion_unal.models.courses_graph import CoursesGraph
from graduacion_unal.models.User import User
import os
import uic
from PyQt5.QtWidgets import QMainWindow

class ScheduleService:
    """
    Servicio de API para manejar la lógica de planificación semestral.
    """
    
    def __init__(self):
        self.schedule = Schedule()
        self.graph: Optional[CoursesGraph] = None
    
    def set_graph(self, graph: CoursesGraph) -> None:
        """
        Establece el grafo de cursos para el servicio.
        
        Args:
            graph: Grafo de cursos cargado
        """
        self.graph = graph
    
    def get_course_tree(self, max_credits_per_semester: int = 18) -> Dict[str, Any]:
        """
        Obtiene el árbol de cursos disponibles organizados por niveles.
        
        Args:
            max_credits_per_semester: Límite de créditos por semestre
            
        Returns:
            Diccionario con información del árbol de cursos
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            course_tree = self.schedule.tree_of_availible_courses(max_credits_per_semester, self.graph)
            
            # Convertir a formato más legible
            tree_info = {}
            total_courses = 0
            
            for level, courses in course_tree.items():
                courses_info = []
                level_credits = 0
                
                for course_id in courses:
                    course = self.graph.get_course(course_id)
                    if course:
                        courses_info.append({
                            "id": course.id,
                            "name": course.name,
                            "credits": course.credits,
                            "prereqs": course.prereqs
                        })
                        level_credits += course.credits
                
                tree_info[level] = {
                    "courses": courses_info,
                    "total_courses": len(courses_info),
                    "total_credits": level_credits
                }
                total_courses += len(courses_info)
            
            return {
                "success": True,
                "course_tree": tree_info,
                "total_levels": len(course_tree),
                "total_courses": total_courses,
                "max_credits_per_semester": max_credits_per_semester
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "TREE_GENERATION_ERROR",
                "message": f"Error al generar el árbol de cursos: {str(e)}",
                "details": str(e)
            }
    
    def validate_schedule(self, schedule: Dict[int, List[int]], max_credits_per_semester: int = 18) -> Dict[str, Any]:
        """
        Valida una planificación de semestres.
        
        Args:
            schedule: Diccionario con la planificación de semestres
            max_credits_per_semester: Límite de créditos por semestre
            
        Returns:
            Diccionario con el resultado de la validación
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            validation_result = self.schedule.is_valid_schedule(schedule, self.graph, max_credits_per_semester)
            
            return {
                "success": True,
                "valid": validation_result["valid"],
                "errors": validation_result["errors"],
                "total_semesters": validation_result["total_semesters"],
                "total_courses": validation_result["total_courses"],
                "schedule": schedule
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "VALIDATION_ERROR",
                "message": f"Error al validar la planificación: {str(e)}",
                "details": str(e)
            }
    
    def generate_random_schedule(self, max_credits_per_semester: int = 18) -> Dict[str, Any]:
        """
        Genera una planificación aleatoria de semestres.
        
        Args:
            max_credits_per_semester: Límite de créditos por semestre
            
        Returns:
            Diccionario con la planificación generada
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            schedule = self.schedule.random_schedule(max_credits_per_semester, self.graph)
            
            # Validar la planificación generada
            validation_result = self.schedule.is_valid_schedule(schedule, self.graph, max_credits_per_semester)
            
            # Convertir a formato más detallado
            schedule_details = {}
            total_credits = 0
            
            for semester, courses in schedule.items():
                semester_info = []
                semester_credits = 0
                
                for course_id in courses:
                    course = self.graph.get_course(course_id)
                    if course:
                        semester_info.append({
                            "id": course.id,
                            "name": course.name,
                            "credits": course.credits,
                            "prereqs": course.prereqs
                        })
                        semester_credits += course.credits
                
                schedule_details[semester] = {
                    "courses": semester_info,
                    "total_courses": len(semester_info),
                    "total_credits": semester_credits
                }
                total_credits += semester_credits
            
            return {
                "success": True,
                "schedule": schedule_details,
                "total_semesters": len(schedule),
                "total_courses": sum(len(courses) for courses in schedule.values()),
                "total_credits": total_credits,
                "valid": validation_result["valid"],
                "errors": validation_result["errors"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "RANDOM_SCHEDULE_ERROR",
                "message": f"Error al generar planificación aleatoria: {str(e)}",
                "details": str(e)
            }
    
    def generate_greedy_schedule(self, max_credits_per_semester: int = 18) -> Dict[str, Any]:
        """
        Genera una planificación greedy que maximiza los créditos por semestre.
        
        Args:
            max_credits_per_semester: Límite de créditos por semestre
            
        Returns:
            Diccionario con la planificación generada
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            schedule = self.schedule.max_greedy_schedule(max_credits_per_semester, self.graph)
            
            # Validar la planificación generada
            validation_result = self.schedule.is_valid_schedule(schedule, self.graph, max_credits_per_semester)
            
            # Convertir a formato más detallado
            schedule_details = {}
            total_credits = 0
            
            for semester, courses in schedule.items():
                semester_info = []
                semester_credits = 0
                
                for course_id in courses:
                    course = self.graph.get_course(course_id)
                    if course:
                        semester_info.append({
                            "id": course.id,
                            "name": course.name,
                            "credits": course.credits,
                            "prereqs": course.prereqs
                        })
                        semester_credits += course.credits
                
                schedule_details[semester] = {
                    "courses": semester_info,
                    "total_courses": len(semester_info),
                    "total_credits": semester_credits
                }
                total_credits += semester_credits
            
            return {
                "success": True,
                "schedule": schedule_details,
                "total_semesters": len(schedule),
                "total_courses": sum(len(courses) for courses in schedule.values()),
                "total_credits": total_credits,
                "valid": validation_result["valid"],
                "errors": validation_result["errors"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "GREEDY_SCHEDULE_ERROR",
                "message": f"Error al generar planificación greedy: {str(e)}",
                "details": str(e)
            }
    
    def generate_personalized_schedule(self, user: User, max_credits_per_semester: int = 18) -> Dict[str, Any]:
        """
        Genera una planificación personalizada basada en el progreso del usuario.
        
        Args:
            user: Objeto User con el progreso actual
            max_credits_per_semester: Límite de créditos por semestre
            
        Returns:
            Diccionario con la planificación personalizada
        """
        if not self.graph:
            return {
                "success": False,
                "error": "GRAPH_NOT_LOADED",
                "message": "El grafo no ha sido cargado"
            }
        
        try:
            # Obtener cursos que el usuario puede tomar
            available_courses = self.graph.get_ready_courses(user.completed_courses)
            
            # Filtrar cursos que ya está tomando actualmente
            available_courses = [course for course in available_courses 
                              if course.id not in user.current_courses]
            
            # Organizar por semestres considerando el progreso actual
            schedule = {}
            current_semester = user.semester
            remaining_courses = available_courses.copy()
            
            while remaining_courses:
                semester_courses = []
                semester_credits = 0
                
                # Seleccionar cursos para el semestre actual
                for course in remaining_courses[:]:
                    if (semester_credits + course.credits) <= max_credits_per_semester:
                        semester_courses.append(course.id)
                        semester_credits += course.credits
                        remaining_courses.remove(course)
                    else:
                        break
                
                if semester_courses:
                    schedule[current_semester] = semester_courses
                    current_semester += 1
                else:
                    break
            
            # Convertir a formato detallado
            schedule_details = {}
            total_credits = 0
            
            for semester, courses in schedule.items():
                semester_info = []
                semester_credits = 0
                
                for course_id in courses:
                    course = self.graph.get_course(course_id)
                    if course:
                        semester_info.append({
                            "id": course.id,
                            "name": course.name,
                            "credits": course.credits,
                            "prereqs": course.prereqs
                        })
                        semester_credits += course.credits
                
                schedule_details[semester] = {
                    "courses": semester_info,
                    "total_courses": len(semester_info),
                    "total_credits": semester_credits
                }
                total_credits += semester_credits
            
            return {
                "success": True,
                "schedule": schedule_details,
                "total_semesters": len(schedule),
                "total_courses": sum(len(courses) for courses in schedule.values()),
                "total_credits": total_credits,
                "user_progress": {
                    "completed_courses": len(user.completed_courses),
                    "current_semester": user.semester,
                    "total_credits_completed": user.total_credits
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": "PERSONALIZED_SCHEDULE_ERROR",
                "message": f"Error al generar planificación personalizada: {str(e)}",
                "details": str(e)
            }

    def cargar_ver_arbol(self, ui_dir):
        self.limpiar_panel()
        ui_file = os.path.join(ui_dir, 'VerArbolMaterias.ui')
        widget = uic.loadUi(ui_file)
        self.panel_layout.addWidget(widget, alignment=Qt.AlignCenter)
        widget.ButtonVerArbol.clicked.connect(lambda: self.mostrar_arbol(widget))

    def mostrar_arbol(self, widget):
        resultado = self.get_course_tree()
        if resultado["success"]:
            texto = ""
            for nivel, info in resultado["course_tree"].items():
                texto += f"Nivel {nivel}:\n"
                for curso in info["courses"]:
                    texto += f"  {curso['id']} - {curso['name']} ({curso['credits']} créditos)\n"
            widget.TextArbol.setPlainText(texto)
        else:
            widget.TextArbol.setPlainText("Error: " + resultado["message"]) 