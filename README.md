# Renombrador de Archivos de Video

Este programa proporciona una interfaz gráfica para renombrar archivos de video de manera automatizada, basándose en ciertos criterios.

## Funcionalidades

- **Interfaz Gráfica:** El archivo `videorename.py` contiene la interfaz de usuario principal del programa.
- **Funciones de Procesamiento:**
  - `obtener_archivos_de_video(directorio)`: Obtiene archivos de video con extensiones específicas en un directorio dado.
  - `obtener_subcarpetas_recursivas(directorio)`: Obtiene subcarpetas que contienen archivos en forma recursiva desde un directorio dado.
  - `eliminar_numeros_repetidos(json_data)`: Elimina números repetidos de los nombres de archivos en los datos JSON proporcionados.

## Uso

1. **Ejecución:**
   - Ejecuta `videorename.py` para abrir la interfaz gráfica.
   - Selecciona un directorio para procesar archivos de video.
   - Procede con la renombrado de archivos según los criterios definidos.
.

## Requisitos

- Python 3.x
- Bibliotecas requeridas: `PyQt5`

