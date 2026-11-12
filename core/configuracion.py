import os

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DATA = os.path.join(RUTA_PROYECTO, "data")

RUTA_USUARIOS = os.path.join(RUTA_DATA, "usuarios.json")