import json


def eliminar_numeros_repetidos(json_data):
    """
    Elimina números repetidos de los nombres de archivos en los datos JSON proporcionados.

    Args:
    - json_data (str): Datos en formato JSON que contienen información sobre archivos.

    Returns:
    - json_actualizado (str): Datos actualizados en formato JSON con nombres de archivos modificados.
    """
    info_archivos = json.loads(json_data)
    numeros_archivos = [archivo['numeros_en_nombre']
                        for archivo in info_archivos]
    numeros_repetidos = []
    numeros_unicos = set()

    for numeros in numeros_archivos:
        for num in numeros:
            if num in numeros_unicos:
                numeros_repetidos.append(num)
            else:
                numeros_unicos.add(num)
    for archivo in info_archivos:
        archivo['numeros_repetidos'] = list(
            set(archivo['numeros_en_nombre']) & set(numeros_repetidos))

    for archivo in info_archivos:
        lista_principal = archivo['numeros_en_nombre']
        elementos_a_eliminar = archivo['numeros_repetidos']

        if len(lista_principal) > 1:
            lista_final = [
                elemento for elemento in lista_principal if str(elemento).zfill(archivo['cantidad_digitos']) not in [str(num).zfill(archivo['cantidad_digitos']) for num in elementos_a_eliminar]
            ]
        else:
            lista_final = lista_principal
        if lista_final:
            nuevo_nombre = archivo['nombre_carpeta'] + ' ' + \
                str(lista_final[0]).zfill(archivo['cantidad_digitos'])
            archivo['nuevo_nombre'] = nuevo_nombre
            archivo['nuevo_ruta'] = archivo['ruta_carpeta'] + \
                '/' + nuevo_nombre + '' + archivo['extension']
        else:
            archivo['nuevo_nombre'] = archivo['nombre']
            archivo['nuevo_ruta'] = archivo['ruta']

    json_actualizado = json.dumps(info_archivos, indent=4)
    # print(json_actualizado)
    return json_actualizado
