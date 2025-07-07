import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import resources_rc

"""
    Este es un archivo para probar la interfaz, no es la aplicacion final.
"""

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # Determinar la ruta al directorio 'gui', donde están los .ui
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

        # Configurar ventana
        self.setWindowTitle("Graduacion UNAL")

        # Referenciar widgets importantes
        self.panel = self.findChild(QtWidgets.QWidget, 'panel')
        self.sidebar = self.findChild(QtWidgets.QWidget, 'sidebar')

        # obtener el layout existente en lugar de crear uno nuevo
        self.panel_layout = self.panel.layout()

        # Si no tenía layout, crear uno (esto es por seguridad)
        if self.panel_layout is None:
            self.panel_layout = QtWidgets.QVBoxLayout(self.panel)
            self.panel_layout.setContentsMargins(0, 0, 0, 0)

        # Conectar botones
        self.asignar_botones(ui_dir)

    def limpiar_panel(self):
        # Eliminar todos los widgets del panel
        while self.panel_layout.count():
            child = self.panel_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def cambiar_menu(self, menu: str, ui_dir: str):
        """
            Cambia al menú pasado como argumento.
        """
        self.limpiar_panel()
        ui_file = os.path.join(ui_dir, f"{menu}.ui")
        if not os.path.isfile(ui_file):
            print(f"[ERROR] No se encontró {ui_file}")
            return
        try:
            materia_widget = uic.loadUi(ui_file)
            self.panel_layout.addWidget(materia_widget, alignment=Qt.AlignCenter)
        except Exception as e:
            print(f"[ERROR] Error cargando {menu}: {e}")

    def cargar(self):
        print("[DEBUG] Cargar")

    def guardar(self):
        print("[DEBUG] Guardar")

    def nuevo(self):
        print("[DEBUG] Nuevo")

    def asignar_botones(self, ui_dir: str):
        mappings = {
            'ButtonAgregarMateria':        'AñadirMateria',
            'ButtonAgregarPrerrequisito':  'AñadirPrerrequisito',
            'ButtonEliminarMateria':       'EliminarMateria',
            'ButtonEliminarPrerrequisito': 'EliminarPrerrequisito',
            'ButtonVerMaterias':           'VerMaterias',
            'ButtonCalcularSemestres':     'CalcularSemestres',
        }
        # Botones de cambio de menú
        for obj_name, menu_name in mappings.items():
            btn = self.findChild(QtWidgets.QPushButton, obj_name)
            if not btn:
                print(f"[ERROR] no encontré botón con objectName='{obj_name}'")
                continue
            print(f"[OK] Conectando {obj_name} → cambiar_menu('{menu_name}')")
            btn.clicked.connect(lambda _, m=menu_name: self.cambiar_menu(m, ui_dir))

        # Botones de archivo
        for name, handler in [('ButtonGuardar', self.guardar), ('ButtonCargar', self.cargar), ('ButtonNuevo', self.nuevo)]:
            btn = self.findChild(QtWidgets.QPushButton, name)
            if btn:
                btn.clicked.connect(handler)
            else:
                print(f"[ERROR] no encontré botón con objectName='{name}'")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
