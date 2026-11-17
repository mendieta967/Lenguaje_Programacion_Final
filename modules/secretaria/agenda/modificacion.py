from core.configuracion import RUTA_AGENDA, cargar_json, guardar_json
from modules.secretaria.agenda.consultas import (
    buscar_agenda_por_medico,
    consultar_agenda,
)
from modules.secretaria.agenda.horarios import (
    DIA_NOMBRE,
    pedir_bloques_horarios,
    pedir_tipo_horario,
)


def _pedir_agenda(agendas):

    consultar_agenda()

    while True:
        try:
            id_medico = int(
                input("\nIngrese el ID del médico (0 para volver): ")
            )
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        if id_medico == 0:
            return None

        agenda = buscar_agenda_por_medico(agendas, id_medico)

        if agenda is not None:
            return agenda

        print("\nEse médico no tiene una agenda registrada.")


def _pedir_dia(agenda):

    dias = sorted(
        {bloque["dia"] for bloque in agenda["bloques"]},
        key=lambda dia: list(DIA_NOMBRE).index(dia),
    )

    if not dias:
        print("\nLa agenda no tiene días configurados.")
        return None

    print("\nSeleccione el día que desea modificar:")

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


def modificar_agenda():

    agendas = cargar_json(RUTA_AGENDA) or []

    if not agendas:
        print("\nNo hay agendas registradas.")
        return

    agenda = _pedir_agenda(agendas)

    if agenda is None:
        return

    while True:
        dia = _pedir_dia(agenda)

        if dia is None:
            return

        cantidad_bloques = pedir_tipo_horario()
        if cantidad_bloques is None:
            continue

        bloques_existentes = [
            bloque for bloque in agenda["bloques"] if bloque["dia"] != dia
        ]

        print(f"\nNuevo horario para {DIA_NOMBRE[dia]}:")
        bloques_nuevos = pedir_bloques_horarios(
            dia,
            cantidad_bloques,
            bloques_existentes,
        )

        agenda["bloques"] = bloques_existentes + bloques_nuevos
        guardar_json(RUTA_AGENDA, agendas)

        print("\nAgenda modificada correctamente.")
        return