from resources.modules.read_files_modules import *
from resources.modules.video_processor_modules import *
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QWidget, QLabel, QHeaderView, QProgressBar, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon  # Agregar esta línea al inicio de tus importaciones
import os
import json
import re
import subprocess


class RenombrarImagenesThread(QThread):
    progreso_actualizado = pyqtSignal(int)
    renombrado_completado = pyqtSignal()

    def __init__(self, datos):
        super().__init__()
        self.datos = datos

    def run(self):
        """Ejecuta el proceso de renombrado de archivos."""
        total_archivos = len(self.datos)
        for index, item in enumerate(self.datos):
            nombre_original = item.get("ruta", "")
            nuevo_nombre = item.get("ruta_carpeta", "")+'/'+re.sub(
                r'^.*?- ', '', item.get("nuevo_nombre", "")) + item.get("extension", "")
            os.rename(nombre_original, nuevo_nombre)
            progreso = int((index + 1) * 100 / total_archivos)
            self.progreso_actualizado.emit(progreso)
        self.renombrado_completado.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.datos = None
        self.path_cache = None
        self.setWindowTitle("Renombrar archivos")
        self.resize(1000, 600)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        self.layout_principal = QVBoxLayout()
        self.label_estado_carpeta = QLabel("No has seleccionado una carpeta")
        self.layout_principal.addWidget(self.label_estado_carpeta)

        self.crear_boton_procesar_datos()
        self.crear_boton_abrir_carpeta()
        self.crear_tabla()

        self.widget_central.setLayout(self.layout_principal)

    def crear_boton_abrir_carpeta(self):
        """Crea el botón para abrir la carpeta seleccionada."""
        self.boton_abrir_carpeta = QPushButton("Abrir carpeta seleccionada")
        self.boton_abrir_carpeta.clicked.connect(
            self.abrir_carpeta_seleccionada)
        self.boton_abrir_carpeta.setEnabled(False)
        self.layout_principal.addWidget(self.boton_abrir_carpeta)

    def crear_tabla(self):
        """Crea y configura la tabla para mostrar los datos."""
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(
            ["Carpeta", "Nombre original", "Nuevo nombre"])
        self.actualizar_tabla([])

        self.layout_principal.addWidget(self.tabla)
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.boton_renombrar = QPushButton("Renombrar archivos")
        self.boton_renombrar.clicked.connect(self.ejecutar_renombre_datos)
        self.boton_renombrar.setEnabled(False)
        self.layout_principal.addWidget(self.boton_renombrar)

        self.barra_progreso = QProgressBar()
        self.barra_progreso.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(self.barra_progreso)

    def crear_boton_procesar_datos(self):
        """Crea el botón para procesar los datos."""
        boton_procesar = QPushButton("Selecciona una carpeta")
        boton_procesar.clicked.connect(self.seleccionar_nueva_ruta)
        self.layout_principal.addWidget(boton_procesar)

    def ejecutar_procesar_datos(self):
        """Ejecuta el procesamiento de datos."""
        try:
            self.datos = self.procesar_datos()
            self.limpiar_tabla()
            self.actualizar_tabla(self.datos)
            self.boton_renombrar.setEnabled(bool(self.datos))
            # Habilitar botón al seleccionar carpeta
            self.boton_abrir_carpeta.setEnabled(True)

        except Exception as e:
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setWindowTitle("Error al procesar datos:")
            error_box.setText(str(e))
            error_box.exec_()

    def seleccionar_nueva_ruta(self):
        ruta = QFileDialog.getExistingDirectory(
            self, "Seleccionar directorio", ".")
        if ruta:
            self.path_cache = ruta
            self.label_estado_carpeta.setText(
                f"Ruta seleccionada: {self.path_cache}")
            self.ejecutar_procesar_datos()

    def abrir_carpeta_seleccionada(self):
        if self.path_cache:
            # Abre la carpeta en el explorador de archivos
            subprocess.Popen(f'explorer "{os.path.abspath(self.path_cache)}"')

    def limpiar_tabla(self):
        self.tabla.setRowCount(0)

    def procesar_datos(self):
        if self.path_cache is None:
            folders, directorio = obtener_subcarpetas_recursivas()
            self.path_cache = directorio
        else:
            folders, directorio = obtener_subcarpetas_recursivas(
                self.path_cache)
        datos_procesados = []

        for folder in folders:
            datos_procesados.extend(json.loads(
                eliminar_numeros_repetidos(obtener_archivos_de_video(folder))))

        datos_json = json.dumps(datos_procesados, indent=4)
        datos_json = json.loads(datos_json)

        return datos_json

    def ejecutar_renombre_datos(self):
        self.boton_renombrar.setEnabled(False)
        self.barra_progreso.setValue(0)
        self.thread_renombrar = RenombrarImagenesThread(self.datos)
        self.thread_renombrar.progreso_actualizado.connect(
            self.actualizar_barra_progreso)
        self.thread_renombrar.renombrado_completado.connect(
            self.mostrar_mensaje_finalizado)
        self.thread_renombrar.finished.connect(self.habilitar_boton_renombrar)
        self.thread_renombrar.start()

    def mostrar_mensaje_finalizado(self):
        QMessageBox.information(
            self, "Proceso completado", "El renombrado de archivos ha finalizado.")

    def actualizar_barra_progreso(self, valor):
        self.barra_progreso.setValue(valor)

    def habilitar_boton_renombrar(self):
        self.boton_renombrar.setEnabled(True)

    def actualizar_tabla(self, datos):
        self.tabla.setRowCount(len(datos))
        for indice, item in enumerate(datos):
            carpeta = item.get("nombre_carpeta", "")
            nombre_original = item.get(
                "nombre", "") + item.get("extension", "")
            nuevo_nombre = re.sub(
                r'^.*?- ', '', item.get("nuevo_nombre", "")) + item.get("extension", "")
            self.tabla.setItem(indice, 0, QTableWidgetItem(carpeta))
            self.tabla.setItem(indice, 1, QTableWidgetItem(nombre_original))
            self.tabla.setItem(indice, 2, QTableWidgetItem(nuevo_nombre))


def mostrar_interfaz():
    """Inicializa y muestra la interfaz gráfica."""
    app = QApplication([])
    ventana = MainWindow()
    # Reemplaza con la ruta de tu icono
    icono = QIcon("./resources/icon/video.png")
    ventana.setWindowIcon(icono)
    ventana.show()
    app.exec_()


if __name__ == "__main__":
    mostrar_interfaz()
