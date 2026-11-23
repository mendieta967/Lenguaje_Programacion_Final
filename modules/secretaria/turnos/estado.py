from datetime import datetime, timedelta

from core.configuracion import RUTA_TURNOS, cargar_json, guardar_json
from modules.secretaria.turnos.consultas import mostrar_turnos


def turno_puede_marcarse_ausente(turno, ahora=None):
    if (
        turno["estado"] != "RESERVADO"
        or turno.get("atencion") is not None
        or turno.get("id_atencion") is not None
    ):
        return False

    if ahora is None:
        ahora = datetime.now()

    fin_turno = datetime.strptime(
        f"{turno['fecha']} {turno['hora']}",
        "%d/%m/%Y %H:%M",
    ) + timedelta(minutes=30)
    return fin_turno <= ahora


def obtener_turnos_para_marcar_ausente(turnos, ahora=None):
    return [
        turno
        for turno in turnos
        if turno_puede_marcarse_ausente(turno, ahora)
    ]


def aplicar_estado_ausente(turno, ahora=None):
    if not turno_puede_marcarse_ausente(turno, ahora):
        raise ValueError("El turno todavía no puede marcarse como AUSENTE.")

    turno["estado"] = "AUSENTE"


def cancelar_turno():
    turnos = cargar_json(RUTA_TURNOS) or []
    turnos_reservados = [
        turno for turno in turnos if turno["estado"] == "RESERVADO"
    ]

    if not turnos_reservados:
        print("\nNo hay turnos reservados para cancelar.")
        return

    print("\nSeleccione el turno que desea cancelar.")
    mostrar_turnos(turnos_reservados)

    while True:
        opcion = input("\nIngrese el ID del turno (0 para volver): ").strip()

        if opcion == "0":
            return

        try:
            id_turno = int(opcion)
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        turno_seleccionado = None
        for turno in turnos_reservados:
            if turno["id"] == id_turno:
                turno_seleccionado = turno
                break

        if turno_seleccionado is None:
            print("\nNo existe un turno reservado con ese ID.")
            continue

        confirmar = input("¿Confirma la cancelación? (S/N): ").strip().casefold()

        if confirmar == "s":
            turno_seleccionado["estado"] = "CANCELADO"
            guardar_json(RUTA_TURNOS, turnos)
            print("\nTurno cancelado correctamente.")
            return

        if confirmar == "n":
            print("\nCancelación anulada.")
            return

        print("\nIngrese S o N.")


def marcar_ausente():
    turnos = cargar_json(RUTA_TURNOS) or []
    turnos_ausentes = obtener_turnos_para_marcar_ausente(turnos)

    if not turnos_ausentes:
        print("\nNo hay turnos que puedan marcarse como no asistidos.")
        return

    print("\nSeleccione el turno del paciente que no asistió.")
    mostrar_turnos(turnos_ausentes)

    while True:
        opcion = input("\nIngrese el ID del turno (0 para volver): ").strip()
        if opcion == "0":
            return

        try:
            id_turno = int(opcion)
        except ValueError:
            print("\nEl ID debe ser un número.")
            continue

        turno_seleccionado = next(
            (turno for turno in turnos_ausentes if turno["id"] == id_turno),
            None,
        )
        if turno_seleccionado is None:
            print("\nNo existe un turno que pueda marcarse como no asistido con ese ID.")
            continue

        while True:
            confirmar = input(
                "¿Confirma que el paciente no asistió? (S/N): "
            ).strip().casefold()
            if confirmar == "n":
                print("\nOperación cancelada; el turno sigue reservado.")
                return
            if confirmar == "s":
                break
            print("\nIngrese S o N.")

        turnos_actualizados = cargar_json(RUTA_TURNOS) or []
        turno_actualizado = next(
            (turno for turno in turnos_actualizados if turno["id"] == id_turno),
            None,
        )
        if turno_actualizado is None:
            print("\nEl turno ya no está disponible.")
            return

        try:
            aplicar_estado_ausente(turno_actualizado, datetime.now())
        except ValueError as error:
            print(f"\n{error}")
            return

        guardar_json(RUTA_TURNOS, turnos_actualizados)
        print("\nTurno marcado como AUSENTE.")
        return
