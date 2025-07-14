import sys
import os
from pathlib import Path
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMessageBox, QVBoxLayout, QLabel, QFrame, QFileDialog, QAction, QApplication
)

from graduacion_unal.gui import resources_rc
from graduacion_unal.api.courses_service import CoursesService
from pprint import pprint
"""
    Este es un archivo para probar la interfaz, no es la aplicacion final.
"""

def load_stylesheet(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

        
class MainWindow(QtWidgets.QMainWindow):
    """
    Ventana principal de la aplicacion.
    
    """
    
    def __init__(self):
        super().__init__()

        # Determina la ruta al directorio donde están los archivos de interfaz .ui
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_dir = script_dir + "/ui"

        # Verificar existencia del directorio ui_dir
        if not os.path.isdir(ui_dir):
            raise FileNotFoundError(f"No se encontró la carpeta de UI en {ui_dir}")

        # Cargar la interfaz principal
        main_ui = os.path.join(ui_dir, 'MainWindow.ui')
        if not os.path.isfile(main_ui):
            raise FileNotFoundError(f"No se encontró {main_ui}")
        uic.loadUi(main_ui, self)

        # Configurar titulo
        self.setWindowTitle("Planificador de Ruta Académica UNAL")

        self.resize(1500, 800)         # Tamaño inicial (ancho x alto)
        self.setMinimumSize(900, 600)

        # Referenciar widgets importantes
        self.panel = self.findChild(QtWidgets.QWidget, 'panel')
        self.sidebar = self.findChild(QtWidgets.QWidget, 'sidebar')

        # === Configuracion de la API === #

        # Instancia el servicio de cursos
        self.courses_service = CoursesService()

        # === Configuracion de layout y botones === #

        # Obtener el layout existente (En el .ui) en lugar de crear uno nuevo
        self.panel_layout = self.panel.layout()

        # Si no tenía layout, crear uno (Por seguridad)
        if self.panel_layout is None:
            self.panel_layout = QtWidgets.QVBoxLayout(self.panel)
            self.panel_layout.setContentsMargins(0, 0, 0, 0)

        # Configurar menú
        self.setup_menu()
        
        # Conectar botones de la sidebar
        self.asignar_botones(ui_dir)
        
        # Cargar archivo de ejemplo por defecto
        # self.cargar_archivo_ejemplo() El archivo se esta cargando en el main para que primero se muestre la ventana

    def setup_menu(self):
        """Configura el menú de la aplicación."""
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu('Archivo')
        
        # Acción Abrir
        open_action = QAction('Abrir archivo JSON', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.abrir_archivo)
        file_menu.addAction(open_action)
        
        # Acción Guardar
        save_action = QAction('Guardar como...', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.guardar_archivo)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        # Acción Cargar ejemplo
        example_action = QAction('Cargar archivo de ejemplo', self)
        example_action.triggered.connect(self.cargar_archivo)
        file_menu.addAction(example_action)
        
        # Menú Ver
        view_menu = menubar.addMenu('Ver')
        
        # Acción Información del grafo
        info_action = QAction('Información del grafo', self)
        info_action.triggered.connect(self.mostrar_info_grafo)
        view_menu.addAction(info_action)

    def abrir_archivo(self):
        """Abre un archivo JSON de materias."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo de materias",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        
        if file_path:
            self.cargar_archivo(file_path)

    def guardar_archivo(self):
        """Guarda el grafo actual en un archivo JSON."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar archivo de materias",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        
        if file_path:
            resultado = self.courses_service.save_graph_to_json(file_path)
            if resultado.get('success'):
                QMessageBox.information(self, "Archivo guardado", resultado['message'])
            else:
                QMessageBox.critical(self, "Error al guardar", resultado.get('message', 'Error desconocido'))

    def cargar_archivo_ejemplo(self):
        """Carga el archivo de ejemplo por defecto."""
        # Buscar el archivo de ejemplo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        example_file = os.path.join(script_dir, "..", "..", "data", "courses.json")
        
        if os.path.exists(example_file):
            self.cargar_archivo(example_file)
        else:
            QMessageBox.warning(self, "Archivo no encontrado", 
                               f"No se encontró el archivo de ejemplo: {example_file}")

    def cargar_archivo(self, file_path):
        """Carga un archivo JSON de materias."""
        resultado = self.courses_service.load_graph_from_json(file_path)
        
        if resultado.get('success'):
            QMessageBox.information(self, "Archivo cargado", resultado['message'])
            # Actualizar título de la ventana
            self.setWindowTitle(f"Graduacion UNAL - {os.path.basename(file_path)}")
        else:
            QMessageBox.critical(self, "Error al cargar archivo", resultado.get('message', 'Error desconocido'))

    def mostrar_info_grafo(self):
        """Muestra información del grafo actual."""
        info = self.courses_service.get_graph_info()
        
        if info.get('success'):
            mensaje = f"""
Información del Grafo:
• Total de materias: {info['total_courses']}
• Sin prerrequisitos: {info['courses_without_prereqs']}
• Con prerrequisitos: {info['courses_with_prereqs']}
• Total créditos: {info['total_credits']}
• Tiene ciclos: {'Sí' if info['has_cycle'] else 'No'}
• Archivo actual: {info['current_file'] or 'Ninguno'}
• Modificado: {'Sí' if info['is_modified'] else 'No'}
            """
            QMessageBox.information(self, "Información del Grafo", mensaje.strip())
        else:
            QMessageBox.critical(self, "Error", info.get('message', 'Error desconocido'))

    def limpiar_panel(self):
        """
        Elimina **todo** del panel: widgets y layouts anidados.
        """
        while self.panel_layout.count():
            item = self.panel_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _clear_layout(self, layout):
        """
        Limpia recursivamente un QLayout (widgets y sub-layouts), y luego lo marca para eliminación.
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._clear_layout(child.layout())
        # Marcar el layout para eliminación segura por Qt
        layout.deleteLater()

    def cambiar_menu(self, menu: str, ui_dir: str):
        """
            Carga el archivo .ui pasado como argumento y actualiza el panel con la nueva interfaz
            Argumentos:
                Nombre del archivo .ui (Sin la extension)
        """
        self.limpiar_panel()
        ui_file = os.path.join(ui_dir, f"{menu}.ui")
        if not os.path.isfile(ui_file):
            print(f"[ERROR] No se encontró {ui_file}")
            return
        try:
            materia_widget = uic.loadUi(ui_file)
            self.panel_layout.addWidget(materia_widget, alignment=Qt.AlignCenter)
            
            # Configurar cada menú específico
            if menu == 'AñadirMateria':
                self.setup_add_materia(materia_widget)
            elif menu == 'AñadirPrerrequisito':
                self.setup_add_prerrequisito(materia_widget)
            elif menu == 'EliminarMateria':
                self.setup_eliminar_materia(materia_widget)
            elif menu == 'EliminarPrerrequisito':
                self.setup_eliminar_prerrequisito(materia_widget)
            elif menu == 'VerMaterias':
                self.setup_ver_materias(materia_widget)
                
        except Exception as e:
            print(f"[ERROR] Error cargando {menu}: {e}")

    def asignar_botones(self, ui_dir: str):
        mappings = {
            'ButtonAgregarMateria':        'AñadirMateria',
            'ButtonAgregarPrerrequisito':  'AñadirPrerrequisito',
            'ButtonEliminarMateria':       'EliminarMateria',
            'ButtonEliminarPrerrequisito': 'EliminarPrerrequisito',
            'ButtonVerMaterias':           'VerMaterias',
            'ButtonSugerenciaAleatoria':   'SugerenciaAleatoria',
            'ButtonVerCaminosMaterias':    'VerCaminosMaterias',
            'ButtonGuardar':               'Guardar',
            'ButtonCargarArchivo':         'CargarArchivo'
        }
        # Botones de cambio de menú o acción
        for obj_name, menu_name in mappings.items():
            btn = self.findChild(QtWidgets.QPushButton, obj_name)
            if not btn:
                print(f"[ERROR] no encontré botón con objectName='{obj_name}'")
                continue
            print(f"[OK] Conectando {obj_name} → cambiar_menu('{menu_name}')")
            if menu_name == 'VerCaminosMaterias':
                btn.clicked.connect(self.setup_ver_caminos_materias)
            elif menu_name == 'SugerenciaAleatoria':
                btn.clicked.connect(self.setup_sugerencia_aleatoria)
            elif menu_name == 'Guardar':
                btn.clicked.connect(self.guardar_archivo_panel)
            elif menu_name == 'CargarArchivo':
                btn.clicked.connect(self.cargar_archivo_panel)
            else:
                btn.clicked.connect(lambda _, m=menu_name: self.cambiar_menu(m, ui_dir))

    def guardar_archivo_panel(self):
        """Guarda el grafo actual en el archivo actual o pide ruta si no hay."""
        file_path = self.courses_service.get_current_file_path()
        if not file_path:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Guardar archivo de materias",
                "",
                "Archivos JSON (*.json);;Todos los archivos (*)"
            )
            if not file_path:
                return
        resultado = self.courses_service.save_graph_to_json(file_path)
        if resultado.get('success'):
            QMessageBox.information(self, "Archivo guardado", resultado['message'])
        else:
            QMessageBox.critical(self, "Error al guardar", resultado.get('message', 'Error desconocido'))
        # Sincronizar ScheduleService
        self.sincronizar_schedule_service()

    def cargar_archivo_panel(self):
        """Carga un archivo JSON de materias desde cualquier ubicación."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Abrir archivo de materias",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )
        if file_path:
            resultado = self.courses_service.load_graph_from_json(file_path)
            if resultado.get('success'):
                QMessageBox.information(self, "Archivo cargado", resultado['message'])
                self.setWindowTitle(f"Graduacion UNAL - {os.path.basename(file_path)}")
            else:
                QMessageBox.critical(self, "Error al cargar archivo", resultado.get('message', 'Error desconocido'))
            # Sincronizar ScheduleService
            self.sincronizar_schedule_service()

    def sincronizar_schedule_service(self):
        """Actualiza el grafo de ScheduleService para mantenerlo sincronizado."""
        if not hasattr(self, 'schedule_service'):
            from graduacion_unal.api.schedule_service import ScheduleService
            self.schedule_service = ScheduleService()
        self.schedule_service.set_graph(self.courses_service.graph)

    def setup_add_materia(self, widget):
        """
        Conecta los campos y el botón de AñadirMateria.ui con la API.
        """
        # Referencias a los campos
        input_name    = widget.findChild(QtWidgets.QLineEdit, 'InputNombre')
        input_id      = widget.findChild(QtWidgets.QLineEdit, 'InputID')
        input_credits = widget.findChild(QtWidgets.QLineEdit, 'InputCreditos')
        btn_add       = widget.findChild(QtWidgets.QPushButton, 'buttonAgregar')

        def on_add_clicked():
            # Leer y validar datos
            print("[DEBUG] Boton presionado: Añadir Materia")
            try:
                course_data = {
                    'id':      int(input_id.text()),
                    'name':    input_name.text().strip(),
                    'credits': int(input_credits.text()),
                    'prereqs': []  # Por defecto sin prerrequisitos
                }
            except ValueError:
                QMessageBox.warning(widget, "Datos inválidos",
                                    "ID y créditos deben ser números enteros.")
                return

            # Validar que los campos no estén vacíos
            if not course_data['name']:
                QMessageBox.warning(widget, "Datos inválidos",
                                    "El nombre de la materia no puede estar vacío.")
                return

            # Llamar al servicio
            resultado = self.courses_service.add_course(course_data)

            # Mostrar resultado
            if resultado.get('success'):
                QMessageBox.information(widget, "Curso añadido",
                                        resultado['message'])
                # Limpiar campos
                input_name.clear()
                input_id.clear()
                input_credits.clear()
            else:
                QMessageBox.critical(widget, "Error al añadir curso",
                                     resultado.get('message', 'Error desconocido'))

        btn_add.clicked.connect(on_add_clicked)

    def setup_add_prerrequisito(self, widget):
        """
        Conecta los campos y el botón de AñadirPrerrequisito.ui con la API.
        """
        # Referencias a los campos
        input_id_materia = widget.findChild(QtWidgets.QLineEdit, 'InputID')
        input_id_prereq  = widget.findChild(QtWidgets.QLineEdit, 'InputIDPrerreq')
        btn_add          = widget.findChild(QtWidgets.QPushButton, 'pushButton')

        def on_add_clicked():
            print("[DEBUG] Boton presionado: Añadir Prerrequisito")
            try:
                course_id = int(input_id_materia.text())
                prereq_id = int(input_id_prereq.text())
            except ValueError:
                QMessageBox.warning(widget, "Datos inválidos",
                                    "Los IDs deben ser números enteros.")
                return

            # Llamar al servicio
            resultado = self.courses_service.add_prerequisite(prereq_id, course_id)

            # Mostrar resultado
            if resultado.get('success'):
                QMessageBox.information(widget, "Prerrequisito añadido",
                                        resultado['message'])
                # Limpiar campos
                input_id_materia.clear()
                input_id_prereq.clear()
            else:
                QMessageBox.critical(widget, "Error al añadir prerrequisito",
                                     resultado.get('message', 'Error desconocido'))

        btn_add.clicked.connect(on_add_clicked)

    def setup_eliminar_materia(self, widget):
        """
        Conecta los campos y el botón de EliminarMateria.ui con la API.
        """
        # Referencias a los campos
        input_id = widget.findChild(QtWidgets.QLineEdit, 'InputID')
        btn_eliminar = widget.findChild(QtWidgets.QPushButton, 'pushButton')

        def on_eliminar_clicked():
            print("[DEBUG] Boton presionado: Eliminar Materia")
            try:
                course_id = int(input_id.text())
            except ValueError:
                QMessageBox.warning(widget, "Datos inválidos",
                                    "El ID debe ser un número entero.")
                return

            # Confirmar eliminación
            reply = QMessageBox.question(widget, "Confirmar eliminación",
                                        "¿Estás seguro de que quieres eliminar esta materia?",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Llamar al servicio
                resultado = self.courses_service.remove_course(course_id)

                # Mostrar resultado
                if resultado.get('success'):
                    QMessageBox.information(widget, "Materia eliminada",
                                            resultado['message'])
                    # Limpiar campo
                    input_id.clear()
                else:
                    QMessageBox.critical(widget, "Error al eliminar materia",
                                         resultado.get('message', 'Error desconocido'))

        btn_eliminar.clicked.connect(on_eliminar_clicked)

    def setup_eliminar_prerrequisito(self, widget):
        """
        Conecta los campos y el botón de EliminarPrerrequisito.ui con la API.
        """
        # Referencias a los campos
        input_id_materia = widget.findChild(QtWidgets.QLineEdit, 'InputID')
        input_id_prereq  = widget.findChild(QtWidgets.QLineEdit, 'InputIDPrerreq')
        btn_eliminar     = widget.findChild(QtWidgets.QPushButton, 'pushButton')

        def on_eliminar_clicked():
            print("[DEBUG] Boton presionado: Eliminar Prerrequisito")
            try:
                course_id = int(input_id_materia.text())
                prereq_id = int(input_id_prereq.text())
            except ValueError:
                QMessageBox.warning(widget, "Datos inválidos",
                                    "Los IDs deben ser números enteros.")
                return

            # Llamar al servicio
            resultado = self.courses_service.remove_prerequisite(prereq_id, course_id)

            # Mostrar resultado
            if resultado.get('success'):
                QMessageBox.information(widget, "Prerrequisito eliminado",
                                        resultado['message'])
                # Limpiar campos
                input_id_materia.clear()
                input_id_prereq.clear()
            else:
                QMessageBox.critical(widget, "Error al eliminar prerrequisito",
                                     resultado.get('message', 'Error desconocido'))

        btn_eliminar.clicked.connect(on_eliminar_clicked)

    def setup_ver_materias(self, widget):
        """
        Conecta la vista de VerMaterias.ui con la API para mostrar todas las materias.
        """

        #self.limpiar_panel()

        # Referencias a los widgets
        scroll_area = widget.findChild(QtWidgets.QScrollArea, 'ScrollMaterias')
        contenido = scroll_area.findChild(QtWidgets.QWidget, 'Contenido')
        
        # Crear layout para el contenido
        layout = QVBoxLayout(contenido)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        def actualizar_lista_materias():
            # Limpiar contenido anterior
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Obtener todas las materias
            resultado = self.courses_service.get_all_courses()
            
            if not resultado.get('success'):
                # Mostrar error
                error_label = QLabel(f"Error al cargar materias: {resultado.get('message', 'Error desconocido')}")
                error_label.setStyleSheet("color: red; font-weight: bold;")
                layout.addWidget(error_label)
                return

            cursos = resultado.get('courses', [])
            
            if not cursos:
                # Mostrar mensaje de no hay materias
                no_materias_label = QLabel("No hay materias registradas.")
                no_materias_label.setStyleSheet("color: gray; font-style: italic;")
                layout.addWidget(no_materias_label)
                return

            # Crear tarjetas para cada materia
            for curso in cursos:
                card = self.crear_tarjeta_materia(curso)
                layout.addWidget(card)

            # Añadir spacer al final
            layout.addStretch()

        # Crear función para crear tarjetas de materias
        def crear_tarjeta_materia(self, curso):
            """Crea una tarjeta visual para mostrar una materia."""
            # Crear frame principal
            card = QFrame()
            card.setFrameStyle(QFrame.Box)
            card.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 5px;
                }
                QFrame:hover {
                    border: 2px solid #007bff;
                }
            """)

            # Layout para la tarjeta
            card_layout = QVBoxLayout(card)
            
            # Título con ID y nombre
            titulo = QLabel(f"ID: {curso['id']} - {curso['name']}")
            titulo.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
            card_layout.addWidget(titulo)
            
            # Información adicional
            info_text = f"Créditos: {curso['credits']}"
            if curso.get('prereqs'):
                info_text += f" | Prerrequisitos: {', '.join(map(str, curso['prereqs']))}"
            else:
                info_text += " | Sin prerrequisitos"
            
            info_label = QLabel(info_text)
            info_label.setStyleSheet("color: #666; font-size: 12px;")
            card_layout.addWidget(info_label)
            
            return card

        # Asignar el método a la instancia
        self.crear_tarjeta_materia = crear_tarjeta_materia.__get__(self, MainWindow)
        
        # Cargar materias inicialmente
        actualizar_lista_materias()

    def setup_ver_caminos_materias(self):
        """
        Muestra la malla curricular en un QTableWidget, con los semestres como columnas y las materias como filas.
        """
        self.limpiar_panel()

        # Obtener datos del API
        resultado = self.courses_service.get_graph_info()
        if not resultado.get('success') or resultado.get('total_courses', 0) == 0:
            label = QLabel("No hay materias cargadas o error al obtener la información.")
            label.setStyleSheet("color: red; font-weight: bold;")
            self.panel_layout.addWidget(label, alignment=Qt.AlignHCenter)
            return

        tree_result = self.courses_service.get_course_tree()
        if not tree_result.get('success'):
            label = QLabel(f"Error: {tree_result.get('message', 'Error desconocido')}")
            label.setStyleSheet("color: red; font-weight: bold;")
            self.panel_layout.addWidget(label, alignment=Qt.AlignHCenter)
            return

        course_tree = tree_result['course_tree']
        niveles = sorted(course_tree.keys(), key=lambda x: int(x))
        max_materias = max(len(course_tree[n]['courses']) for n in niveles)
        num_semestres = len(niveles)

        # Contenedor principal con márgenes
        contenedor = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(contenedor)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Título
        titulo = QLabel("Malla Curricular por Semestre (Nivel)")
        titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        main_layout.addWidget(titulo, alignment=Qt.AlignHCenter)

        # Crear tabla
        table = QtWidgets.QTableWidget()
        table.setColumnCount(num_semestres)
        table.setRowCount(max_materias)
        table.setHorizontalHeaderLabels([f"Semestre {int(n)}" for n in niveles])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        table.setStyleSheet("font-size: 12px;")

        # Llenar la tabla
        for col, nivel in enumerate(niveles):
            cursos = course_tree[nivel]['courses']
            for row, curso in enumerate(cursos):
                texto = (f"ID: {curso['id']}\n{curso['name']}\n"
                        f"Créditos: {curso['credits']}\nPrerreq: ")
                texto += (', '.join(str(pid) for pid in curso['prereqs'])
                        if curso['prereqs'] else 'Ninguno')
                item = QtWidgets.QTableWidgetItem(texto)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, col, item)

        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setMinimumHeight(400)
        table.setMinimumWidth(900)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Scroll y contenedor intermedio para centrar
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)

        tabla_wrapper = QtWidgets.QWidget()
        wrapper_layout = QtWidgets.QVBoxLayout(tabla_wrapper)
        wrapper_layout.setContentsMargins(10, 10, 10, 10)
        wrapper_layout.addWidget(table, alignment=Qt.AlignHCenter)

        scroll.setWidget(tabla_wrapper)
        main_layout.addWidget(scroll)

        # Añadir todo al panel principal
        self.panel_layout.addWidget(contenedor)

    def setup_sugerencia_aleatoria(self):
        """
        Muestra la malla generada aleatoriamente por semestres usando generate_random_schedule.
        Permite al usuario elegir el tope de créditos por semestre.
        """
        self.limpiar_panel()

        # Layout vertical para el panel (con márgenes y spacing)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)   # márgenes: izquierda, arriba, derecha, abajo
        layout.setSpacing(15)

        # Campo para ingresar el tope de créditos
        creditos_layout = QtWidgets.QHBoxLayout()
        creditos_layout.setContentsMargins(0, 0, 0, 0)
        creditos_layout.setSpacing(10)
        label_creditos = QLabel("Créditos máximos por semestre:")
        spin_creditos = QtWidgets.QSpinBox()
        spin_creditos.setMinimum(1)
        spin_creditos.setMaximum(40)
        spin_creditos.setValue(18)
        spin_creditos.setSingleStep(1)
        creditos_layout.addWidget(label_creditos)
        creditos_layout.addWidget(spin_creditos)
        creditos_layout.addStretch()

        # Botón para recalcular
        btn_generar = QtWidgets.QPushButton("Generar horario")
        btn_generar.setStyleSheet("font-weight: bold; padding: 6px 12px;")
        creditos_layout.addWidget(btn_generar)

        layout.addLayout(creditos_layout)

        # Título
        titulo = QLabel("Sugerencia de planificacion de horario por semestre")
        titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        layout.insertWidget(0, titulo, alignment=Qt.AlignHCenter)

        # Widget para la tabla (se actualizará)
        tabla_scroll = QtWidgets.QScrollArea()
        tabla_scroll.setWidgetResizable(True)
        layout.addWidget(tabla_scroll)

        # Contenedor para la tabla con márgenes internos
        tabla_container = QtWidgets.QWidget()
        tabla_layout = QtWidgets.QVBoxLayout(tabla_container)
        tabla_layout.setContentsMargins(10, 10, 10, 10)
        tabla_layout.setSpacing(10)
        tabla_scroll.setWidget(tabla_container)

        def actualizar_tabla():
            # Limpiar tabla previa
            for i in reversed(range(tabla_layout.count())):
                item = tabla_layout.itemAt(i)
                widget = item.widget() if item else None
                if widget:
                    widget.setParent(None)

            # Obtener datos del API
            resultado = self.courses_service.get_graph_info()
            pprint(f"[DEBUG] (sugerencia) get_graph_info → {resultado}")

            if not resultado.get('success') or resultado.get('total_courses', 0) == 0:
                label = QLabel("No hay materias cargadas o error al obtener la información.")
                label.setStyleSheet("color: red; font-weight: bold;")
                tabla_layout.addWidget(label, alignment=Qt.AlignHCenter)
                return

            max_cred = spin_creditos.value()
            schedule_result = self.courses_service.generate_random_schedule(max_cred)
            pprint(f"[DEBUG] generate_random_schedule →{schedule_result}")
            if not schedule_result.get('success'):
                label = QLabel(f"Error: {schedule_result.get('message', 'Error desconocido')}")
                label.setStyleSheet("color: red; font-weight: bold;")
                tabla_layout.addWidget(label, alignment=Qt.AlignHCenter)
                return

            schedule = schedule_result['schedule']
            pprint(f"[DEBUG] schedule dict → {schedule}")
            semestres = sorted(schedule.keys(), key=lambda x: int(x))
            max_materias = max(len(schedule[s]['courses']) for s in semestres)
            num_semestres = len(semestres)

            # Crear tabla
            table = QtWidgets.QTableWidget()
            table.setColumnCount(num_semestres)
            table.setRowCount(max_materias)
            table.setHorizontalHeaderLabels([f"Semestre {int(s)}" for s in semestres])
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            table.setStyleSheet("font-size: 12px;")

            # Llenar la tabla
            for col, semestre in enumerate(semestres):
                cursos = schedule[semestre]['courses']
                for row, curso in enumerate(cursos):
                    texto = (f"ID: {curso['id']}\n{curso['name']}\n"
                            f"Créditos: {curso['credits']}\nPrerreq: ")
                    texto += (', '.join(str(pid) for pid in curso['prereqs'])
                            if curso['prereqs'] else 'Ninguno')
                    item = QtWidgets.QTableWidgetItem(texto)
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(row, col, item)

            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            table.setMinimumHeight(400)
            table.setMinimumWidth(900)
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            # Añadir y centrar tabla
            tabla_layout.addWidget(table, alignment=Qt.AlignHCenter)

        # Conectar botón
        btn_generar.clicked.connect(actualizar_tabla)
        # Generar tabla inicial
        actualizar_tabla()

        # Limpiar y agregar el layout al panel principal
        self.limpiar_panel()
        self.panel_layout.addLayout(layout)


def main():
    # 1) Antes de instanciar QApplication, indicamos que NO use
    #    los diálogos nativos del SO para que respete nuestro QSS:
    QApplication.setAttribute(Qt.AA_DontUseNativeDialogs, True)

    # 2) Creamos la aplicación
    app = QApplication(sys.argv)

    # 3) Cargamos el QSS desde un archivo externo
    qss_path = os.path.join(os.path.dirname(__file__), 'styles/global.css')
    if os.path.exists(qss_path):
        app.setStyleSheet(load_stylesheet(qss_path))
    else:
        print(f"[WARNING] No se encontró el QSS en: {qss_path}")

    # 4) Instanciamos y mostramos la ventana principal
    main_window = MainWindow()
    main_window.show()
    main_window.cargar_archivo_ejemplo()

    # 5) Ejecutamos el bucle de eventos
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

