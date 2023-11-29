import tkinter as tk
from tkinter import filedialog
import os
import json
import re


def obtener_archivos_de_video(directorio):
    """
    Obtiene archivos de video con extensiones específicas en un directorio dado.

    Args:
    - directorio (str): La ruta del directorio del cual se obtendrán los archivos.

    Returns:
    - json_data (str): Datos de los archivos de video en formato JSON si se encuentran,
      None si no se encontraron archivos de video en el directorio.
    """
    if directorio:
        archivos_video = []
        archivos_en_directorio = os.listdir(directorio)

        extensiones_video = ['.mp4', '.avi', '.mkv', '.mov']
        archivos_video = [archivo for archivo in archivos_en_directorio if os.path.splitext(
            archivo)[1].lower() in extensiones_video]

        if archivos_video:
            info_archivos = []
            digitos = len(str(len(archivos_video))) if any(char.isdigit()
                                                           for char in str(len(archivos_video))) else 1
            for archivo in archivos_video:
                nombre, extension = os.path.splitext(archivo)
                nombre = re.sub(r'_', ' ', nombre)
                nombre = re.sub(r'\[.*?\]|\(.*?\)', ' ', nombre)

                ruta_completa = os.path.join(directorio, archivo)
                numeros = re.findall(r'\d+', nombre)
                numeros = [int(num)
                           for num in numeros if len(str(num)) <= digitos]
                numeros = list(set(numeros))
                numeros.sort()
                info_archivos.append({
                    'nombre': nombre,
                    'extension': extension,
                    'ruta': ruta_completa,
                    'numeros_en_nombre': numeros,
                    'ruta_carpeta': directorio,
                    'nombre_carpeta': os.path.basename(directorio),
                    'cantidad_digitos': digitos

                })

            json_data = json.dumps(info_archivos, indent=4)

            return json_data
        else:
            return None
    else:
        return None


def obtener_subcarpetas_recursivas(directorio=None):
    """
    Obtiene subcarpetas que contienen archivos de video desde un directorio dado.

    Args:
    - directorio (str, opcional): La ruta del directorio del cual se iniciarán las búsquedas.
      Si no se proporciona, se abrirá un diálogo para seleccionar el directorio.

    Returns:
    - obtener_subcarpetas_recursivas (list): Lista de subcarpetas que contienen archivos de video.
    - directorio (str): Ruta del directorio seleccionado o provisto.
    """
    if directorio is None:
        root = tk.Tk()
        root.withdraw()
        directorio = filedialog.askdirectory(title="Selecciona un directorio")

    if not os.path.isdir(directorio):
        return None, None

    obtener_subcarpetas_recursivas = []
    # Extensiones de archivos de video admitidas
    extensiones_video = ['.mp4', '.avi', '.mkv', '.mov']

    for raiz, carpetas, archivos in os.walk(directorio):
        for archivo in archivos:
            # Verificar si la extensión del archivo está en la lista de extensiones de video
            if os.path.splitext(archivo)[1].lower() in extensiones_video:
                # Agregar la subcarpeta al resultado si contiene archivos de video
                obtener_subcarpetas_recursivas.append(raiz)
                break  # Salir del bucle interno, ya que encontramos un video en esta subcarpeta

    if obtener_subcarpetas_recursivas:
        return obtener_subcarpetas_recursivas, directorio
    else:
        obtener_subcarpetas_recursivas.append(directorio)
        return obtener_subcarpetas_recursivas, directorio


def imprimir_json(json_data):
    parsed_json = json.loads(json_data)
    formatted_json = json.dumps(parsed_json, indent=4)
    print(formatted_json)
