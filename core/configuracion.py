import os
from core.repositorio_json import RepositorioJson

RUTA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_DATA = os.path.join(RUTA_PROYECTO, "data")

RUTA_USUARIOS = os.path.join(RUTA_DATA, "usuarios.json")
RUTA_PACIENTES = os.path.join(RUTA_DATA, "pacientes.json")
RUTA_AGENDA = os.path.join(RUTA_DATA, "agendas.json")
RUTA_TURNOS = os.path.join(RUTA_DATA, "turnos.json")
RUTA_HISTORIAS_CLINICAS = os.path.join(RUTA_DATA, "historiasClinicas.json")

def cargar_json(ruta):
    return RepositorioJson().cargar(ruta)


def guardar_json(ruta, datos):
    RepositorioJson().guardar(ruta, datos)