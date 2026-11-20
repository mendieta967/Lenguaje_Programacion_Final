from core.configuracion import (
    RUTA_AGENDA,
    RUTA_TURNOS,
    cargar_json,
    guardar_json,
)
from modules.secretaria.agenda.consultas import (
    buscar_agenda_por_medico,
    consultar_agenda,
)
from modules.secretaria.agenda.horarios import DIA_NOMBRE
from datetime import datetime


def _confirmar_eliminacion(id_medico, dia=None):

    if dia is None:
        mensaje = (
            f"\n¿Confirma que desea eliminar toda la agenda del médico "
            f"con ID {id_medico}? (s/n): "
        )
    else:
        mensaje = (
            f"\n¿Confirma que desea eliminar los horarios del día "
            f"{DIA_NOMBRE[dia]} del médico con ID {id_medico}? (s/n): "
        )

    confirmacion = input(mensaje).strip().lower()

    if confirmacion not in ("s", "si"):
        print("\nOperación cancelada.")
        return False

    return True


def _dia_de_fecha(fecha):

    if not isinstance(fecha, str):
        return None

    try:
        fecha_convertida = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        return None

    dias = (
        "LUNES",
        "MARTES",
        "MIERCOLES",
        "JUEVES",
        "VIERNES",
        "SABADO",
        "DOMINGO",
    )
    return dias[fecha_convertida.weekday()]


def _tiene_turnos_asociados(id_medico, dia=None):

    turnos = cargar_json(RUTA_TURNOS) or []

    for turno in turnos:
        if turno.get("id_medico") != id_medico:
            continue

        if dia is None:
            return True

        dia_turno = turno.get("dia")
        if dia_turno is None:
            dia_turno = _dia_de_fecha(turno.get("fecha"))

        if dia_turno == dia:
            return True

    return False


def _pedir_dia(agenda):

    dias = sorted(
        {bloque["dia"] for bloque in agenda["bloques"]},
        key=lambda dia: list(DIA_NOMBRE).index(dia),
    )

    if not dias:
        print("\nLa agenda no tiene días configurados.")
        return None

    print("\nSeleccione el día que desea eliminar:")

    for numero, dia in enumerate(dias, start=1):
        horarios = [
            f"{bloque['inicio']}-{bloque['fin']}"
            for bloque in agenda["bloques"]
            if bloque["dia"] == dia
        ]
        print(f"{numero}. {DIA_NOMBRE[dia]} ({', '.join(horarios)})")

    print("0. Volver")

    while True:
        opcion = input("Opción: ").strip()

        if opcion == "0":
            return None

        try:
            indice = int(opcion) - 1
        except ValueError:
            print("\nSeleccione un número válido.")
            continue

        if 0 <= indice < len(dias):
            return dias[indice]

        print("\nSeleccione un día de la lista.")


def eliminar_agenda():

    agendas = cargar_json(RUTA_AGENDA) or []

    if not agendas:
        print("\nNo hay agendas registradas.")
        return

    consultar_agenda()

    try:
        id_medico = int(
            input("\nIngrese el ID del médico cuya agenda desea eliminar "
                  "(0 para volver): ")
        )
    except ValueError:
        print("\nEl ID debe ser un número.")
        return

    if id_medico == 0:
        return

    agenda = buscar_agenda_por_medico(agendas, id_medico)

    if agenda is None:
        print("\nEse médico no tiene una agenda registrada.")
        return

    print("\n¿Qué desea eliminar?")
    print("1. Un día")
    print("2. Toda la agenda")
    print("0. Volver")

    opcion = input("Opción: ").strip()

    if opcion == "0":
        return

    if opcion == "1":
        dia = _pedir_dia(agenda)

        if dia is None:
            return

        if _tiene_turnos_asociados(id_medico, dia):
            print(
                f"\nNo es posible eliminar {DIA_NOMBRE[dia]} porque existen "
                "turnos asociados a ese día."
            )
            return

        if not _confirmar_eliminacion(id_medico, dia):
            return

        agenda["bloques"] = [
            bloque for bloque in agenda["bloques"] if bloque["dia"] != dia
        ]

        if not agenda["bloques"]:
            agendas.remove(agenda)

        guardar_json(RUTA_AGENDA, agendas)
        print(f"\nHorarios de {DIA_NOMBRE[dia]} eliminados correctamente.")
        return

    if opcion != "2":
        print("\nSeleccione una opción válida.")
        return

    if _tiene_turnos_asociados(id_medico):
        print(
            "\nNo es posible eliminar la agenda porque existen "
            "turnos asociados a este médico."
        )
        return

    if not _confirmar_eliminacion(id_medico):
        return

    agendas.remove(agenda)
    guardar_json(RUTA_AGENDA, agendas)

    print("\nAgenda eliminada correctamente.")
