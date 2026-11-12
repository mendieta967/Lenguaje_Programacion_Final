import os
import json

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DATA = os.path.join(RUTA_PROYECTO, "data")

RUTA_USUARIOS = os.path.join(RUTA_DATA, "usuarios.json")
RUTA_PACIENTES = os.path.join(RUTA_DATA, "pacientes.json")

def cargar_json(ruta):

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


def guardar_json(ruta, datos):

    with open(ruta, "w", encoding="utf-8") as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )