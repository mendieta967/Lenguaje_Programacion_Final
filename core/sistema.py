import os
import json

from modules.admin.creacion import crear_primer_admin
from core.configuracion import RUTA_DATA, RUTA_USUARIOS

def inicializar_sistema():

    ruta_data = RUTA_DATA
    ruta_usuarios = RUTA_USUARIOS

    # Crear carpeta data
    if not os.path.exists(ruta_data):
        os.mkdir(ruta_data)

    # Crear archivo usuarios.json
    if not os.path.exists(ruta_usuarios):
        with open(ruta_usuarios, "w", encoding="utf-8") as archivo:
            json.dump([], archivo, indent=4)

    # Leer usuarios
    with open(ruta_usuarios, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
        usuarios = json.loads(contenido) if contenido.strip() else []

    # Si no existen usuarios
    if not usuarios:
        crear_primer_admin(ruta_usuarios)